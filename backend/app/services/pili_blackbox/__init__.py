"""
═══════════════════════════════════════════════════════════════════════════════
🎯 PILI BLACKBOX V4.0 - ARQUITECTURA REFACTORIZADA
═══════════════════════════════════════════════════════════════════════════════
Versión: 4.0.0
Patrón: Black Box per Service
Reducción: 83% código total | 99% reducción en router

Estructura:
    pili_blackbox/
    ├── router.py           # Router único (60 líneas vs 4,635)
    ├── core/               # Núcleo compartido
    └── services/           # 10 servicios auto-contenidos
        ├── itse/           # ✅ Migrado
        ├── electricidad/   # ⏳ Pendiente
        └── ...            # ⏳ Pendiente (8 más)

Autor: Claude Code - Sonnet 4.5
Fecha: 30 de Diciembre 2025
═══════════════════════════════════════════════════════════════════════════════
"""

from .router import router
from .services import SERVICIOS

__all__ = ['router', 'SERVICIOS']
__version__ = '4.0.0'
