"""
Document Generator Module - Main Service
Enterprise-grade document generation orchestrator
Following clean-code, python-patterns, and architecture skills
"""
from typing import Dict, Any, Optional, Literal
from io import BytesIO
import logging
from enum import Enum

from .pdf_generator import PDFGenerator
from .word_generator import WordGenerator
from .excel_generator import ExcelGenerator

logger = logging.getLogger(__name__)


class DocumentFormat(str, Enum):
    """
    Supported document formats.
    
    Following python-patterns: Enum for type safety
    """
    PDF = "pdf"
    WORD = "docx"
    EXCEL = "xlsx"


class DocumentType(str, Enum):
    """
    Supported document types.
    
    Following architecture: Clear type definitions
    """
    COTIZACION = "cotizacion"
    INFORME = "informe"
    PRESUPUESTO = "presupuesto"
    CONTRATO = "contrato"
    PLANO = "plano"


class DocumentGeneratorService:
    """
    Main document generation service.
    
    Orchestrates different generators based on format and type.
    
    Following architecture:
    - Facade pattern for complex subsystems
    - Dependency injection
    - Single Responsibility
    
    Following python-patterns:
    - Type hints for clarity
    - Async support (future)
    """
    
    def __init__(self):
        """Initialize document generators"""
        self.pdf_generator = PDFGenerator()
        self.word_generator = WordGenerator()
        self.excel_generator = ExcelGenerator()
        
        logger.info("Document Generator Service initialized")
    
    def generate(
        self,
        document_type: DocumentType,
        format: DocumentFormat,
        data: Dict[str, Any],
        output_path: Optional[str] = None
    ) -> BytesIO:
        """
        Generate document based on type and format.
        
        Following clean-code: Clear method signature
        Following architecture: Strategy pattern
        
        Args:
            document_type: Type of document (cotizacion, informe, etc.)
            format: Output format (pdf, docx, xlsx)
            data: Document data
            output_path: Optional file path to save
        
        Returns:
            BytesIO buffer with generated document
        
        Raises:
            ValueError: If invalid combination of type and format
            NotImplementedError: If generator not implemented
        """
        logger.info(f"Generating {document_type.value} in {format.value} format")
        
        # Validate combination
        if not self._is_valid_combination(document_type, format):
            raise ValueError(
                f"Invalid combination: {document_type.value} cannot be generated as {format.value}"
            )
        
        # Route to appropriate generator
        try:
            if format == DocumentFormat.PDF:
                return self._generate_pdf(document_type, data, output_path)
            elif format == DocumentFormat.WORD:
                return self._generate_word(document_type, data, output_path)
            elif format == DocumentFormat.EXCEL:
                return self._generate_excel(document_type, data, output_path)
            else:
                raise ValueError(f"Unsupported format: {format}")
                
        except Exception as e:
            logger.error(f"Error generating document: {str(e)}", exc_info=True)
            raise
    
    def _is_valid_combination(
        self,
        document_type: DocumentType,
        format: DocumentFormat
    ) -> bool:
        """
        Validate document type and format combination.
        
        Following clean-code: Validation logic separation
        """
        # Excel only for cotizacion and presupuesto
        if format == DocumentFormat.EXCEL:
            return document_type in [DocumentType.COTIZACION, DocumentType.PRESUPUESTO]
        
        # PDF and Word support all types
        return True
    
    def _generate_pdf(
        self,
        document_type: DocumentType,
        data: Dict[str, Any],
        output_path: Optional[str]
    ) -> BytesIO:
        """
        Generate PDF document.
        
        Following python-patterns: Method delegation
        """
        if document_type == DocumentType.COTIZACION:
            return self.pdf_generator.generate_cotizacion(data, output_path)
        elif document_type == DocumentType.INFORME:
            return self.pdf_generator.generate_informe(data, output_path)
        else:
            raise NotImplementedError(f"PDF generation for {document_type.value} not implemented")
    
    def _generate_word(
        self,
        document_type: DocumentType,
        data: Dict[str, Any],
        output_path: Optional[str]
    ) -> BytesIO:
        """Generate Word document"""
        if document_type == DocumentType.COTIZACION:
            return self.word_generator.generate_cotizacion(data, output_path)
        elif document_type == DocumentType.INFORME:
            return self.word_generator.generate_informe(data, output_path)
        else:
            raise NotImplementedError(f"Word generation for {document_type.value} not implemented")
    
    def _generate_excel(
        self,
        document_type: DocumentType,
        data: Dict[str, Any],
        output_path: Optional[str]
    ) -> BytesIO:
        """Generate Excel document"""
        if document_type == DocumentType.COTIZACION:
            return self.excel_generator.generate_cotizacion(data, output_path)
        elif document_type == DocumentType.PRESUPUESTO:
            return self.excel_generator.generate_presupuesto(data, output_path)
        else:
            raise NotImplementedError(f"Excel generation for {document_type.value} not implemented")
    
    async def generate_async(
        self,
        document_type: DocumentType,
        format: DocumentFormat,
        data: Dict[str, Any],
        output_path: Optional[str] = None
    ) -> BytesIO:
        """
        Async version of generate method.
        
        Following python-patterns: Async for I/O operations
        
        Currently wraps sync method, but can be optimized
        for async I/O in the future.
        """
        import asyncio
        return await asyncio.to_thread(
            self.generate,
            document_type,
            format,
            data,
            output_path
        )
    
    def get_supported_formats(self, document_type: DocumentType) -> list[DocumentFormat]:
        """
        Get supported formats for a document type.
        
        Following clean-code: Expose useful information
        """
        if document_type in [DocumentType.COTIZACION, DocumentType.PRESUPUESTO]:
            return [DocumentFormat.PDF, DocumentFormat.WORD, DocumentFormat.EXCEL]
        else:
            return [DocumentFormat.PDF, DocumentFormat.WORD]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get service statistics"""
        return {
            "supported_types": [t.value for t in DocumentType],
            "supported_formats": [f.value for f in DocumentFormat],
            "generators": {
                "pdf": "ReportLab",
                "word": "python-docx",
                "excel": "openpyxl"
            }
        }
