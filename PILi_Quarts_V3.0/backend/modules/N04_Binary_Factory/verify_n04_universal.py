"""
Script de Verificación Universal N04.
Prueba la generación de documentos usando el Motor Universal (Template Engine).
"""
import sys
import os
import logging
from pathlib import Path

# Setup paths
current_dir = Path(__file__).parent
backend_dir = current_dir.parent.parent
sys.path.append(str(backend_dir))

# Config Logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("N04_Univ_Certifier")

from modules.N04_Binary_Factory.index import binary_factory

def verify_universal_engine():
    logger.info("🚀 Iniciando Prueba de Motor Universal (N04)...")
    
    # 1. request with STRING document_type (Folder Name)
    template_name = "MODELO_USUARIO_TEST"
    
    request = {
        "header": {
            "user_id": "TEST_USER_UNIV",
            "service_id": 3,
            "document_type": template_name # The Magic String
        },
        "branding": {
            "color_hex": "#0052A3"
        },
        "payload": {
            "items": [
                {"descripcion": "Item Universal A", "cantidad": 10, "total": 100},
                {"descripcion": "Item Universal B", "cantidad": 5, "total": 50}
            ],
            "totals": {"total": 150},
            "client_info": {"nombre": "Cliente Universal S.A."}
        },
        "output_format": "XLSX"
    }

    logger.info(f"📄 Solicitando plantilla: {template_name}")
    response = binary_factory.process_request(request)
    
    if response.get("success"):
        logger.info(f"✅ ÉXITO: Motor Universal generó el archivo.")
        logger.info(f"   📂 Filename: {response.get('filename')}")
        logger.info(f"   ⚙️ Engine: {response.get('engine')}")
        
        # Save validation
        output_path = current_dir / "output_test" / response.get("filename")
        import base64
        with open(output_path, "wb") as f:
            f.write(base64.b64decode(response.get("file_b64")))
        logger.info(f"   💾 Guardado en: {output_path}")
        
    else:
        logger.error(f"❌ FALLO: {response.get('error')}")

if __name__ == "__main__":
    verify_universal_engine()
