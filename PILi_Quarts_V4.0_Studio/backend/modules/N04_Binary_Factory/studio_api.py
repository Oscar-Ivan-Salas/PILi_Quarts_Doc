import os
import logging
from datetime import datetime
from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pathlib import Path
from typing import List
from jinja2 import Environment, FileSystemLoader, select_autoescape

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("N04_Studio_API")

# Intentar importar la factoría soberana
try:
    from index import binary_factory
except ImportError:
    import sys
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from index import binary_factory

# Configuración de Entorno (Cloud Ready)
PORT = int(os.environ.get("PORT", 8005))
CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "*").split(",")

app = FastAPI(title="N04 Mirror Studio API - SOBERANO V10")

# Habilitar CORS dinámico
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"]
)

BASE_DIR = Path(__file__).parent
TEMPLATES_DIR = BASE_DIR / "templates" / "html"
OUTPUT_DIR = BASE_DIR / "output_sandbox"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Configuración de Jinja2 para el Studio
jinja_env = Environment(
    loader=FileSystemLoader(str(TEMPLATES_DIR)),
    autoescape=select_autoescape(['html', 'xml'])
)

# Filtro personalizado para moneda
def format_currency(value):
    try:
        return f"{float(value):,.2f}"
    except:
        return value

# Filtro para formatear números (usado por templates)
def format_number(value):
    try:
        return f"{float(value):,.2f}"
    except:
        return value

jinja_env.filters['format_currency'] = format_currency
jinja_env.filters['format_number'] = format_number

@app.get("/api/studio/ping")
async def ping():
    logger.info("📡 PING recibido desde el navegador")
    return {"status": "pong", "message": "N04 Mirror Studio API is ALIVE"}

@app.get("/api/studio/templates")
async def list_templates():
    templates = []
    if TEMPLATES_DIR.exists():
        for f in TEMPLATES_DIR.glob("PLANTILLA_HTML_*.html"):
            name = f.stem.replace("PLANTILLA_HTML_", "")
            templates.append(name)
    return sorted(templates)

