from typing import Dict, Any
from datetime import datetime, timedelta

def generar_preview_proyecto_complejo_pmi_editable(datos: Dict[str, Any], agente: str) -> str:
    """
    AGENTE 2 - Vista previa HTML COMPLETAMENTE EDITABLE - Proyecto Complejo (PMI)

    Características:
    - Estructura PMI completa
    - Múltiples pestañas de gestión (General, Stakeholders, Cronograma, Riesgos, Presupuesto)
    - Tablas dinámicas editables
    """

    nombre = datos.get('nombre', 'Proyecto Estándar')
    cliente = datos.get('cliente', 'Cliente General')
    codigo = datos.get('codigo', f"PMI-{datetime.now().strftime('%Y%m')}-001")
    presupuesto = datos.get('presupuesto', 0)
    fecha_inicio = datos.get('fecha_inicio', datetime.now().strftime('%Y-%m-%d'))
    fecha_fin = datos.get('fecha_fin', (datetime.now() + timedelta(days=180)).strftime('%Y-%m-%d'))
    alcance = datos.get('alcance', '')

    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Proyecto PMI Complejo - {agente}</title>
    <style>
        :root {{
            --primary: #0052A3;
            --primary-dark: #1E40AF;
            --primary-light: #fff;
            --accent: #3B82F6;
            --text-main: #0f172a;
            --text-light: #64748b;
            --bg-body: #f1f5f9;
            --bg-card: #ffffff;
            --border: #e2e8f0;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', system-ui, sans-serif; }}
        body {{ background-color: var(--bg-body); color: var(--text-main); line-height: 1.5; padding: 20px; }}
        
        .container {{
            max-width: 1300px;
            margin: 0 auto;
            background: var(--bg-card);
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            overflow: hidden;
            border: 1px solid var(--border);
        }}

        /* Header Profesional */
        .project-header {{
            background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
            color: white;
            padding: 30px;
            position: relative;
        }}
        
        .project-meta {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 20px;
        }}
        
        .project-id {{
            background: rgba(255, 255, 255, 0.2);
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 13px;
            font-weight: 600;
            border: 1px solid rgba(255,255,255,0.3);
        }}

        .project-title h1 {{
            font-size: 28px;
            font-weight: 800;
            margin-bottom: 8px;
            text-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        .project-title p {{
            opacity: 0.9;
            font-size: 16px;
        }}

        /* Sistema de Tabs Estilo Folder */
        .tabs-container {{
            background: #f8fafc;
            border-bottom: 1px solid var(--border);
            padding: 0 30px;
            display: flex;
            gap: 5px;
            overflow-x: auto;
        }}

        .tab-btn {{
            padding: 15px 25px;
            background: transparent;
            border: none;
            border-bottom: 3px solid transparent;
            font-size: 15px;
            font-weight: 600;
            color: var(--text-light);
            cursor: pointer;
            transition: all 0.2s;
            white-space: nowrap;
        }}

        .tab-btn:hover {{
            color: var(--primary);
            background: #eef2ff;
        }}

        .tab-btn.active {{
            color: var(--primary);
            border-bottom-color: var(--primary);
            background: white;
            border-radius: 8px 8px 0 0;
            box-shadow: 0 -4px 6px -4px rgba(0,0,0,0.1);
        }}

        /* Contenido de Tabs */
        .tab-content {{
            padding: 40px;
            display: none;
            animation: fadeIn 0.3s ease;
        }}
        
        .tab-content.active {{
            display: block;
        }}

        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        /* Estilos de Formularios y Grids */
        .grid-2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 25px; }}
        .grid-3 {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }}
        
        .form-section {{ margin-bottom: 30px; }}
        .form-section h3 {{
            color: var(--primary);
            font-size: 18px;
            border-bottom: 2px solid #e2e8f0;
            padding-bottom: 10px;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .input-group {{ margin-bottom: 15px; }}
        .input-group label {{
            display: block;
            font-size: 13px;
            font-weight: 700;
            color: var(--text-light);
            margin-bottom: 5px;
            text-transform: uppercase;
        }}

        .input-control {{
            width: 100%;
            padding: 10px 12px;
            border: 2px solid var(--border);
            border-radius: 6px;
            font-size: 14px;
            transition: all 0.2s;
            background: #f8fafc;
        }}

        .input-control:focus {{
            outline: none;
            border-color: var(--accent);
            background: white;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        }}

        textarea.input-control {{ min-height: 100px; resize: vertical; }}

        /* Tablas Profesionales */
        .table-container {{
            border: 1px solid var(--border);
            border-radius: 8px;
            overflow: hidden;
            margin-top: 15px;
        }}

        table {{ width: 100%; border-collapse: collapse; }}
        
        th {{
            background: #f1f5f9;
            color: var(--text-main);
            font-weight: 700;
            text-align: left;
            padding: 12px 15px;
            font-size: 13px;
            border-bottom: 1px solid var(--border);
        }}

        td {{
            padding: 10px 15px;
            border-bottom: 1px solid var(--border);
        }}

        tr:last-child td {{ border-bottom: none; }}
        tr:hover td {{ background: #f8fafc; }}

        /* Badges de Estado */
        .badge {{
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 600;
            display: inline-block;
        }}
        
        .badge-pending {{ background: #fef3c7; color: #92400e; }}
        .badge-active {{ background: #dbeafe; color: #1e40af; }}
        .badge-done {{ background: #dcfce7; color: #166534; }}
        .badge-risk {{ background: #fee2e2; color: #991b1b; }}

        /* Footer */
        .footer-bar {{
            background: #f8fafc;
            border-top: 1px solid var(--border);
            padding: 15px 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 13px;
            color: var(--text-light);
        }}
        
        .btn-action {{
            background: var(--primary);
            color: white;
            padding: 8px 16px;
            border-radius: 6px;
            text-decoration: none;
            font-weight: 600;
            font-size: 13px;
            border: none;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }}

        .btn-action:hover {{ background: var(--primary-dark); }}

        /* Utilidades */
        .h-full {{ height: 100%; }}
        .text-right {{ text-align: right; }}
    </style>
    <script>
        function openTab(evt, tabName) {{
            var i, tabcontent, tablinks;
            tabcontent = document.getElementsByClassName("tab-content");
            for (i = 0; i < tabcontent.length; i++) {{
                tabcontent[i].style.display = "none";
                tabcontent[i].classList.remove("active");
            }}
            tablinks = document.getElementsByClassName("tab-btn");
            for (i = 0; i < tablinks.length; i++) {{
                tablinks[i].className = tablinks[i].className.replace(" active", "");
            }}
            document.getElementById(tabName).style.display = "block";
            document.getElementById(tabName).classList.add("active");
            evt.currentTarget.className += " active";
        }}
    </script>
</head>
<body>

<div class="container">
    <div class="project-header">
        <div class="project-meta">
            <span class="project-id">{codigo}</span>
            <span class="project-id" style="background: rgba(16, 185, 129, 0.2); border-color: rgba(16, 185, 129, 0.4);">🟢 ESTADO: PLANIFICACIÓN</span>
        </div>
        <div class="project-title">
            <h1>{nombre}</h1>
            <p>{cliente} | {agente}</p>
        </div>
    </div>

    <div class="tabs-container">
        <button class="tab-btn active" onclick="openTab(event, 'general')">📌 General & Alcance</button>
        <button class="tab-btn" onclick="openTab(event, 'stakeholders')">👥 Stakeholders</button>
        <button class="tab-btn" onclick="openTab(event, 'cronograma')">📅 Cronograma (WBS)</button>
        <button class="tab-btn" onclick="openTab(event, 'riesgos')">⚠️ Gestión de Riesgos</button>
        <button class="tab-btn" onclick="openTab(event, 'presupuesto')">💰 Presupuesto Detallado</button>
    </div>

    <!-- TAB: GENERAL -->
    <div id="general" class="tab-content active">
        <div class="grid-2">
            <div>
                <div class="form-section">
                    <h3>📝 Información Principal</h3>
                    <div class="grid-2">
                        <div class="input-group">
                            <label>Nombre del Proyecto</label>
                            <input type="text" class="input-control" value="{nombre}">
                        </div>
                        <div class="input-group">
                            <label>Código Interno</label>
                            <input type="text" class="input-control" value="{codigo}">
                        </div>
                    </div>
                </div>
                
                <div class="form-section">
                    <h3>👤 Datos del Cliente</h3>
                    <div class="input-group">
                        <label>Cliente / Empresa</label>
                        <input type="text" class="input-control" value="{cliente}">
                    </div>
                    <div class="grid-2">
                        <div class="input-group">
                            <label>Contacto Principal</label>
                            <input type="text" class="input-control" placeholder="Nombre contacto">
                        </div>
                        <div class="input-group">
                            <label>Email / Teléfono</label>
                            <input type="text" class="input-control" placeholder="Datos contacto">
                        </div>
                    </div>
                </div>
            </div>
            
            <div>
                <div class="form-section">
                    <h3>📅 Fechas Clave</h3>
                    <div class="grid-2">
                         <div class="input-group">
                            <label>Inicio Planificado</label>
                            <input type="date" class="input-control" value="{fecha_inicio}">
                        </div>
                         <div class="input-group">
                            <label>Cierre Estimado</label>
                            <input type="date" class="input-control" value="{fecha_fin}">
                        </div>
                    </div>
                </div>

                <div class="form-section">
                    <h3>🎯 Definición del Alcance (SOW)</h3>
                    <div class="input-group">
                        <label>Descripción del Alcance</label>
                        <textarea class="input-control" style="height: 150px;">{alcance}</textarea>
                    </div>
                    <div class="input-group">
                        <label>❌ Exclusiones (Fuera del Alcance)</label>
                        <textarea class="input-control" placeholder="Especifique qué NO incluye este proyecto..."></textarea>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- TAB: STAKEHOLDERS -->
    <div id="stakeholders" class="tab-content">
        <div class="form-section">
            <h3>👥 Registro de Interesados (Stakeholders)</h3>
            <p style="margin-bottom: 15px; color: var(--text-light); font-size: 14px;">Gestión de todas las partes involucradas en el proyecto según estándar PMI.</p>
            
            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>Nombre</th>
                            <th>Rol / Cargo</th>
                            <th>Tipo</th>
                            <th>Nivel de Influencia</th>
                            <th>Estrategia Gestión</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><input type="text" class="input-control" value="Gerencia General" style="border:none; padding:5px; background:transparent;"></td>
                            <td><input type="text" class="input-control" value="Sponsor" style="border:none; padding:5px; background:transparent;"></td>
                            <td><span class="badge badge-active">Interno</span></td>
                            <td><select class="input-control" style="padding: 2px;"><option>Alto</option><option>Medio</option></select></td>
                            <td><input type="text" class="input-control" value="Mantener informado" style="border:none; padding:5px; background:transparent;"></td>
                        </tr>
                        <tr>
                            <td><input type="text" class="input-control" value="{cliente}" style="border:none; padding:5px; background:transparent;"></td>
                            <td>Clientes</td>
                            <td><span class="badge badge-pending">Externo</span></td>
                            <td>Alto</td>
                            <td>Gestionar atentamente</td>
                        </tr>
                        <tr>
                            <td><input type="text" class="input-control" value="Proveedores Locales" style="border:none; padding:5px; background:transparent;"></td>
                            <td>Suministros</td>
                            <td><span class="badge badge-pending">Externo</span></td>
                            <td>Medio</td>
                            <td>Monitorear</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <button class="btn-action" style="margin-top: 15px; background: #fff; color: var(--primary); border: 2px solid var(--primary);">+ Agregar Interesado</button>
        </div>
    </div>

    <!-- TAB: CRONOGRAMA -->
    <div id="cronograma" class="tab-content">
        <div class="form-section">
            <h3>📅 Cronograma de Trabajo (WBS Nivel 1)</h3>
            
            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th width="5%">ID</th>
                            <th width="40%">Entregable / Fase</th>
                            <th width="15%">Duración</th>
                            <th width="15%">Inicio</th>
                            <th width="15%">Fin</th>
                            <th width="10%">Estado</th>
                        </tr>
                    </thead>
                    <tbody>
"""

    # Fases PMI estándar
    fases_pmi = [
        ("1.0", "Iniciación y Acta de Constitución", "5 días", "En curso"),
        ("2.0", "Planificación de Ingeniería", "15 días", "Pendiente"),
        ("3.0", "Adquisiciones y Logística", "20 días", "Pendiente"),
        ("4.0", "Ejecución y Obras Civiles", "30 días", "Pendiente"),
        ("5.0", "Instalaciones Eléctricas", "25 días", "Pendiente"),
        ("6.0", "Pruebas y Comisionamiento", "10 días", "Pendiente"),
        ("7.0", "Cierre y Entrega", "5 días", "Pendiente")
    ]

    fecha_iter = datetime.strptime(fecha_inicio, '%Y-%m-%d')
    
    for id_fase, nombre_fase, duracion, estado in fases_pmi:
        dias = int(duracion.split()[0])
        fin_fase = fecha_iter + timedelta(days=dias)
        
        badge_cls = "badge-active" if estado == "En curso" else "badge-pending"
        
        html += f"""
                        <tr>
                            <td><b>{id_fase}</b></td>
                            <td><input type="text" class="input-control" value="{nombre_fase}" style="border:none; padding:5px; background:transparent; font-weight:600;"></td>
                            <td><input type="text" class="input-control" value="{duracion}" style="width: 80px;"></td>
                            <td>{fecha_iter.strftime('%d/%m')}</td>
                            <td>{fin_fase.strftime('%d/%m')}</td>
                            <td><span class="badge {badge_cls}">{estado}</span></td>
                        </tr>
        """
        fecha_iter = fin_fase

    html += """
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <!-- TAB: RIESGOS -->
    <div id="riesgos" class="tab-content">
        <div class="form-section">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:20px;">
                <h3>⚠️ Matriz de Riesgos</h3>
                <span class="badge badge-risk" style="font-size:14px;">Nivel de Riesgo Global: MODERADO</span>
            </div>
            
            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th width="30%">Riesgo Identificado</th>
                            <th width="15%">Probabilidad</th>
                            <th width="15%">Impacto</th>
                            <th width="40%">Plan de Respuesta</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><input type="text" class="input-control" value="Retraso en suministro de equipos" style="border:none;"></td>
                            <td><select class="input-control"><option>Media</option><option>Alta</option><option>Baja</option></select></td>
                            <td><select class="input-control"><option>Alto</option><option selected>Medio</option></select></td>
                            <td><textarea class="input-control" style="min-height:40px;">Contar con proveedores alternativos pre-aprobados.</textarea></td>
                        </tr>
                        <tr>
                            <td><input type="text" class="input-control" value="Cambios en alcance por cliente" style="border:none;"></td>
                            <td><select class="input-control"><option selected>Alta</option></select></td>
                            <td><select class="input-control"><option selected>Alto</option></select></td>
                            <td><textarea class="input-control" style="min-height:40px;">Estricto control de cambios y actas de aprobación.</textarea></td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <!-- TAB: PRESUPUESTO -->
    <div id="presupuesto" class="tab-content">
        <div class="form-section">
            <h3>💰 Estructura de Costos</h3>
            <div class="grid-3" style="margin-bottom:20px;">
                <div class="input-group">
                    <label>Presupuesto Total (S/)</label>
                    <input type="number" class="input-control" value="{presupuesto}" style="font-size:18px; font-weight:700; color:var(--primary);">
                </div>
                <div class="input-group">
                    <label>Reserva de Contingencia (10%)</label>
                    <input type="number" class="input-control" value="{float(presupuesto)*0.10:.2f}" readonly>
                </div>
                <div class="input-group">
                    <label>Margen Estimado</label>
                    <input type="text" class="input-control" value="25%">
                </div>
            </div>

            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>Partida Presupuestal</th>
                            <th>Monto Estimado (S/)</th>
                            <th>Monto Real (S/)</th>
                            <th>Desviación</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>1. Materiales y Equipos</td>
                            <td><input type="number" class="input-control" value="{float(presupuesto)*0.45:.2f}"></td>
                            <td>0.00</td>
                            <td>0%</td>
                        </tr>
                        <tr>
                            <td>2. Mano de Obra</td>
                            <td><input type="number" class="input-control" value="{float(presupuesto)*0.30:.2f}"></td>
                            <td>0.00</td>
                            <td>0%</td>
                        </tr>
                        <tr>
                            <td>3. Gastos Generales</td>
                            <td><input type="number" class="input-control" value="{float(presupuesto)*0.15:.2f}"></td>
                            <td>0.00</td>
                            <td>0%</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <!-- FOOTER -->
    <div class="footer-bar">
        <div>
            <strong>PILI System v3.0</strong> | {datetime.now().strftime('%Y-%m-%d %H:%M')}
        </div>
        <div>
            <button class="btn-action">💾 Guardar Cambios</button>
            <button class="btn-action" style="background:#166534; margin-left:10px;">📄 Generar PDF Oficial</button>
        </div>
    </div>

</div>

</body>
</html>
"""

    return html
