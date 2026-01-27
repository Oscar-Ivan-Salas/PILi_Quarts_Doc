"""
Router Admin - Panel de administración
Endpoints para dashboard, métricas y configuración de servicios
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Dict, Any
import secrets
import logging

from app.core.database import get_db
from app.core.features import (
    FeatureFlags,
    SERVICIOS_CONFIG,
    get_servicios_habilitados,
    toggle_servicio
)
from app.models.usuario import Usuario
from app.models.cotizacion import Cotizacion
from app.models.proyecto import Proyecto
from app.services.token_manager import TokenManager

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/admin",
    tags=["Admin"]
)

security = HTTPBasic()

# Credenciales de administrador (desarrollo)
ADMIN_USERNAME = "Admin"
ADMIN_PASSWORD = "Admin1234"


def verificar_admin(credentials: HTTPBasicCredentials = Depends(security)):
    """Verificar credenciales de administrador"""
    correct_username = secrets.compare_digest(credentials.username, ADMIN_USERNAME)
    correct_password = secrets.compare_digest(credentials.password, ADMIN_PASSWORD)

    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@router.get("/dashboard")
async def get_dashboard(
    db: Session = Depends(get_db),
    admin: str = Depends(verificar_admin)
):
    """
    Obtiene todas las métricas del dashboard

    Requiere autenticación básica: Admin/Admin1234
    """
    try:
        # Métricas de usuarios
        total_usuarios = db.query(Usuario).count()
        usuarios_free = db.query(Usuario).filter(Usuario.plan == "free").count()
        usuarios_pro = db.query(Usuario).filter(Usuario.plan == "pro").count()
        usuarios_enterprise = db.query(Usuario).filter(Usuario.plan == "enterprise").count()

        # Métricas de cotizaciones
        total_cotizaciones = db.query(Cotizacion).count()

        # Métricas de proyectos
        total_proyectos = db.query(Proyecto).count()

        # Métricas de tokens (si está habilitado)
        token_manager = TokenManager(db)
        estadisticas_tokens = token_manager.get_estadisticas_globales()

        # Ingresos estimados
        ingresos_mensuales = (usuarios_pro * 29.99) + (usuarios_enterprise * 299)

        # Feature flags
        features = FeatureFlags.get_all_flags()

        # Servicios habilitados
        servicios = SERVICIOS_CONFIG

        # Actividad reciente (últimas cotizaciones)
        from datetime import datetime, timedelta
        hace_24h = datetime.utcnow() - timedelta(hours=24)

        cotizaciones_hoy = db.query(Cotizacion).filter(
            Cotizacion.fecha_creacion >= hace_24h
        ).count()

        return {
            "exito": True,
            "metricas": {
                "usuarios": {
                    "total": total_usuarios,
                    "free": usuarios_free,
                    "pro": usuarios_pro,
                    "enterprise": usuarios_enterprise,
                    "distribucion": {
                        "free": round((usuarios_free / total_usuarios * 100), 1) if total_usuarios > 0 else 0,
                        "pro": round((usuarios_pro / total_usuarios * 100), 1) if total_usuarios > 0 else 0,
                        "enterprise": round((usuarios_enterprise / total_usuarios * 100), 1) if total_usuarios > 0 else 0
                    }
                },
                "documentos": {
                    "total": total_cotizaciones,
                    "hoy": cotizaciones_hoy,
                    "cambio_24h": "+34%"  # TODO: calcular real
                },
                "proyectos": {
                    "total": total_proyectos,
                    "activos": total_proyectos  # TODO: filtrar por estado
                },
                "tokens": estadisticas_tokens,
                "ingresos": {
                    "mensual": round(ingresos_mensuales, 2),
                    "anual_estimado": round(ingresos_mensuales * 12, 2)
                }
            },
            "features": features,
            "servicios": servicios,
            "timestamp": datetime.utcnow().isoformat()
        }

    except Exception as e:
        logger.error(f"❌ Error en dashboard: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/usuarios")
async def get_usuarios(
    db: Session = Depends(get_db),
    admin: str = Depends(verificar_admin),
    limit: int = 50,
    offset: int = 0
):
    """Lista todos los usuarios con paginación"""
    try:
        usuarios = db.query(Usuario).offset(offset).limit(limit).all()
        total = db.query(Usuario).count()

        return {
            "exito": True,
            "total": total,
            "usuarios": [
                {
                    "id": u.id,
                    "nombre": f"{u.nombre} {u.apellido}",
                    "email": u.email,
                    "empresa": u.empresa,
                    "plan": u.plan,
                    "tokens_disponibles": u.tokens_disponibles(),
                    "activo": u.activo,
                    "ultimo_acceso": u.ultimo_acceso.isoformat() if u.ultimo_acceso else None
                }
                for u in usuarios
            ]
        }
    except Exception as e:
        logger.error(f"❌ Error al listar usuarios: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/toggle-servicio/{servicio_id}")
async def toggle_servicio_endpoint(
    servicio_id: str,
    admin: str = Depends(verificar_admin)
):
    """Habilita/deshabilita un servicio"""
    try:
        nuevo_estado = toggle_servicio(servicio_id)

        logger.info(f"🔄 Servicio '{servicio_id}' cambiado a: {'ON' if nuevo_estado else 'OFF'} por admin")

        return {
            "exito": True,
            "servicio": servicio_id,
            "habilitado": nuevo_estado,
            "mensaje": f"Servicio {'habilitado' if nuevo_estado else 'deshabilitado'} exitosamente"
        }
    except Exception as e:
        logger.error(f"❌ Error al toggle servicio: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/actividad-reciente")
async def get_actividad_reciente(
    db: Session = Depends(get_db),
    admin: str = Depends(verificar_admin),
    limit: int = 10
):
    """Obtiene actividad reciente del sistema"""
    try:
        # Últimas cotizaciones
        cotizaciones = db.query(Cotizacion).order_by(
            Cotizacion.fecha_creacion.desc()
        ).limit(limit).all()

        actividad = []
        for cot in cotizaciones:
            actividad.append({
                "tipo": "cotizacion",
                "mensaje": f"Cotización {cot.numero} creada para {cot.cliente}",
                "timestamp": cot.fecha_creacion.isoformat(),
                "usuario": "Usuario demo"  # TODO: relacionar con usuario real
            })

        return {
            "exito": True,
            "actividad": actividad
        }

    except Exception as e:
        logger.error(f"❌ Error en actividad reciente: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/estadisticas/tokens")
async def get_estadisticas_tokens(
    db: Session = Depends(get_db),
    admin: str = Depends(verificar_admin)
):
    """Obtiene estadísticas detalladas de tokens"""
    try:
        token_manager = TokenManager(db)
        stats = token_manager.get_estadisticas_globales()

        return {
            "exito": True,
            "estadisticas": stats
        }
    except Exception as e:
        logger.error(f"❌ Error en estadísticas de tokens: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/toggle-feature/{feature_name}")
async def toggle_feature(
    feature_name: str,
    admin: str = Depends(verificar_admin)
):
    """
    Habilita/deshabilita una feature flag

    NOTA: En desarrollo cambia el estado en memoria.
    En producción debería actualizar el archivo .env
    """
    try:
        feature_upper = feature_name.upper()

        if not hasattr(FeatureFlags, feature_upper):
            raise HTTPException(status_code=404, detail="Feature no encontrada")

        # En desarrollo, cambiar el atributo de clase
        # NOTA: Esto solo funciona en la sesión actual
        # Para persistencia real, modificar .env
        current_value = getattr(FeatureFlags, feature_upper)
        setattr(FeatureFlags, feature_upper, not current_value)
        new_value = getattr(FeatureFlags, feature_upper)

        logger.warning(
            f"⚠️ Feature '{feature_name}' cambiada a: {'ON' if new_value else 'OFF'} "
            f"(solo en memoria - reiniciar backend perderá el cambio)"
        )

        return {
            "exito": True,
            "feature": feature_name,
            "habilitado": new_value,
            "mensaje": f"Feature {'habilitada' if new_value else 'deshabilitada'}",
            "advertencia": "Cambio solo en memoria. Modificar .env para persistencia."
        }

    except Exception as e:
        logger.error(f"❌ Error al toggle feature: {e}")
        raise HTTPException(status_code=500, detail=str(e))