@app.get("/api/studio/template/{name}")
async def get_template(name: str):
    template_file = f"PLANTILLA_HTML_{name}.html"
    if not (TEMPLATES_DIR / template_file).exists():
        template_file = f"{name}.html"
        if not (TEMPLATES_DIR / template_file).exists():
            raise HTTPException(status_code=404, detail=f"Template {name} not found")
             
    try:
        # Data de Prueba Detallada (Mock Data para Fidelidad Oro)
        data_payload = {
            "TITULO_DOCUMENTO": name.replace("_", " "),
            "SUBTITULO_DOCUMENTO": "Servicios de Ingeniería Especializada",
            "CODIGO_DOC": f"N04-SOL-{datetime.now().year}-045",
            "FECHA_DOC": datetime.now().strftime("%d/%m/%Y"),
            "NOMBRE_EMISOR": "TU EMPRESA S.A.C.",
            "RUC_EMISOR": "20123456789",
            "DIRECCION_EMISOR": "Av. Tecnología 123, Lima",
            "CLIENTE_NOMBRE": "INDUSTRIAL SOLUTIONS PERÚ S.A.",
            "CLIENTE_RUC": "20555666777",
            "CLIENTE_DIRECCION": "Parque Industrial Lote 45, Lurín",
            "CLIENTE_EMAIL": "gerencia@industrial.com",
            "PROYECTO_NOMBRE": "SISTEMA DE AUTOMATIZACIÓN Y CONTROL Q3",
            "PROYECTO_RESUMEN": "Implementación de red de control redundante y optimización de KPIs operativos.",
            "VIGENCIA": "15 días calendario",
            "MONEDA_SIMBOLO": "S/",
            "MONEDA_NOMBRE": "SOLES",
            "SUBTOTAL": 4550.00,
            "IGV": 819.00,
            "TOTAL": 5369.00,
            "DURACION": "60",
            # KPIs para Proyectos PMI
            "KPI_SPI": "1.05",
            "KPI_CPI": "0.98",
            "AVANCE_FISICO": "45%",
            "AVANCE_FINAN": "42%",
            # Listas Detalladas
            "suministros": [
                {"item": "01", "descripcion": "Controlador PLC Siemens S7-1200", "cantidad": 1, "unidad": "und", "precioTotal": 1250.00},
                {"item": "02", "descripcion": "Licencia TIA Portal V17 Premium", "cantidad": 1, "unidad": "srv", "precioTotal": 800.00},
                {"item": "03", "descripcion": "Instalación y Configuración en Planta", "cantidad": 1, "unidad": "glob", "precioTotal": 2500.00}
            ],
            "entregables": [
                "Planos Eléctricos en AutoCAD v2026",
                "Manuales de Operación y Mantenimiento",
                "Protocolos de Pruebas de Funcionamiento (FAT/SAT)"
            ],
            "fases_pmi": [
                {"nombre": "Ingeniería y Diseño", "descripcion": "Cálculos y planos de detalle.", "presupuesto": 5000.00},
                {"nombre": "Suministro e Instalación", "descripcion": "Montaje de componentes.", "presupuesto": 12000.00},
                {"nombre": "Comisionamiento", "descripcion": "Puesta en marcha final.", "presupuesto": 8000.00}
            ],
            "fases": [
                {"nombre": "Fase 1: Preparación", "descripcion": "Logística y materiales.", "duracion": 2, "presupuesto": 5000},
                {"nombre": "Fase 2: Ejecución", "descripcion": "Instalación técnica.", "duracion": 4, "presupuesto": 10000}
            ],
            "riesgos": [
                {"descripcion": "Retraso en importación de PLC", "probabilidad": "media", "mitigacion": "Uso de stock local"},
                {"descripcion": "Falta de acceso a tableros", "probabilidad": "baja", "mitigacion": "Coordinación previa"}
            ],
            # Informes
            "RESUMEN_EJECUTIVO": "Se recomienda la aprobación inmediata dada la tasa de retorno proyectada de 85%.",
            "METRICA_ROI": "85%",
            "METRICA_PAYBACK": "14m",
            "METRICA_TIR": "32%",
            "METRICA_AHORRO": "S/ 12,500",
            "conclusiones": [
                "El sistema es viable según estándares internacionales.",
                "Se proyecta un ahorro energético del 15%."
            ],
            "recomendaciones": [
                "Programar mantenimiento trimestral.",
                "Actualizar firmware de actuadores."
            ]
        }
        
        # Renderizado de prueba (Inyección de Datos Reales del Payload)
        template = jinja_env.get_template(template_file)
        
        # Guardar HTML crudo para re-renderizado dinámico (moneda/logo)
        raw_content = (TEMPLATES_DIR / template_file).read_text(encoding='utf-8')
        
        # Mezclar data_payload con overrides si vienen de la sesión (simulado)
        # En el Studio, el usuario espera ver sus cambios.
        content = template.render(**data_payload)
        
        # LIMPIEZA FINAL: Si después de renderizar quedan {{ }}, es que faltan keys.
        # Por seguridad, removemos tags de control restantes para una vista limpia.
        import re
        content = re.sub(r'\{\{.*?\}\}', '', content)
        content = re.sub(r'\{%.*?%\}', '', content)
        
        return {"content": content, "raw_content": raw_content}
    except Exception as e:
        logger.error(f"Error rendering template {name}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/studio/render")
