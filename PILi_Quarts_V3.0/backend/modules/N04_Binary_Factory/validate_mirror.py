
import os
import sys
import logging
from pathlib import Path
import datetime

# --- CONFIGURACIÓN DE LOGGING ---
logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(message)s')
logger = logging.getLogger("TeslaValidation")

# --- PATHS ---
# Current Script Dir: modules/N04_Binary_Factory
CURRENT_DIR = Path(__file__).parent
MODULES_DIR = CURRENT_DIR.parent
BACKEND_DIR = MODULES_DIR.parent

# Add backend to sys.path to import modules if needed (though we try to keep local)
sys.path.append(str(BACKEND_DIR))

# N04 Paths
TEMPLATE_DIR = CURRENT_DIR / "templates" / "html"
OUTPUT_DIR = CURRENT_DIR / "output_mirror"
ASSETS_DIR = CURRENT_DIR / "templates" / "assets"
LOGO_PATH = ASSETS_DIR / "logo.png"

# Import Generators
try:
    from excel_converter import TeslaExcelConverter
    from html_to_word_generator import HTMLToWordGenerator
    from pdf_generator import PDFGenerator
except ImportError:
    from modules.N04_Binary_Factory.excel_converter import TeslaExcelConverter
    from modules.N04_Binary_Factory.html_to_word_generator import HTMLToWordGenerator
    from modules.N04_Binary_Factory.pdf_generator import PDFGenerator

def create_dummy_logo(path):
    try:
        from PIL import Image
        img = Image.new('RGB', (200, 80), color=(0, 82, 163))
        os.makedirs(os.path.dirname(path), exist_ok=True)
        img.save(path)
        logger.info(f"✅ Dummy Logo created at: {path}")
    except ImportError:
        logger.warning("⚠️ PIL not installed. Skipping Logo creation.")

class UniversalFactoryValidator:
    def __init__(self):
        self.excel = TeslaExcelConverter()
        self.word = HTMLToWordGenerator()
        self.pdf = PDFGenerator()
        
        # Configure Check
        self.excel.assets_dir = ASSETS_DIR
        self.excel.logo_path = LOGO_PATH
        
        # Word needs logo b64 sometimes or path? 
        # HTMLToWord uses Jinja, so assumes images are in HTML or handled.
        # PDF uses path or b64
        
    def generate_all_formats(self, model_name, data, output_base):
        results = []
        
        # 1. EXCEL
        try:
            xls_path = output_base.with_suffix('.xlsx')
            logger.info(f"   Generating Excel: {xls_path.name}")
            if "Cotizacion" in model_name: 
                # Need html string for Excel
                # Re-reading template here simplifies logic vs passing complex separate args
                template_name = self._get_template_name(model_name)
                html_filled = self._get_filled_html(template_name, data)
                self.excel.convert_html_string(html_filled, xls_path)
            elif "Informe" in model_name or "Proyecto" in model_name:
                template_name = self._get_template_name(model_name)
                html_filled = self._get_filled_html(template_name, data)
                self.excel.convert_html_string(html_filled, xls_path)
            results.append("XLSX: OK")
        except Exception as e:
            results.append(f"XLSX: FAIL ({e})")
            logger.error(f"XLSX Error: {e}")

        # 2. WORD
        try:
            doc_path = output_base.with_suffix('.docx')
            logger.info(f"   Generating Word: {doc_path.name}")
            
            # Map model name to internal generator method
            # Cotizacion_Compleja -> generar_cotizacion_compleja
            method_name = f"generar_{model_name.lower()}"
            if hasattr(self.word, method_name):
                method = getattr(self.word, method_name)
                method(data, doc_path)
                results.append("DOCX: OK")
            else:
                 results.append("DOCX: SKIP (No Method)")
        except Exception as e:
            results.append(f"DOCX: FAIL ({e})")
            logger.error(f"DOCX Error: {e}")

        # 3. PDF
        try:
            pdf_path = output_base.with_suffix('.pdf')
            logger.info(f"   Generating PDF: {pdf_path.name}")
            
            # PDF Generator uses specific methods too
            # generar_cotizacion, generar_informe_proyecto, generar_informe_simple
            if "Cotizacion" in model_name:
                self.pdf.generar_cotizacion(data, str(pdf_path))
            elif "Proyecto" in model_name:
                # Use Informe Proyecto logic for Projects
                self.pdf.generar_informe_proyecto(data, str(pdf_path))
            elif "Informe" in model_name:
                if "Simple" in model_name:
                     self.pdf.generar_informe_simple(data, str(pdf_path))
                else: 
                     # Reporte Tecnico? Use Proyecto as fallback or create new
                     self.pdf.generar_informe_proyecto(data, str(pdf_path))
            
            results.append("PDF: OK")
        except Exception as e:
            results.append(f"PDF: FAIL ({e})")
            logger.error(f"PDF Error: {e}")
            
        return results

    def _get_template_name(self, model_name):
        map = {
            "Cotizacion_Compleja": "PLANTILLA_HTML_COTIZACION_COMPLEJA.html",
            "Cotizacion_Simple": "PLANTILLA_HTML_COTIZACION_SIMPLE.html",
            "Informe_Tecnico": "PLANTILLA_HTML_INFORME_TECNICO.html",
            "Informe_Ejecutivo": "PLANTILLA_HTML_INFORME_EJECUTIVO_APA.html",
            "Proyecto_Complejo": "PLANTILLA_HTML_PROYECTO_COMPLEJO_PMI.html",
            "Proyecto_Simple": "PLANTILLA_HTML_PROYECTO_SIMPLE.html"
        }
        return map.get(model_name)

    def _get_filled_html(self, template_file, data):
        path = TEMPLATE_DIR / template_file
        with open(path, 'r', encoding='utf-8') as f:
            html = f.read()
            for k, v in data.items():
                if isinstance(v, (str, int, float)):
                    html = html.replace(f"{{{{{k}}}}}", str(v))
        return html


