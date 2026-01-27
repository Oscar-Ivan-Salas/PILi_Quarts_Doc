
from fastapi import FastAPI, HTTPException, UploadFile, File, Body, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
from pathlib import Path
import uvicorn
from typing import List, Optional, Dict, Any
import logging
import json
from datetime import datetime
import sys

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import Configuration
try:
    from app.core.config import settings, validate_gemini_key, get_gemini_api_key
    from app.services.gemini_service import gemini_service
    TIENE_GEMINI_SERVICE = True
except ImportError as e:
    logger.error(f"Error loading core services: {e}")
    TIENE_GEMINI_SERVICE = False

# Import pydantic models
from pydantic import BaseModel

class ChatRequest(BaseModel):
    tipo_flujo: str
    mensaje: str
    historial: List[dict] = []
    contexto_adicional: str = ""
    archivos_procesados: List[dict] = []
    generar_html: bool = True

# ═══════════════════════════════════════════════════════════════
# CREATE FASTAPI APP
# ═══════════════════════════════════════════════════════════════

app = FastAPI(
    title="PILI_Quarts API",
    description="Professional AI Document Generation System",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# ═══════════════════════════════════════════════════════════════
# CORS CONFIGURATION
# ═══════════════════════════════════════════════════════════════

origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://localhost:3005",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:3001",
    "http://127.0.0.1:3005",
    # Add other origins as needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ═══════════════════════════════════════════════════════════════
# STATIC FILES
# ═══════════════════════════════════════════════════════════════

static_path = Path(__file__).parent.parent / "static"
if not static_path.exists():
    static_path.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

# ═══════════════════════════════════════════════════════════════
# ROUTER REGISTRATION
# ═══════════════════════════════════════════════════════════════

# Import Routers (Direct Imports - No "Try/Except" masking)
from app.routers import chat
from app.routers import cotizaciones
from app.routers import proyectos
from app.routers import informes
from app.routers import documentos
from app.routers import system
from app.routers import generar_directo
from app.routers import clientes
from app.routers import admin
from app.routers import calculos
from app.routers import templates

# Include Routers
app.include_router(chat.router, prefix="/api/chat", tags=["Chat PILI"])
app.include_router(cotizaciones.router, prefix="/api/cotizaciones", tags=["Cotizaciones"])
app.include_router(proyectos.router, prefix="/api/proyectos", tags=["Proyectos"])
app.include_router(informes.router, prefix="/api/informes", tags=["Informes"])
app.include_router(documentos.router, prefix="/api/documentos", tags=["Documentos"])
app.include_router(system.router, prefix="/api/system", tags=["Sistema"])
app.include_router(generar_directo.router, prefix="/api", tags=["Generación Directa"])
app.include_router(clientes.router, prefix="/api/clientes", tags=["Clientes"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])
app.include_router(calculos.router, prefix="/api/calculos", tags=["Calculos"])
app.include_router(templates.router, prefix="/api/templates", tags=["Templates"])

logger.info("✅ All routers registered successfully.")

# ═══════════════════════════════════════════════════════════════
# ROOT ENDPOINT
# ═══════════════════════════════════════════════════════════════

@app.get("/")
async def root():
    return {
        "message": "PILI_Quarts API v1.0",
        "status": "running",
        "timestamp": datetime.now().isoformat(),
        "docs": "/docs"
    }

# ═══════════════════════════════════════════════════════════════
# DIRECTORIES
# ═══════════════════════════════════════════════════════════════

try:
    from app.core.config import get_generated_directory, get_upload_directory
    storage_path = get_generated_directory()
    upload_path = get_upload_directory()
except:
    storage_path = Path("./backend/storage/generados")
    upload_path = Path("./backend/storage/documentos")
    storage_path.mkdir(parents=True, exist_ok=True)
    upload_path.mkdir(parents=True, exist_ok=True)

# ═══════════════════════════════════════════════════════════════
# UPLOAD ENDPOINT
# ═══════════════════════════════════════════════════════════════

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        file_path = upload_path / file.filename
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)
        
        return {
            "success": True,
            "filename": file.filename,
            "path": str(file_path)
        }
    except Exception as e:
        logger.error(f"Error uploading file: {e}")
        raise HTTPException(status_code=500, detail=str(e))
