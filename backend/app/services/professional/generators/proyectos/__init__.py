"""
Generadores de Proyectos
"""
from .simple import generar_proyecto_simple
from .complejo_pmi import generar_proyecto_complejo_pmi

__all__ = [
    'generar_proyecto_simple',
    'generar_proyecto_complejo_pmi'
]
