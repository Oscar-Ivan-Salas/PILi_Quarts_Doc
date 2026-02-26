
import logging
from pydantic import ValidationError
try:
    from models import BinaryFactoryInput
except ImportError:
    from .models import BinaryFactoryInput

logger = logging.getLogger("TEST_VALIDATION")
logging.basicConfig(level=logging.INFO)

def test_bridge_contract():
    # Simulamos el payload que genera el Puente en index.py
    input_dict = {
        "header": {
            "user_id": "Studio_User",
            "service_id": 1, 
            "document_type": "COTIZACION_SIMPLE"
        },
        "branding": {
            "logo_b64": None,
            "color_hex": "#0052A3"
        },
        "payload": {
            "items": [],
            "totals": {
                "subtotal": 0,
                "igv": 0,
                "total": 0
            },
            "technical_notes": "", # El culpable sospechoso
            "client_info": {
                "nombre": "Test Cliente",
                "ruc": "",
                "direccion": "",
                "fecha": ""
            }
        },
        "output_format": "DOCX"
    }
    
    try:
        validated_input = BinaryFactoryInput(**input_dict)
        print("✅ VALIDACION EXITOSA: El contrato es correcto.")
    except ValidationError as e:
        print(f"❌ FALLO DE CONTRATO: {e.errors()}")

if __name__ == "__main__":
    test_bridge_contract()
