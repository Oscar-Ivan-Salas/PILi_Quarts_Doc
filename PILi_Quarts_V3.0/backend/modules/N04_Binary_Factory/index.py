import logging
import base64
import json
import os
from pathlib import Path
from pydantic import ValidationError
try:
    from .models import BinaryFactoryInput
except (ImportError, ValueError):
    from models import BinaryFactoryInput

# Native Generators Imports
try:
    from .generators.cotizacion_simple_generator import generar_cotizacion_simple
    from .generators.cotizacion_compleja_generator import generar_cotizacion_compleja
    from .generators.proyecto_simple_generator import generar_proyecto_simple
    from .generators.proyecto_complejo_pmi_generator import generar_proyecto_complejo_pmi
    from .generators.informe_tecnico_generator import generar_informe_tecnico
    from .generators.informe_ejecutivo_apa_generator import generar_informe_ejecutivo_apa
except (ImportError, ValueError):
    from generators.cotizacion_simple_generator import generar_cotizacion_simple
    from generators.cotizacion_compleja_generator import generar_cotizacion_compleja
    from generators.proyecto_simple_generator import generar_proyecto_simple
    from generators.proyecto_complejo_pmi_generator import generar_proyecto_complejo_pmi
    from generators.informe_tecnico_generator import generar_informe_tecnico
    from generators.informe_ejecutivo_apa_generator import generar_informe_ejecutivo_apa

# Importar Generador de Excel Profesional Original
try:
    from modules.documents.generators.excel_generator import ExcelGenerator
except ImportError:
    try:
        from ..documents.generators.excel_generator import ExcelGenerator
    except ImportError:
        ExcelGenerator = None
        logger.warning("⚠️ ExcelGenerator profesional no encontrado. Fallback activo.")
# Binary Factory Entry Point - Restored to V9 "The Mirror" Engine


logger = logging.getLogger("N04_Binary_Factory")

