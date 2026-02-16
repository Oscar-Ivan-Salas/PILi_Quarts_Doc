"""
Generador de PDF V2 - Convierte Word a PDF
Usa LibreOffice o alternativas para conversión
"""
from pathlib import Path
import logging
import subprocess
import platform
import os

logger = logging.getLogger(__name__)

class PDFGeneratorV2:
    """Generador de PDF desde Word"""
    
    def __init__(self):
        self.libreoffice_path = self._find_libreoffice()
        logger.info(f"✅ PDFGeneratorV2 inicializado")
        if self.libreoffice_path:
            logger.info(f"📄 LibreOffice encontrado en: {self.libreoffice_path}")
        else:
            logger.warning("⚠️ LibreOffice no encontrado, PDF puede no funcionar")
    
    def _find_libreoffice(self) -> str:
        """Buscar LibreOffice en el sistema"""
        if platform.system() == 'Windows':
            possible_paths = [
                r"C:\Program Files\LibreOffice\program\soffice.exe",
                r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
            ]
            for path in possible_paths:
                if os.path.exists(path):
                    return path
        return "soffice"  # Asumir que está en PATH
    
    def convertir_word_a_pdf(self, ruta_word: Path) -> Path:
        """
        Convertir documento Word a PDF
        
        Args:
            ruta_word: Path al archivo .docx
            
        Returns:
            Path al archivo .pdf generado
        """
        logger.info(f"📄 Convirtiendo Word a PDF: {ruta_word.name}")
        
        ruta_pdf = ruta_word.with_suffix('.pdf')
        
        try:
            # Usar LibreOffice para conversión
            cmd = [
                self.libreoffice_path,
                '--headless',
                '--convert-to', 'pdf',
                '--outdir', str(ruta_word.parent),
                str(ruta_word)
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0 and ruta_pdf.exists():
                logger.info(f"✅ PDF generado: {ruta_pdf.name}")
                return ruta_pdf
            else:
                logger.error(f"❌ Error en conversión: {result.stderr}")
                raise Exception(f"Error al convertir a PDF: {result.stderr}")
                
        except FileNotFoundError:
            logger.error("❌ LibreOffice no encontrado. Instalar LibreOffice para generar PDFs")
            raise Exception("LibreOffice no instalado. Necesario para generar PDFs")
        except subprocess.TimeoutExpired:
            logger.error("❌ Timeout al convertir a PDF")
            raise Exception("Timeout al convertir documento a PDF")
        except Exception as e:
            logger.error(f"❌ Error al convertir a PDF: {e}")
            raise

# Instancia global
pdf_generator_v2 = PDFGeneratorV2()
