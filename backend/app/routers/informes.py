from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
import os

from app.core.database import get_db
from app.models import Cotizacion, Proyecto
# <<< CORRECCIÓN: word_generator ya no se usa aquí

from app.core.config import settings # <<< CORRECCIÓN: Importar settings

router = APIRouter()

# <<< CORRECCIÓN: El endpoint 'generar_pdf_cotizacion' se movió a 'cotizaciones.py'

# <<< CORRECCIÓN: El endpoint 'generar_word_proyecto' se movió a 'proyectos.py'
# (Nota: La lógica de 'generar_word_proyecto' no estaba completa,
# el router 'proyectos.py' necesitará un desarrollo similar al de 'cotizaciones.py'
# para implementar la generación de sus propios informes de Word/PDF)


@router.post("/generar-pdf-simple")
async def generar_pdf_simple(
    datos: dict
):
    """
    Genera un PDF simple con datos arbitrarios (para testing)
    """
    
    try:
        nombre_archivo = f"informe_simple_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        # <<< CORRECCIÓN: Usar settings.GENERATED_DIR
        ruta_salida = os.path.join(settings.GENERATED_DIR, nombre_archivo)
        
        pdf_generator.generar_informe_simple(datos, ruta_salida)
        
        return FileResponse(
            path=ruta_salida,
            filename=nombre_archivo,
            media_type="application/pdf"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error: {str(e)}"
        )

@router.get("/formatos-disponibles")
async def obtener_formatos_disponibles():
    """
    Lista los formatos de documentos disponibles
    """
    
    return {
        "formatos": [
            {
                "tipo": "pdf",
                "descripcion": "Documento PDF profesional",
                "uso": "Para envío a clientes, presentaciones formales"
            },
            {
                "tipo": "word",
                "descripcion": "Documento Word editable",
                "uso": "Para edición posterior, personalización"
            },
            {
                "tipo": "informe_ejecutivo",
                "descripcion": "Informe completo del proyecto",
                "uso": "Resúmenes ejecutivos, análisis de IA"
            }
        ]
    }

    