class BinaryFactory:
    def __init__(self):
        self.excel_gen = ExcelGenerator() if ExcelGenerator else None
        
    def process_request(self, input_data: dict) -> dict:
        """
        Procesa una solicitud de generación de documento validando contra contrato.
        """
        try:
            # 1. Validación Estricta (Contract First con Pydantic)
            try:
                validated_input = BinaryFactoryInput(**input_data)
            except ValidationError as e:
                logger.error(f"Contract Violation: {e.errors()}")
                return {"success": False, "error": f"Contract Violation: {e.errors()}"}

            # 2. Desestructuración Segura
            header = validated_input.header
            branding = validated_input.branding
            payload = validated_input.payload
            output_format = validated_input.output_format

            logger.info(f"🏭 Processing Request: DocType {header.document_type} | Service {header.service_id} | Format {output_format}")

            # 3. Despacho (Factory Pattern) - FORCE V10 ENGINE RECALL
            # Bypass _generate_universal_* methods to enforce Strict Naming and V10 Layouts
            if output_format == "XLSX":
                return self._generate_excel(header, branding, payload)
            elif output_format == "DOCX":
                return self._generate_word(header, branding, payload)
            elif output_format == "PDF":
                return self._generate_pdf(header, branding, payload)
            
            return {"success": False, "error": "Unsupported format"}

        except Exception as e:
            logger.error(f"Critical Error in BinaryFactory: {e}", exc_info=True)
            return {"success": False, "error": str(e)}

    def _generate_universal_pdf(self, template_name, branding, payload, header):
        """Universal Engine: Reads mapping.json and generates PDF"""
        try:
            from fpdf import FPDF
            import io
            
            template_dir = Path(__file__).parent / "templates" / template_name
            mapping_path = template_dir / "mapping.json"
            
            if not mapping_path.exists():
                 return {"success": False, "error": f"Template {template_name} not found"}
            
            with open(mapping_path, "r", encoding="utf-8") as f:
                mapping = json.load(f)
                
            w_layout = mapping.get("word_layout", {})
            title_text = w_layout.get("title", "Documento").replace("{{ service_name }}", f"Servicio {header.service_id}")
            
            pdf = FPDF()
            pdf.add_page()
            
            # Logo
            # If b64 logo provided, we could save temp and use it.
            # Simplified for Seal: Text Header
            pdf.set_font("Arial", 'B', 16)
            pdf.set_text_color(204, 0, 0) # Primary red
            pdf.cell(0, 10, "SOLUCIONES ELECTRICAS", 0, 1, 'C')
            
            pdf.set_font("Arial", 'B', 14)
            pdf.cell(0, 10, title_text, 0, 1, 'C')
            
            pdf.set_font("Arial", '', 10)
            pdf.set_text_color(0, 0, 0)
            pdf.cell(0, 6, f"Cliente: {payload.client_info.get('nombre', 'N/A')}", 0, 1)
            pdf.cell(0, 6, f"Fecha: {payload.client_info.get('fecha', 'N/A')}", 0, 1)
            pdf.ln(10)
            
            # Mirror Logic: Use Excel Columns to define Order
            # 1. Get Columns Definition
            tables = mapping.get("excel_layout", {}).get("tables", [])
            if not tables:
                 return {"success": False, "error": "No tables defined in mapping"}
            
            columns_map = tables[0].get("columns", {})
            # 2. Sort keys by Value (Column Letter)
            # Logic: B->1, C->2...
            # We assume single letters for now or handle simple comparison
            sorted_keys = sorted(columns_map.keys(), key=lambda k: columns_map[k])
            
            # Table
            headers = w_layout.get("headers", [])
            if not headers:
                # Fallback to Keys if no headers
                headers = [k.capitalize() for k in sorted_keys]
                
            # Dynamic Column Widths based on content count
            # Total width approx 190 (A4)
            # Index (1st) = 15, Others distributed
            col_count = len(headers)
            if col_count == 0: col_count = 1
            
            col_w = []
            available_w = 175
            for i in range(col_count):
                if i == 0: col_w.append(15) # Index/Item usually small
                else: col_w.append(available_w / (col_count - 1))
            
            pdf.set_font("Arial", 'B', 8)
            pdf.set_fill_color(240, 240, 240)
            
            # Draw Headers
            for i, h in enumerate(headers):
                w = col_w[i] if i < len(col_w) else 20
                pdf.cell(w, 8, str(h)[:15], 1, 0, 'C', 1)
            pdf.ln()
            
            pdf.set_font("Arial", '', 8)
            for item in payload.items:
                # Dynamic Row
                for i, key in enumerate(sorted_keys):
                    w = col_w[i] if i < len(col_w) else 20
                    
                    # Special Handlers based on key name?
                    # "index" -> calculated from loop?
                    if key == "index":
                        val = str(payload.items.index(item)+1)
                    else:
                        val = item.get(key, "")
                        
                    # Handle Formula
                    if isinstance(val, str) and val.startswith("="):
                        val = "(Calc)"
                        
                    pdf.cell(w, 8, str(val)[:40], 1)
                pdf.ln()

            pdf.ln(5)
            # Only show Total if it exists in 'totals' object and fits the context
            if payload.totals.get('total'):
                 pdf.cell(0, 8, f"TOTAL: {payload.totals.get('total')}", 0, 1, 'R')
            
            # Output
            try:
                pdf_bytes = pdf.output(dest='S').encode('latin-1')
            except:
                pdf_bytes = pdf.output().encode('latin-1') # Fallback
                
            b64_data = base64.b64encode(pdf_bytes).decode('utf-8')
            
            return {
                "success": True, 
                "filename": f"{template_name}_GEN.pdf",
                "file_b64": b64_data,
                "engine": "Universal PDF v1.0"
            }

        except Exception as e:
            logger.error(f"Universal PDF Gen Error: {e}", exc_info=True)
            return {"success": False, "error": str(e)}
    def _generate_universal_word(self, template_name, branding, payload, header):
        """Universal Engine: Reads mapping.json and generates Word (DOCX)"""
        try:
            from docx import Document
            from docx.shared import Pt, RGBColor
            from docx.enum.text import WD_ALIGN_PARAGRAPH
            import io
            
            template_dir = Path(__file__).parent / "templates" / template_name
            mapping_path = template_dir / "mapping.json"
            
            if not mapping_path.exists():
                 return {"success": False, "error": f"Template {template_name} not found"}
            
            with open(mapping_path, "r", encoding="utf-8") as f:
                mapping = json.load(f)
                
            w_layout = mapping.get("word_layout", {})
            styles_map = mapping.get("styles", {})
            
            doc = Document()
            
            # Title
            title_text = w_layout.get("title", "Documento").replace("{{ service_name }}", f"Servicio {header.service_id}")
            h1 = doc.add_heading(title_text, 0)
            h1.alignment = WD_ALIGN_PARAGRAPH.CENTER
            
            # Client Info (Simple implementation)
            doc.add_paragraph(f"Cliente: {payload.client_info.get('nombre', 'N/A')}")
            doc.add_paragraph(f"Fecha: {payload.client_info.get('fecha', 'N/A')}")
            
            # Table
            # Mirror Logic: Use Excel Columns to define Order
            # 1. Get Columns Definition
            tables = mapping.get("excel_layout", {}).get("tables", [])
            if not tables:
                 return {"success": False, "error": "No tables defined in mapping"}
            
            columns_map = tables[0].get("columns", {})
            # 2. Sort keys by Value (Column Letter)
            sorted_keys = sorted(columns_map.keys(), key=lambda k: columns_map[k])
            
            headers = w_layout.get("headers", [])
            if not headers: headers = [k.capitalize() for k in sorted_keys]

            items = payload.items
            
            # Verify Column Count Match?
            # if len(headers) != len(sorted_keys):
            #     logger.warning(f"Header count {len(headers)} != Key count {len(sorted_keys)}")
            
            table = doc.add_table(rows=1, cols=len(headers))
            table.style = 'Table Grid'
            hdr_cells = table.rows[0].cells
            for i, h in enumerate(headers):
                if i < len(hdr_cells):
                    hdr_cells[i].text = str(h)
                
            for item in items:
                row_cells = table.add_row().cells
                for i, key in enumerate(sorted_keys):
                    if i < len(row_cells):
                        if key == "index":
                           val = str(items.index(item) + 1)
                        else:
                           val = str(item.get(key, ""))
                        
                        if val.startswith("="): val = "(Calc)"
                        row_cells[i].text = val
            
            # Totals
            doc.add_paragraph("")
            if payload.totals.get('total'):
                p_total = doc.add_paragraph(f"TOTAL: {payload.totals.get('total', 0)}")
                p_total.alignment = WD_ALIGN_PARAGRAPH.RIGHT

            # Output
            output = io.BytesIO()
            doc.save(output)
            output.seek(0)
            b64_data = base64.b64encode(output.read()).decode('utf-8')
            
            return {
                "success": True, 
                "filename": f"{template_name}_GEN.docx",
                "file_b64": b64_data,
                "engine": "Universal Word v1.0"
            }

        except Exception as e:
            logger.error(f"Universal Word Gen Error: {e}", exc_info=True)
            return {"success": False, "error": str(e)}

    def _generate_universal_excel(self, template_name, branding, payload, header):
        """Universal Engine: Reads mapping.json and generates Excel"""
        try:
            template_dir = Path(__file__).parent / "templates" / template_name
            mapping_path = template_dir / "mapping.json"
            
            if not mapping_path.exists():
                 return {"success": False, "error": f"Template {template_name} not found"}
            
            with open(mapping_path, "r", encoding="utf-8") as f:
                mapping = json.load(f)
            
            # --- MICRO ENGINE FOR EXCEL ---
            from openpyxl import Workbook
            from openpyxl.styles import Font, PatternFill, Border, Side, Alignment
            import io
            
            wb = Workbook()
            ws = wb.active
            ws.title = mapping.get("excel_layout", {}).get("sheet_name", "Doc")
            
            layout = mapping.get("excel_layout", {})
            styles = mapping.get("styles", {})
            
            # 1. Static Cells
            for cell_coord, value in layout.get("static_cells", {}).items():
                ws[cell_coord] = value
                ws[cell_coord].font = Font(bold=True, size=12)
            
            # 2. Dynamic Cells
            dyn_map = layout.get("dynamic_cells", {})
            
            # Flatten context for simple mapping resolution
            ctx = {
                "client_name": payload.client_info.get("nombre", "N/A"),
                "total_value": payload.totals.get("total", 0),
                "service_name": f"Service {header.service_id}",
                # Add more as needed by mapping
            }
            
            if "client_name" in dyn_map:
                ws[dyn_map["client_name"]] = ctx["client_name"]
            if "total_value" in dyn_map:
                ws[dyn_map["total_value"]] = ctx["total_value"]
            
            # 3. Tables
            for table_def in layout.get("tables", []):
                data_key = table_def.get("data_key") # "items"
                start_row = table_def.get("start_row", 10)
                cols_map = table_def.get("columns", {})
                
                items = payload.items # List of models (dicts)
                
                current_row = start_row
                for idx, item in enumerate(items, 1):
                    # Item is dict
                    row_data = {
                        "index": idx,
                        "description": item.get("descripcion", ""),
                        "quantity": item.get("cantidad", 0),
                        "total": item.get("total", 0),
                        "unit": item.get("unidad", ""),
                        "price": item.get("precio_unitario", 0)
                    }
                    
                    for field, col_letter in cols_map.items():
                        if field in row_data:
                            cell_ref = f"{col_letter}{current_row}"
                            val = row_data[field]
                            
                            # FORMULA ENGINE (Simple)
                            if isinstance(val, str) and val.startswith("="):
                                # Replace placeholders? No, simpliest is direct formula.
                                # But formulas usually need relative row references like =C{row}*D{row}
                                # "Cuadro de Cargas" specifics require verifying "formulas en el Excel funcionen".
                                # If mapping.json defines a column as a formula template?
                                # E.g. "total": "=E{row}*F{row}"
                                # Let's assume the mapping or the data provides the formula pattern.
                                # Or better: allow mapping.json to define a "formula" for a column.
                                ws[cell_ref] = val.replace("{row}", str(current_row))
                            else:
                                ws[cell_ref] = val
                    
                    current_row += 1

            # Output
            output = io.BytesIO()
            wb.save(output)
            output.seek(0)
            b64_data = base64.b64encode(output.read()).decode('utf-8')
            
            return {
                "success": True, 
                "filename": f"{template_name}_GEN.xlsx",
                "file_b64": b64_data,
                "engine": "Universal v1.0"
            }

        except Exception as e:
            logger.error(f"Universal Gen Error: {e}", exc_info=True)
            return {"success": False, "error": str(e)}

    def _generate_excel(self, header, branding, payload):
        """
        Usa el Generador de Excel Profesional Original (Engineering Engine).
        Esto asegura celdas nativas, fórmulas y estructura perfecta.
        """
        try:
            if not self.excel_gen:
                return {"success": False, "error": "ExcelGenerator no disponible"}

            # Mapear tipo de documento al método del generador profesional
            doc_type_map = {
                1: "cotizacion_simple",
                2: "cotizacion_compleja",
                3: "proyecto_simple",
                4: "proyecto_complejo",
                5: "informe_tecnico",
                6: "informe_ejecutivo",
                "ELECTRICIDAD_COTIZACION_SIMPLE": "cotizacion_simple",
                "ELECTRICIDAD_COT_COMPLEJA": "cotizacion_compleja",
                "ELECTRICIDAD_PROYECTO_SIMPLE": "proyecto_simple",
                "ELECTRICIDAD_PROYECTO_COMPLEJO": "proyecto_complejo",
                "ELECTRICIDAD_INFORME_TECNICO": "informe_tecnico",
                "ELECTRICIDAD_INFORME_EJECUTIVO": "informe_ejecutivo"
            }
            
            mode = doc_type_map.get(header.document_type)
            if not mode:
                mode = "cotizacion_simple" # Fallback

            # Preparar datos para el generador original
            datos = {
                "numero": f"DOC-{header.user_id}-{header.service_id}",
                "cliente": payload.client_info,
                "proyecto": f"Proyecto Serv.{header.service_id}",
                "fecha": payload.client_info.get("fecha", ""),
                "items": payload.items,
                "totales": payload.totals,
                "subtotal": payload.totals.get("subtotal", 0),
                "igv": payload.totals.get("igv", 0),
                "total": payload.totals.get("total", 0),
                "normativa": payload.technical_notes.get("normativa", "CNE") if isinstance(payload.technical_notes, dict) else ""
            }

            import tempfile
            from pathlib import Path
            import io
            
            svc_id_fmt = str(header.service_id).zfill(4)
            final_name = f"{mode.upper()}_{svc_id_fmt}_TESLA.xlsx"
            tmp_path = Path(tempfile.gettempdir()) / final_name

            # Ejecutar generador profesional
            if mode == "cotizacion_simple":
                buffer = self.excel_gen.generate_cotizacion(datos, str(tmp_path))
            elif mode == "proyecto_simple":
                buffer = self.excel_gen.generate_proyecto_simple(datos, str(tmp_path))
            elif mode == "proyecto_complejo":
                buffer = self.excel_gen.generate_proyecto_complejo(datos, str(tmp_path))
            elif mode == "informe_tecnico":
                buffer = self.excel_gen.generate_informe_tecnico(datos, str(tmp_path))
            else:
                # Default a cotización si no hay método específico
                buffer = self.excel_gen.generate_cotizacion(datos, str(tmp_path))

            # Leer archivo generado
            with open(tmp_path, "rb") as f:
                b64_data = base64.b64encode(f.read()).decode('utf-8')
                
            return {
                "success": True,
                "filename": final_name,
                "file_b64": b64_data,
                "engine": "Professional Excel Native Engine"
            }

        except Exception as e:
            logger.error(f"Excel Generation Error (Native): {e}", exc_info=True)
            return {"success": False, "error": str(e)}
            
    def _generate_word(self, header, branding, payload):
        """
        Usa los Generadores Nativos (Engineering Engine).
        Utiliza las plantillas maestras (.docx) para asegurar la máxima calidad.
        """
        try:
            try:
                from .html_to_word_generator import html_to_word_generator
            except (ImportError, ValueError):
                from html_to_word_generator import html_to_word_generator
            
            # Map Document Type ID/String to HTML Generator Method
            doc_type_map = {
                1: "cotizacion_simple",
                2: "cotizacion_compleja",
                3: "proyecto_simple",
                4: "proyecto_complejo",
                5: "informe_tecnico",
                6: "informe_ejecutivo",
                "ELECTRICIDAD_COTIZACION_SIMPLE": "cotizacion_simple",
                "ELECTRICIDAD_COT_COMPLEJA": "cotizacion_compleja",
                "ELECTRICIDAD_PROYECTO_SIMPLE": "proyecto_simple",
                "ELECTRICIDAD_PROYECTO_COMPLEJO": "proyecto_complejo",
                "ELECTRICIDAD_INFORME_TECNICO": "informe_tecnico",
                "ELECTRICIDAD_INFORME_EJECUTIVO": "informe_ejecutivo"
            }
            
            mode = doc_type_map.get(header.document_type)
            if not mode:
                # String check fallback
                str_type = str(header.document_type)
                if "COTIZACION_SIMPLE" in str_type: mode = "cotizacion_simple"
                elif "COT_COMPLEJA" in str_type or "COTIZACION_COMPLEJA" in str_type: mode = "cotizacion_compleja"
                elif "PROYECTO_SIMPLE" in str_type: mode = "proyecto_simple"
                elif "PROYECTO_COMPLEJO" in str_type: mode = "proyecto_complejo"
                elif "INFORME_TECNICO" in str_type: mode = "informe_tecnico"
                elif "INFORME_EJECUTIVO" in str_type: mode = "informe_ejecutivo"
                else:
                    logger.warning(f"⚠️ No mapping for {header.document_type}. Falling back to 'cotizacion_simple' per RALFTH Resilience.")
                    mode = "cotizacion_simple"

            # Prepare Input Data for HTML Injection
            # Flatten payload for Jinja2/BeautifulSoup
            # Ensure we have valid dictionaries even if Model passed None/Empty
            client_info = payload.client_info if isinstance(payload.client_info, dict) else {}
            totals = payload.totals if isinstance(payload.totals, dict) else {}
            
            input_data = {
                "numero": f"DOC-{header.user_id}-{header.service_id}",
                "cliente": client_info,
                "proyecto": f"Proyecto Serv.{header.service_id}",
                "fecha": client_info.get("fecha", ""),
                "servicio_nombre": f"Servicio {header.service_id}",
                "items": payload.items if payload.items else [],
                "subtotal": totals.get("subtotal", 0),
                "igv": totals.get("igv", 0),
                "total": totals.get("total", 0),
                "branding_color": branding.color_hex,
                "technical_notes": payload.technical_notes,
                "user_id": header.user_id
            }
            
            # STRICT NAMING CONVENTION: INFORME_TECNICO_0001_TESLA.DOCX
            type_map = {
                "1": "COTIZACION_SIMPLE", "2": "COTIZACION_COMPLEJA",
                "3": "PROYECTO_SIMPLE", "4": "PROYECTO_COMPLEJO",
                "5": "INFORME_TECNICO", "6": "INFORME_EJECUTIVO",
                "ELECTRICIDAD_COTIZACION_SIMPLE": "COTIZACION_SIMPLE",
                "ELECTRICIDAD_COT_COMPLEJA": "COTIZACION_COMPLEJA",
                "ELECTRICIDAD_PROYECTO_SIMPLE": "PROYECTO_SIMPLE",
                "ELECTRICIDAD_PROYECTO_COMPLEJO": "PROYECTO_COMPLEJO",
                "ELECTRICIDAD_INFORME_TECNICO": "INFORME_TECNICO",
                "ELECTRICIDAD_INFORME_EJECUTIVO": "INFORME_EJECUTIVO"
            }
            doc_label = type_map.get(str(header.document_type), f"DOC_{header.document_type}")
            svc_id_fmt = str(header.service_id).zfill(4)
            final_name = f"{doc_label}_{svc_id_fmt}_TESLA.docx"
            
            import tempfile
            from pathlib import Path
            tmp_dir = Path(tempfile.gettempdir())
            output_path = tmp_dir / final_name
            
            # Dispatch to Native Word Generators (The Legacy Perfect Engine)
            try:
                # Handle Logo Path (Extract from Branding or use Default)
                logo_path = None
                default_logo = Path(__file__).parent / "templates" / "assets" / "logo.png"
                
                if branding.logo_b64:
                    try:
                        logo_data = base64.b64decode(branding.logo_b64.split(",")[-1])
                        logo_tmp = tmp_dir / f"logo_{header.user_id}_{header.service_id}.png"
                        with open(logo_tmp, "wb") as f:
                            f.write(logo_data)
                        logo_path = str(logo_tmp)
                        logger.info(f"🎨 Logo extracted to: {logo_path}")
                    except Exception as e:
                        logger.error(f"Failed to extract logo: {e}")
                
                # Fallback to local default logo if exists
                if not logo_path and default_logo.exists():
                    logo_path = str(default_logo)
                    logger.info(f"🎨 Using default Tesla logo: {logo_path}")

                options = {
                    "esquema_colores": "azul-tesla",
                    "logo_path": logo_path,
                    "mode": mode
                }


                if mode == "cotizacion_simple":
                    gen_fn = generar_cotizacion_simple
                elif mode == "cotizacion_compleja":
                    gen_fn = generar_cotizacion_compleja
                elif mode == "proyecto_simple":
                    gen_fn = generar_proyecto_simple
                elif mode == "proyecto_complejo":
                    gen_fn = generar_proyecto_complejo_pmi
                elif mode == "informe_tecnico":
                    gen_fn = generar_informe_tecnico
                elif mode == "informe_ejecutivo":
                    gen_fn = generar_informe_ejecutivo_apa
                else:
                    gen_fn = generar_cotizacion_simple
                
                # Execution with Options
                path = gen_fn(input_data, str(output_path), opciones=options)
                engine_used = "Native Word Generator (Legacy V8-V9 Perfect)"
            except Exception as e:
                import traceback
                logger.error(f"FATAL ERROR in native generator {mode}: {e}")
                logger.error(traceback.format_exc())
                raise e # CRITICAL: No more silent fallbacks

            # Read back file
            with open(path, "rb") as f:
                b64_data = base64.b64encode(f.read()).decode('utf-8')
                
            return {
                "success": True, 
                "filename": final_name,
                "file_b64": b64_data,
                "engine": engine_used
            }

        except Exception as e:
            logger.error(f"HTML-DOCX Generation Failed: {e}", exc_info=True)
            return {"success": False, "error": str(e)}

    def _generate_pdf(self, header, branding, payload):
        """Delegates to Playwright PDF Strategy (The HTML Mirror)"""
        try:
            # We must use the HTML -> PDF generator (Playwright) as originally intended
            # This logic captures the exact HTML look.
            try:
                from .generators.html_to_pdf_generator import generate_pdf_playwright
            except (ImportError, ValueError):
                from generators.html_to_pdf_generator import generate_pdf_playwright
            
            # STRICT NAMING CONVENTION
            # Determine Mode and Mapping (Same as Word/Excel)
            doc_type_map = {
                1: "cotizacion_simple",
                2: "cotizacion_compleja",
                3: "proyecto_simple",
                4: "proyecto_complejo",
                5: "informe_tecnico",
                6: "informe_ejecutivo",
                "ELECTRICIDAD_COTIZACION_SIMPLE": "cotizacion_simple",
                "ELECTRICIDAD_COT_COMPLEJA": "cotizacion_compleja",
                "ELECTRICIDAD_PROYECTO_SIMPLE": "proyecto_simple",
                "ELECTRICIDAD_PROYECTO_COMPLEJO": "proyecto_complejo",
                "ELECTRICIDAD_INFORME_TECNICO": "informe_tecnico",
                "ELECTRICIDAD_INFORME_EJECUTIVO": "informe_ejecutivo"
            }
            
            mode = doc_type_map.get(header.document_type)
            if not mode:
                str_type = str(header.document_type)
                if "COTIZACION_SIMPLE" in str_type: mode = "cotizacion_simple"
                elif "COT_COMPLEJA" in str_type or "COTIZACION_COMPLEJA" in str_type: mode = "cotizacion_compleja"
                elif "PROYECTO_SIMPLE" in str_type: mode = "proyecto_simple"
                elif "PROYECTO_COMPLEJO" in str_type: mode = "proyecto_complejo"
                elif "INFORME_TECNICO" in str_type: mode = "informe_tecnico"
                elif "INFORME_EJECUTIVO" in str_type: mode = "informe_ejecutivo"
                else:
                    mode = "cotizacion_simple"

            # Resolve Template File (Modern Mirror Layouts)
            template_filename_map = {
                "cotizacion_simple": "PLANTILLA_HTML_COTIZACION_SIMPLE.html",
                "cotizacion_compleja": "PLANTILLA_HTML_COTIZACION_COMPLEJA.html",
                "proyecto_simple": "PLANTILLA_HTML_PROYECTO_SIMPLE.html",
                "proyecto_complejo": "PLANTILLA_HTML_PROYECTO_COMPLEJO_PMI.html",
                "informe_tecnico": "PLANTILLA_HTML_INFORME_TECNICO.html",
                "informe_ejecutivo": "PLANTILLA_HTML_INFORME_EJECUTIVO_APA.html"
            }
            
            template_file = template_filename_map.get(mode, "PLANTILLA_HTML_COTIZACION_SIMPLE.html")
            template_path = Path(__file__).parent / "templates" / "html" / template_file
            
            if not template_path.exists():
                logger.warning(f"Template not found: {template_path}. Using fallback.")
                template_path = Path(__file__).parent / "templates" / "html" / "PLANTILLA_HTML_COTIZACION_SIMPLE.html"

            logger.info(f"📄 PDF Generation using Mirror Template: {template_path}")


            input_data = {
                "numero": f"DOC-{header.user_id}-{header.service_id}",
                "cliente": payload.client_info.get("nombre", "Cliente"),
                "fecha": payload.client_info.get("fecha", ""),
                "items": payload.items,
                "subtotal": payload.totals.get("subtotal", 0),
                "igv": payload.totals.get("igv", 0),
                "total": payload.totals.get("total", 0),
                "branding": {
                    "logo_b64": branding.logo_b64,
                    "color": branding.color_hex
                },
                "document_type": header.document_type,
                "technical_notes": payload.technical_notes,
                "client_info": payload.client_info, # Pass full info
                "totals": payload.totals # Ensure totals dict is passed correctly
            }
            
            doc_label = mode.upper()
            svc_id_fmt = str(header.service_id).zfill(4)
            final_name = f"{doc_label}_{svc_id_fmt}_TESLA.pdf"
            
            import tempfile
            tmp_dir = Path(tempfile.gettempdir())
            output_path = tmp_dir / final_name
            
            # Execute Generator with Explicit Template Path
            path = generate_pdf_playwright(input_data, str(output_path), template_path=str(template_path))
            
            # Read and return B64
            with open(path, "rb") as f:
                b64_data = base64.b64encode(f.read()).decode('utf-8')
                
            return {
                "success": True, 
                "filename": final_name,
                "file_b64": b64_data,
                "engine": "Playwright V10 (HTML Mirror)"
            }
        except Exception as e:
            logger.error(f"Playwright PDF Generation Failed: {e}", exc_info=True)
    def _generate_mirror_pdf(self, html_content: str, output_path: str) -> dict:
        """
        Generates a 100% fidelity PDF from raw HTML using Playwright.
        """
        try:
            import subprocess
            import tempfile
            import sys
            import base64
            from pathlib import Path
            
            # 1. Create temporary HTML file
            with tempfile.NamedTemporaryFile(suffix=".html", delete=False, mode="w", encoding="utf-8") as tmp:
                tmp.write(html_content)
                html_tmp_path = tmp.name
            
            try:
                # 2. Invoke specialized CLI
                cli_path = Path(__file__).parent / "generators" / "playwright_pdf_cli.py"
                result = subprocess.run(
                    [sys.executable, str(cli_path), html_tmp_path, str(output_path)],
                    capture_output=True,
                    text=True
                )
                
                if result.returncode != 0 or "ERROR:" in result.stdout:
                    logger.error(f"Mirror PDF CLI Error: {result.stdout} {result.stderr}")
                    return {"success": False, "error": f"CLI Error: {result.stdout}"}
                
                # 3. Read back file
                if os.path.exists(output_path):
                    with open(output_path, "rb") as f:
                        b64_data = base64.b64encode(f.read()).decode('utf-8')
                    
                    return {
                        "success": True,
                        "filename": os.path.basename(output_path),
                        "file_b64": b64_data,
                        "engine": "Playwright Mirror V10"
                    }
                else:
                    return {"success": False, "error": "Output PDF not found after CLI execution"}
                    
            finally:
                if os.path.exists(html_tmp_path):
                    os.remove(html_tmp_path)
                    
        except Exception as e:
            logger.error(f"Mirror PDF Generation Crash: {e}", exc_info=True)
            return {"success": False, "error": str(e)}


    async def generate_document(self, html_content: str, output_path: str, format_type: str, doc_type: str, options: dict = None) -> dict:
        """
        Bridge method for V3 Compatibility.
        Parses HTML and then calls the V10 process_request.
        """
        try:
            try:
                from .html_parser import html_parser
            except (ImportError, ValueError):
                from html_parser import html_parser
            
            # 1. Parse HTML to structured Data (Soberano V10 Robust Parser)
            logger.info(f"🔍 Parsing HTML for {doc_type} in Studio Bridge...")
            extracted_data = html_parser.parsear_html_editado(html_content, doc_type)
            
            if extracted_data.get("error"):
                return {"success": False, "error": extracted_data.get("mensaje")}

            # 2. Map to V10 BinaryFactoryInput structure (Strict Contract)
            # Normalizar doc_type para el mapeo del generador
            normalized_doc_type = doc_type.upper().replace(" ", "_").replace("-", "_")
            
            input_dict = {
                "header": {
                    "user_id": extracted_data.get("emisor_nombre") or "Studio_User",
                    "service_id": 1, 
                    "document_type": normalized_doc_type
                },
                "branding": {
                    "logo_b64": options.get("logoBase64") if options else None,
                    "color_hex": options.get("esquemaColores", "#0052A3") if options else "#0052A3"
                },
                "payload": {
                    "items": extracted_data.get("items", []),
                    "totals": {
                        "subtotal": extracted_data.get("subtotal", 0),
                        "igv": extracted_data.get("igv", 0),
                        "total": extracted_data.get("total", 0)
                    },
                    "technical_notes": "",
                    "client_info": {
                        "nombre": extracted_data.get("cliente", ""),
                        "ruc": extracted_data.get("cliente_ruc", ""),
                        "direccion": extracted_data.get("cliente_direccion", ""),
                        "fecha": extracted_data.get("fecha", "")
                    }
                },
                "output_format": format_type.upper().replace("WORD", "DOCX").replace("EXCEL", "XLSX")
            }
            
            # 3. Process via V10 Engine (Synchronous Core)
            logger.info(f"⚙️ Dispatching to V10 Engine: {input_dict['output_format']}")
            
            # EXCEPCION SOBERANA: PDF es el único que usa Playwright (Confirmado correcto por usuario)
            # Word y Excel DEBEN usar sus motores de ingeniería nativos (V9 Perfect)
            target_format = format_type.upper()
            if target_format == "PDF":
                logger.info("🎨 Applying High-Fidelity PDF Mirror Strategy (Playwright)...")
                result = self._generate_mirror_pdf(html_content, output_path)
            else:
                # Word (DOCX) y Excel (XLSX) vuelven a la ruta de ingeniería probada
                logger.info(f"🏛️ Using Native Engineering Engine for {target_format}")
                result = self.process_request(input_dict)
            
            # 4. Handle output path for V3 compatibility (FileResponse expects the file at output_path)
            if result.get("success") and "file_b64" in result:
                import base64
                file_data = base64.b64decode(result["file_b64"])
                
                # Asegurar directorio de salida
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                
                with open(output_path, "wb") as f:
                    f.write(file_data)
                
                logger.info(f"✅ Bridge Success: File written to {output_path}")
                return {"success": True, "filename": os.path.basename(output_path)}
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Error in V3-V10 Bridge: {e}", exc_info=True)
            return {"success": False, "error": str(e)}


# Singleton Instance
binary_factory = BinaryFactory()
