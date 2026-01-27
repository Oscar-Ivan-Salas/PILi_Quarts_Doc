"""
Servicios de lógica de negocio

IMPORTANTE: Evitar importaciones a nivel de paquete para prevenir cascadas
de import (p. ej. al importar submódulos como `app.services.word_generator`)
que a su vez intenten importar `gemini_service` u otros módulos pesados.

Las importaciones se deben realizar de forma explícita dentro de los
módulos/funciones que las necesiten para mantener la carga perezosa
(lazy-import) y evitar errores por dependencias opcionales.
"""

# Exportar nombres de módulos disponibles (sin importarlos aquí)
# Los consumidores deben importar submódulos directamente, por ejemplo:
#   from app.services.word_generator import word_generator
# Esto evita ejecutar código no deseado en el paquete al importarlo.
__all__ = [
    "word_generator",
    "pdf_generator",
    "file_processor",
    "rag_service",
    "gemini_service",
]