"""
Unit Tests for Document Generators
Following testing-patterns: AAA pattern, test data factories
"""
import pytest
from io import BytesIO

from modules.documents.generators.pdf_generator import PDFGenerator
from modules.documents.generators.word_generator import WordGenerator
from modules.documents.generators.excel_generator import ExcelGenerator
from modules.documents.service import DocumentGeneratorService, DocumentType, DocumentFormat


@pytest.mark.unit
class TestPDFGenerator:
    """
    PDF Generator unit tests.
    
    Following testing-patterns: Group related tests
    """
    
    def test_generate_cotizacion_returns_buffer(self, cotizacion_data):
        """
        Should generate PDF and return BytesIO buffer.
        
        Following testing-patterns: AAA pattern
        """
        # Arrange
        generator = PDFGenerator()
        
        # Act
        result = generator.generate_cotizacion(cotizacion_data)
        
        # Assert
        assert isinstance(result, BytesIO)
        assert result.tell() == 0  # Buffer position at start
        assert len(result.getvalue()) > 0  # Has content
    
    def test_generate_cotizacion_has_pdf_header(self, cotizacion_data):
        """Should generate valid PDF file"""
        # Arrange
        generator = PDFGenerator()
        
        # Act
        result = generator.generate_cotizacion(cotizacion_data)
        
        # Assert
        content = result.getvalue()
        assert content.startswith(b'%PDF')  # PDF magic number
    
    def test_generate_informe_returns_buffer(self):
        """Should generate technical report PDF"""
        # Arrange
        generator = PDFGenerator()
        data = {
            "titulo": "Informe Técnico de Prueba",
            "secciones": [
                {
                    "titulo": "Introducción",
                    "contenido": "Este es un informe de prueba."
                },
                {
                    "titulo": "Análisis",
                    "contenido": "Resultados del análisis técnico."
                }
            ]
        }
        
        # Act
        result = generator.generate_informe(data)
        
        # Assert
        assert isinstance(result, BytesIO)
        assert len(result.getvalue()) > 0
        assert result.getvalue().startswith(b'%PDF')


@pytest.mark.unit
class TestWordGenerator:
    """Word Generator unit tests"""
    
    def test_generate_cotizacion_returns_buffer(self, cotizacion_data):
        """Should generate Word document"""
        # Arrange
        generator = WordGenerator()
        
        # Act
        result = generator.generate_cotizacion(cotizacion_data)
        
        # Assert
        assert isinstance(result, BytesIO)
        assert len(result.getvalue()) > 0
    
    def test_generate_cotizacion_has_docx_header(self, cotizacion_data):
        """Should generate valid Word file"""
        # Arrange
        generator = WordGenerator()
        
        # Act
        result = generator.generate_cotizacion(cotizacion_data)
        
        # Assert
        content = result.getvalue()
        # DOCX files are ZIP archives
        assert content.startswith(b'PK')  # ZIP magic number
    
    def test_generate_informe_returns_buffer(self):
        """Should generate technical report Word"""
        # Arrange
        generator = WordGenerator()
        data = {
            "titulo": "Informe Técnico",
            "secciones": [
                {"titulo": "Sección 1", "contenido": "Contenido 1"}
            ]
        }
        
        # Act
        result = generator.generate_informe(data)
        
        # Assert
        assert isinstance(result, BytesIO)
        assert len(result.getvalue()) > 0


@pytest.mark.unit
class TestExcelGenerator:
    """Excel Generator unit tests"""
    
    def test_generate_cotizacion_returns_buffer(self, cotizacion_data):
        """Should generate Excel workbook"""
        # Arrange
        generator = ExcelGenerator()
        
        # Act
        result = generator.generate_cotizacion(cotizacion_data)
        
        # Assert
        assert isinstance(result, BytesIO)
        assert len(result.getvalue()) > 0
    
    def test_generate_cotizacion_has_xlsx_header(self, cotizacion_data):
        """Should generate valid Excel file"""
        # Arrange
        generator = ExcelGenerator()
        
        # Act
        result = generator.generate_cotizacion(cotizacion_data)
        
        # Assert
        content = result.getvalue())
        # XLSX files are ZIP archives
        assert content.startswith(b'PK')  # ZIP magic number


