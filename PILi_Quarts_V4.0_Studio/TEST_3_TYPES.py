import sys
import os
import logging
from pathlib import Path
from datetime import datetime

# Setup paths
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))

from backend.modules.documents.service import unified_service, DocumentType, DocumentFormat

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_all_types():
    print("🚀 Verificando los 3 Tipos Principales (Cotización, Proyecto, Informe)...")
    
    # 1. COTIZACIÓN
    data_cot = {
        "numero": "COT-TEST-001",
        "cliente": {"nombre": "Cliente Cotización"},
        "items": [{"descripcion": "Item 1", "cantidad": 1, "precio_unitario": 100, "subtotal": 100}],
        "totales": {"subtotal": 100, "iva": 18, "total": 118}
    }
    print("\n--- 1. Generando Cotización ---")
    try:
        path = unified_service.generate(DocumentType.COTIZACION_COMPLEJA, DocumentFormat.WORD, data_cot)
        print(f"✅ Cotización DOCX: {path}")
    except Exception as e: print(f"❌ Cotización DOCX Error: {e}")

    # 2. PROYECTO
    data_proj = {
        "codigo": "PROJ-TEST-001",
        "nombre": "Proyecto de Prueba Unificado",
        "cliente": {"nombre": "Cliente Proyecto"},
        "duracion_total": "30 días",
        "presupuesto": 50000,
        "alcance": "Alcance de prueba para validación de tipo proyecto."
    }
    print("\n--- 2. Generando Proyecto ---")
    try:
        path = unified_service.generate(DocumentType.PROYECTO_COMPLEJO, DocumentFormat.WORD, data_proj)
        print(f"✅ Proyecto DOCX: {path}")
    except Exception as e: print(f"❌ Proyecto DOCX Error: {e}")

    # 3. INFORME
    data_inf = {
        "codigo": "INF-TEST-001",
        "titulo": "Informe Técnico de Prueba",
        "cliente": {"nombre": "Cliente Informe"},
        "resumen": "Resumen ejecutivo de prueba.",
        "secciones": [
            {"titulo": "Introducción", "contenido": "Contenido de prueba sección 1."},
            {"titulo": "Conclusiones", "contenido": "Contenido de prueba sección 2."}
        ]
    }
    print("\n--- 3. Generando Informe ---")
    try:
        path = unified_service.generate(DocumentType.INFORME_TECNICO, DocumentFormat.WORD, data_inf)
        print(f"✅ Informe DOCX: {path}")
    except Exception as e: print(f"❌ Informe DOCX Error: {e}")

if __name__ == "__main__":
    test_all_types()
