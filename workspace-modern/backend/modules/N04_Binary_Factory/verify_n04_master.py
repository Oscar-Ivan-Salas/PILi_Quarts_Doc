"""
Script de Certificación N04 - Master Verification.
Ejecuta el ciclo completo para los 6 tipos de documentos en aislamiento total.
"""
import sys
import os
import json
import base64
from pathlib import Path
import logging

# Setup Logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("N04_Certifier")

# 1. Isolation Setup (No app imports)
current_dir = Path(__file__).parent
backend_dir = current_dir.parent.parent
sys.path.append(str(backend_dir))

# Import N04 Only
try:
    from modules.N04_Binary_Factory.index import binary_factory
    logger.info("✅ N04 Factory Loaded Successfully.")
except ImportError as e:
    logger.error(f"❌ Isolation Failed. Could not import N04: {e}")
    sys.exit(1)

# 2. Test Data Generation
def create_test_payload(doc_type_id):
    return {
        "header": {
            "user_id": "TEST_USER_UUID",
            "service_id": 3, # Puesta a Tierra
            "document_type": doc_type_id
        },
        "branding": {
            "logo_b64": "", # Empty for test or mock base64
            "color_hex": "#CC0000" # Tesla Red for visibility
        },
        "payload": {
            "items": [
                {"descripcion": "Varilla de Cobre 3/4", "cantidad": 1, "precio": 280.00, "total": 280.00},
                {"descripcion": "Cemento Conductivo", "cantidad": 3, "precio": 120.00, "total": 360.00},
                {"descripcion": "Mano de Obra Especializada", "cantidad": 1, "precio": 600.00, "total": 600.00}
            ],
            "totals": {
                "subtotal": 1240.00,
                "igv": 223.20,
                "total": 1463.20
            },
            "technical_notes": "Instalación en terreno arcilloso. Resistencia objetiva < 5 Ohms.",
            "client_info": {
                "nombre": "Cliente Certificación N04",
                "ruc": "20600000001",
                "direccion": "Av. Test de Aislamiento 123"
            }
        },
        "output_format": "XLSX"
    }

# 3. Execution Loop
DOC_TYPES = {
    1: "Cotización Simple",
    2: "Cotización Compleja",
    3: "Proyecto Simple",
    4: "Proyecto Complejo",
    5: "Informe Técnico",
    6: "Informe Ejecutivo"
}

def run_certification():
    logger.info("🚀 Iniciando Protocolo de Certificación de N04 Binary Factory...")
    
    success_count = 0
    output_dir = current_dir / "output_test"
    output_dir.mkdir(exist_ok=True)
    
    for doc_id, doc_name in DOC_TYPES.items():
        logger.info(f"📄 Generando Documento Tipo {doc_id}: {doc_name}...")
        
        request_data = create_test_payload(doc_id)
        
        response = binary_factory.process_request(request_data)
        
        if response.get("success"):
            # Save file to prove it works
            file_b64 = response.get("file_b64")
            filename = f"CERTIFIED_DOC_{doc_id}_{doc_name.replace(' ', '_')}.xlsx"
            filepath = output_dir / filename
            
            with open(filepath, "wb") as f:
                f.write(base64.b64decode(file_b64))
                
            logger.info(f"   ✅ ÉXITO: Archivo generado en {filepath} ({len(file_b64)} bytes base64)")
            success_count += 1
        else:
            logger.error(f"   ❌ FALLO: {response.get('error')}")

    print("\n" + "="*50)
    print(f"RESUMEN DE CERTIFICACIÓN: {success_count}/6 Documentos Generados")
    print("="*50)

if __name__ == "__main__":
    run_certification()