@pytest.mark.unit
class TestDocumentGeneratorService:
    """
    Document Generator Service unit tests.
    
    Following testing-patterns: Test facade/orchestrator
    """
    
    def test_generate_pdf_cotizacion(self, cotizacion_data):
        """Should generate PDF quotation"""
        # Arrange
        service = DocumentGeneratorService()
        
        # Act
        result = service.generate(
            document_type=DocumentType.COTIZACION,
            format=DocumentFormat.PDF,
            data=cotizacion_data
        )
        
        # Assert
        assert isinstance(result, BytesIO)
        assert len(result.getvalue()) > 0
    
    def test_generate_word_cotizacion(self, cotizacion_data):
        """Should generate Word quotation"""
        # Arrange
        service = DocumentGeneratorService()
        
        # Act
        result = service.generate(
            document_type=DocumentType.COTIZACION,
            format=DocumentFormat.WORD,
            data=cotizacion_data
        )
        
        # Assert
        assert isinstance(result, BytesIO)
        assert len(result.getvalue()) > 0
    
    def test_generate_excel_cotizacion(self, cotizacion_data):
        """Should generate Excel quotation"""
        # Arrange
        service = DocumentGeneratorService()
        
        # Act
        result = service.generate(
            document_type=DocumentType.COTIZACION,
            format=DocumentFormat.EXCEL,
            data=cotizacion_data
        )
        
        # Assert
        assert isinstance(result, BytesIO)
        assert len(result.getvalue()) > 0
    
    def test_invalid_combination_raises_error(self):
        """Should raise error for invalid format/type combination"""
        # Arrange
        service = DocumentGeneratorService()
        data = {}
        
        # Act & Assert
        with pytest.raises(ValueError, match="Invalid combination"):
            service.generate(
                document_type=DocumentType.INFORME,
                format=DocumentFormat.EXCEL,  # Informe doesn't support Excel
                data=data
            )
    
    def test_get_supported_formats_cotizacion(self):
        """Should return all formats for cotizacion"""
        # Arrange
        service = DocumentGeneratorService()
        
        # Act
        formats = service.get_supported_formats(DocumentType.COTIZACION)
        
        # Assert
        assert DocumentFormat.PDF in formats
        assert DocumentFormat.WORD in formats
        assert DocumentFormat.EXCEL in formats
    
    def test_get_supported_formats_informe(self):
        """Should return PDF and Word for informe"""
        # Arrange
        service = DocumentGeneratorService()
        
        # Act
        formats = service.get_supported_formats(DocumentType.INFORME)
        
        # Assert
        assert DocumentFormat.PDF in formats
        assert DocumentFormat.WORD in formats
        assert DocumentFormat.EXCEL not in formats
    
    def test_get_stats(self):
        """Should return service statistics"""
        # Arrange
        service = DocumentGeneratorService()
        
        # Act
        stats = service.get_stats()
        
        # Assert
        assert "supported_types" in stats
        assert "supported_formats" in stats
        assert "generators" in stats
        assert stats["generators"]["pdf"] == "ReportLab"
    
    @pytest.mark.asyncio
    async def test_generate_async(self, cotizacion_data):
        """Should generate document asynchronously"""
        # Arrange
        service = DocumentGeneratorService()
        
        # Act
        result = await service.generate_async(
            document_type=DocumentType.COTIZACION,
            format=DocumentFormat.PDF,
            data=cotizacion_data
        )
        
        # Assert
        assert isinstance(result, BytesIO)
        assert len(result.getvalue()) > 0
