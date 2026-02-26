
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

# IMPORT N04 SOVEREIGN BINARY FACTORY (Protocolo R.A.L.F.T.H. V2)
try:
    from modules.N04_Binary_Factory.index import binary_factory
except ImportError as e:
    logger.error(f"Failed to import N04 Sovereign Factory: {e}")
    binary_factory = None

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
    """Genera Excel ESPEJO usando el Nodo N04 Soberano"""
    try:
        if not binary_factory:
            raise ImportError("N04 Binary Factory not available")
            
        logger.info(f"📊 Generando Excel ESPEJO (N04 Sovereign Engine)")
        result = binary_factory.generate_document(html_content, output_path, "excel")
        
        if not result.get("success"):
            raise Exception(result.get("error"))
            
        return output_path
    except Exception as e:
        logger.error(f"Error generating Excel via N04: {e}")
        raise e




def _generate_pdf_from_html(html_content: str, output_path: str, filename: str, customization: dict = None, request_data: dict = None) -> str:
    """Genera PDF ESPEJO usando el Nodo N04 Soberano"""
    try:
        if not binary_factory:
            raise ImportError("N04 Binary Factory not available")
            
        logger.info(f"📄 Generando PDF ESPEJO (N04 Sovereign Engine)")
        result = binary_factory.generate_document(html_content, output_path, "pdf")
        
        if not result.get("success"):
            raise Exception(result.get("error"))
            
        return output_path
    except Exception as e:
        logger.error(f"Error generating PDF via N04: {e}")
        raise e


def _generate_word_from_html(html_content: str, output_path: str, filename: str, doc_type: str = "cotizacion_simple") -> str:
    """Genera Word ESPEJO usando el Nodo N04 Soberano"""
    try:
        if not binary_factory:
            raise ImportError("N04 Binary Factory not available")
            
        logger.info(f"📄 Generando Word ESPEJO (N04 Sovereign Engine) para {doc_type}")
        result = binary_factory.generate_document(html_content, output_path, "word", doc_type)
        
        if not result.get("success"):
            raise Exception(result.get("error"))
            
        return output_path
    except Exception as e:
        logger.error(f"Error generating Word via N04: {e}")
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
            doc_type = request.doc_type or request.type
            final_path = _generate_word_from_html(request.html_content, filepath, filename, doc_type)
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
            final_path = _generate_pdf_from_html(request.html_content, pdf_path, pdf_filename)
            
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