def verify_full_suite():
    timestamp = datetime.datetime.now().strftime("%H%M%S")
    
    # 1. Output Directory inside Node
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    logger.info(f"📂 Output Directory: {OUTPUT_DIR}")

    # 2. Ensure Assets
    create_dummy_logo(LOGO_PATH)

    # 3. Test Data (Expanded for all formats)
    base_data = {
        "numero": f"COT-{timestamp}", # Word expects lowercase keys sometimes?
        "CODIGO_COTIZACION": f"COT-{timestamp}",
        "cliente": "MINERA LAS BAMBAS S.A.",
        "CLIENTE": "MINERA LAS BAMBAS S.A.",
        "fecha": "15/02/2026",
        "FECHA": "15/02/2026",
        "total": 45250.00,
        "TOTAL": "45,250.00",
        "subtotal": 38347.46,
        "SUBTOTAL": "38,347.46",
        "igv": 6902.54,
        "IGV": "6,902.54",
        "moneda": "USD",
        "MONEDA": "USD",
        "vigencia": "15 Días",
        "VALIDEZ": "15 Días",
        "tiempo_entrega": "10 Días",
        "TIEMPO_ENTREGA": "10 Días",
        "forma_pago": "50% Adelanto",
        "FORMA_PAGO": "50% Adelanto",
        "garantia": "12 Meses",
        "GARANTIA": "12 Meses",
        "titulo": "MANTENIMIENTO DE SUBESTACIÓN 22.9KV",
        "TITULO_INFORME": "MANTENIMIENTO DE SUBESTACIÓN 22.9KV",
        "codigo": f"INF-{timestamp}",
        "CODIGO_INFORME": f"INF-{timestamp}",
        "resumen": "Se realizó el mantenimiento preventivo de la celda de media tensión...",
        "RESUMEN_EJECUTIVO": "Se realizó el mantenimiento preventivo de la celda de media tensión...",
        "servicio_nombre": "MANTENIMIENTO PREVENTIVO",
        "SERVICIO_NOMBRE": "MANTENIMIENTO PREVENTIVO",
        "normativa": "IEEE 80-2013 / CNE Suministro",
        "NORMATIVA_APLICABLE": "IEEE 80-2013 / CNE Suministro",
        "nombre": "AMPLIACIÓN DE SISTEMA DE PUESTA A TIERRA",
        "NOMBRE_PROYECTO": "AMPLIACIÓN DE SISTEMA DE PUESTA A TIERRA",
        "CODIGO_PROYECTO": f"PRJ-{timestamp}",
        "duracion_total": "45",
        "DURACION_TOTAL": "45",
        "fecha_inicio": "01/03/2026",
        "FECHA_INICIO": "01/03/2026",
        "fecha_fin": "15/04/2026",
        "FECHA_FIN": "15/04/2026",
        "presupuesto": 125000.00,
        "PRESUPUESTO": "125,000.00",
        "spi": "0.98",
        "SPI": "0.98",
        "cpi": "1.02",
        "CPI": "1.02",
        "ev": 45000,
        "EV_K": "45",
        "pv": 46000,
        "PV_K": "46",
        "ac": 44000,
        "AC_K": "44",
        "alcance": "Ingeniería de detalle, suministro de materiales...",
        "ALCANCE_PROYECTO": "Ingeniería de detalle, suministro de materiales...",
        "items": [
           {"descripcion": "Item 1 Demo", "cantidad": 1, "unidad": "und", "precio_unitario": 100, "total": 100},
           {"descripcion": "Item 2 Demo", "cantidad": 2, "unidad": "m", "precio_unitario": 50, "total": 100}
        ]
    }

    validator = UniversalFactoryValidator()
    
    models = [
        "Cotizacion_Compleja",
        "Cotizacion_Simple",
        "Informe_Tecnico",
        "Informe_Ejecutivo",
        "Proyecto_Complejo",
        "Proyecto_Simple"
    ]
    
    print(f"🚀 Iniciando Verificación UNIVERSAL (Node N04)...")
    print(f"Formatos: XLSX (Mirror), DOCX (HTML->Word), PDF (ReportLab)")

    for name in models:
        logger.info(f"🔄 Procesando Modelo: {name}")
        base_path = OUTPUT_DIR / f"{name}_V10_{timestamp}"
        results = validator.generate_all_formats(name, base_data, base_path)
        logger.info(f"   👉 Estado {name}: {', '.join(results)}")


if __name__ == "__main__":
    verify_full_suite()
