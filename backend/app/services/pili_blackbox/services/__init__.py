"""
═══════════════════════════════════════════════════════════════════════════════
🎯 REGISTRO DE SERVICIOS PILI - AUTO-DISCOVERY
═══════════════════════════════════════════════════════════════════════════════
Cada servicio se auto-registra aquí
Patrón: Black Box per Service
═══════════════════════════════════════════════════════════════════════════════
"""

from .itse import ITSEChatPili

# ═══════════════════════════════════════════════════════════════════════════
# 📋 REGISTRO DE SERVICIOS (Auto-Discovery Pattern)
# ═══════════════════════════════════════════════════════════════════════════
SERVICIOS = {
    "itse": ITSEChatPili,
    # Próximos servicios a migrar:
    # "electricidad": ElectricidadChatPili,
    # "pozo-tierra": PozoTierraChatPili,
    # "contraincendios": ContraincendiosChatPili,
    # "domotica": DomoticaChatPili,
    # "cctv": CCTVChatPili,
    # "redes": RedesChatPili,
    # "automatizacion": AutomatizacionChatPili,
    # "expedientes": ExpedientesChatPili,
    # "saneamiento": SaneamientoChatPili,
}

__all__ = ['SERVICIOS']
