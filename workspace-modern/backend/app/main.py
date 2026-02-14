from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import pili, generation
from modules.pili.api.router import router as pili_v2_router

app = FastAPI(title="PILi_Quarts Workspace API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3010", "http://127.0.0.1:3010"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pili.router)
app.include_router(generation.router)
app.include_router(pili_v2_router)
# Include Document Router (Removed - see modules/documents)
# from routers import documents
# app.include_router(documents.router)
# Include Admin Dashboard Router
from modules.pili.api.admin_router import router as admin_router
app.include_router(admin_router)

# Include Unified Documents Router
from modules.documents.api.router import router as documents_unified_router
app.include_router(documents_unified_router)

@app.get("/")
def read_root():
    return {"message": "PILi_Quarts Workspace API", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "workspace-api"}
