from fastapi import APIRouter, HTTPException
from typing import Optional
from app.routers.chat import (
    generar_preview_cotizacion_simple_editable,
    generar_preview_cotizacion_compleja_editable,
    generar_preview_proyecto_simple_editable,
    generar_preview_proyecto_complejo_pmi_editable,
    generar_preview_informe_tecnico_editable,
    generar_preview_informe_ejecutivo_apa_editable
)

router = APIRouter(prefix="/api/templates", tags=["templates"])

@router.get("/{template_name}")
async def get_template(template_name: str):
    """
    Retorna el HTML editable profesional para una plantilla específica.
    Integra los generadores del agente PILI para asegurar consistencia con la Tesis.
    """
    
    agente_default = "PILI v3.0"
    
    try:
        html = ""
        
        if template_name == "cotizacion-simple":
            # Usar generador de Cotización Simple
            # Pasamos items vacíos para que genere la fila por defecto
            datos = {
                'cliente': '{{CLIENTE_NOMBRE}}',
                'proyecto': '{{PROYECTO_NOMBRE}}',
                # Items vacíos activan la fila por defecto en el generador
                'items': [],
                'condiciones': 'Validez de la oferta: 15 días. Precios incluyen IGV.'
            }
            html = generar_preview_cotizacion_simple_editable(datos, agente_default)
            
        elif template_name == "cotizacion-compleja":
            # Usar generador de Cotización Compleja
            datos = {
                'cliente': '{{CLIENTE_NOMBRE}}',
                'proyecto': '{{PROYECTO_NOMBRE}}',
                'items': [],
                'condiciones': 'Forma de pago: 50% adelanto, 50% contra entrega.',
                'terminos_pago': '50/50'
            }
            html = generar_preview_cotizacion_compleja_editable(datos, agente_default)
            
        elif template_name == "proyecto-simple":
            # Usar generador de Proyecto Simple
            datos = {
                'nombre': '{{NOMBRE_PROYECTO}}',
                'cliente': '{{CLIENTE_NOMBRE}}',
                'codigo': 'PRY-NEW-001',
                # Usamos value="0.00" si no hay reemplazo, pero aquí pasamos string para que App.jsx reemplace
                # El generador usa value="{presupuesto}", así que {{PRESUPUESTO}} funciona visualmente
                'presupuesto': '{{PRESUPUESTO}}',
                'alcance': '{{DESCRIPCION_PROYECTO}}',
                'fecha_inicio': '{{FECHA}}'
            }
            html = generar_preview_proyecto_simple_editable(datos, agente_default)
            
        elif template_name == "proyecto-complejo":
            # Usar generador de Proyecto Complejo PMI
            datos = {
                'nombre': '{{NOMBRE_PROYECTO}}',
                'cliente': '{{CLIENTE_NOMBRE}}',
                'codigo': 'PRY-PMI-NEW-001',
                'presupuesto': '{{PRESUPUESTO}}',
                'alcance': '{{DESCRIPCION_PROYECTO}}',
                'fecha_inicio': '{{FECHA}}',
                # Métricas por defecto
                'metricas_pmi': {
                    'SPI': 1.0, 'CPI': 1.0, 'EV': 0, 'PV': 0, 'AC': 0
                }
            }
            html = generar_preview_proyecto_complejo_pmi_editable(datos, agente_default)
            
        elif template_name == "informe-tecnico":
            # Usar generador de Informe Técnico
            datos = {
               'titulo': '{{TITULO_INFORME}}',
               'proyecto': '{{PROYECTO_NOMBRE}}', 
               'fecha': '{{FECHA}}',
               'contenido': '{{DESCRIPCION_PROYECTO}}'
            }
            html = generar_preview_informe_tecnico_editable(datos, agente_default)
            
        elif template_name == "informe-ejecutivo":
             # Usar generador de Informe Ejecutivo APA
            datos = {
               'titulo': '{{TITULO_INFORME}}',
               'proyecto': '{{PROYECTO_NOMBRE}}',
               'fecha': '{{FECHA}}',
               'resumen': '{{DESCRIPCION_PROYECTO}}'
            }
            html = generar_preview_informe_ejecutivo_apa_editable(datos, agente_default)
            
        else:
            raise HTTPException(status_code=404, detail="Plantilla no encontrada")
            
        return {"html": html}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando plantilla: {str(e)}")
