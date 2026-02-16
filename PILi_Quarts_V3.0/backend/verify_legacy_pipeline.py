
import os
import sys
import logging
from datetime import datetime


# Validating PYTHONPATH
file_path = os.path.abspath(__file__)
backend_dir = os.path.dirname(file_path)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# Ensure app can be imported
try:
    import app
except ImportError:
    # Try adding parent directory if needed (though backend_dir should work if structure is correct)
    parent_dir = os.path.dirname(backend_dir)
    sys.path.insert(0, parent_dir)

from app.services.generators.cotizacion_compleja_generator import generar_cotizacion_compleja
from app.services.pdf_generator_v2 import pdf_generator_v2

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("LegacyVerifier")

def test_legacy_pipeline():
    output_dir = os.path.join(os.path.dirname(__file__), 'legacy_test_output')
    os.makedirs(output_dir, exist_ok=True)
    
    # Mock Data (Complex Quote)
    data = {
        "cliente": "Minera Las Bambas",
        "proyecto": "Mantenimiento Sistema Scada",
        "codigo": "COT-LEGACY-001",
        "fecha_generacion": datetime.now().strftime("%d/%m/%Y"),
        "moneda": "USD",
        "items": [
            {"descripcion": "Servidor Dell PowerEdge R740", "cantidad": 2, "unidad": "UND", "precio_unitario": 12500.00, "total": 25000.00},
            {"descripcion": "Licencia Windows Server 2019", "cantidad": 2, "unidad": "LIC", "precio_unitario": 850.00, "total": 1700.00},
            {"descripcion": "Servicio de Configuración y Migración", "cantidad": 1, "unidad": "SRV", "precio_unitario": 4500.00, "total": 4500.00}
        ],
        "subtotal": 31200.00,
        "igv": 5616.00,
        "total": 36816.00,
        "condiciones": {
            "forma_pago": "30 días",
            "validez": "15 días",
            "garantia": "12 meses"
        },
        "cronograma": [
            {"fase": "Adquisición de Equipos", "duracion": "15 días"},
            {"fase": "Configuración en Laboratorio", "duracion": "5 días"},
            {"fase": "Implementación en Sitio", "duracion": "3 días"}
        ]
    }
    
    timestamp = datetime.now().strftime("%H%M%S")
    word_filename = f"COT_LEGACY_TEST_{timestamp}.docx"
    word_path = os.path.join(output_dir, word_filename)
    
    logger.info("🚀 Starting Legacy Pipeline Test...")
    
    # 1. Generate Word (Legacy Generator)
    try:
        logger.info(f"📝 Step 1: Generating DOCX using 'cotizacion_compleja_generator.py'...")
        final_word_path = generar_cotizacion_compleja(data, word_path, {})
        logger.info(f"✅ DOCX Generated: {final_word_path}")
    except Exception as e:
        logger.error(f"❌ Word Generation Failed: {e}")
        return

    # 2. Convert to PDF (Legacy LibreOffice Engine)
    try:
        logger.info(f"🖨️ Step 2: Converting to PDF using 'pdf_generator_v2.py' (LibreOffice)...")
        pdf_path = pdf_generator_v2.convertir_word_a_pdf(Path(final_word_path))
        
        if pdf_path.exists():
            logger.info(f"✅ PDF Generated: {pdf_path}")
            print(f"\n✨ SUCCESS: Pipeline Verified.")
            print(f"📄 DOCX: {final_word_path}")
            print(f"📕 PDF:  {pdf_path}")
        else:
            logger.error("❌ PDF file was not created (LibreOffice silent failure?)")
    except Exception as e:
        logger.error(f"❌ PDF Conversion Failed: {e}")
        print("\n⚠️ NOTE: If PDF conversion failed, ensure LibreOffice is installed and 'soffice' is in PATH or configured in pdf_generator_v2.py")

if __name__ == "__main__":
    test_legacy_pipeline()
