"""
Sistema de Feature Flags para Tesla Cotizador V3.0
Permite habilitar/deshabilitar funcionalidades sin tocar código
"""
import os
from typing import Dict, Any


class FeatureFlags:
    """
    Feature Flags para control de funcionalidades
    Se configura desde .env con variables FEATURE_*
    """

    # ========== FUNCIONALIDADES AVANZADAS ==========
    TOKEN_MANAGER = os.getenv("FEATURE_TOKEN_MANAGER", "False").lower() == "true"
    MULTI_IA = os.getenv("FEATURE_MULTI_IA", "False").lower() == "true"
    MULTI_AGENT = os.getenv("FEATURE_MULTI_AGENT", "False").lower() == "true"
    AUTH_USUARIOS = os.getenv("FEATURE_AUTH_USUARIOS", "False").lower() == "true"
    RATE_LIMIT = os.getenv("FEATURE_RATE_LIMIT", "False").lower() == "true"
    ANALYTICS = os.getenv("FEATURE_ANALYTICS", "False").lower() == "true"

    # ========== FUNCIONALIDADES BÁSICAS (Siempre ON) ==========
    DOCUMENTOS = True  # Generación de documentos
    CHAT_PILI = True   # Chat conversacional
    ADMIN_PANEL = True # Panel de administrador

    @classmethod
    def is_enabled(cls, feature: str) -> bool:
        """Verifica si una feature está habilitada"""
        return getattr(cls, feature.upper(), False)

    @classmethod
    def get_all_flags(cls) -> Dict[str, Any]:
        """Retorna todas las feature flags y su estado"""
        return {
            "token_manager": cls.TOKEN_MANAGER,
            "multi_ia": cls.MULTI_IA,
            "multi_agent": cls.MULTI_AGENT,
            "auth_usuarios": cls.AUTH_USUARIOS,
            "rate_limit": cls.RATE_LIMIT,
            "analytics": cls.ANALYTICS,
            "documentos": cls.DOCUMENTOS,
            "chat_pili": cls.CHAT_PILI,
            "admin_panel": cls.ADMIN_PANEL,
        }

    @classmethod
    def get_status_display(cls) -> str:
        """Retorna un string legible del estado de features"""
        flags = cls.get_all_flags()
        status = []
        for name, enabled in flags.items():
            emoji = "🟢" if enabled else "🔴"
            state = "ON" if enabled else "OFF"
            status.append(f"{emoji} {name}: {state}")
        return "\n".join(status)


# Configuración de servicios disponibles
SERVICIOS_CONFIG = {
    "electrico-residencial": {
        "id": "electrico-residencial",
        "nombre": "Eléctrico Residencial",
        "emoji": "⚡",
        "habilitado": True,
        "descripcion": "Instalaciones eléctricas residenciales",
        "icono": "Zap",
        "color": "#3B82F6"
    },
    "electrico-comercial": {
        "id": "electrico-comercial",
        "nombre": "Eléctrico Comercial",
        "emoji": "🏢",
        "habilitado": True,
        "descripcion": "Instalaciones eléctricas comerciales",
        "icono": "Building2",
        "color": "#0052A3"
    },
    "electrico-industrial": {
        "id": "electrico-industrial",
        "nombre": "Eléctrico Industrial",
        "emoji": "🏭",
        "habilitado": True,
        "descripcion": "Instalaciones eléctricas industriales",
        "icono": "Factory",
        "color": "#1E40AF"
    },
    "contraincendios": {
        "id": "contraincendios",
        "nombre": "Contraincendios",
        "emoji": "🔥",
        "habilitado": True,
        "descripcion": "Sistemas contra incendios",
        "icono": "Flame",
        "color": "#DC2626"
    },
    "domotica": {
        "id": "domotica",
        "nombre": "Domótica",
        "emoji": "🏠",
        "habilitado": True,
        "descripcion": "Sistemas de automatización",
        "icono": "Home",
        "color": "#22C55E"
    },
    "itse": {
        "id": "itse",
        "nombre": "ITSE",
        "emoji": "📋",
        "habilitado": True,
        "descripcion": "Certificados ITSE",
        "icono": "ClipboardCheck",
        "color": "#F59E0B"
    },
    "pozo-tierra": {
        "id": "pozo-tierra",
        "nombre": "Pozo a Tierra",
        "emoji": "🔌",
        "habilitado": True,
        "descripcion": "Sistemas de puesta a tierra",
        "icono": "Plug",
        "color": "#8B5CF6"
    },
    "redes-cctv": {
        "id": "redes-cctv",
        "nombre": "Redes y CCTV",
        "emoji": "📹",
        "habilitado": True,
        "descripcion": "Redes de datos y CCTV",
        "icono": "Camera",
        "color": "#EC4899"
    },
    "expedientes": {
        "id": "expedientes",
        "nombre": "Expedientes Técnicos",
        "emoji": "📐",
        "habilitado": True,
        "descripcion": "Expedientes técnicos completos",
        "icono": "FileText",
        "color": "#14B8A6"
    },
    "saneamiento": {
        "id": "saneamiento",
        "nombre": "Saneamiento",
        "emoji": "💧",
        "habilitado": True,
        "descripcion": "Proyectos de saneamiento",
        "icono": "Droplet",
        "color": "#06B6D4"
    }
}


def get_servicios_habilitados():
    """Retorna solo los servicios habilitados"""
    return {
        key: value
        for key, value in SERVICIOS_CONFIG.items()
        if value["habilitado"]
    }


def is_servicio_habilitado(servicio_id: str) -> bool:
    """Verifica si un servicio está habilitado"""
    servicio = SERVICIOS_CONFIG.get(servicio_id)
    return servicio["habilitado"] if servicio else False


def toggle_servicio(servicio_id: str) -> bool:
    """Habilita/deshabilita un servicio. Retorna nuevo estado."""
    if servicio_id in SERVICIOS_CONFIG:
        SERVICIOS_CONFIG[servicio_id]["habilitado"] = not SERVICIOS_CONFIG[servicio_id]["habilitado"]
        return SERVICIOS_CONFIG[servicio_id]["habilitado"]
    return False
