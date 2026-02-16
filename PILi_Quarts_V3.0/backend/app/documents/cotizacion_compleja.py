from typing import Dict, Any
from datetime import datetime

def generar_preview_cotizacion_compleja_editable(datos: Dict[str, Any], agente: str) -> str:
    """
    🆕 Vista previa HTML COMPLETAMENTE EDITABLE para Cotización Compleja

    Incluye todo lo de la versión simple MÁS:
    - Select de términos de pago (30, 60, 90 días)
    - Textarea para condiciones comerciales
    - Sección de cronograma con 4 fases editables
    - 3 tipos de garantía con checkboxes
    - Diseño más profesional y completo

    Args:
        datos: Diccionario con datos de cotización completa
        agente: Nombre del agente que genera la cotización

    Returns:
        str: HTML completo con formulario editable avanzado
    """

    items = datos.get('items', [])
    cliente = datos.get('cliente', '')
    proyecto = datos.get('proyecto', '')
    terminos_pago = datos.get('terminos_pago', '30')
    condiciones = datos.get('condiciones_comerciales', '')

    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cotización Compleja Editable - {agente}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', 'Arial', sans-serif; background: linear-gradient(135deg, #dbeafe 0%, #eff6ff 100%); padding: 20px; line-height: 1.6; }}
        .container {{ max-width: 1400px; margin: 0 auto; background: white; border-radius: 12px; box-shadow: 0 10px 40px rgba(0, 82, 163, 0.2); overflow: hidden; }}
        .header {{ background: linear-gradient(135deg, #0052A3 0%, #1E40AF 100%); color: white; padding: 40px; text-align: center; position: relative; overflow: hidden; }}
        .header::before {{ content: ''; position: absolute; top: -50%; right: -10%; width: 400px; height: 400px; background: rgba(255, 255, 255, 0.1); border-radius: 50%; }}
        .header h1 {{ font-size: 32px; font-weight: 900; letter-spacing: -0.5px; margin-bottom: 10px; position: relative; z-index: 1; }}
        .header .agente {{ font-size: 15px; opacity: 0.95; font-weight: 600; position: relative; z-index: 1; }}
        .content {{ padding: 40px; }}
        .titulo-seccion {{ color: #0052A3; font-size: 24px; font-weight: 800; margin: 30px 0 20px 0; padding-bottom: 12px; border-bottom: 4px solid #3B82F6; display: flex; align-items: center; gap: 10px; }}
        .titulo-seccion:first-of-type {{ margin-top: 0; }}
        .info-basica {{ display: grid; grid-template-columns: 1fr 1fr; gap: 25px; margin-bottom: 30px; }}
        .campo {{ display: flex; flex-direction: column; }}
        .campo label {{ font-weight: 700; color: #1E40AF; margin-bottom: 10px; font-size: 15px; }}
        .campo input[type="text"], .campo input[type="number"], .campo textarea, .campo select {{ padding: 14px; border: 2px solid #bfdbfe; border-radius: 8px; font-size: 15px; font-weight: 600; color: #1e293b; transition: all 0.3s; }}
        .campo textarea {{ min-height: 120px; resize: vertical; font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; }}
        .campo input:focus, .campo textarea:focus, .campo select:focus {{ outline: none; border-color: #3B82F6; box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.15); }}
        .items-table {{ width: 100%; border-collapse: separate; border-spacing: 0; margin: 20px 0; box-shadow: 0 6px 16px rgba(0, 82, 163, 0.12); border-radius: 10px; overflow: hidden; }}
        .items-table thead th {{ background: linear-gradient(135deg, #0052A3 0%, #1E40AF 100%); color: white; padding: 18px 14px; text-align: left; font-weight: 800; font-size: 14px; text-transform: uppercase; letter-spacing: 0.5px; }}
        .items-table tbody tr {{ transition: background 0.2s; }}
        .items-table tbody tr:hover {{ background: #f0f9ff; }}
        .items-table tbody td {{ padding: 14px; border-bottom: 1px solid #dbeafe; }}
        .items-table input[type="text"], .items-table input[type="number"] {{ width: 100%; padding: 10px; border: 2px solid #bfdbfe; border-radius: 6px; font-size: 14px; font-weight: 600; color: #1e293b; }}
        .items-table input:focus {{ border-color: #3B82F6; outline: none; }}
        .total-item {{ color: #0052A3; font-weight: 700; font-size: 15px; }}
        .seccion-avanzada {{ background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); padding: 25px; border-radius: 10px; margin: 25px 0; border: 2px solid #bfdbfe; }}
        .cronograma-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-top: 20px; }}
        .fase-item {{ background: white; padding: 20px; border-radius: 8px; border: 2px solid #bfdbfe; transition: all 0.3s; }}
        .fase-item:hover {{ border-color: #3B82F6; box-shadow: 0 4px 12px rgba(59, 130, 246, 0.2); }}
        .fase-item h4 {{ color: #1E40AF; font-weight: 800; margin-bottom: 12px; font-size: 16px; }}
        .garantias-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-top: 20px; }}
        .garantia-item {{ background: white; padding: 20px; border-radius: 8px; border: 2px solid #bfdbfe; display: flex; align-items: flex-start; gap: 15px; transition: all 0.3s; }}
        .garantia-item:hover {{ border-color: #3B82F6; }}
        .garantia-item input[type="checkbox"] {{ width: 22px; height: 22px; cursor: pointer; accent-color: #0052A3; margin-top: 2px; }}
        .garantia-info {{ flex: 1; }}
        .garantia-info h4 {{ color: #1E40AF; font-weight: 800; margin-bottom: 8px; font-size: 16px; }}
        .garantia-info p {{ color: #64748b; font-size: 14px; line-height: 1.5; }}
        .opciones-visualizacion {{ background: #eff6ff; padding: 25px; border-radius: 10px; margin: 25px 0; border: 2px solid #bfdbfe; }}
        .opciones-visualizacion h3 {{ color: #1E40AF; font-size: 18px; font-weight: 800; margin-bottom: 18px; }}
        .checkbox-group {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 15px; }}
        .checkbox-item {{ display: flex; align-items: center; gap: 10px; }}
        .checkbox-item input[type="checkbox"] {{ width: 20px; height: 20px; cursor: pointer; accent-color: #0052A3; }}
        .checkbox-item label {{ font-weight: 600; color: #334155; cursor: pointer; font-size: 15px; }}
        .totales {{ background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); padding: 30px; border-radius: 10px; margin-top: 25px; border: 3px solid #3B82F6; }}
        .total-row {{ display: flex; justify-content: space-between; padding: 12px 0; font-size: 17px; font-weight: 700; color: #1e293b; }}
        .total-row.igv {{ border-top: 2px solid #93c5fd; margin-top: 12px; padding-top: 18px; }}
        .total-row.final {{ background: white; padding: 22px; border-radius: 8px; margin-top: 18px; font-size: 26px; font-weight: 900; color: #0052A3; border: 3px solid #1E40AF; box-shadow: 0 4px 12px rgba(0, 82, 163, 0.2); }}
        .boton-calcular {{ background: linear-gradient(135deg, #0052A3 0%, #1E40AF 100%); color: white; border: none; padding: 18px 50px; font-size: 17px; font-weight: 800; border-radius: 10px; cursor: pointer; transition: all 0.3s; box-shadow: 0 6px 16px rgba(0, 82, 163, 0.3); width: 100%; margin-top: 25px; }}
        .boton-calcular:hover {{ transform: translateY(-3px); box-shadow: 0 8px 24px rgba(0, 82, 163, 0.4); }}
        .boton-calcular:active {{ transform: translateY(0); }}
        .footer {{ text-align: center; padding: 25px; color: #64748b; font-size: 14px; border-top: 3px solid #e2e8f0; margin-top: 40px; }}
        .nota-edicion {{ background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); border: 3px solid #fbbf24; padding: 18px; border-radius: 10px; margin: 25px 0; color: #78350f; font-weight: 600; font-size: 15px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>⚡ TESLA ELECTRICIDAD Y AUTOMATIZACIÓN</h1>
            <p class="agente">🤖 Generado por {agente} - Cotización Compleja Editable</p>
        </div>
        <div class="content">
            <h2 class="titulo-seccion">📋 COTIZACIÓN COMPLEJA - MODO EDITABLE AVANZADO</h2>
            <div class="info-basica">
                <div class="campo"><label>👤 Cliente:</label><input type="text" id="cliente" value="{cliente}" placeholder="Nombre completo del cliente"></div>
                <div class="campo"><label>📁 Proyecto:</label><input type="text" id="proyecto" value="{proyecto}" placeholder="Nombre del proyecto"></div>
            </div>
            <div class="nota-edicion">✏️ <strong>MODO EDICIÓN COMPLETA ACTIVA:</strong> Cotización compleja con todas las funcionalidades editables. Modifica items, condiciones comerciales, cronograma, garantías y más. Los cálculos se actualizan automáticamente.</div>
            <h2 class="titulo-seccion">📦 Items de la Cotización</h2>
            <table class="items-table">
                <thead><tr><th style="width: 40%">📋 Descripción</th><th style="width: 12%">🔢 Cantidad</th><th style="width: 10%">📏 Unidad</th><th style="width: 15%">💰 Precio Unit.</th><th style="width: 10%">⏱️ Días</th><th style="width: 13%">💵 Total</th></tr></thead>
                <tbody>
"""

    for i, item in enumerate(items):
        desc = item.get('descripcion', '')
        cant = item.get('cantidad', 0)
        unid = item.get('unidad', 'und')
        prec = item.get('precio_unitario', 0)
        dias = item.get('dias_ejecucion', 1)
        total = cant * prec
        html += f"""                    <tr class="item-row">
                        <td><input type="text" class="item-desc" value="{desc}" placeholder="Descripción detallada"></td>
                        <td><input type="number" class="item-cant" value="{cant}" min="0" step="0.01" onchange="calcularTotales()"></td>
                        <td><input type="text" class="item-unidad" value="{unid}"></td>
                        <td><input type="number" class="item-precio" value="{prec}" min="0" step="0.01" onchange="calcularTotales()"></td>
                        <td><input type="number" class="item-dias" value="{dias}" min="1" step="1"></td>
                        <td class="total-item">S/ {total:.2f}</td>
                    </tr>
"""

    if not items:
        html += """                    <tr class="item-row">
                        <td><input type="text" class="item-desc" value="" placeholder="Descripción"></td>
                        <td><input type="number" class="item-cant" value="1" min="0" step="0.01" onchange="calcularTotales()"></td>
                        <td><input type="text" class="item-unidad" value="und"></td>
                        <td><input type="number" class="item-precio" value="0" min="0" step="0.01" onchange="calcularTotales()"></td>
                        <td><input type="number" class="item-dias" value="1" min="1" step="1"></td>
                        <td class="total-item">S/ 0.00</td>
                    </tr>
"""

    html += f"""                </tbody>
            </table>
            <h2 class="titulo-seccion">💼 Condiciones Comerciales</h2>
            <div class="seccion-avanzada">
                <div class="info-basica">
                    <div class="campo"><label>💳 Términos de Pago:</label>
                        <select id="terminos_pago">
                            <option value="contado" {"selected" if terminos_pago == "contado" else ""}>Pago al Contado</option>
                            <option value="30" {"selected" if terminos_pago == "30" else ""}>30 días</option>
                            <option value="60" {"selected" if terminos_pago == "60" else ""}>60 días</option>
                            <option value="90" {"selected" if terminos_pago == "90" else ""}>90 días</option>
                            <option value="personalizado" {"selected" if terminos_pago == "personalizado" else ""}>Personalizado</option>
                        </select>
                    </div>
                    <div class="campo"><label>📅 Vigencia de la Oferta:</label><input type="number" id="vigencia_dias" value="30" min="1" step="1"></div>
                </div>
                <div class="campo" style="margin-top: 20px;"><label>📝 Condiciones Adicionales:</label><textarea id="condiciones_comerciales" placeholder="Condiciones comerciales adicionales, descuentos, bonificaciones...">{condiciones}</textarea></div>
            </div>
            <h2 class="titulo-seccion">📅 Cronograma de Ejecución</h2>
            <div class="seccion-avanzada">
                <div class="cronograma-grid">
                    <div class="fase-item"><h4>🔷 Fase 1: Planificación</h4><div class="campo"><label>Descripción:</label><input type="text" id="fase1_desc" value="Planificación y diseño inicial"></div><div class="campo" style="margin-top: 10px;"><label>Duración (días):</label><input type="number" id="fase1_dias" value="5" min="1" step="1"></div></div>
                    <div class="fase-item"><h4>🔷 Fase 2: Ejecución</h4><div class="campo"><label>Descripción:</label><input type="text" id="fase2_desc" value="Instalación y montaje"></div><div class="campo" style="margin-top: 10px;"><label>Duración (días):</label><input type="number" id="fase2_dias" value="10" min="1" step="1"></div></div>
                    <div class="fase-item"><h4>🔷 Fase 3: Pruebas</h4><div class="campo"><label>Descripción:</label><input type="text" id="fase3_desc" value="Pruebas y ajustes"></div><div class="campo" style="margin-top: 10px;"><label>Duración (días):</label><input type="number" id="fase3_dias" value="3" min="1" step="1"></div></div>
                    <div class="fase-item"><h4>🔷 Fase 4: Entrega</h4><div class="campo"><label>Descripción:</label><input type="text" id="fase4_desc" value="Capacitación y entrega final"></div><div class="campo" style="margin-top: 10px;"><label>Duración (días):</label><input type="number" id="fase4_dias" value="2" min="1" step="1"></div></div>
                </div>
            </div>
            <h2 class="titulo-seccion">🛡️ Garantías Incluidas</h2>
            <div class="seccion-avanzada">
                <div class="garantias-grid">
                    <div class="garantia-item"><input type="checkbox" id="garantia_materiales" checked><div class="garantia-info"><h4>🔧 Garantía de Materiales</h4><p>12 meses de garantía en todos los materiales y equipos instalados contra defectos de fabricación.</p></div></div>
                    <div class="garantia-item"><input type="checkbox" id="garantia_mano_obra" checked><div class="garantia-info"><h4>👷 Garantía de Mano de Obra</h4><p>6 meses de garantía en la instalación y mano de obra contra defectos de ejecución.</p></div></div>
                    <div class="garantia-item"><input type="checkbox" id="garantia_soporte"><div class="garantia-info"><h4>📞 Soporte Técnico Extendido</h4><p>Soporte técnico telefónico y visitas de mantenimiento preventivo durante 12 meses.</p></div></div>
                </div>
            </div>
            <div class="opciones-visualizacion">
                <h3>⚙️ Opciones de Visualización del Documento</h3>
                <div class="checkbox-group">
                    <div class="checkbox-item"><input type="checkbox" id="mostrar_precios_unitarios" checked onchange="calcularTotales()"><label for="mostrar_precios_unitarios">Mostrar Precios Unitarios</label></div>
                    <div class="checkbox-item"><input type="checkbox" id="mostrar_igv" checked onchange="calcularTotales()"><label for="mostrar_igv">Mostrar IGV (18%)</label></div>
                    <div class="checkbox-item"><input type="checkbox" id="mostrar_total" checked onchange="calcularTotales()"><label for="mostrar_total">Mostrar Total Final</label></div>
                    <div class="checkbox-item"><input type="checkbox" id="mostrar_cronograma" checked><label for="mostrar_cronograma">Incluir Cronograma</label></div>
                    <div class="checkbox-item"><input type="checkbox" id="mostrar_garantias" checked><label for="mostrar_garantias">Incluir Garantías</label></div>
                </div>
            </div>
            <div class="totales">
                <div class="total-row"><span>💰 Subtotal:</span><span id="subtotal_valor">S/ 0.00</span></div>
                <div class="total-row igv" id="fila-igv"><span>📋 IGV (18%):</span><span id="igv_valor">S/ 0.00</span></div>
                <div class="total-row final" id="fila-total"><span>🏆 TOTAL:</span><span id="total_valor">S/ 0.00</span></div>
            </div>
            <button class="boton-calcular" onclick="calcularTotales()">🧮 Calcular Totales y Actualizar Documento</button>
            <div class="footer">
                <strong style="font-size: 16px;">Tesla Electricidad y Automatización S.A.C.</strong><br>
                RUC: 20601138787 | Huancayo, Junín, Perú<br>
                📧 ingenieria.teslaelectricidad@gmail.com | 📱 +51 906 315 961<br><br>
                Documento generado por {agente} v3.0 - Sistema de Cotización Compleja<br>
                {datetime.now().strftime('%d/%m/%Y %H:%M')}
            </div>
        </div>
    </div>
    <script>
        function calcularTotales() {{
            let subtotal = 0;
            const filas = document.querySelectorAll('.item-row');
            filas.forEach((fila) => {{
                const cantidad = parseFloat(fila.querySelector('.item-cant').value) || 0;
                const precio = parseFloat(fila.querySelector('.item-precio').value) || 0;
                const total = cantidad * precio;
                fila.querySelector('.total-item').textContent = 'S/ ' + total.toFixed(2);
                subtotal += total;
            }});
            const mostrarIGV = document.getElementById('mostrar_igv').checked;
            const mostrarTotal = document.getElementById('mostrar_total').checked;
            const igv = mostrarIGV ? subtotal * 0.18 : 0;
            const total = subtotal + igv;
            document.getElementById('subtotal_valor').textContent = 'S/ ' + subtotal.toFixed(2);
            document.getElementById('igv_valor').textContent = 'S/ ' + igv.toFixed(2);
            document.getElementById('total_valor').textContent = 'S/ ' + total.toFixed(2);
            document.getElementById('fila-igv').style.display = mostrarIGV ? 'flex' : 'none';
            document.getElementById('fila-total').style.display = mostrarTotal ? 'flex' : 'none';
            let duracionTotal = 0;
            for (let i = 1; i <= 4; i++) {{
                duracionTotal += parseFloat(document.getElementById('fase' + i + '_dias').value) || 0;
            }}
            console.log('Duración total del proyecto:', duracionTotal, 'días');
        }}
        window.addEventListener('DOMContentLoaded', function() {{ calcularTotales(); }});
    </script>
</body>
</html>
"""

    return html
