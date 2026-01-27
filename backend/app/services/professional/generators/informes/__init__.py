"""
Generadores de Informes
"""
from .tecnico import generar_informe_tecnico
from .ejecutivo_apa import generar_informe_ejecutivo_apa

__all__ = [
    'generar_informe_tecnico',
    'generar_informe_ejecutivo_apa'
]
