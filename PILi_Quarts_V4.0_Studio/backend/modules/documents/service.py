import logging
import time
from enum import Enum
from typing import Dict, Any, Optional, List
from io import BytesIO
from datetime import datetime
import os

# --- LOCAL GENERATORS (Moved from N04) ---
# Note: Relative imports or absolute imports from backend.modules.documents.generators
from .generators.cotizacion_simple_generator import generar_cotizacion_simple
from .generators.cotizacion_compleja_generator import generar_cotizacion_compleja
from .generators.proyecto_simple_generator import generar_proyecto_simple
# Corrected: generar_proyecto_complejo_pmi
from .generators.proyecto_complejo_pmi_generator import generar_proyecto_complejo_pmi as generar_proyecto_complejo
from .generators.informe_tecnico_generator import generar_informe_tecnico
# Corrected: generar_informe_ejecutivo_apa
from .generators.informe_ejecutivo_apa_generator import generar_informe_ejecutivo_apa as generar_informe_ejecutivo

# --- GENERIC GENERATORS ---
# These are still used for fallback or specific formats? 
# The user plan mentioned pdf_generator and excel_generator.
# We assume they reside in .generators (the ones that were already there) or we import from app.services if they are not moved.
# My list_dir showed excel_generator.py and pdf_generator.py in documents/generators.
from .generators.pdf_generator import PDFGenerator
from .generators.excel_generator import ExcelGenerator
# HTMLToWordGenerator is still in N04 or app.services? 
# I did NOT move it. It was in N04 root. Let's assume we import from N04 for now or move it too.
# For Clean Architecture, we should move it. But strict move was only for generators folder.
# Let's import from N04 for now to be safe.
from modules.N04_Binary_Factory.html_to_word_generator import html_to_word_generator

logger = logging.getLogger("UnifiedDocumentService")

class DocumentType(str, Enum):
    COTIZACION_SIMPLE = "cotizacion_simple"
    COTIZACION_COMPLEJA = "cotizacion_compleja"
    PROYECTO_SIMPLE = "proyecto_simple"
    PROYECTO_COMPLEJO = "proyecto_complejo"
    INFORME_TECNICO = "informe_tecnico"
    INFORME_EJECUTIVO = "informe_ejecutivo"


class DocumentFormat(str, Enum):
    HTML = "html"
    WORD = "docx"
    PDF = "pdf"
    EXCEL = "xlsx"


