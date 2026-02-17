import json
import os
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from pydantic import BaseModel

# Import N08 Identity DB
from modules.N08_User_Management.identity_db import SessionLocal, UsuarioEjecutor, ClienteFinal, ProyectoActivo

router = APIRouter(prefix="/api/admin", tags=["admin"])


# Path to persistent settings
SETTINGS_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "storage", "settings.json")

class ToggleRequest(BaseModel):
    id: str
    estado: bool

# Helper to read/write settings
def load_settings():
    if not os.path.exists(SETTINGS_PATH):
        # Create default settings if not exists
        default = {
            "services": [
                {"id": "doc_gen", "nombre": "Generación de Documentos", "estado": True, "descripcion": "Motor principal de creación de Word y PDF"},
                {"id": "pili_brain", "nombre": "PILI Brain (AI)", "estado": True, "descripcion": "Análisis inteligente y extracción de datos"},
                {"id": "database", "nombre": "Conexión Base de Datos", "estado": True, "descripcion": "Acceso a N08 Identity"},
                {"id": "previsualizacion", "nombre": "Modo Previsualización", "estado": True, "descripcion": "Renderizado HTML en tiempo real"}
            ],
            "features": [
                {"id": "advanced_metrics", "nombre": "Métricas Avanzadas", "estado": True},
                {"id": "auto_save", "nombre": "Auto-guardado", "estado": True},
                {"id": "notifications", "nombre": "Notificaciones Push", "estado": False}
            ]
        }
        os.makedirs(os.path.dirname(SETTINGS_PATH), exist_ok=True)
        with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
            json.dump(default, f, indent=2)
        return default
    
    with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_settings(settings):
    with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=2)

# Dependency
def get_identity_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/dashboard")
async def get_dashboard_metrics(db: Session = Depends(get_identity_db)):
    """
    Get comprehensive dashboard metrics and system settings
    """
    try:
        settings = load_settings()
        
        # User metrics
        total_users = db.query(UsuarioEjecutor).count()
        admin_users = 1 
        regular_users = total_users
        active_users = total_users
        
        # Client metrics
        total_clients = db.query(ClienteFinal).count()
        active_clients = total_clients
        
        # Industries
        industries = db.query(
            ProyectoActivo.industry_sector,
            func.count(ProyectoActivo.id).label('count')
        ).group_by(ProyectoActivo.industry_sector).order_by(desc('count')).limit(5).all()
        
        # Project metrics
        total_projects = db.query(ProyectoActivo).count()
        
        # Status mapping
        projects_by_status = {}
        db_statuses = db.query(ProyectoActivo.status, func.count(ProyectoActivo.id)).group_by(ProyectoActivo.status).all()
        for s, c in db_statuses:
            if s:
                key = s.lower()
                projects_by_status[key] = c
            
        for k in ['draft', 'pending_review', 'approved', 'sent', 'generated']:
            if k not in projects_by_status:
                projects_by_status[k] = 0
        
        # Mock financial
        total_value = total_projects * 5250.50 
        avg_project_value = 5250.50 if total_projects > 0 else 0
        
        # Priority distribution (mock)
        high_priority = int(total_projects * 0.2)
        normal_priority = int(total_projects * 0.6)
        low_priority = total_projects - high_priority - normal_priority
        
        # Recent activity
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        recent_count = db.query(ProyectoActivo).filter(
            ProyectoActivo.created_at >= seven_days_ago
        ).count()
        
        # Document types
        doc_type_names = {
            1: "Cotización Simple", 2: "Cotización Compleja", 3: "Cuadro Cargas",
            4: "Memoria Descriptiva", 5: "Protocolo Pruebas", 6: "Informe Levantamiento",
            7: "Presupuesto Base", 8: "Cronograma", 9: "Esp. Técnicas", 10: "Plan Seguridad"
        }
        
        doc_type_stats = []
        db_doc_stats = db.query(ProyectoActivo.document_type_id, func.count(ProyectoActivo.id)).group_by(ProyectoActivo.document_type_id).all()
        for did, count in db_doc_stats:
            doc_type_stats.append({
                "id": str(did),
                "nombre": doc_type_names.get(did, f"Doc {did}"),
                "count": count
            })
        
        # Top clients
        top_clients_db = db.query(
            ClienteFinal.razon_social,
            func.count(ProyectoActivo.id).label('project_count')
        ).join(ProyectoActivo).group_by(ClienteFinal.id).order_by(desc('project_count')).limit(10).all()
        
        top_clients_formatted = []
        for tc in top_clients_db:
            top_clients_formatted.append({
                "razon_social": tc[0],
                "total_value": tc[1] * 5250.50,
                "project_count": tc[1]
            })
        
        # Recent projects list
        recent_projects_list = db.query(ProyectoActivo).order_by(desc(ProyectoActivo.created_at)).limit(10).all()
        recent_projects_data = []
        for p in recent_projects_list:
            client = db.query(ClienteFinal).filter(ClienteFinal.id == p.cliente_id).first()
            recent_projects_data.append({
                "id": str(p.id),
                "nombre": p.project_code,
                "client_name": client.razon_social if client else "N/A",
                "total": 5250.50,
                "estado": p.status.lower() if p.status else "draft",
                "created_at": p.created_at.isoformat() if p.created_at else None
            })
        
        return {
            "success": True,
            "timestamp": datetime.now().isoformat(),
            "settings": settings,
            "metrics": {
                "users": {
                    "total": total_users,
                    "admins": admin_users,
                    "regular": regular_users,
                    "active": active_users
                },
                "clients": {
                    "total": total_clients,
                    "active": active_clients,
                    "top_industries": [{"industria": i[0] or "Otros", "count": i[1]} for i in industries]
                },
                "projects": {
                    "total": total_projects,
                    "by_status": projects_by_status,
                    "by_priority": {
                        "high": high_priority,
                        "normal": normal_priority,
                        "low": low_priority
                    },
                    "recent_7_days": recent_count
                },
                "financial": {
                    "total_value": float(total_value),
                    "avg_project_value": float(avg_project_value),
                    "currency": "PEN"
                },
                "document_types": doc_type_stats,
                "price_references": {
                    "total": 1250,
                    "active": 1250,
                    "categories": []
                }
            },
            "top_clients": top_clients_formatted,
            "recent_projects": recent_projects_data
        }
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/toggle-service")
async def toggle_service(req: ToggleRequest):
    settings = load_settings()
    updated = False
    for s in settings["services"]:
        if s["id"] == req.id:
            s["estado"] = req.estado
            updated = True
            break
    
    if not updated:
        raise HTTPException(status_code=404, detail="Service not found")
    
    save_settings(settings)
    return {"success": True, "message": f"Service {req.id} updated"}

@router.post("/toggle-feature")
async def toggle_feature(req: ToggleRequest):
    settings = load_settings()
    updated = False
    for f in settings["features"]:
        if f["id"] == req.id:
            f["estado"] = req.estado
            updated = True
            break
    
    if not updated:
        raise HTTPException(status_code=404, detail="Feature not found")
    
    save_settings(settings)
    return {"success": True, "message": f"Feature {req.id} updated"}
