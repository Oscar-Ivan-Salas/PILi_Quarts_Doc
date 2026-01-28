from typing import Dict, Any
from datetime import datetime

def generar_preview_cotizacion_simple_editable(datos: Dict[str, Any], agente: str) -> str:
    """
    🆕 Vista previa HTML COMPLETAMENTE EDITABLE para Cotización Simple

    Características:
    - Colores AZULES Tesla (#0052A3, #1E40AF, #3B82F6)
    - Inputs editables en toda la tabla
    - Checkboxes para opciones de visualización
    - Cálculo automático de totales con JavaScript
    - Sin dependencias externas

    Args:
        datos: Diccionario con datos de cotización (cliente, items, etc.)
        agente: Nombre del agente que genera la cotización

    Returns:
        str: HTML completo con formulario editable
    """

    items = datos.get('items', [])
    cliente = datos.get('cliente', '')
    proyecto = datos.get('proyecto', '')

    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cotización Simple Editable - {agente}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', 'Arial', sans-serif;
            background: linear-gradient(135deg, #e0f2fe 0%, #f0f9ff 100%);
            padding: 20px;
            line-height: 1.6;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 8px 32px rgba(0, 82, 163, 0.15);
            overflow: hidden;
        }}

        .header {{
            background: linear-gradient(135deg, #0052A3 0%, #1E40AF 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}

        .header h1 {{
            font-size: 28px;
            font-weight: 900;
            letter-spacing: -0.5px;
            margin-bottom: 8px;
        }}

        .header .agente {{
            font-size: 14px;
            opacity: 0.9;
            font-weight: 600;
        }}

        .content {{
            padding: 30px;
        }}

        .titulo-seccion {{
            color: #0052A3;
            font-size: 22px;
            font-weight: 800;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #3B82F6;
        }}

        .info-basica {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 30px;
        }}

        .campo {{
            display: flex;
            flex-direction: column;
        }}

        .campo label {{
            font-weight: 700;
            color: #1E40AF;
            margin-bottom: 8px;
            font-size: 14px;
        }}

        .campo input[type="text"],
        .campo input[type="number"],
        .campo textarea,
        .campo select {{
            padding: 12px;
            border: 2px solid #bfdbfe;
            border-radius: 6px;
            font-size: 15px;
            font-weight: 600;
            color: #1e293b;
            transition: all 0.3s;
        }}

        .campo input:focus,
        .campo textarea:focus,
        .campo select:focus {{
            outline: none;
            border-color: #3B82F6;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        }}

        .items-table {{
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
            margin: 20px 0;
            box-shadow: 0 4px 12px rgba(0, 82, 163, 0.1);
            border-radius: 8px;
            overflow: hidden;
        }}

        .items-table thead th {{
            background: linear-gradient(135deg, #0052A3 0%, #1E40AF 100%);
            color: white;
            padding: 16px 12px;
            text-align: left;
            font-weight: 800;
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .items-table tbody tr {{
            transition: background 0.2s;
        }}

        .items-table tbody tr:hover {{
            background: #eff6ff;
        }}

        .items-table tbody td {{
            padding: 12px;
            border-bottom: 1px solid #dbeafe;
        }}

        .items-table input[type="text"],
        .items-table input[type="number"] {{
            width: 100%;
            padding: 8px;
            border: 2px solid #bfdbfe;
            border-radius: 4px;
            font-size: 14px;
            font-weight: 600;
            color: #1e293b;
        }}

        .items-table input[type="text"]:focus,
        .items-table input[type="number"]:focus {{
            border-color: #3B82F6;
            outline: none;
        }}

        .total-item {{
            color: #0052A3;
            font-weight: 700;
            font-size: 15px;
        }}

        .opciones-visualizacion {{
            background: #eff6ff;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
            border: 2px solid #bfdbfe;
        }}

        .opciones-visualizacion h3 {{
            color: #1E40AF;
            font-size: 16px;
            font-weight: 800;
            margin-bottom: 15px;
        }}

        .checkbox-group {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 12px;
        }}

        .checkbox-item {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .checkbox-item input[type="checkbox"] {{
            width: 18px;
            height: 18px;
            cursor: pointer;
            accent-color: #0052A3;
        }}

        .checkbox-item label {{
            font-weight: 600;
            color: #334155;
            cursor: pointer;
            font-size: 14px;
        }}

        .totales {{
            background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
            padding: 25px;
            border-radius: 8px;
            margin-top: 20px;
            border: 3px solid #3B82F6;
        }}

        .total-row {{
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            font-size: 16px;
            font-weight: 700;
            color: #1e293b;
        }}

        .total-row.igv {{
            border-top: 2px solid #93c5fd;
            margin-top: 10px;
            padding-top: 15px;
        }}

        .total-row.final {{
            background: white;
            padding: 18px;
            border-radius: 6px;
            margin-top: 15px;
            font-size: 22px;
            font-weight: 900;
            color: #0052A3;
            border: 2px solid #1E40AF;
        }}

        .boton-calcular {{
            background: linear-gradient(135deg, #0052A3 0%, #1E40AF 100%);
            color: white;
            border: none;
            padding: 15px 40px;
            font-size: 16px;
            font-weight: 800;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s;
            box-shadow: 0 4px 12px rgba(0, 82, 163, 0.3);
            width: 100%;
            margin-top: 20px;
        }}

        .boton-calcular:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0, 82, 163, 0.4);
        }}

        .boton-calcular:active {{
            transform: translateY(0);
        }}

        .footer {{
            text-align: center;
            padding: 20px;
            color: #64748b;
            font-size: 13px;
            border-top: 2px solid #e2e8f0;
            margin-top: 30px;
        }}

        .nota-edicion {{
            background: #fef3c7;
            border: 2px solid #fbbf24;
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
            color: #78350f;
            font-weight: 600;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>⚡ TESLA ELECTRICIDAD Y AUTOMATIZACIÓN</h1>
            <p class="agente">🤖 Generado por {agente} - Vista Editable</p>
        </div>

        <div class="content">
            <h2 class="titulo-seccion">📋 COTIZACIÓN SIMPLE - MODO EDITABLE</h2>

            <div class="info-basica">
                <div class="campo">
                    <label>👤 Cliente:</label>
                    <input type="text" id="cliente" name="cliente" value="{cliente}" placeholder="Nombre del cliente">
                </div>
                <div class="campo">
                    <label>📁 Proyecto:</label>
                    <input type="text" id="proyecto" name="proyecto" value="{proyecto}" placeholder="Nombre del proyecto">
                </div>
            </div>

            <div class="nota-edicion">
                ✏️ <strong>MODO EDICIÓN ACTIVA:</strong> Puedes modificar todos los campos directamente.
                Los totales se calcularán automáticamente al presionar el botón "Calcular Totales" o al cambiar cualquier valor.
            </div>

            <table class="items-table">
                <thead>
                    <tr>
                        <th style="width: 45%">📋 Descripción</th>
                        <th style="width: 15%">🔢 Cantidad</th>
                        <th style="width: 12%">📏 Unidad</th>
                        <th style="width: 15%">💰 Precio Unit.</th>
                        <th style="width: 13%">💵 Total</th>
                    </tr>
                </thead>
                <tbody id="items-body">
"""

    # Agregar items editables
    for i, item in enumerate(items):
        descripcion = item.get('descripcion', '')
        cantidad = item.get('cantidad', 0)
        unidad = item.get('unidad', 'und')
        precio = item.get('precio_unitario', 0)
        total = cantidad * precio

        html += f"""
                    <tr class="item-row">
                        <td>
                            <input type="text" class="item-desc" value="{descripcion}"
                                   placeholder="Descripción del servicio/producto">
                        </td>
                        <td>
                            <input type="number" class="item-cant" value="{cantidad}"
                                   min="0" step="0.01" onchange="calcularTotales()">
                        </td>
                        <td>
                            <input type="text" class="item-unidad" value="{unidad}"
                                   placeholder="und">
                        </td>
                        <td>
                            <input type="number" class="item-precio" value="{precio}"
                                   min="0" step="0.01" onchange="calcularTotales()">
                        </td>
                        <td class="total-item">S/ {total:.2f}</td>
                    </tr>
"""

    # Si no hay items, agregar una fila vacía
    if not items:
        html += """
                    <tr class="item-row">
                        <td>
                            <input type="text" class="item-desc" value=""
                                   placeholder="Descripción del servicio/producto">
                        </td>
                        <td>
                            <input type="number" class="item-cant" value="1"
                                   min="0" step="0.01" onchange="calcularTotales()">
                        </td>
                        <td>
                            <input type="text" class="item-unidad" value="und"
                                   placeholder="und">
                        </td>
                        <td>
                            <input type="number" class="item-precio" value="0"
                                   min="0" step="0.01" onchange="calcularTotales()">
                        </td>
                        <td class="total-item">S/ 0.00</td>
                    </tr>
"""

    html += f"""
                </tbody>
            </table>

            <div class="opciones-visualizacion">
                <h3>⚙️ Opciones de Visualización</h3>
                <div class="checkbox-group">
                    <div class="checkbox-item">
                        <input type="checkbox" id="mostrar_precios_unitarios" checked
                               onchange="calcularTotales()">
                        <label for="mostrar_precios_unitarios">Mostrar Precios Unitarios</label>
                    </div>
                    <div class="checkbox-item">
                        <input type="checkbox" id="mostrar_igv" checked
                               onchange="calcularTotales()">
                        <label for="mostrar_igv">Mostrar IGV (18%)</label>
                    </div>
                    <div class="checkbox-item">
                        <input type="checkbox" id="mostrar_total" checked
                               onchange="calcularTotales()">
                        <label for="mostrar_total">Mostrar Total Final</label>
                    </div>
                </div>
            </div>

            <div class="totales" id="seccion-totales">
                <div class="total-row">
                    <span>💰 Subtotal:</span>
                    <span id="subtotal_valor">S/ 0.00</span>
                </div>
                <div class="total-row igv" id="fila-igv">
                    <span>📋 IGV (18%):</span>
                    <span id="igv_valor">S/ 0.00</span>
                </div>
                <div class="total-row final" id="fila-total">
                    <span>🏆 TOTAL:</span>
                    <span id="total_valor">S/ 0.00</span>
                </div>
            </div>

            <button class="boton-calcular" onclick="calcularTotales()">
                🧮 Calcular Totales
            </button>

            <div class="footer">
                <strong>Tesla Electricidad y Automatización S.A.C.</strong><br>
                RUC: 20601138787 | Huancayo, Junín, Perú<br>
                📧 ingenieria.teslaelectricidad@gmail.com | 📱 +51 906 315 961<br>
                <br>
                Documento generado por {agente} v3.0 | {datetime.now().strftime('%d/%m/%Y %H:%M')}
            </div>
        </div>
    </div>

    <script>
        function calcularTotales() {{
            let subtotal = 0;

            // Calcular totales de cada fila
            const filas = document.querySelectorAll('.item-row');
            filas.forEach((fila, index) => {{
                const cantidad = parseFloat(fila.querySelector('.item-cant').value) || 0;
                const precio = parseFloat(fila.querySelector('.item-precio').value) || 0;
                const total = cantidad * precio;

                // Actualizar celda de total
                const celdaTotal = fila.querySelector('.total-item');
                celdaTotal.textContent = 'S/ ' + total.toFixed(2);

                subtotal += total;
            }});

            // Calcular IGV y total
            const mostrarIGV = document.getElementById('mostrar_igv').checked;
            const mostrarTotal = document.getElementById('mostrar_total').checked;

            const igv = mostrarIGV ? subtotal * 0.18 : 0;
            const total = subtotal + igv;

            // Actualizar valores
            document.getElementById('subtotal_valor').textContent = 'S/ ' + subtotal.toFixed(2);
            document.getElementById('igv_valor').textContent = 'S/ ' + igv.toFixed(2);
            document.getElementById('total_valor').textContent = 'S/ ' + total.toFixed(2);

            // Mostrar/ocultar filas según checkboxes
            document.getElementById('fila-igv').style.display = mostrarIGV ? 'flex' : 'none';
            document.getElementById('fila-total').style.display = mostrarTotal ? 'flex' : 'none';
        }}

        // Calcular totales al cargar la página
        window.addEventListener('DOMContentLoaded', function() {{
            calcularTotales();
        }});
    </script>
</body>
</html>
"""

    return html
