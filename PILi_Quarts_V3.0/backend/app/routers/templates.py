"""
Templates Router - Sirve plantillas HTML de N04 al frontend
"""
from fastapi import APIRouter, HTTPException
from pathlib import Path
import logging

router = APIRouter(prefix="/api/templates", tags=["templates"])
logger = logging.getLogger(__name__)

# Ruta a plantillas N04
TEMPLATES_DIR = Path(__file__).parent.parent.parent / "modules" / "N04_Binary_Factory" / "templates" / "html"

# Mapeo de tipos de documento a archivos de plantilla
TEMPLATE_MAP = {
    "cotizacion-simple": "PLANTILLA_HTML_COTIZACION_SIMPLE.html",
    "cotizacion-compleja": "PLANTILLA_HTML_COTIZACION_COMPLEJA.html",
    "proyecto-simple": "PLANTILLA_HTML_PROYECTO_SIMPLE.html",
    "proyecto-complejo": "PLANTILLA_HTML_PROYECTO_COMPLEJO_PMI.html",
    "informe-simple": "PLANTILLA_HTML_INFORME_EJECUTIVO_APA.html",
    "informe-complejo": "PLANTILLA_HTML_INFORME_TECNICO.html"
}

@router.get("/{tipo}")
async def get_template(tipo: str):
    """
    Retorna plantilla HTML de N04 para el tipo de documento especificado
    
    Args:
        tipo: Tipo de documento (cotizacion-simple, proyecto-complejo, etc.)
    
    Returns:
        {"html": "contenido HTML de la plantilla"}
    """
    logger.info(f"📄 Solicitando plantilla: {tipo}")
    
    # Verificar que el tipo existe
    template_file = TEMPLATE_MAP.get(tipo)
    if not template_file:
        logger.error(f"❌ Tipo de plantilla no encontrado: {tipo}")
        raise HTTPException(
            status_code=404, 
            detail=f"Template type not found: {tipo}. Available types: {list(TEMPLATE_MAP.keys())}"
        )
    
    # Verificar que el archivo existe
    template_path = TEMPLATES_DIR / template_file
    if not template_path.exists():
        logger.error(f"❌ Archivo de plantilla no encontrado: {template_path}")
        raise HTTPException(
            status_code=404, 
            detail=f"Template file not found: {template_file}"
        )
    
    # Leer plantilla
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        logger.info(f"✅ Plantilla cargada: {template_file} ({len(html_content)} caracteres)")
        
        return {
            "html": html_content,
            "tipo": tipo,
            "archivo": template_file
        }
        
    except Exception as e:
        logger.error(f"❌ Error leyendo plantilla: {e}")
        raise HTTPException(status_code=500, detail=f"Error reading template: {str(e)}")

@router.get("/")
async def list_templates():
    """Lista todos los tipos de plantillas disponibles"""
    return {
        "templates": list(TEMPLATE_MAP.keys()),
        "count": len(TEMPLATE_MAP)
    }
