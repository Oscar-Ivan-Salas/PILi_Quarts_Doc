from typing import Dict, Any
from datetime import datetime

def generar_preview_informe_tecnico_editable(datos: Dict[str, Any], agente: str) -> str:
    """
    AGENTE 3 - Vista previa HTML COMPLETAMENTE EDITABLE para Informe Técnico

    Genera HTML con colores AZULES Tesla (#0052A3, #1E40AF, #3B82F6).
    Incluye 5 secciones técnicas editables:
    1. Resumen Ejecutivo
    2. Marco Normativo
    3. Descripción Técnica
    4. Metodología
    5. Resultados y Conclusiones
    """

    titulo = datos.get('titulo', 'INFORME TÉCNICO ELÉCTRICO')
    codigo = datos.get('codigo', f'IT-{datetime.now().strftime("%Y%m%d")}')
    cliente = datos.get('cliente', '')
    fecha = datos.get('fecha', datetime.now().strftime('%Y-%m-%d'))
    normativa = datos.get('normativa', 'CNE Suministro 2011, RD N° 037-2006-EM/DGE')

    # Contenidos por defecto
    resumen = datos.get('resumen', '')
    marco_normativo = datos.get('marco_normativo', 'Código Nacional de Electricidad - Suministro 2011\nReglamento de la Ley de Concesiones Eléctricas - D.L. N° 25844\nNorma DGE - Procedimiento de Elaboración de Proyectos y Ejecución de Obras en Sistemas de Distribución')
    descripcion_tecnica = datos.get('descripcion_tecnica', '')
    metodologia = datos.get('metodologia', '')
    conclusiones = datos.get('conclusiones', '')

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{titulo}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Times New Roman', Times, serif;
            background: linear-gradient(135deg, #e0f2fe 0%, #f0f9ff 100%);
            padding: 20px;
            line-height: 1.6;
        }}

        .container {{
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            box-shadow: 0 10px 40px rgba(0, 82, 163, 0.15);
            border-radius: 12px;
            overflow: hidden;
        }}

        .header {{
            background: linear-gradient(135deg, #0052A3 0%, #1E40AF 100%);
            color: white;
            padding: 40px;
            text-align: center;
            position: relative;
            overflow: hidden;
        }}

        .header::before {{
            content: '';
            position: absolute;
            top: -50%;
            right: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
            animation: pulse 3s ease-in-out infinite;
        }}

        @keyframes pulse {{
            0%, 100% {{ opacity: 0.5; }}
            50% {{ opacity: 1; }}
        }}

        .header-content {{
            position: relative;
            z-index: 1;
        }}

        .titulo-input {{
            font-size: 28px;
            text-align: center;
            background: transparent;
            border: 2px solid rgba(255,255,255,0.3);
            color: white;
            font-weight: 900;
            padding: 15px;
            width: 100%;
            border-radius: 8px;
            text-transform: uppercase;
            letter-spacing: 1px;
            transition: all 0.3s ease;
        }}

        .titulo-input:focus {{
            outline: none;
            border-color: white;
            background: rgba(255,255,255,0.1);
        }}

        .codigo-container {{
            margin-top: 15px;
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 10px;
        }}

        .codigo-label {{
            font-weight: 700;
            font-size: 14px;
        }}

        .codigo-input {{
            background: rgba(255,255,255,0.2);
            border: 1px solid rgba(255,255,255,0.4);
            color: white;
            padding: 8px 15px;
            border-radius: 6px;
            font-size: 14px;
            font-weight: 600;
            width: 220px;
            text-align: center;
        }}

        .codigo-input:focus {{
            outline: none;
            background: rgba(255,255,255,0.3);
        }}

        .empresa {{
            margin-top: 20px;
            font-size: 16px;
            font-weight: 600;
            opacity: 0.95;
        }}

        .info-section {{
            padding: 30px 40px;
            background: #f8fafc;
            border-bottom: 2px solid #e0f2fe;
        }}

        .info-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
        }}

        .info-field {{
            background: white;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #0052A3;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }}

        .info-label {{
            font-weight: 800;
            color: #1E40AF;
            font-size: 13px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
        }}

        .info-input {{
            border: 1px solid #bfdbfe;
            padding: 10px;
            width: 100%;
            border-radius: 6px;
            font-size: 15px;
            color: #1f2937;
            font-weight: 600;
            transition: all 0.3s ease;
        }}

        .info-input:focus {{
            outline: none;
            border-color: #3B82F6;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        }}

        .content {{
            padding: 40px;
        }}

        .seccion {{
            background: white;
            margin-bottom: 30px;
            border: 2px solid #bfdbfe;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0, 82, 163, 0.08);
            transition: all 0.3s ease;
        }}

        .seccion:hover {{
            box-shadow: 0 6px 20px rgba(0, 82, 163, 0.15);
            transform: translateY(-2px);
        }}

        .seccion-header {{
            background: linear-gradient(135deg, #0052A3 0%, #1E40AF 100%);
            color: white;
            padding: 18px 25px;
            font-weight: 800;
            font-size: 18px;
            display: flex;
            align-items: center;
            gap: 12px;
        }}

        .seccion-icon {{
            font-size: 24px;
        }}

        .seccion-content {{
            padding: 25px;
            background: #fafbfc;
        }}

        textarea {{
            border: 2px solid #bfdbfe;
            padding: 15px;
            width: 100%;
            border-radius: 8px;
            font-family: 'Times New Roman', Times, serif;
            font-size: 15px;
            line-height: 1.8;
            color: #1f2937;
            resize: vertical;
            min-height: 120px;
            transition: all 0.3s ease;
        }}

        textarea:focus {{
            outline: none;
            border-color: #3B82F6;
            box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1);
            background: white;
        }}

        .edit-note {{
            background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
            border: 2px solid #fbbf24;
            padding: 20px;
            border-radius: 10px;
            margin-top: 30px;
            font-weight: 600;
            color: #78350f;
            display: flex;
            align-items: center;
            gap: 15px;
            box-shadow: 0 4px 12px rgba(251, 191, 36, 0.2);
        }}

        .edit-icon {{
            font-size: 28px;
        }}

        .footer {{
            text-align: center;
            padding: 30px;
            background: #f8fafc;
            border-top: 3px solid #0052A3;
            color: #64748b;
            font-size: 13px;
        }}

        .footer-bold {{
            color: #1E40AF;
            font-weight: 700;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="header-content">
                <input type="text" name="titulo" value="{titulo}" placeholder="TÍTULO DEL INFORME TÉCNICO" class="titulo-input">
                <div class="codigo-container">
                    <span class="codigo-label">Código:</span>
                    <input type="text" name="codigo" value="{codigo}" class="codigo-input">
                </div>
                <div class="empresa">⚡ TESLA ELECTRICIDAD Y AUTOMATIZACIÓN S.A.C.</div>
            </div>
        </div>

        <div class="info-section">
            <div class="info-grid">
                <div class="info-field">
                    <div class="info-label">👤 Cliente</div>
                    <input type="text" name="cliente" value="{cliente}" placeholder="Nombre del cliente" class="info-input">
                </div>
                <div class="info-field">
                    <div class="info-label">📅 Fecha</div>
                    <input type="date" name="fecha" value="{fecha}" class="info-input">
                </div>
                <div class="info-field">
                    <div class="info-label">⚖️ Normativa Aplicable</div>
                    <input type="text" name="normativa" value="{normativa}" class="info-input">
                </div>
            </div>
        </div>

        <div class="content">
            <div class="seccion">
                <div class="seccion-header">
                    <span class="seccion-icon">📋</span>
                    <span>I. RESUMEN EJECUTIVO</span>
                </div>
                <div class="seccion-content">
                    <textarea name="resumen" rows="5" placeholder="Resumen ejecutivo del informe técnico. Incluya el objetivo principal, alcance y conclusiones clave...">{resumen}</textarea>
                </div>
            </div>

            <div class="seccion">
                <div class="seccion-header">
                    <span class="seccion-icon">📖</span>
                    <span>II. MARCO NORMATIVO</span>
                </div>
                <div class="seccion-content">
                    <textarea name="marco_normativo" rows="5" placeholder="Normativas, códigos y reglamentos aplicables al proyecto...">{marco_normativo}</textarea>
                </div>
            </div>

            <div class="seccion">
                <div class="seccion-header">
                    <span class="seccion-icon">🔧</span>
                    <span>III. DESCRIPCIÓN TÉCNICA</span>
                </div>
                <div class="seccion-content">
                    <textarea name="descripcion_tecnica" rows="6" placeholder="Descripción detallada de las instalaciones eléctricas, equipos, materiales y especificaciones técnicas...">{descripcion_tecnica}</textarea>
                </div>
            </div>

            <div class="seccion">
                <div class="seccion-header">
                    <span class="seccion-icon">⚙️</span>
                    <span>IV. METODOLOGÍA</span>
                </div>
                <div class="seccion-content">
                    <textarea name="metodologia" rows="5" placeholder="Procedimientos de instalación, pruebas realizadas, herramientas utilizadas y metodología de trabajo...">{metodologia}</textarea>
                </div>
            </div>

            <div class="seccion">
                <div class="seccion-header">
                    <span class="seccion-icon">✅</span>
                    <span>V. RESULTADOS Y CONCLUSIONES</span>
                </div>
                <div class="seccion-content">
                    <textarea name="conclusiones" rows="5" placeholder="Resultados obtenidos, análisis de cumplimiento normativo y conclusiones finales...">{conclusiones}</textarea>
                </div>
            </div>

            <div class="edit-note">
                <span class="edit-icon">✏️</span>
                <div>
                    <strong>Edición Completa Habilitada:</strong> Todos los campos son editables. Modifica título, código, fecha, secciones y contenido según tus necesidades. Los cambios se guardarán automáticamente al generar el documento Word final.
                </div>
            </div>
        </div>

        <div class="footer">
            <div class="footer-bold">Documento generado por {agente} v3.0</div>
            <div style="margin-top: 8px;">{datetime.now().strftime('%d/%m/%Y %H:%M')} - Sistema de Gestión Tesla Electricidad</div>
        </div>
    </div>
</body>
</html>
"""

    return html
