
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from word_master_generator import word_master_generator
from generators.html_to_pdf_generator import generate_pdf_playwright

logger = logging.getLogger(__name__)

class BinaryFactory:
    """
    FACTORÍA SOBERANA (Protocolo Triple Mirror - 14 Dic 2025)
    Centraliza la generación de documentos de alta fidelidad.
    """
    
    def __init__(self):
        self.output_dir = Path(__file__).parent / "output_sandbox"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_document(self, html_content: str, output_path: str, format_type: str = "word", doc_type: str = "cotizacion_simple") -> Dict[str, Any]:
        """
        Punto de entrada único para la generación.
        """
        logger.info(f"🚀 Generando {format_type} para tipo: {doc_type}")
        
        if format_type.lower() in ["word", "docx"]:
            # Usar el generador de alta fidelidad basado en MASTERS
            return word_master_generator.generate(html_content, output_path, doc_type)
        
        elif format_type.lower() == "pdf":
            # Usar Playwright para PDF (espejo del HTML)
            success = generate_pdf_playwright(html_content, output_path)
            return {"success": success, "path": output_path if success else None}
            
        else:
            return {"success": False, "error": f"Formato '{format_type}' no soportado."}

# Instancia central
binary_factory = BinaryFactory()
