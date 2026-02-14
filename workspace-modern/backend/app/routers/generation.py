
from fastapi import APIRouter, HTTPException, Body
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Dict, Any, Optional
import logging
import os
from datetime import datetime

from app.core.config import get_generated_directory
from app.services.excel_generator import excel_generator
# Import fallback generic generators if specific ones fail or for simple usage
# Note: We assume these were copied from legacy
# from app.services.word_generator import word_generator  # MISSING
# from app.services.pdf_generator import pdf_generator    # MISSING

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/generate",
    tags=["generation"]
)

class DocumentRequest(BaseModel):
    title: str = "Documento"
    type: str = "general"
    data: Dict[str, Any]
    user_id: str

@router.post("/excel")
async def generate_excel(request: DocumentRequest):
    try:
        storage_path = get_generated_directory()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{request.title}_{timestamp}.xlsx"
        filepath = os.path.join(storage_path, filename)
        
        # Ensure 'items' is in data if it's nested or needing extraction
        # The generator expects 'cliente', 'items' etc inside 'data'
        
        excel_generator.generar_cotizacion(request.data, filepath)
        
        if not os.path.exists(filepath):
             raise HTTPException(status_code=500, detail="Failed to create Excel file")
             
        return FileResponse(
            path=filepath,
            filename=filename,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except Exception as e:
        logger.error(f"Excel generation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/word")
async def generate_word(request: DocumentRequest):
    raise HTTPException(status_code=501, detail="Endpoint Migrated to N04_Binary_Factory. Use N06 Integrator.")
    # try:
    #     storage_path = get_generated_directory()
    #     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    #     filename = f"{request.title}_{timestamp}.docx"
    #     filepath = os.path.join(storage_path, filename)
    #
    #     # Adapt request.data to what word_generator expects
    #     # Legacy word_generator.generar_cotizacion(datos, ruta_salida, opciones)
    #     
    #     # We might need to map keys if they differ
    #     word_generator.generar_cotizacion(
    #         datos=request.data, 
    #         ruta_salida=filepath,
    #         opciones={'mostrar_logo': True} 
    #     )
    #     
    #     if not os.path.exists(filepath):
    #          raise HTTPException(status_code=500, detail="Failed to create Word file")
    #
    #     return FileResponse(
    #         path=filepath,
    #         filename=filename,
    #         media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    #     )
    # except Exception as e:
    #     logger.error(f"Word generation error: {e}")
    #     raise HTTPException(status_code=500, detail=str(e))

@router.post("/pdf")
async def generate_pdf(request: DocumentRequest):
    raise HTTPException(status_code=501, detail="Endpoint Migrated to N04_Binary_Factory. Use N06 Integrator.")
    # try:
    #     storage_path = get_generated_directory()
    #     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    #     filename = f"{request.title}_{timestamp}.pdf"
    #     filepath = os.path.join(storage_path, filename)
    #
    #     pdf_generator.generar_cotizacion(
    #         datos=request.data,
    #         ruta_salida=filepath,
    #         opciones={'mostrar_logo': True}
    #     )
    #
    #     if not os.path.exists(filepath):
    #          raise HTTPException(status_code=500, detail="Failed to create PDF file")
    #
    #     return FileResponse(
    #         path=filepath,
    #         filename=filename,
    #         media_type="application/pdf"
    #     )
    # except Exception as e:
    #     logger.error(f"PDF generation error: {e}")
    #     raise HTTPException(status_code=500, detail=str(e))
