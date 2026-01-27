"""
═══════════════════════════════════════════════════════════════════════════════
🎯 ROUTER PILI V4.0 - PATRÓN CAJA NEGRA
═══════════════════════════════════════════════════════════════════════════════
Router unificado para todos los servicios PILI
Máximo 60 líneas de código (vs 4,635 actuales = 99% reducción)

Patrón:
    Request → Detectar servicio → Caja Negra → Response

Cada servicio es una caja negra auto-contenida.
═══════════════════════════════════════════════════════════════════════════════
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import logging

from .services import SERVICIOS

# Configurar logging
logger = logging.getLogger(__name__)

# Crear router
router = APIRouter(
    prefix="/api/pili",
    tags=["PILI Blackbox"]
)

# ═══════════════════════════════════════════════════════════════════════════
# 📊 MODELOS DE REQUEST/RESPONSE
# ═══════════════════════════════════════════════════════════════════════════

class ChatRequest(BaseModel):
    """Request para chat PILI"""
    mensaje: str
    servicio: Optional[str] = None  # Si es None, detecta automático
    historial: List[Dict[str, Any]] = []

class ChatResponse(BaseModel):
    """Response de chat PILI"""
    exito: bool
    respuesta: str
    datos: Dict[str, Any]
    servicio_detectado: str
    botones: Optional[List[Dict[str, str]]] = None
    progreso: Optional[str] = None

# ═══════════════════════════════════════════════════════════════════════════
# 🚀 ENDPOINT PRINCIPAL
# ═══════════════════════════════════════════════════════════════════════════

@router.post("/chat", response_model=ChatResponse)
async def chat_pili(request: ChatRequest):
    """
    Endpoint único para TODO PILI
    Patrón Caja Negra aplicado

    FLUJO:
    1. Detectar servicio (si no viene explícito)
    2. Obtener handler del servicio
    3. Procesar mensaje (CAJA NEGRA)
    4. Retornar resultado
    """
    try:
        # 1. Detectar servicio si no viene explícito
        servicio = request.servicio or detectar_servicio(request.mensaje)

        # 2. Validar que el servicio existe
        if servicio not in SERVICIOS:
            logger.warning(f"Servicio no válido: {servicio}")
            raise HTTPException(
                status_code=400,
                detail=f"Servicio '{servicio}' no disponible. Servicios válidos: {list(SERVICIOS.keys())}"
            )

        # 3. Obtener handler del servicio (Caja Negra)
        HandlerClass = SERVICIOS[servicio]
        handler = HandlerClass()

        # 4. Procesar mensaje (TODO sucede en la caja negra)
        resultado = handler.procesar(
            mensaje=request.mensaje,
            historial=request.historial
        )

        # 5. Retornar respuesta estructurada
        return ChatResponse(
            exito=True,
            respuesta=resultado.get("respuesta", ""),
            datos=resultado.get("datos", {}),
            servicio_detectado=servicio,
            botones=resultado.get("botones"),
            progreso=resultado.get("progreso")
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error en chat PILI: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error interno del servidor: {str(e)}"
        )

# ═══════════════════════════════════════════════════════════════════════════
# 🔍 DETECCIÓN DE SERVICIO
# ═══════════════════════════════════════════════════════════════════════════

def detectar_servicio(mensaje: str) -> str:
    """
    Detecta servicio automáticamente del mensaje
    Simple keyword matching (puede mejorarse con ML)
    """
    mensaje_lower = mensaje.lower()

    # Keywords por servicio
    keywords_servicios = {
        "itse": ["itse", "certificado", "inspeccion", "seguridad"],
        # Próximos servicios:
        # "electricidad": ["electricidad", "electrico", "instalacion"],
        # "pozo-tierra": ["pozo", "tierra", "puesta a tierra"],
        # "contraincendios": ["incendio", "contraincendios", "extintor"],
    }

    for servicio, keywords in keywords_servicios.items():
        if any(kw in mensaje_lower for kw in keywords):
            return servicio

    # Default: ITSE (servicio más común)
    return "itse"
