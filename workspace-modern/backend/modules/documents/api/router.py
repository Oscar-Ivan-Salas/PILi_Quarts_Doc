"""
API Router para Generación Unificada de Documentos
"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Dict, Any, Optional
from pathlib import Path
import logging

# Importar generadores directamente
# from app.services.generators.cotizacion_simple_generator import generar_cotizacion_simple
# from app.services.generators.cotizacion_compleja_generator import generar_cotizacion_compleja
# from app.services.generators.proyecto_simple_generator import generar_proyecto_simple
# from app.services.generators.proyecto_complejo_pmi_generator import generar_proyecto_complejo_pmi
# from app.services.generators.informe_tecnico_generator import generar_informe_tecnico
# from app.services.generators.informe_ejecutivo_apa_generator import generar_informe_ejecutivo_apa

# from app.services.pdf_generator import PDFGenerator
# from app.services.excel_generator_complete import ExcelGeneratorComplete
# from app.services.html_to_word_generator import HTMLToWordGenerator

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/documents", tags=["documents"])


class GenerateRequest(BaseModel):
    """Request para generar documento"""
    document_type: str  # cotizacion_simple, proyecto_complejo, etc.
    format: str  # html, docx, pdf, xlsx
    data: Dict[str, Any]
    options: Optional[Dict[str, Any]] = None


# Inicializar generadores
# pdf_gen = PDFGenerator()
# excel_gen = ExcelGeneratorComplete()
# html_gen = HTMLToWordGenerator()

# Mapeo de generadores Word
WORD_GENERATORS = {
    # "cotizacion_simple": generar_cotizacion_simple,
    # "cotizacion_compleja": generar_cotizacion_compleja,
    # "proyecto_simple": generar_proyecto_simple,
    # "proyecto_complejo": generar_proyecto_complejo_pmi,
    # "informe_tecnico": generar_informe_tecnico,
    # "informe_ejecutivo": generar_informe_ejecutivo_apa,
}

# Mapeo de generadores Excel
EXCEL_GENERATORS = {
    # "cotizacion_simple": excel_gen.generar_cotizacion_simple,
    # "cotizacion_compleja": excel_gen.generar_cotizacion_compleja,
    # "proyecto_simple": excel_gen.generar_proyecto_simple,
    # "proyecto_complejo": excel_gen.generar_proyecto_complejo,
    # "informe_tecnico": excel_gen.generar_informe_tecnico,
    # "informe_ejecutivo": excel_gen.generar_informe_ejecutivo,
}


@router.post("/generate")
async def generate_document(request: GenerateRequest):
    """
    Endpoint unificado para generar cualquier documento en cualquier formato
    
    Ejemplos:
        POST /api/documents/generate
        {
            "document_type": "cotizacion_simple",
            "format": "xlsx",
            "data": {...},
            "options": {"esquema_colores": "azul-tesla"}
        }
    """
    raise HTTPException(status_code=501, detail="Endpoint Disabled. Use N06 Integrator (Universal Factory) instead.")
    # try:
    #     logger.info(f"📄 Generando {request.document_type} en formato {request.format}")
    #     
    #     file_path = None
    #     
    #     # Generar según formato
    #     if request.format == "html":
    #         # HTML
    #         html_content = html_gen._cargar_plantilla(request.document_type)
    #         html_rendered = html_gen._reemplazar_variables(html_content, request.data)
    #         
    #         import tempfile
    #         from datetime import datetime
    #         file_path = Path(tempfile.gettempdir()) / f"{request.document_type}_{datetime.now().strftime('%Y%m%d%H%M%S')}.html"
    #         with open(file_path, 'w', encoding='utf-8') as f:
    #             f.write(html_rendered)
    #             
    #     elif request.format == "docx":
    #         # Word
    #         generator_func = WORD_GENERATORS.get(request.document_type)
    #         if not generator_func:
    #             raise HTTPException(status_code=400, detail=f"Tipo de documento no soportado: {request.document_type}")
    #         
    #         import tempfile
    #         from datetime import datetime
    #         file_path = Path(tempfile.gettempdir()) / f"{request.document_type}_{datetime.now().strftime('%Y%m%d%H%M%S')}.docx"
    #         file_path = generator_func(request.data, str(file_path), request.options or {})
    #         
    #     elif request.format == "pdf":
    #         # PDF
    #         import tempfile
    #         from datetime import datetime
    #         file_path = Path(tempfile.gettempdir()) / f"{request.document_type}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    #         
    #         if "cotizacion" in request.document_type:
    #             file_path = pdf_gen.generar_cotizacion(request.data, str(file_path), request.options or {})
    #         elif "proyecto" in request.document_type or "informe" in request.document_type:
    #             file_path = pdf_gen.generar_informe_proyecto(request.data, str(file_path), request.options or {})
    #         else:
    #             raise HTTPException(status_code=400, detail=f"Tipo de documento no soportado para PDF: {request.document_type}")
    #             
    #     elif request.format == "xlsx":
    #         # Excel
    #         generator_func = EXCEL_GENERATORS.get(request.document_type)
    #         if not generator_func:
    #             raise HTTPException(status_code=400, detail=f"Tipo de documento no soportado para Excel: {request.document_type}")
    #         
    #         import tempfile
    #         from datetime import datetime
    #         file_path = Path(tempfile.gettempdir()) / f"{request.document_type}_{datetime.now().strftime('%Y%m%d%H%M%S')}.xlsx"
    #         file_path = generator_func(request.data, str(file_path))
    #         
    #     else:
    #         raise HTTPException(status_code=400, detail=f"Formato no soportado: {request.format}")
    #     
    #     # Determinar media type
    #     media_types = {
    #         "html": "text/html",
    #         "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    #         "pdf": "application/pdf",
    #         "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    #     }
    #     
    #     logger.info(f"✅ Documento generado: {file_path}")
    #     
    #     return FileResponse(
    #         path=str(file_path),
    #         media_type=media_types[request.format],
    #         filename=f"{request.document_type}.{request.format}"
    #     )
    #     
    # except Exception as e:
    #     logger.error(f"❌ Error generando documento: {str(e)}", exc_info=True)
    #     raise HTTPException(status_code=500, detail=str(e))


@router.get("/formats/{document_type}")
async def get_supported_formats(document_type: str):
    """
    Obtener formatos soportados para un tipo de documento
    
    Todos los tipos soportan: html, docx, pdf, xlsx
    """
    return {
        "document_type": document_type,
        "formats": ["html", "docx", "pdf", "xlsx"]
    }


@router.get("/types")
async def get_document_types():
    """
    Listar todos los tipos de documentos disponibles
    """
    return {
        "types": [
            "cotizacion_simple",
            "cotizacion_compleja",
            "proyecto_simple",
            "proyecto_complejo",
            "informe_tecnico",
            "informe_ejecutivo"
        ]
    }
