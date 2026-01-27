"""
Módulo de Routing para Generadores de Documentos Profesionales
Enruta las solicitudes al generador correcto según el tipo de documento
"""

from pathlib import Path
from .cotizaciones import generar_cotizacion_simple, generar_cotizacion_compleja
from .proyectos import generar_proyecto_simple, generar_proyecto_complejo_pmi
from .informes import generar_informe_tecnico, generar_informe_ejecutivo_apa
from .document_generator_pro import DocumentGeneratorPro


# Mapeo de tipos de documento a generadores
GENERADORES = {
    # Cotizaciones
    'cotizacion-simple': generar_cotizacion_simple,
    'cotizacion': generar_cotizacion_simple,  # Alias
    'cotizacion-compleja': generar_cotizacion_compleja,

    # Proyectos
    'proyecto-simple': generar_proyecto_simple,
    'proyecto-complejo': generar_proyecto_complejo_pmi,
    'proyecto-pmi': generar_proyecto_complejo_pmi,  # Alias

    # Informes
    'informe-tecnico': generar_informe_tecnico,
    'informe-ejecutivo': generar_informe_ejecutivo_apa,
    'informe-apa': generar_informe_ejecutivo_apa,  # Alias
}


def generar_documento(tipo_documento, datos, ruta_salida, opciones=None):
    """
    Genera un documento Word del tipo especificado

    Args:
        tipo_documento: Tipo de documento (cotizacion-simple, proyecto-pmi, etc.)
        datos: Diccionario con datos del documento
        ruta_salida: Ruta donde guardar el documento
        opciones: Opciones de personalización (colores, fuente, etc.)

    Returns:
        Ruta del documento generado

    Raises:
        ValueError: Si el tipo de documento no es válido
    """
    # Normalizar tipo de documento
    tipo_normalizado = tipo_documento.lower().strip()

    # Buscar generador
    generador = GENERADORES.get(tipo_normalizado)

    if not generador:
        raise ValueError(f"Tipo de documento no soportado: {tipo_documento}")

    # Generar documento
    return generador(datos, ruta_salida, opciones)


def tipos_disponibles():
    """Retorna lista de tipos de documentos disponibles"""
    return list(GENERADORES.keys())


__all__ = [
    'DocumentGeneratorPro',
    'generar_documento',
    'tipos_disponibles',
    'GENERADORES',
    'generar_cotizacion_simple',
    'generar_cotizacion_compleja',
    'generar_proyecto_simple',
    'generar_proyecto_complejo_pmi',
    'generar_informe_tecnico',
    'generar_informe_ejecutivo_apa'
]
