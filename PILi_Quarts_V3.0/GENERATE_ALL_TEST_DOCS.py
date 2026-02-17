
import sys
import os
import json
import logging
import base64
from pathlib import Path

# Setup Path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))

from modules.N04_Binary_Factory.index import binary_factory

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MassGenerator")

def generate_mass_test():
    doc_types = {
        1: "COTIZACION_SIMPLE",
        2: "COTIZACION_COMPLEJA",
        3: "PROYECTO_SIMPLE",
        4: "PROYECTO_COMPLEJO",
        5: "INFORME_TECNICO",
        6: "INFORME_EJECUTIVO"
    }
    formats = ["DOCX"]
    output_dir = Path("e:/PILi_Quarts/PILi_Quarts_V3.0/DOCUMENTOS PRUEBA WORD")
    output_dir.mkdir(parents=True, exist_ok=True)

    logger.info(f"🚀 Starting Word-Only Generation of 6 documents in: {output_dir}")


    count = 0
    for doc_id, doc_label in doc_types.items():
        for fmt in formats:
            count += 1
            logger.info(f"[{count}/18] Generating {doc_label} in {fmt}...")
            
            payload = {
                "header": {
                    "service_id": count,
                    "user_id": "PILI_V3_MASTER",
                    "document_type": doc_id
                },
                "branding": {
                    "logo_b64": None,
                    "color_hex": "#0052A3"
                },
                "payload": {
                    "client_info": {
                        "nombre": "CORPORACIÓN TESLA TEST",
                        "ruc": "20601138787",
                        "fecha": "16/02/2026",
                        "proyecto": f"MEGA-PROYECTO {doc_label}",
                        "area_m2": 250
                    },
                    "items": [
                        {"descripcion": f"Servicio Especializado {doc_label} Phase 1", "cantidad": 1, "unidad": "glb", "precio_unitario": 1500.00, "total": 1500.00},
                        {"descripcion": "Instalación de Tableros Eléctricos Tesla", "cantidad": 2, "unidad": "und", "precio_unitario": 450.00, "total": 900.00},
                        {"descripcion": "Mano de Obra Certificada", "cantidad": 40, "unidad": "hh", "precio_unitario": 25.00, "total": 1000.00}
                    ],
                    "totals": {
                        "subtotal": 3400.00,
                        "igv": 612.00,
                        "total": 4012.00
                    },
                    "technical_notes": "Este documento ha sido generado automáticamente por el motor V9 Mirror para validación de sistema."
                },
                "output_format": fmt
            }

            try:
                result = binary_factory.process_request(payload)
                if result.get("success"):
                    filename = result.get("filename")
                    file_b64 = result.get("file_b64")
                    
                    final_path = output_dir / filename
                    with open(final_path, "wb") as f:
                        f.write(base64.b64decode(file_b64))
                    
                    logger.info(f"✅ Saved: {filename} (Engine: {result.get('engine')})")
                else:
                    logger.error(f"❌ Failed {doc_label} [{fmt}]: {result.get('error')}")
            except Exception as e:
                logger.error(f"💥 Exception in {doc_label} [{fmt}]: {e}")

    logger.info("🏁 Mass Generation Complete!")

if __name__ == "__main__":
    generate_mass_test()
