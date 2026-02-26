
import sys
import os
import json
import base64
from pathlib import Path
import logging

# Setup Logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("ADN_Pro_Verifier")

# Isolation Setup
current_dir = Path(__file__).parent
backend_dir = current_dir.parent.parent
sys.path.append(str(backend_dir))

try:
    from modules.N04_Binary_Factory.index import binary_factory
    logger.info("✅ N04 Factory Loaded.")
except ImportError as e:
    logger.error(f"❌ Could not import N04: {e}")
    sys.exit(1)

# Mock Logo (1x1 Transparent Pixel)
LOGO_B64 = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="

def create_payload(moneda, fmt):
    return {
        "header": {
            "user_id": "U001",
            "service_id": 100,
            "document_type": "COTIZACION_SIMPLE"
        },
        "branding": {
            "logo_b64": LOGO_B64,
            "color_hex": "#0052A3" # Tesla Blue
        },
        "payload": {
            "items": [
                {"descripcion": "Servicio de Ingeniería Pro", "cantidad": 1, "precio_unitario": 500.00, "total": 500.00},
                {"descripcion": "Materiales Eléctricos ADN", "cantidad": 5, "precio_unitario": 100.00, "total": 500.00}
            ],
            "totals": {
                "subtotal": 1000.00,
                "igv": 180.00,
                "total": 1180.00
            },
            "settings": {
                "currency": moneda,
                "primaryColor": "#0052A3"
            },
            "client_info": {
                "nombre": f"Cliente VIP ({moneda})",
                "ruc": "20601122334",
                "direccion": "Av. Los Innovadores 456"
            }
        },
        "output_format": fmt
    }

def run_test():
    output_dir = current_dir / "output_test_adn"
    output_dir.mkdir(exist_ok=True)
    
    scenarios = [
        ("PEN", "DOCX"),
        ("USD", "XLSX"),
        ("EUR", "PDF")
    ]
    
    for moneda, fmt in scenarios:
        logger.info(f"🚀 Generando {fmt} en {moneda}...")
        payload = create_payload(moneda, fmt)
        res = binary_factory.process_request(payload)
        
        if res.get("success"):
            filename = res.get("filename")
            filepath = output_dir / filename
            with open(filepath, "wb") as f:
                f.write(base64.b64decode(res.get("file_b64")))
            logger.info(f"   ✅ Generado: {filename}")
        else:
            logger.error(f"   ❌ Falló {fmt}/{moneda}: {res.get('error')}")

if __name__ == "__main__":
    run_test()
