from typing import Dict, Any
from datetime import datetime, timedelta

def generar_preview_proyecto_simple_editable(datos: Dict[str, Any], agente: str) -> str:
    """
    AGENTE 2 - Vista previa HTML COMPLETAMENTE EDITABLE para Proyecto Simple

    Genera HTML con inputs editables para gestión de proyectos básicos.
    Colores: Paleta AZUL Tesla (#0052A3, #1E40AF, #3B82F6)
    """

    nombre = datos.get('nombre', '')
    cliente = datos.get('cliente', '')
    codigo = datos.get('codigo', f"PRY-{datetime.now().strftime('%Y%m')}-001")
    presupuesto = datos.get('presupuesto', 0)
    fecha_inicio = datos.get('fecha_inicio', datetime.now().strftime('%Y-%m-%d'))
    fecha_fin = datos.get('fecha_fin', (datetime.now() + timedelta(days=90)).strftime('%Y-%m-%d'))
    alcance = datos.get('alcance', '')

    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Proyecto Simple - {agente}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Arial, sans-serif;
            margin: 20px;
            background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
        }}
        .container {{
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 8px 32px rgba(0, 82, 163, 0.2);
            border: 3px solid #3B82F6;
        }}
        .header {{
            background: linear-gradient(135deg, #0052A3 0%, #1E40AF 100%);
            color: white;
            padding: 25px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 4px 12px rgba(0, 82, 163, 0.3);
        }}
        .company {{
            font-size: 28px;
            font-weight: 900;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
            letter-spacing: -0.5px;
        }}
        .agent {{
            font-size: 14px;
            margin-top: 8px;
            opacity: 0.95;
            font-weight: 600;
        }}
        .title {{
            color: #0052A3;
            font-size: 24px;
            margin: 25px 0;
            font-weight: 800;
            border-left: 6px solid #1E40AF;
            padding-left: 15px;
            background: linear-gradient(90deg, #EFF6FF 0%, transparent 100%);
            padding: 10px 15px;
            border-radius: 4px;
        }}
        .form-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin: 25px 0;
        }}
        .form-group {{
            background: #F0F9FF;
            padding: 18px;
            border-radius: 8px;
            border: 2px solid #BFDBFE;
        }}
        .form-group label {{
            display: block;
            font-weight: 800;
            color: #1E40AF;
            font-size: 14px;
            margin-bottom: 8px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        .form-group input, .form-group textarea {{
            width: 100%;
            padding: 12px;
            border: 2px solid #3B82F6;
            border-radius: 6px;
            font-size: 15px;
            font-weight: 600;
            color: #1F2937;
            transition: all 0.3s ease;
            box-sizing: border-box;
        }}
        .form-group input:focus, .form-group textarea:focus {{
            outline: none;
            border-color: #0052A3;
            box-shadow: 0 0 0 3px rgba(0, 82, 163, 0.1);
        }}
        .full-width {{
            grid-column: 1 / -1;
        }}
        .fase-card {{
            background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
            border-left: 5px solid #0052A3;
            padding: 18px;
            margin: 12px 0;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0, 82, 163, 0.15);
        }}
        .fase-header {{
            font-weight: 800;
            color: #0052A3;
            font-size: 16px;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .fase-inputs {{
            display: grid;
            grid-template-columns: 2fr 1fr 1fr;
            gap: 12px;
        }}
        .fase-inputs input, .fase-inputs select {{
            padding: 10px;
            border: 2px solid #3B82F6;
            border-radius: 5px;
            font-weight: 600;
        }}
        .recursos-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
            margin: 20px 0;
        }}
        .recurso-card {{
            background: white;
            padding: 15px;
            border: 2px solid #3B82F6;
            border-radius: 8px;
            box-shadow: 0 2px 6px rgba(59, 130, 246, 0.15);
        }}
        .edit-note {{
            background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%);
            border: 2px solid #F59E0B;
            padding: 18px;
            border-radius: 8px;
            margin-top: 25px;
            font-weight: 700;
            color: #92400E;
            box-shadow: 0 2px 8px rgba(245, 158, 11, 0.2);
        }}
        .signature {{
            text-align: right;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 3px solid #BFDBFE;
            font-weight: 700;
            color: #0052A3;
        }}
        select {{
            cursor: pointer;
        }}
        select:hover {{
            background: #EFF6FF;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="company">⚡ TESLA ELECTRICIDAD Y AUTOMATIZACIÓN S.A.C.</div>
            <div class="agent">🤖 {agente} - Sistema de Gestión de Proyectos</div>
        </div>

        <h2 class="title">📋 PROYECTO SIMPLE - EDITABLE</h2>

        <div class="form-grid">
            <div class="form-group">
                <label>📝 Nombre del Proyecto</label>
                <input type="text" name="nombre" value="{nombre}" placeholder="Ej: Instalación Eléctrica Oficina XYZ">
            </div>
            <div class="form-group">
                <label>👤 Cliente</label>
                <input type="text" name="cliente" value="{cliente}" placeholder="Nombre del cliente">
            </div>
            <div class="form-group">
                <label>🔢 Código de Proyecto</label>
                <input type="text" name="codigo" value="{codigo}" placeholder="PRY-202512-001">
            </div>
            <div class="form-group">
                <label>💰 Presupuesto Estimado (S/)</label>
                <input type="number" name="presupuesto" value="{presupuesto}" step="0.01" placeholder="0.00">
            </div>
            <div class="form-group">
                <label>📅 Fecha de Inicio</label>
                <input type="date" name="fecha_inicio" value="{fecha_inicio}">
            </div>
            <div class="form-group">
                <label>📅 Fecha de Fin Estimada</label>
                <input type="date" name="fecha_fin" value="{fecha_fin}">
            </div>
            <div class="form-group full-width">
                <label>📄 Alcance del Proyecto</label>
                <textarea name="alcance" rows="4" placeholder="Descripción detallada del alcance del proyecto...">{alcance}</textarea>
            </div>
        </div>

        <h3 class="title" style="font-size: 20px; margin-top: 30px;">🔄 Fases del Proyecto (5 etapas)</h3>
"""

    fases_default = [
        {'nombre': 'Planificación y Diseño', 'duracion': '1-2 semanas', 'estado': 'pendiente'},
        {'nombre': 'Ingeniería de Detalle', 'duracion': '2-3 semanas', 'estado': 'pendiente'},
        {'nombre': 'Ejecución y Montaje', 'duracion': '3-4 semanas', 'estado': 'pendiente'},
        {'nombre': 'Pruebas y Comisionamiento', 'duracion': '1 semana', 'estado': 'pendiente'},
        {'nombre': 'Entrega y Cierre', 'duracion': '1 semana', 'estado': 'pendiente'}
    ]

    fases = datos.get('fases', fases_default)

    for i, fase in enumerate(fases[:5], 1):
        nombre_fase = fase.get('nombre', f'Fase {{i}}')
        duracion = fase.get('duracion', '1 semana')
        estado = fase.get('estado', 'pendiente')

        html += f"""
        <div class="fase-card">
            <div class="fase-header">
                ▶️ Fase {i}
            </div>
            <div class="fase-inputs">
                <input type="text" value="{nombre_fase}" placeholder="Nombre de la fase">
                <input type="text" value="{duracion}" placeholder="Duración">
                <select>
                    <option value="pendiente" {"selected" if estado == "pendiente" else ""}>⏳ Pendiente</option>
                    <option value="en_curso" {"selected" if estado == "en_curso" else ""}>🔄 En Curso</option>
                    <option value="completado" {"selected" if estado == "completado" else ""}>✅ Completado</option>
                    <option value="pausado" {"selected" if estado == "pausado" else ""}>⏸️ Pausado</option>
                </select>
            </div>
        </div>
"""

    html += """
        <h3 class="title" style="font-size: 20px; margin-top: 30px;">👥 Recursos Asignados</h3>
        <div class="recursos-grid">
"""

    recursos_default = [
        {'rol': 'Jefe de Proyecto', 'nombre': 'Por asignar'},
        {'rol': 'Ingeniero Eléctrico', 'nombre': 'Por asignar'},
        {'rol': 'Técnico Instalador', 'nombre': 'Por asignar'},
        {'rol': 'Supervisor de Obra', 'nombre': 'Por asignar'}
    ]

    recursos = datos.get('recursos', recursos_default)

    for recurso in recursos[:4]:
        rol = recurso.get('rol', 'Rol')
        nombre = recurso.get('nombre', 'Por asignar')

        html += f"""
            <div class="recurso-card">
                <label style="font-weight: 800; color: #1E40AF; font-size: 13px; display: block; margin-bottom: 6px;">
                    {rol}
                </label>
                <input type="text" value="{nombre}" placeholder="Nombre del recurso"
                       style="width: 100%; padding: 8px; border: 2px solid #3B82F6; border-radius: 5px; font-weight: 600;">
            </div>
"""

    html += f"""
        </div>

        <div class="edit-note">
            ✏️ <strong>Vista Previa Editable:</strong> Todos los campos son editables. Modifica los datos según las necesidades del proyecto.
            Los cambios se reflejarán en el documento final Word/PDF.
        </div>

        <div class="signature">
            <div style="color: #6b7280; font-size: 12px;">
                Documento generado por {agente} v3.0<br>
                {datetime.now().strftime('%d/%m/%Y %H:%M')} - Sistema Tesla
            </div>
        </div>
    </div>
</body>
</html>
"""

    return html
