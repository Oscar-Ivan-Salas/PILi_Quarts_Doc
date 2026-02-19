
from fastapi import APIRouter, HTTPException, Body
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Dict, Any, Optional
import logging
import os
import tempfile
import re
from datetime import datetime
from pathlib import Path

from app.core.config import get_generated_directory
from app.services.excel_generator import excel_generator

# IMPORT LEGACY GENERATORS (THE "GOLDEN" MODELS)
from app.services.generators.cotizacion_simple_generator import generar_cotizacion_simple
from app.services.generators.cotizacion_compleja_generator import generar_cotizacion_compleja
from app.services.generators.proyecto_simple_generator import generar_proyecto_simple
from app.services.generators.proyecto_complejo_pmi_generator import generar_proyecto_complejo_pmi
from app.services.generators.informe_tecnico_generator import generar_informe_tecnico
from app.services.generators.informe_ejecutivo_apa_generator import generar_informe_ejecutivo_apa

# IMPORT LIBREOFFICE PDF ENGINE
try:
    from app.services.pdf_generator_v2 import pdf_generator_v2
except ImportError:
    pdf_generator_v2 = None

# IMPORT N04 BINARY FACTORY GENERATORS (New Engine)
try:
    from modules.N04_Binary_Factory import html_to_word_generator
    from modules.N04_Binary_Factory import excel_converter
except ImportError as e:
    logger.error(f"Failed to import N04 Generators: {e}")
    html_to_word_generator = None
    excel_converter = None

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/generate",
    tags=["generation"]
)

class DocumentRequest(BaseModel):
    html_content: Optional[str] = None  # ✅ NUEVO: HTML de vista previa
    title: str = "Documento"
    type: str = "general"
    data: Dict[str, Any]
    user_id: str
    doc_type: Optional[str] = None
    personalizacion: Optional[Dict[str, Any]] = {}