async def render_html(payload: dict = Body(...)):
    """
    Renderiza un fragmento o documento HTML con el motor Jinja2 SOBERANO.
    Esto permite que la vista previa sea IDÉNTICA al documento final.
    """
    html_content = payload.get("html", "")
    settings = payload.get("settings", {})
    
    if not html_content:
        return {"html": ""}
        
    try:
        # CRÍTICO: usar jinja_env.from_string() (con filtros registrados) en vez de Template() directo
        template = jinja_env.from_string(html_content)
        
        # Sincronizar data del Studio con lo que espera el motor (ADN Soberano)
        render_data = settings.get("data", {})
        currency = settings.get("currency", "PEN")
        simbolo = "S/" if currency == "PEN" else "$" if currency == "USD" else "€"
        
        # Extraer ADN Visual para inyectar en la vista previa
        primary_color = settings.get("primaryColor", "#0052A3")
        secondary_color = settings.get("secondaryColor", "#1E40AF")
        font_family = settings.get("fontFamily", "Calibri")
        font_size = settings.get("fontSize", 11)
        logo_b64 = settings.get("logo", "")
        
        # Enriquecer contexto de renderizado con datos mock base + datos del usuario
        MOCK_BASE = {
            "TITULO_DOCUMENTO": render_data.get("PROYECTO_NOMBRE", "DOCUMENTO"),
            "SUBTITULO_DOCUMENTO": "Servicios de Ingeniería Especializada",
            "CODIGO_DOC": render_data.get("CODIGO_DOC", f"N04-SOL-{datetime.now().year}-045"),
            "FECHA_DOC": datetime.now().strftime("%d/%m/%Y"),
            "FECHA_COTIZACION": datetime.now().strftime("%d/%m/%Y"),
            "NOMBRE_EMISOR": render_data.get("NOMBRE_EMISOR", "TU EMPRESA S.A.C."),
            "RUC_EMISOR": render_data.get("RUC_EMISOR", "20123456789"),
            "CLIENTE_NOMBRE": render_data.get("CLIENTE", "INDUSTRIAL SOLUTIONS PERÚ S.A."),
            "CLIENTE_RUC": render_data.get("CLIENTE_RUC", "20555666777"),
            "PROYECTO_NOMBRE": render_data.get("PROYECTO_NOMBRE", "SISTEMA DE CONTROL N04"),
            "VIGENCIA": render_data.get("VIGENCIA", "15 días calendario"),
            "NORMATIVA_APLICABLE": "CNE - Código Nacional de Electricidad",
            "SERVICIO_NOMBRE": "Instalaciones Eléctricas",
            "AREA_M2": render_data.get("AREA_M2", ""),
            "DESCRIPCION_PROYECTO": render_data.get("DESCRIPCION_PROYECTO", "Implementación de sistema de control y automatización industrial."),
            "SUBTOTAL": 4550.00,
            "IGV": 819.00,
            "TOTAL": 5369.00,
            "RESUMEN_EJECUTIVO": "Se recomienda la aprobación inmediata dada la tasa de retorno proyectada.",
            "METRICA_ROI": "85%",
            "METRICA_PAYBACK": "14m",
            "METRICA_TIR": "32%",
            "METRICA_AHORRO": f"{simbolo} 12,500",
            "KPI_SPI": "1.05",
            "KPI_CPI": "0.98",
            "AVANCE_FISICO": "45%",
            "AVANCE_FINAN": "42%",
            "DURACION": "60",
            "logo_url": logo_b64 if logo_b64 else None,
            "items": [
                {"item": "01", "descripcion": "Ingeniería y Diseño del Sistema", "cantidad": 1, "unidad": "srv", "precio_unitario": 1500, "total": 1500},
                {"item": "02", "descripcion": "Suministro de Equipos Principales", "cantidad": 1, "unidad": "glob", "precio_unitario": 2000, "total": 2000},
                {"item": "03", "descripcion": "Instalación y Comisionamiento", "cantidad": 1, "unidad": "glob", "precio_unitario": 1050, "total": 1050},
            ],
            "suministros": [
                {"item": "01", "descripcion": "Controlador PLC Siemens S7-1200", "cantidad": 1, "unidad": "und", "precioTotal": 1250.00},
                {"item": "02", "descripcion": "Licencia TIA Portal V17", "cantidad": 1, "unidad": "srv", "precioTotal": 800.00},
                {"item": "03", "descripcion": "Instalación y Configuración", "cantidad": 1, "unidad": "glob", "precioTotal": 2500.00},
            ],
            "entregables": ["Planos Eléctricos en AutoCAD", "Manuales de Operación", "Protocolos de Pruebas"],
            "fases_pmi": [
                {"nombre": "Ingeniería y Diseño", "descripcion": "Cálculos y planos.", "presupuesto": 5000.00},
                {"nombre": "Instalación", "descripcion": "Montaje de componentes.", "presupuesto": 12000.00},
                {"nombre": "Comisionamiento", "descripcion": "Puesta en marcha.", "presupuesto": 8000.00},
            ],
            "fases": [
                {"nombre": "Fase 1: Preparación", "descripcion": "Logística.", "duracion": 2, "presupuesto": 5000},
                {"nombre": "Fase 2: Ejecución", "descripcion": "Instalación.", "duracion": 4, "presupuesto": 10000},
            ],
            "riesgos": [
                {"descripcion": "Retraso en importación", "probabilidad": "media", "mitigacion": "Uso de stock local"},
            ],
            "conclusiones": ["El sistema es viable.", "Se proyecta ahorro energético del 15%."],
            "recomendaciones": ["Mantenimiento trimestral.", "Actualizar firmware."],
        }
        
        # Los datos del usuario sobreescriben los mock base
        MOCK_BASE.update(render_data)
        
        # Siempre agregar/sobreescribir estos valores dinámicos
        MOCK_BASE.update({
            "MONEDA_SIMBOLO": simbolo,
            "MONEDA_NOMBRE": "SOLES" if currency == "PEN" else "DÓLARES AMERICANOS" if currency == "USD" else "EUROS",
            "PRIMARY_COLOR": primary_color,
            "SECONDARY_COLOR": secondary_color,
            "FONT_FAMILY": font_family,
            "FONT_SIZE": font_size,
            "LOGO_URL": logo_b64,
            "logo_url": logo_b64 if logo_b64 else None,
        })
        
        rendered_html = template.render(**MOCK_BASE)
        
        # INYECCIÓN CSS ADN VISUAL - Quirúrgico: aplica colores del usuario al template
        # sin romper los fondos de info-box ni el layout general
        style_block = f"""
        <style id="adn-visual-preview">
            :root {{
                --pili-primary: {primary_color};
                --pili-secondary: {secondary_color};
                --pili-font: "{font_family}", sans-serif;
                --pili-font-size: {font_size}pt;
            }}

            /* Fuente global */
            body {{
                font-family: var(--pili-font) !important;
                font-size: var(--pili-font-size);
                background: white;
            }}

            /* === COLORES DE TEXTO === */
            .color-primario, .empresa-nombre, .footer-empresa {{
                color: {primary_color} !important;
            }}
            .color-secundario, .info-label, .totales-label, .numero-cotizacion {{
                color: {secondary_color} !important;
            }}
            .totales-valor {{
                color: {primary_color} !important;
            }}
            .info-box h3 {{
                color: {primary_color} !important;
                border-bottom-color: {primary_color} !important;
            }}
            .tabla-section h2 {{
                color: {primary_color} !important;
                border-bottom-color: {primary_color} !important;
            }}
            .observaciones h3 {{
                color: {primary_color} !important;
            }}
            .observaciones li:before {{
                color: {primary_color} !important;
            }}
            .titulo-documento h1 {{
                color: {primary_color} !important;
            }}

            /* === BORDES CON COLOR === */
            .header {{
                border-bottom-color: {primary_color} !important;
            }}
            .titulo-documento {{
                border-left-color: {primary_color} !important;
                background: linear-gradient(135deg, {primary_color}15 0%, {secondary_color}25 100%) !important;
            }}
            .totales-box {{
                border-color: {primary_color} !important;
            }}
            .footer {{
                border-top-color: {primary_color} !important;
            }}
            .observaciones {{
                border-left-color: {secondary_color} !important;
            }}
            .logo-placeholder, .pili-logo {{
                border-color: {primary_color} !important;
            }}

            /* === THEAD (fondo de tabla) === */
            thead {{
                background: linear-gradient(135deg, {primary_color} 0%, {secondary_color} 100%) !important;
                color: white !important;
            }}
            thead th {{
                color: white !important;
            }}

            /* === FILA TOTAL (azul) === */
            .totales-row:last-child {{
                background: linear-gradient(135deg, {primary_color} 0%, {secondary_color} 100%) !important;
                color: white !important;
            }}
            .totales-row:last-child .totales-label,
            .totales-row:last-child .totales-valor {{
                color: white !important;
            }}

            /* === HOVER DE TABLA === */
            tbody tr:hover {{
                background-color: {primary_color}10 !important;
            }}
        </style>
        """
        
        # Inyectar el CSS antes de cerrar </head> o al inicio del body
        if "</head>" in rendered_html:
            rendered_html = rendered_html.replace("</head>", f"{style_block}</head>")
        elif "<body" in rendered_html:
            rendered_html = rendered_html.replace("<body", f"{style_block}<body")
        else:
            rendered_html = f"{style_block}{rendered_html}"
        
        # Inyectar logo si existe
        if logo_b64 and isinstance(logo_b64, str) and logo_b64.startswith("data:image"):
            # Reemplazar placeholders de logo con la imagen real
            import re
            logo_img_tag = f'<img src="{logo_b64}" alt="Logo" style="max-height: 80px; max-width: 160px; object-fit: contain;">'
            rendered_html = re.sub(r'<div[^>]*class="[^"]*logo-placeholder[^"]*"[^>]*>.*?</div>', logo_img_tag, rendered_html, flags=re.DOTALL)
            rendered_html = re.sub(r'<div[^>]*class="[^"]*pili-logo[^"]*"[^>]*>.*?</div>', logo_img_tag, rendered_html, flags=re.DOTALL)
        
        # Limpieza de placeholders residuales
        import re
        rendered_html = re.sub(r'\{\{.*?\}\}', '', rendered_html)
        rendered_html = re.sub(r'\{%.*?%\}', '', rendered_html)
        
        return {"html": rendered_html}
    except Exception as e:
        logger.error(f"Error en renderizado dinámico: {e}")
        return {"html": html_content, "error": str(e)}

