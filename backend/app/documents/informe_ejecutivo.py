from typing import Dict, Any
from datetime import datetime

def generar_preview_informe_ejecutivo_apa_editable(datos: Dict[str, Any], agente: str) -> str:
    """
    AGENTE 3 - Vista previa HTML COMPLETAMENTE EDITABLE para Informe Ejecutivo APA

    Genera HTML con formato APA 7th edition, colores AZULES Tesla.
    Incluye:
    - Portada editable estilo APA
    - Métricas financieras (ROI, TIR, Payback, Ahorro)
    - Desglose de inversión detallado
    - Resumen ejecutivo extenso
    - Sección de recomendaciones
    """

    titulo = datos.get('titulo', 'ANÁLISIS DE FACTIBILIDAD TÉCNICO-ECONÓMICA')
    subtitulo = datos.get('subtitulo', 'Proyecto de Instalación Eléctrica Industrial')
    cliente = datos.get('cliente', '')
    codigo = datos.get('codigo', f'APA-{datetime.now().strftime("%Y%m%d")}')
    fecha = datos.get('fecha', datetime.now().strftime('%Y-%m-%d'))

    # Métricas financieras
    roi = datos.get('roi', 0)
    tir = datos.get('tir', 0)
    payback = datos.get('payback', 0)
    ahorro_anual = datos.get('ahorro_anual', 0)
    ahorro_energia = datos.get('ahorro_energia', 0)

    # Inversión
    inv_equipos = datos.get('inv_equipos', 0)
    inv_mano_obra = datos.get('inv_mano_obra', 0)
    capital_trabajo = datos.get('capital_trabajo', 0)

    # Contenido
    resumen = datos.get('resumen', '')
    recomendaciones = datos.get('recomendaciones', '')

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
            background: white;
            padding: 40px;
            line-height: 2.0; /* APA requiere doble espacio */
            color: #000;
        }}

        .container {{
            max-width: 900px;
            margin: 0 auto;
            background: white;
        }}

        /* PORTADA ESTILO APA */
        .portada {{
            text-align: center;
            padding: 100px 40px;
            border: 4px solid #0052A3;
            border-radius: 8px;
            background: linear-gradient(135deg, #f8fafc 0%, #e0f2fe 100%);
            margin-bottom: 50px;
            position: relative;
        }}

        .portada::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 8px;
            background: linear-gradient(90deg, #0052A3 0%, #1E40AF 50%, #3B82F6 100%);
        }}

        .portada-titulo {{
            font-size: 28px;
            font-weight: 900;
            color: #0052A3;
            margin: 20px 0;
            text-transform: uppercase;
            letter-spacing: 1px;
            width: 100%;
            border: 2px solid #bfdbfe;
            padding: 15px;
            background: white;
            border-radius: 8px;
        }}

        .portada-subtitulo {{
            font-size: 18px;
            color: #1E40AF;
            margin: 15px 0;
            font-weight: 600;
            width: 100%;
            border: 2px solid #bfdbfe;
            padding: 12px;
            background: white;
            border-radius: 6px;
        }}

        .portada-info {{
            margin: 30px 0;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }}

        .portada-field {{
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            font-size: 15px;
        }}

        .portada-label {{
            font-weight: 700;
            color: #1E40AF;
            min-width: 80px;
            text-align: right;
        }}

        .portada-input {{
            border: 2px solid #bfdbfe;
            padding: 8px 15px;
            border-radius: 6px;
            font-size: 15px;
            min-width: 250px;
            background: white;
        }}

        .portada-input:focus {{
            outline: none;
            border-color: #3B82F6;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        }}

        .portada-empresa {{
            margin-top: 40px;
            font-size: 16px;
            font-weight: 700;
            color: #0052A3;
        }}

        /* SECCIONES */
        .seccion {{
            margin-bottom: 40px;
            page-break-inside: avoid;
        }}

        .seccion-titulo {{
            font-size: 20px;
            font-weight: 900;
            color: #0052A3;
            border-bottom: 3px solid #1E40AF;
            padding-bottom: 10px;
            margin-bottom: 20px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        textarea {{
            width: 100%;
            border: 2px solid #bfdbfe;
            padding: 15px;
            border-radius: 8px;
            font-family: 'Times New Roman', Times, serif;
            font-size: 14px;
            line-height: 2.0; /* Doble espacio APA */
            resize: vertical;
            min-height: 150px;
            background: #fafbfc;
        }}

        textarea:focus {{
            outline: none;
            border-color: #3B82F6;
            background: white;
            box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.08);
        }}

        /* MÉTRICAS FINANCIERAS */
        .metricas-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 25px 0;
        }}

        .metrica {{
            background: linear-gradient(135deg, #e0f2fe 0%, #bae6fd 100%);
            padding: 20px;
            border-radius: 10px;
            border-left: 6px solid #0052A3;
            box-shadow: 0 4px 12px rgba(0, 82, 163, 0.1);
            transition: all 0.3s ease;
        }}

        .metrica:hover {{
            transform: translateY(-4px);
            box-shadow: 0 6px 20px rgba(0, 82, 163, 0.2);
        }}

        .metrica-label {{
            color: #1E40AF;
            font-weight: 800;
            font-size: 14px;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .metrica-value {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .metrica-input {{
            border: 2px solid #3B82F6;
            padding: 10px;
            border-radius: 6px;
            font-size: 18px;
            font-weight: 700;
            color: #0052A3;
            background: white;
            width: 120px;
        }}

        .metrica-input:focus {{
            outline: none;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
        }}

        .metrica-unit {{
            font-weight: 700;
            color: #1E40AF;
            font-size: 16px;
        }}

        /* TABLA INVERSIÓN */
        .tabla-inversion {{
            width: 100%;
            border-collapse: collapse;
            margin: 25px 0;
            box-shadow: 0 4px 12px rgba(0, 82, 163, 0.1);
            border-radius: 8px;
            overflow: hidden;
        }}

        .tabla-inversion thead {{
            background: linear-gradient(135deg, #0052A3 0%, #1E40AF 100%);
            color: white;
        }}

        .tabla-inversion th {{
            padding: 16px;
            font-weight: 800;
            text-align: left;
            font-size: 15px;
        }}

        .tabla-inversion td {{
            padding: 16px;
            border-bottom: 2px solid #e0f2fe;
            background: white;
        }}

        .tabla-inversion tr:hover td {{
            background: #f8fafc;
        }}

        .tabla-label {{
            font-weight: 700;
            color: #1f2937;
        }}

        .tabla-input {{
            border: 2px solid #bfdbfe;
            padding: 10px;
            border-radius: 6px;
            font-size: 16px;
            font-weight: 700;
            color: #0052A3;
            width: 100%;
            max-width: 200px;
        }}

        .tabla-input:focus {{
            outline: none;
            border-color: #3B82F6;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        }}

        .total-row {{
            background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%) !important;
            font-weight: 900;
        }}

        /* NOTAS */
        .nota-apa {{
            background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
            border: 2px solid #fbbf24;
            padding: 18px;
            border-radius: 8px;
            margin: 30px 0;
            font-size: 13px;
            color: #78350f;
        }}

        .nota-apa strong {{
            color: #92400e;
        }}

        /* FOOTER */
        .footer {{
            margin-top: 50px;
            padding-top: 20px;
            border-top: 3px solid #0052A3;
            text-align: center;
            color: #64748b;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- PORTADA ESTILO APA -->
        <div class="portada">
            <input type="text" name="titulo" value="{titulo}" class="portada-titulo">
            <input type="text" name="subtitulo" value="{subtitulo}" class="portada-subtitulo">

            <div class="portada-info">
                <div class="portada-field">
                    <span class="portada-label">Cliente:</span>
                    <input type="text" name="cliente" value="{cliente}" class="portada-input">
                </div>
                <div class="portada-field">
                    <span class="portada-label">Código:</span>
                    <input type="text" name="codigo" value="{codigo}" class="portada-input">
                </div>
                <div class="portada-field">
                    <span class="portada-label">Fecha:</span>
                    <input type="date" name="fecha" value="{fecha}" class="portada-input">
                </div>
            </div>

            <div class="portada-empresa">
                ⚡ TESLA ELECTRICIDAD Y AUTOMATIZACIÓN S.A.C.<br>
                Departamento de Ingeniería y Proyectos
            </div>
        </div>

        <!-- RESUMEN EJECUTIVO -->
        <div class="seccion">
            <h2 class="seccion-titulo">Resumen Ejecutivo</h2>
            <textarea name="resumen" rows="6" placeholder="Resumen ejecutivo del análisis. Incluya el contexto del proyecto, objetivos principales, metodología aplicada y conclusiones clave. Formato APA requiere párrafos con doble espacio y redacción objetiva en tercera persona...">{resumen}</textarea>
        </div>

        <!-- MÉTRICAS FINANCIERAS -->
        <div class="seccion">
            <h2 class="seccion-titulo">Métricas Financieras</h2>

            <div class="metricas-grid">
                <div class="metrica">
                    <div class="metrica-label">📊 ROI Estimado</div>
                    <div class="metrica-value">
                        <input type="number" name="roi" value="{roi}" step="0.1" class="metrica-input">
                        <span class="metrica-unit">%</span>
                    </div>
                </div>

                <div class="metrica">
                    <div class="metrica-label">📈 TIR Proyectada</div>
                    <div class="metrica-value">
                        <input type="number" name="tir" value="{tir}" step="0.1" class="metrica-input">
                        <span class="metrica-unit">%</span>
                    </div>
                </div>

                <div class="metrica">
                    <div class="metrica-label">⏱️ Período de Retorno (Payback)</div>
                    <div class="metrica-value">
                        <input type="number" name="payback" value="{payback}" class="metrica-input">
                        <span class="metrica-unit">meses</span>
                    </div>
                </div>

                <div class="metrica">
                    <div class="metrica-label">💰 Ahorro Anual Estimado</div>
                    <div class="metrica-value">
                        <span class="metrica-unit">S/</span>
                        <input type="number" name="ahorro_anual" value="{ahorro_anual}" step="0.01" class="metrica-input">
                    </div>
                </div>

                <div class="metrica">
                    <div class="metrica-label">⚡ Ahorro Energético</div>
                    <div class="metrica-value">
                        <input type="number" name="ahorro_energia" value="{ahorro_energia}" step="0.1" class="metrica-input">
                        <span class="metrica-unit">kWh/año</span>
                    </div>
                </div>
            </div>
        </div>

        <!-- INVERSIÓN TOTAL -->
        <div class="seccion">
            <h2 class="seccion-titulo">Desglose de Inversión Total</h2>

            <table class="tabla-inversion">
                <thead>
                    <tr>
                        <th>Concepto</th>
                        <th>Monto (S/)</th>
                        <th>% del Total</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td class="tabla-label">💼 Equipos y Materiales</td>
                        <td>
                            <span style="font-weight: 700; margin-right: 5px;">S/</span>
                            <input type="number" name="inv_equipos" value="{inv_equipos}" step="0.01" class="tabla-input">
                        </td>
                        <td id="percent_equipos" style="font-weight: 700; color: #0052A3;">-</td>
                    </tr>
                    <tr>
                        <td class="tabla-label">👷 Mano de Obra Especializada</td>
                        <td>
                            <span style="font-weight: 700; margin-right: 5px;">S/</span>
                            <input type="number" name="inv_mano_obra" value="{inv_mano_obra}" step="0.01" class="tabla-input">
                        </td>
                        <td id="percent_mano_obra" style="font-weight: 700; color: #0052A3;">-</td>
                    </tr>
                    <tr>
                        <td class="tabla-label">💰 Capital de Trabajo</td>
                        <td>
                            <span style="font-weight: 700; margin-right: 5px;">S/</span>
                            <input type="number" name="capital_trabajo" value="{capital_trabajo}" step="0.01" class="tabla-input">
                        </td>
                        <td id="percent_capital" style="font-weight: 700; color: #0052A3;">-</td>
                    </tr>
                    <tr class="total-row">
                        <td class="tabla-label" style="font-size: 18px;">🏆 INVERSIÓN TOTAL</td>
                        <td id="total_inversion" style="font-size: 18px; color: #0052A3;">S/ 0.00</td>
                        <td style="font-weight: 700; font-size: 16px;">100%</td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- RECOMENDACIONES -->
        <div class="seccion">
            <h2 class="seccion-titulo">Recomendaciones</h2>
            <textarea name="recomendaciones" rows="5" placeholder="Recomendaciones técnicas y estratégicas basadas en el análisis. Incluya sugerencias de implementación, precauciones, optimizaciones y próximos pasos...">{recomendaciones}</textarea>
        </div>

        <!-- NOTA APA -->
        <div class="nota-apa">
            <strong>📚 Formato APA 7th Edition:</strong> Este documento sigue las normas de la American Psychological Association (7ª edición).
            Incluye portada formal, doble espacio, numeración de secciones y referencias estructuradas.
            Al exportar a Word, se mantendrá el formato profesional APA para presentaciones ejecutivas.
        </div>

        <!-- FOOTER -->
        <div class="footer">
            <div style="font-weight: 700; color: #1E40AF; margin-bottom: 5px;">
                Documento generado por {agente} v3.0
            </div>
            <div>
                {datetime.now().strftime('%d/%m/%Y %H:%M')} - Sistema de Gestión Tesla Electricidad<br>
                Formato APA 7th Edition - Confidencial
            </div>
        </div>
    </div>

    <script>
        // Cálculo automático de porcentajes y total
        function calcularTotales() {{
            const equipos = parseFloat(document.querySelector('[name="inv_equipos"]').value) || 0;
            const manoObra = parseFloat(document.querySelector('[name="inv_mano_obra"]').value) || 0;
            const capital = parseFloat(document.querySelector('[name="capital_trabajo"]').value) || 0;

            const total = equipos + manoObra + capital;

            if (total > 0) {{
                document.getElementById('percent_equipos').textContent = ((equipos / total) * 100).toFixed(1) + '%';
                document.getElementById('percent_mano_obra').textContent = ((manoObra / total) * 100).toFixed(1) + '%';
                document.getElementById('percent_capital').textContent = ((capital / total) * 100).toFixed(1) + '%';
            }}

            document.getElementById('total_inversion').textContent = 'S/ ' + total.toFixed(2).replace(/\\B(?=(\\d{{3}})+(?!\\d))/g, ',');
        }}

        // Actualizar al cargar y al cambiar valores
        document.addEventListener('DOMContentLoaded', calcularTotales);
        document.querySelectorAll('.tabla-input').forEach(input => {{
            input.addEventListener('input', calcularTotales);
        }});
    </script>
</body>
</html>
"""

    return html