@router.post("/excel")
async def generate_excel(request: DocumentRequest):
    print(f"\n\n{'='*50}\n!!! HIT ENDPOINT EXCEL !!!\nREQUEST TITLE: {request.title}\n{'='*50}\n\n")
    try:
        storage_path = get_generated_directory()
        safe_title = "".join([c for c in request.title if c.isalnum() or c in (' ', '_', '-')]).strip()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{safe_title}_{timestamp}.xlsx"
        filepath = os.path.join(storage_path, filename)
        
        logger.info(f"📊 Generating Excel: {filename}")
        
        # ✅ PRIORIDAD 1: Si viene HTML directo, usar N04 Mirror
        if request.html_content:
            logger.info("🎯 Usando HTML directo de vista previa (RALFTH)")
            final_path = _generate_excel_from_html(request.html_content, filepath, filename)
        else:
            # FALLBACK: Método legacy
            logger.info("⚠️ Usando método legacy (sin HTML)")
            final_path = _generate_excel_internal(request, filepath)
        
        if not os.path.exists(final_path):
             raise HTTPException(status_code=500, detail="Failed to create Excel file")
             
        return FileResponse(
            path=final_path,
            filename=filename,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except Exception as e:
        logger.error(f"Excel generation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))





def _generate_excel_from_html(html_content: str, output_path: str, filename: str) -> str:
    """Genera Excel ESPEJO del HTML usando TeslaExcelConverter (Código Probado)"""
    try:
        from modules.N04_Binary_Factory.excel_converter import TeslaExcelConverter
        
        logger.info(f"📊 Generando Excel ESPEJO desde HTML (TeslaExcelConverter)")
        logger.info(f"📏 Tamaño HTML: {len(html_content)} caracteres")
        
        # ✅ USAR CÓDIGO PROBADO que genera espejos perfectos
        converter = TeslaExcelConverter()
        converter.convert_html_string(html_content, output_path)
        
        if not Path(output_path).exists():
            raise Exception("Failed to generate Excel from HTML")
        
        file_size = Path(output_path).stat().st_size
        logger.info(f"✅ Excel ESPEJO generado: {filename} ({file_size} bytes)")
        return output_path
        
    except Exception as e:
        logger.error(f"Error generating Excel from HTML: {e}", exc_info=True)
        raise e




def _generate_pdf_from_html(html_content: str, output_path: str, filename: str, customization: dict = None, request_data: dict = None) -> str:
    """Genera PDF directamente desde HTML de vista previa"""
    try:
        logger.info(f"📄 Generando PDF desde HTML directo (Mirror)")
        
        # 0. RENDERIZADO DE VARIABLES (Fidelidad Espejo)
        try:
            from modules.N04_Binary_Factory import html_to_word_generator
            # Usar datos del request para el reemplazo
            data_to_inject = request_data if request_data else {}
            # Reemplazar variables {{...}} e Imágenes IA <image:...>
            html_content = html_to_word_generator.html_to_word_generator._reemplazar_variables(html_content, data_to_inject)
            logger.info("✅ Variables e Imágenes IA renderizadas en el HTML del PDF.")
        except Exception as e:
            logger.warning(f"⚠️ Error renderizando variables en PDF: {e}")

        # Guardar HTML temporal
        tmp_html = Path(tempfile.gettempdir()) / f"temp_{filename}.html"
        with open(tmp_html, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Intentar con LibreOffice primero
        try:
            from app.services.pdf_generator_v2 import pdf_generator_v2
            if pdf_generator_v2:
                # Convertir HTML a PDF con LibreOffice
                pdf_path = pdf_generator_v2.convertir_html_a_pdf(tmp_html)
                if pdf_path and Path(pdf_path).exists():
                    # Mover a output_path
                    import shutil
                    shutil.move(str(pdf_path), output_path)
                    logger.info(f"✅ PDF generado con LibreOffice: {filename}")
                    return output_path
        except Exception as e:
            logger.warning(f"LibreOffice no disponible: {e}")
        
        # Fallback: Playwright
        try:
            from modules.N04_Binary_Factory.generators.html_to_pdf_generator import generate_pdf_playwright
            
            # generate_pdf_playwright espera template_path, pero podemos pasar el HTML temporal
            # PASAR CUSTOMIZATION A PLAYWRIGHT
            pdf_path = generate_pdf_playwright({}, output_path, template_path=str(tmp_html), customization=customization)
            
            if Path(pdf_path).exists():
                logger.info(f"✅ PDF generado con Playwright: {filename}")
                return pdf_path
        except Exception as e:
            logger.error(f"Playwright también falló: {e}")
            raise Exception("No PDF generator available")
        
    except Exception as e:
        logger.error(f"Error generating PDF from HTML: {e}", exc_info=True)
        raise e


def _generate_word_from_html(html_content: str, output_path: str, filename: str, customization: dict = None, request_data: dict = None) -> str:
    """Genera Word directamente desde HTML de vista previa (Fidelidad Espejo)"""
    try:
        if not html_to_word_generator:
            raise ImportError("html_to_word_generator not available")
            
        logger.info(f"📄 Generando Word desde HTML directo (RALFTH)")
        
        # 0. Personalización de HTML (Estilos forzados)
        if customization:
            try:
                # Mapa de colores para fallback
                color_map = {
                    'azul-tesla': '#3B82F6',
                    'rojo-energia': '#EF4444',
                    'verde-ecologico': '#10B981',
                    'dorado-premium': '#F59E0B'
                }
                
                # Obtener color primario
                color_id = customization.get('esquemaColores', 'azul-tesla')
                primary_color = color_map.get(color_id, '#3B82F6')
                
                # 1. Reemplazo de Colores (Brute Force)
                target_colors = [
                    '#3B82F6', '#2563EB', '#1D4ED8', '#0052cc', # Hex
                    'rgb(59, 130, 246)', 'rgb(37, 99, 235)', 'rgb(29, 78, 216)', 'rgb(0, 82, 204)' # RGB
                ]
                
                html_modified = html_content
                for color in target_colors:
                    html_modified = html_modified.replace(color, primary_color)
                    if color.startswith('#'):
                         html_modified = html_modified.replace(color.lower(), primary_color)
                
                html_content = html_modified
                logger.info(f"🎨 Colores Word reemplazados por {primary_color}")

            except Exception as e:
                logger.error(f"⚠️ Error aplicando estilos a Word (continuando): {e}")

        # 0. RENDERIZADO DE VARIABLES (Fidelidad Espejo)
        try:
            from modules.N04_Binary_Factory.index import binary_factory
            # Si el endpoint principal nos pasó el request.data, lo usamos
            # Pero _generate_word_from_html no recibe 'request', así que asumimos que 
            # para RALFTH, el HTML debería venir ya renderizado o usamos un fallback si tenemos datos
            # Reemplazar variables {{...}} con los datos reales de la personalización
            data_to_use = request_data if request_data else (customization or {})
            html_content = html_to_word_generator.html_to_word_generator._reemplazar_variables(html_content, data_to_use)
            logger.info("✅ Variables renderizadas en el HTML del Word.")
        except Exception as e:
            logger.warning(f"⚠️ No se pudieron renderizar todas las variables en Word: {e}")

        # 1. Instanciar Generador
        # IMPORTANTE: HTMLToWordGenerator es una clase
        generator = html_to_word_generator.HTMLToWordGenerator()
        
        # 2. Convertir
        output_path_obj = Path(output_path)
        # Asegurar directorio
        output_path_obj.parent.mkdir(parents=True, exist_ok=True)
        
        # Usar metodo interno del generador (Sincronizado con N04 Profesional)
        # use_master=False garantiza que NO use el template viejo de Tesla
        generator._convertir_html_a_word(html_content, output_path_obj, use_master=False)
        
        if output_path_obj.exists():
            logger.info(f"✅ Word generado exitosamente: {filename}")
            return str(output_path_obj)
        else:
            raise Exception("Word file not created")
            
    except Exception as e:
        logger.error(f"Error generating Word from HTML: {e}", exc_info=True)
        raise e



def _generate_excel_internal(request: DocumentRequest, output_path: str) -> str:
    """Internal helper to route to the correct Excel Generator"""
    doc_type = request.doc_type or request.type
    
    # Map frontend types to Excel Generator Functions
    if "cotizacion" in doc_type.lower():
        if "compleja" in doc_type.lower():
            return excel_generator.generar_cotizacion_compleja(request.data, output_path)
        else:
            return excel_generator.generar_cotizacion_simple(request.data, output_path)
            
    elif "proyecto" in doc_type.lower():
        if "complejo" in doc_type.lower() or "pmi" in doc_type.lower():
            return excel_generator.generar_proyecto_complejo(request.data, output_path)
        else:
            return excel_generator.generar_proyecto_simple(request.data, output_path)
            
    elif "informe" in doc_type.lower():
        if "ejecutivo" in doc_type.lower() or "apa" in doc_type.lower():
            return excel_generator.generar_informe_ejecutivo(request.data, output_path)
        else:
            return excel_generator.generar_informe_tecnico(request.data, output_path)
            
    else:
        # Default fallback
        logger.warning(f"Unknown doc_type '{doc_type}', defaulting to Cotizacion Simple")
        return excel_generator.generar_cotizacion_simple(request.data, output_path)

def _generate_word_internal(request: DocumentRequest, output_path: str) -> str:
    """Internal helper to route to the correct Legacy Generator"""
    doc_type = request.doc_type or request.type
    
    # Map frontend types to Legacy Generator Functions
    # Based on legacy logic
    
    opciones = request.personalizacion or {}
    
    if "cotizacion" in doc_type:
        if "compleja" in doc_type:
            return generar_cotizacion_compleja(request.data, output_path, opciones)
        else:
            return generar_cotizacion_simple(request.data, output_path, opciones)
            
    elif "proyecto" in doc_type:
        if "complejo" in doc_type or "pmi" in doc_type:
            return generar_proyecto_complejo_pmi(request.data, output_path, opciones)
        else:
            return generar_proyecto_simple(request.data, output_path, opciones)
            
    elif "informe" in doc_type:
        if "ejecutivo" in doc_type or "apa" in doc_type:
            return generar_informe_ejecutivo_apa(request.data, output_path)
        else:
            return generar_informe_tecnico(request.data, output_path, opciones)
            
    else:
        # Default fallback
        logger.warning(f"Unknown doc_type '{doc_type}', defaulting to Cotizacion Simple")
        return generar_cotizacion_simple(request.data, output_path, opciones)

@router.post("/word")
async def generate_word(request: DocumentRequest):
    try:
        storage_path = get_generated_directory()
        safe_title = "".join([c for c in request.title if c.isalnum() or c in (' ', '_', '-')]).strip()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{safe_title}_{timestamp}.docx"
        filepath = str(storage_path / filename)
        
        logger.info(f"📄 Generating Word: {filename}")
        
        # ✅ PRIORIDAD 1: Si viene HTML directo, usar N04 Mirror
        if request.html_content:
            logger.info("🎯 Usando HTML directo de vista previa (RALFTH)")
            # Nota: request.data contiene los valores para reemplazar {{...}}
            final_path = _generate_word_from_html(
                request.html_content, 
                filepath, 
                filename, 
                customization=request.personalizacion,
                request_data=request.data
            )
        else:
            # FALLBACK: Método legacy
            logger.info("📝 Usando método legacy (sin HTML)")
            final_path = _generate_word_internal(request, filepath)
        
        if not os.path.exists(final_path):
             raise HTTPException(status_code=500, detail="Failed to create Word file")

        return FileResponse(
            path=final_path,
            filename=filename,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    except Exception as e:
        logger.error(f"Word generation error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/pdf")
async def generate_pdf(request: DocumentRequest):
    """
    Generates PDF using RALFTH if HTML provided, otherwise Golden Method: 
    Python Generator -> Word -> LibreOffice -> PDF
    """
    try:
        storage_path = get_generated_directory()
        safe_title = "".join([c for c in request.title if c.isalnum() or c in (' ', '_', '-')]).strip()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        pdf_filename = f"{safe_title}_{timestamp}.pdf"
        pdf_path = str(storage_path / pdf_filename)
        
        logger.info(f"📄 Generating PDF: {pdf_filename}")
        
        # ✅ PRIORIDAD 1: Si viene HTML directo, usar N04 Mirror
        if request.html_content:
            logger.info("🎯 Usando HTML directo de vista previa (RALFTH)")
            final_path = _generate_pdf_from_html(
                request.html_content, 
                pdf_path, 
                pdf_filename, 
                customization=request.personalizacion,
                request_data=request.data
            )
            
            return FileResponse(
                path=final_path,
                filename=pdf_filename,
                media_type="application/pdf"
            )
        
        # FALLBACK: Método Golden (Word -> PDF)
        logger.info("🚀 Usando método Golden (Word -> PDF)")
        
        # 1. Generate Word first (The "Golden Model")
        word_filename = f"{safe_title}_{timestamp}.docx"
        word_path = str(storage_path / word_filename)
        
        logger.info(f"📝 Generating Base Word for PDF: {word_filename}")
        word_generated_path = _generate_word_internal(request, word_path)
        
        # 2. Convert to PDF using LibreOffice (The "Golden Engine")
        if pdf_generator_v2:
            logger.info("🖨️ Converting to PDF via LibreOffice...")
            pdf_result = pdf_generator_v2.convertir_word_a_pdf(Path(word_generated_path))
            
            if not pdf_result.exists():
                raise HTTPException(status_code=500, detail="PDF conversion failed (LibreOffice error)")
                
            return FileResponse(
                path=str(pdf_result),
                filename=pdf_result.name,
                media_type="application/pdf"
            )
        else:
            logger.error("❌ PDF Generator V2 (LibreOffice) not available")
            raise HTTPException(status_code=500, detail="PDF Engine Unavailable")
            
    except Exception as e:
        logger.error(f"❌ PDF generation error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
