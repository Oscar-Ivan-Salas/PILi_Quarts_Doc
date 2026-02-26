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
        
        # Mezclar data_payload con overrides si vienen de la sesión (simulado)
        # En el Studio, el usuario espera ver sus cambios.
        content = template.render(**data_payload)
        
        # LIMPIEZA FINAL: Si después de renderizar quedan {{ }}, es que faltan keys.
        # Por seguridad, removemos tags de control restantes para una vista limpia.
        import re
        content = re.sub(r'\{\{.*?\}\}', '', content)
        content = re.sub(r'\{%.*?%\}', '', content)
        
        return {"content": content}
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
        from jinja2 import Template
        template = Template(html_content)
        
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
        
        # Enriquecer contexto de renderizado
        render_data.update({
            "MONEDA_SIMBOLO": simbolo,
            "FECHA_DOC": datetime.now().strftime("%d/%m/%Y"),
            "TITULO_DOCUMENTO": render_data.get("PROYECTO_NOMBRE", "DOCUMENTO"),
            "SUBTOTAL": render_data.get("SUBTOTAL", 0),
            "IGV": render_data.get("IGV", 0),
            "TOTAL": render_data.get("TOTAL", 0),
            "items": render_data.get("items", [
                {"item": "01", "descripcion": "Servicio de Ingeniería N04", "cantidad": 1, "unidad": "und", "precio_unitario": 1500, "total": 1500}
            ]),
            # ADN Visual para templates que lo usen directamente
            "PRIMARY_COLOR": primary_color,
            "SECONDARY_COLOR": secondary_color,
            "FONT_FAMILY": font_family,
            "FONT_SIZE": font_size,
            "LOGO_URL": logo_b64
        })
        
        rendered_html = template.render(**render_data)
        
        # INYECCIÓN CSS ADN VISUAL - Para que la vista previa refleje la personalización
        style_block = f"""
        <style id="adn-visual-preview">
            :root {{
                --pili-primary: {primary_color};
                --pili-secondary: {secondary_color};
                --pili-font: "{font_family}", sans-serif;
                --pili-font-size: {font_size}pt;
            }}
            * {{
                font-family: var(--pili-font) !important;
                font-size: var(--pili-font-size) !important;
            }}
            body {{ 
                font-family: var(--pili-font) !important; 
                font-size: var(--pili-font-size) !important;
                color: #333;
            }}
            h1, h2, h3, h4, h5, h6,
            .color-primario, .empresa-nombre, .cotizacion-titulo, .titulo-documento,
            .title, .subtitle, .header-text, .totales-label, 
            .header, .info-box h3, .tabla-section h2 {{ 
                color: var(--pili-primary) !important; 
            }}
            .color-secundario, .text-secondary, .info-card-label {{ 
                color: var(--pili-secondary) !important; 
            }}
            thead, th, .fase-numero, .fase-duracion,
            .totales-row:last-child, .header-main, .bg-primario,
            .header, .info-box, .titulo-documento {{ 
                background-color: var(--pili-primary) !important; 
                color: white !important;
            }}
            .border-primario, table, th, td, .info-card, .recurso-card,
            .header, .info-box h3, .titulo-documento, .tabla-section h2 {{ 
                border-color: var(--pili-primary) !important; 
            }}
            /* Asegurar que tablas y celdas hereden colores */
            table {{ border-color: var(--pili-primary) !important; }}
            th {{ 
                background-color: var(--pili-primary) !important; 
                color: white !important;
                border-color: var(--pili-primary) !important;
            }}
            td {{ border-color: var(--pili-primary) !important; }}
            /* Logo placeholder */
            .logo-placeholder, .pili-logo {{
                background: #f8fafc !important;
                border: 2px dashed var(--pili-primary) !important;
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
    logger.info("🎨 N04 Mirror Studio API starting on http://localhost:8006")
    uvicorn.run(app, host="0.0.0.0", port=8006)
