"""
SISTEMA PROFESIONAL DE GENERACION DE DOCUMENTOS
TESLA ELECTRICIDAD v4.0 - WORLD CLASS

Este modulo contiene todos los componentes de clase mundial para:
- Procesamiento de archivos (PDF, Word, Excel, imagenes)
- Sistema RAG local con ChromaDB
- Motor de graficas profesionales con Plotly
- ML local con spaCy + sentence-transformers
- Generacion de documentos APA/PMI
"""

from .processors.file_processor_pro import FileProcessorPro
from .rag.rag_engine import RAGEngine
from .ml.ml_engine import MLEngine
from .charts.chart_engine import ChartEngine
from .generators.document_generator_pro import DocumentGeneratorPro

__all__ = [
    'FileProcessorPro',
    'RAGEngine',
    'MLEngine',
    'ChartEngine',
    'DocumentGeneratorPro'
]

__version__ = '4.0.0'
