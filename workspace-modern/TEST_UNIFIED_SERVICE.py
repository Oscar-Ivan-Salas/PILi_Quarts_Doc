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

def test_unified_generation():
    print("🚀 Testing UnifiedDocumentService...")
    
    # Mock Data (Complex Quote)
    data = {
        "numero": "COT-Unified-001",
        "fecha": datetime.now().strftime("%d/%m/%Y"),
        "valida_hasta": "30 días",
        "cliente": {
            "nombre": "Juan Pérez",
            "empresa": "Tech Solutions",
            "email": "juan@tech.com",
            "telefono": "555-1234",
            "direccion": "Av. Reforma 123"
        },
        "items": [
             {"descripcion": "Servicio de Ingeniería (Unified)", "cantidad": 1, "precio_unitario": 5000.00, "subtotal": 5000.00},
             {"descripcion": "Licencia de Software", "cantidad": 2, "precio_unitario": 1200.00, "subtotal": 2400.00}
        ],
        "totales": {
            "subtotal": 7400.00,
            "iva": 1184.00,
            "total": 8584.00
        },
        "terminos": "Pago 50% anticipo, 50% contra entrega.",
        "empresa_nombre": "PILi Engineering",
        "empresa_contacto": "contacto@pili.com"
    }
    
    # 1. Generate DOCX
    try:
        path_docx = unified_service.generate(
            DocumentType.COTIZACION_COMPLEJA,
            DocumentFormat.WORD,
            data
        )
        print(f"✅ DOCX Generated: {path_docx}")
    except Exception as e:
        print(f"❌ DOCX Failed: {e}")

    # 2. Generate PDF (using fallback/generic)
    try:
        path_pdf = unified_service.generate(
            DocumentType.COTIZACION_COMPLEJA,
            DocumentFormat.PDF,
            data
        )
        print(f"✅ PDF Generated: {path_pdf}")
    except Exception as e:
        print(f"❌ PDF Failed: {e}")
        
    # 3. Generate HTML Preview
    try:
        path_html = unified_service.generate(
            DocumentType.COTIZACION_COMPLEJA,
            DocumentFormat.HTML,
            data
        )
        print(f"✅ HTML Generated: {path_html}")
    except Exception as e:
        print(f"❌ HTML Failed: {e}")

if __name__ == "__main__":
    test_unified_generation()
