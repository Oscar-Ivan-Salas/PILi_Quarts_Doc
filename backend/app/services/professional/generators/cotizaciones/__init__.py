"""
Generadores de Cotizaciones
"""
from .simple import generar_cotizacion_simple
from .compleja import generar_cotizacion_compleja

__all__ = [
    'generar_cotizacion_simple',
    'generar_cotizacion_compleja'
]
