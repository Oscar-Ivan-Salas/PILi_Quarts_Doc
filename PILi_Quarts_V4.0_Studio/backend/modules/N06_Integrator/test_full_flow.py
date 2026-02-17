"""
Prueba de Certificación de Integración (Test Full Flow).
Simula un caso real de uso del Integrador N06.
"""
import sys
import os
import logging
from pathlib import Path

# Setup paths
current_dir = Path(__file__).parent
backend_dir = current_dir.parent.parent
sys.path.append(str(backend_dir))

# Config Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("N06_Certifier")

from modules.N06_Integrator.index import integrator_node

def test_circular_flow():
    logger.info("🧪 Iniciando Prueba de Certificación: Flujo Circular Completo")
    
    # 1. Definir Input (Simulando Frontend)
    input_request = {
        "client_info": {
            "nombre": "Constructora ABC",
            "ruc": "20123456789",
            "direccion": "Av. Javier Prado 1234, Lima"
        },
        "service_request": {
            "service_key": "pozo-tierra",     # Key real en BD
            "document_model_id": 2,           # Cotización Compleja
            "quantity": 1
        },
        "user_context": {
            "user_id": "TEST_INTEGRATION_USER",
            "branding": {
                "color_hex": "#CC0000" # Tesla Red Custom
            }
        }
    }
    
    # 2. Ejecutar Integrador
    logger.info(f"📤 Enviando Request: {input_request['service_request']}")
    response = integrator_node.dispatch(input_request)
    
    # 3. Validar Output
    if response.get("success"):
        summary = response.get("summary", {})
        timings = summary.get("timings_ms", {})
        doc = response.get("document", {})
        
        logger.info("✅ Integración Exitosa!")
        logger.info(f"   ⏱️ Latencia N02 (Enriquecimiento): {timings.get('N02_Latency')} ms")
        logger.info(f"   ⏱️ Latencia N04 (Generación): {timings.get('N04_Latency')} ms")
        logger.info(f"   ⏱️ Tiempo Total: {summary.get('total_process_ms')} ms")
        logger.info(f"   💰 Costo Total Calculado: S/ {summary.get('total_cost')}")
        logger.info(f"   📄 Archivo Generado: {doc.get('url')}")
        
        # Validación de Negocio
        if summary.get("total_cost", 0) <= 0:
             logger.error("❌ FALLO: El costo total es 0. N02 no devolvió precios o N06 no calculó bien.")
        else:
             logger.info("✅ Validación de Costos: OK (> 0)")
             
    else:
        logger.error(f"❌ FALLO CRÍTICO: {response.get('error')}")
        logger.error(f"   Timings partial: {response.get('timings_ms')}")
        # Print FULL response for debug
        print(f"DEBUG RESPONSE: {response}", file=sys.stderr)

if __name__ == "__main__":
    test_circular_flow()
