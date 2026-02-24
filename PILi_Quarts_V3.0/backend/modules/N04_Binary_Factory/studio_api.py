import os
import logging
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

app = FastAPI(title="N04 Mirror Studio API")

# Habilitar CORS para desarrollo local (Vite suele estar en port 5173)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
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

jinja_env.filters['format_currency'] = format_currency

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
        # Renderizado de prueba (Mock Data para el visor)
        template = jinja_env.get_template(template_file)
        content = template.render(
            TITULO_DOCUMENTO=name.replace("_", " "),
            SUBTITULO_DOCUMENTO="Servicios de Ingeniería Especializada",
            CODIGO_DOC="N04-STUDIO-2026",
            FECHA_DOC="23/02/2026",
            NOMBRE_EMISOR="EMPRESA SOBERANA S.A.C.",
            RUC_EMISOR="20601234567",
            DIRECCION_EMISOR="Av. Independencia 04, Lima",
            EMAIL_EMISOR="contacto@soberana.com",
            TELEFONO_EMISOR="999 000 000",
            CLIENTE_NOMBRE="INDUSTRIAL SOLUTIONS PERÚ",
            CLIENTE_RUC="20555666777",
            CLIENTE_DIRECCION="Calle Las Begonias 123, San Isidro",
            CLIENTE_EMAIL="proyectos@industrial.pe",
            PROYECTO_NOMBRE="SISTEMA DE CONTROL N04",
            VIGENCIA="15 días",
            MONEDA_SIMBOLO="S/",
            MONEDA_NOMBRE="SOLES",
            SUBTOTAL=1000.0,
            IGV=180.0,
            TOTAL=1180.0,
            DURACION="15",
            suministros=[
                {
                    "item": "01", 
                    "descripcion": "Módulo de Control Soberano N04", 
                    "cantidad": 1, 
                    "unidad": "und",
                    "precioUnitario": 1000, 
                    "precioTotal": 1000,
                    "notas": "Incluye licencia de uso perpetua"
                }
            ],
            entregables=[
                "Acta de Constitución del Proyecto",
                "Certificado de Operatividad N04",
                "Plan de Pruebas de Fidelidad"
            ],
            fases_pmi=[
                {"nombre": "Análisis", "descripcion": "Levantamiento de requerimientos"},
                {"nombre": "Diseño", "descripcion": "Creación de arquitectura Oro"},
                {"nombre": "Ejecución", "descripcion": "Implementación del módulo N04"}
            ]
        )
        return {"content": content}
    except Exception as e:
        logger.error(f"Error rendering template {name}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/studio/generate")
async def generate_doc(payload: dict = Body(...)):
    html_content = payload.get("html")
    format_type = payload.get("format", "word")
    name = payload.get("name", "test_doc")
    
    if not html_content:
        raise HTTPException(status_code=400, detail="HTML content required")
    
    ext = "docx" if format_type == "word" else format_type
    filename = f"STUDIO_{name}.{ext}"
    output_path = OUTPUT_DIR / filename
    
    logger.info(f"🚀 Studio Trigger: Generating {format_type} for {name}")
    result = binary_factory.generate_document(html_content, str(output_path), format_type)
    
    if result.get("success"):
        return FileResponse(
            path=str(output_path),
            filename=filename,
            media_type="application/octet-stream"
        )
    else:
        logger.error(f"❌ Studio Error: {result.get('error')}")
        return JSONResponse(status_code=500, content=result)

if __name__ == "__main__":
    import uvicorn
    logger.info("🎨 N04 Mirror Studio API starting on http://localhost:8004")
    uvicorn.run(app, host="0.0.0.0", port=8004)
