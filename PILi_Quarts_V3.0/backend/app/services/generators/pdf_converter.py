"""
Generador de Conversión Word a PDF
Convierte documentos Word (.docx) a PDF
"""

import subprocess
from pathlib import Path
import platform


def convertir_word_a_pdf(ruta_word, ruta_pdf=None):
    """
    Convierte un documento Word a PDF
    
    Args:
        ruta_word: Ruta del archivo Word (.docx)
        ruta_pdf: Ruta del archivo PDF de salida (opcional)
    
    Returns:
        Ruta del archivo PDF generado
    """
    ruta_word = Path(ruta_word)
    
    if not ruta_word.exists():
        raise FileNotFoundError(f"Archivo Word no encontrado: {ruta_word}")
    
    # Determinar ruta de salida
    if ruta_pdf is None:
        ruta_pdf = ruta_word.with_suffix('.pdf')
    else:
        ruta_pdf = Path(ruta_pdf)
    
    # Método de conversión según sistema operativo
    sistema = platform.system()
    
    if sistema == 'Windows':
        return _convertir_windows(ruta_word, ruta_pdf)
    elif sistema == 'Linux':
        return _convertir_linux(ruta_word, ruta_pdf)
    elif sistema == 'Darwin':  # macOS
        return _convertir_macos(ruta_word, ruta_pdf)
    else:
        raise OSError(f"Sistema operativo no soportado: {sistema}")


def _convertir_windows(ruta_word, ruta_pdf):
    """Conversión en Windows usando docx2pdf"""
    try:
        from docx2pdf import convert
        convert(str(ruta_word), str(ruta_pdf))
        return ruta_pdf
    except ImportError:
        raise ImportError(
            "docx2pdf no está instalado. "
            "Instala con: pip install docx2pdf"
        )
    except Exception as e:
        raise RuntimeError(f"Error convirtiendo a PDF: {e}")


def _convertir_linux(ruta_word, ruta_pdf):
    """Conversión en Linux usando LibreOffice"""
    try:
        # Usar LibreOffice en modo headless
        subprocess.run([
            'libreoffice',
            '--headless',
            '--convert-to', 'pdf',
            '--outdir', str(ruta_pdf.parent),
            str(ruta_word)
        ], check=True, capture_output=True)
        
        return ruta_pdf
    except FileNotFoundError:
        raise RuntimeError(
            "LibreOffice no está instalado. "
            "Instala con: sudo apt-get install libreoffice"
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Error convirtiendo a PDF: {e.stderr.decode()}")


def _convertir_macos(ruta_word, ruta_pdf):
    """Conversión en macOS usando LibreOffice"""
    # Similar a Linux
    return _convertir_linux(ruta_word, ruta_pdf)


# Función helper para generar PDF directamente desde datos
def generar_pdf_desde_datos(tipo_documento, datos, ruta_salida, opciones=None):
    """
    Genera un PDF directamente desde datos
    
    Args:
        tipo_documento: Tipo de documento
        datos: Datos del documento
        ruta_salida: Ruta del PDF de salida
        opciones: Opciones de personalización
    
    Returns:
        Ruta del PDF generado
    """
    from . import generar_documento
    import tempfile
    
    # Generar Word temporal
    with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as tmp:
        ruta_word_temp = Path(tmp.name)
    
    try:
        # Generar Word
        generar_documento(tipo_documento, datos, ruta_word_temp, opciones)
        
        # Convertir a PDF
        return convertir_word_a_pdf(ruta_word_temp, ruta_salida)
    finally:
        # Limpiar archivo temporal
        if ruta_word_temp.exists():
            ruta_word_temp.unlink()
