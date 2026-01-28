from typing import Dict, Any
from datetime import datetime

def generar_preview_informe(datos: Dict[str, Any], agente: str) -> str:
    """Genera vista previa HTML para informes"""

    titulo = datos.get('titulo', 'Informe Técnico')
    cliente = datos.get('cliente', 'Cliente')
    fecha = datetime.now().strftime('%d/%m/%Y')

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Vista Previa Informe - {agente}</title>
        <style>
            body {{ font-family: 'Times New Roman', serif; margin: 40px; line-height: 1.6; }}
            .header {{ text-align: center; border-bottom: 2px solid #333; padding-bottom: 20px; }}
            .title {{ font-size: 24px; font-weight: bold; color: #333; margin: 20px 0; }}
            .info {{ margin: 20px 0; }}
            .section {{ margin: 30px 0; }}
            .section h3 {{ color: #007bff; border-bottom: 1px solid #007bff; padding-bottom: 5px; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>⚡ TESLA ELECTRICIDAD Y AUTOMATIZACIÓN S.A.C.</h1>
            <p>🤖 {agente} - Sistema de Informes Técnicos</p>
        </div>

        <h2 class="title">📋 {titulo}</h2>

        <div class="info">
            <p><strong>Cliente:</strong> {cliente}</p>
            <p><strong>Fecha:</strong> {fecha}</p>
            <p><strong>Elaborado por:</strong> {agente}</p>
        </div>

        <div class="section">
            <h3>1. RESUMEN EJECUTIVO</h3>
            <p>Este informe presenta el análisis técnico realizado por {agente},
            especialista en {agente.lower().replace('pili ', '')}...</p>
        </div>

        <div class="section">
            <h3>2. METODOLOGÍA</h3>
            <p>El análisis se realizó aplicando normativas técnicas peruanas...</p>
        </div>

        <div class="section">
            <h3>3. HALLAZGOS</h3>
            <p>Los principales hallazgos identificados son...</p>
        </div>

        <div class="section">
            <h3>4. RECOMENDACIONES</h3>
            <p>Se recomienda implementar las siguientes acciones...</p>
        </div>
    </body>
    </html>
    """

    return html