class UnifiedDocumentService:
    """
    Servicio unificado que orquesta TODOS los generadores existentes.
    "El Capataz" que ordena a las máquinas de la Fábrica Binaria.
    """
    
    def __init__(self):
        # Inicializar generadores auxiliares
        self.pdf_gen = PDFGenerator()
        self.excel_gen = ExcelGenerator()
        self.html_to_word_gen = html_to_word_generator
        
        # Mapeo de generadores Word especializados (Motor Nativo)
        self.word_generators = {
            DocumentType.COTIZACION_SIMPLE: generar_cotizacion_simple,
            DocumentType.COTIZACION_COMPLEJA: generar_cotizacion_compleja,
            DocumentType.PROYECTO_SIMPLE: generar_proyecto_simple,
            DocumentType.PROYECTO_COMPLEJO: generar_proyecto_complejo,
            DocumentType.INFORME_TECNICO: generar_informe_tecnico,
            DocumentType.INFORME_EJECUTIVO: generar_informe_ejecutivo,
        }
        
        logger.info("✅ UnifiedDocumentService inicializado (Motor Unificado)")
    
    def generate(
        self,
        document_type: DocumentType,
        format: DocumentFormat,
        data: Dict[str, Any],
        options: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Generar documento en el formato especificado
        """
        logger.info(f"🚀 UnifiedDocumentService: Generando {document_type.value} en {format.value}")
        
        if not self._is_valid_combination(document_type, format):
             raise ValueError(f"Combinación inválida: {document_type.value} + {format.value}")

        try:
            if format == DocumentFormat.HTML:
                return self._generate_html(document_type, data)
            elif format == DocumentFormat.WORD:
                return self._generate_word(document_type, data, options)
            elif format == DocumentFormat.PDF:
                return self._generate_pdf(document_type, data, options)
            elif format == DocumentFormat.EXCEL:
                return self._generate_excel(document_type, data)
            else:
                raise ValueError(f"Formato no soportado: {format}")
                
        except Exception as e:
            logger.error(f"❌ Error Critical: {e}", exc_info=True)
            raise e

    def _generate_html(self, doc_type: DocumentType, data: Dict) -> str:
        """Vista previa HTML (Fuente de Verdad)"""
        # Mapeo de tipos a nombres de plantilla
        # PLANTILLA_HTML_COTIZACION_SIMPLE.html, etc.
        template_map = {
            DocumentType.COTIZACION_SIMPLE: "cotizacion_simple",
            DocumentType.COTIZACION_COMPLEJA: "cotizacion_compleja",
            DocumentType.PROYECTO_SIMPLE: "proyecto_simple",
            DocumentType.PROYECTO_COMPLEJO: "proyecto_complejo",
            DocumentType.INFORME_TECNICO: "informe_tecnico",
            DocumentType.INFORME_EJECUTIVO: "informe_ejecutivo"
        }
        
        template_key = template_map.get(doc_type)
        if not template_key:
             raise ValueError(f"No hay plantilla HTML para {doc_type}")
             
        # Cargar plantilla HTML
        html_content = self.html_to_word_gen._cargar_plantilla(template_key)
        
        # Reemplazar variables (Dynamic Injection)
        html_rendered = self.html_to_word_gen._reemplazar_variables(html_content, data)
        
        # Guardar en tmp o storage
        # Usamos storage/preview para persistencia o tmp
        from pathlib import Path
        output_dir = Path("storage/previews")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        filename = f"{doc_type.value}_{int(time.time())}.html"
        output_path = output_dir / filename
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_rendered)
            
        return str(output_path)

    def _generate_word(self, doc_type: DocumentType, data: Dict, options: Dict) -> str:
        """Generar Word (Motor Nativo)"""
        generator_func = self.word_generators.get(doc_type)
        if not generator_func:
            raise NotImplementedError(f"Generador Word para {doc_type.value} no implementado")
        
        from pathlib import Path
        output_dir = Path("storage/generados")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        filename = f"{doc_type.value}_{int(time.time())}.docx"
        output_path = output_dir / filename
        
        result_path = generator_func(data, output_path, options)
        return str(result_path)

    def _generate_pdf(self, doc_type: DocumentType, data: Dict, options: Dict) -> str:
        """Generar PDF"""
        from pathlib import Path
        output_dir = Path("storage/generados")
        output_dir.mkdir(parents=True, exist_ok=True)
        filename = f"{doc_type.value}_{int(time.time())}.pdf"
        output_path = output_dir / filename
        str_output_path = str(output_path)
        
        # Routing Específico
        if doc_type == DocumentType.COTIZACION_SIMPLE:
             self.pdf_gen.generate_cotizacion(data, str_output_path)
        elif doc_type == DocumentType.COTIZACION_COMPLEJA:
             self.pdf_gen.generate_cotizacion(data, str_output_path)
        elif doc_type == DocumentType.PROYECTO_SIMPLE:
             self.pdf_gen.generate_proyecto_simple(data, str_output_path)
        elif doc_type == DocumentType.PROYECTO_COMPLEJO:
             self.pdf_gen.generate_proyecto_complejo(data, str_output_path)
        elif doc_type == DocumentType.INFORME_TECNICO:
             self.pdf_gen.generate_informe_tecnico(data, str_output_path)
        elif doc_type == DocumentType.INFORME_EJECUTIVO:
             self.pdf_gen.generate_informe_ejecutivo(data, str_output_path)
        else:
             self.pdf_gen.generate_informe(data, str_output_path)

        return str_output_path

    def _generate_excel(self, doc_type: DocumentType, data: Dict) -> str:
        """Generar Excel (Matriz Completa 6x6)"""
        from pathlib import Path
        output_dir = Path("storage/generados")
        output_dir.mkdir(parents=True, exist_ok=True)
        filename = f"{doc_type.value}_{int(time.time())}.xlsx"
        output_path = output_dir / filename
        str_output_path = str(output_path)
        
        # Routing Específico
        if "cotizacion" in doc_type.value:
             self.excel_gen.generate_cotizacion(data, str_output_path)
        elif doc_type == DocumentType.PROYECTO_SIMPLE:
             self.excel_gen.generate_proyecto_simple(data, str_output_path)
        elif doc_type == DocumentType.PROYECTO_COMPLEJO:
             self.excel_gen.generate_proyecto_complejo(data, str_output_path)
        elif doc_type == DocumentType.INFORME_TECNICO:
             self.excel_gen.generate_informe_tecnico(data, str_output_path)
        elif doc_type == DocumentType.INFORME_EJECUTIVO:
             self.excel_gen.generate_informe_ejecutivo(data, str_output_path)
        else:
             raise ValueError(f"Excel no soportado para {doc_type.value}")
             
        return str_output_path

    def _is_valid_combination(self, doc_type: DocumentType, format: DocumentFormat) -> bool:
        """Validar si la combinación es válida"""
        # Ahora TODOS soportan TODOS los formatos
        return True

# Instancia global (Singleton)
unified_service = UnifiedDocumentService()