from fastapi.staticfiles import StaticFiles

# Montar carpeta de salida para descargas directas
app.mount("/output", StaticFiles(directory=str(OUTPUT_DIR)), name="output")

@app.post("/api/studio/generate")
async def generate_doc(payload: dict = Body(...)):
    logger.info(f"📥 Payload recibido: {payload.keys()}")
    html_content = payload.get("html")
    format_type = payload.get("format", "word")
    name = payload.get("name", "test_doc")
    settings = payload.get("settings", {})
    
    if not html_content:
        raise HTTPException(status_code=400, detail="HTML content required")
    
    # Normalizar el nombre para usarlo como doc_type (Sincronizado con V10 Engine)
    doc_type = name.upper().replace(" ", "_")
    
    # Normalizar extensión y nombre (Sincronizado con Estándares Office)
    ext_map = {"word": "docx", "excel": "xlsx", "pdf": "pdf"}
    ext = ext_map.get(format_type.lower(), format_type.lower())
    
    filename = f"STUDIO_{doc_type}.{ext}"
    output_path = OUTPUT_DIR / filename
    
    logger.info(f"🚀 Studio Trigger: Generating {format_type} for type: {doc_type}")
    logger.info(f"📦 HTML Payload Size: {len(html_content)} characters")
    
    # 🎨 Procesar Logo Base64 → Archivo Temporal
    logo_path = None
    if settings.get("logo") and isinstance(settings["logo"], str) and settings["logo"].startswith("data:image"):
        try:
            import base64
            import tempfile
            
            # Extraer datos Base64
            logo_data = settings["logo"].split(",")[-1]
            logo_bytes = base64.b64decode(logo_data)
            
            # Crear archivo temporal
            logo_tmp = Path(tempfile.gettempdir()) / f"logo_studio_{int(datetime.now().timestamp())}.png"
            with open(logo_tmp, "wb") as f:
                f.write(logo_bytes)
            
            logo_path = str(logo_tmp)
            logger.info(f"✅ Logo extraído a: {logo_path}")
            
            # Actualizar settings con ruta de archivo
            settings["logo_path"] = logo_path
        except Exception as e:
            logger.error(f"⚠️ Error procesando logo: {e}")
    
    # Pasar doc_type y settings explícitamente a la factoría
    try:
        result = await binary_factory.generate_document(html_content, str(output_path), format_type, doc_type, options=settings)
    except Exception as e:
        logger.error(f"💥 EXC_CRITICA en studio_api: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        result = {"success": False, "error": f"Crash en ejecucion: {str(e)}"}
    
    if result.get("success"):
        logger.info(f"✅ Studio Success: {filename}")
        
        # Determinar Media Type exacto
        mime_types = {
            "word": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "pdf": "application/pdf",
            "excel": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        }
        media_type = mime_types.get(format_type.lower(), "application/octet-stream")
        
        return FileResponse(
            path=str(output_path),
            filename=filename,
            media_type=media_type,
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    else:
        error_msg = result.get('error', 'Unknown error')
        logger.error(f"❌ Studio Error generating {doc_type}: {error_msg}")
        return JSONResponse(
            status_code=500, 
            content={
                "success": False, 
                "error": error_msg,
                "detail": f"Error en Factoría SOBERANA al generar {format_type} para {doc_type}"
            }
        )

if __name__ == "__main__":
    import uvicorn
    logger.info("🎨 N04 Mirror Studio API starting on http://localhost:8005")
    uvicorn.run(app, host="0.0.0.0", port=8005)
