
import os
import sys
import logging
import json
from pathlib import Path

# Setup Path to root
sys.path.append(str(Path(__file__).parent.parent.parent))

from modules.N06_Integrator.index import integrator_node

# Configure Logger
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("integration_test_debug.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("Integration_Test_3x3x6")

# --- DATA MOCKING (R.A.L.F.T.H Step 1) ---

# 1. USERS (The Engineering Team)
USERS = [
    {
        "id": "USR-001-RALFTH",
        "name": "Ing. Oscar Salas",
        "role": "Gerente de Proyectos",
        "branding": {
             "logo_b64": None, # Will use default Tesla
             "color_hex": "#0052A3" # Tesla Blue
        }
    },
    {
        "id": "USR-002-SR",
        "name": "Ing. Senior Electricista",
        "role": "Residente de Obra",
        "branding": {
             "logo_b64": None,
             "color_hex": "#CC0000" # Safety Red
        }
    },
    {
        "id": "USR-003-JR",
        "name": "Téc. Especialista",
        "role": "Supervisor de Campo",
        "branding": {
             "logo_b64": None,
             "color_hex": "#009900" # Field Green
        }
    }
]

# 2. CLIENTS (Real RUCs)
CLIENTS = [
    {
        "nombre": "MINERA LAS BAMBAS S.A.",
        "ruc": "20601138787",
        "direccion": "Av. El Derby 055, Surco, Lima",
        "fecha": "15/02/2026"
    },
    {
        "nombre": "CEMENTIOS PACASMAYO S.A.A.",
        "ruc": "20100128218",
        "direccion": "Calle La Colonia 150, Surco, Lima",
        "fecha": "16/02/2026"
    },
    {
        "nombre": "TOTAL ARTEFACTOS S.A.",
        "ruc": "20100070970",
        "direccion": "Av. Nicolas de Ayllon 2410, Ate, Lima",
        "fecha": "17/02/2026"
    }
]

# 3. MODELS (The 6 Pillars)
MODELS = [
    {"id": 1, "key": "pozo-tierra", "name": "Cotizacion_Simple"},
    {"id": 2, "key": "subestacion-hv", "name": "Cotizacion_Compleja"},
    {"id": 3, "key": "mantenimiento-preventivo", "name": "Proyecto_Simple"},
    {"id": 4, "key": "montaje-electromecanico", "name": "Proyecto_Complejo"},
    {"id": 5, "key": "auditoria-calidad", "name": "Informe_Tecnico"},
    {"id": 6, "key": "consultoria-energetica", "name": "Informe_Ejecutivo"}
]

OUTPUT_BASE = Path(__file__).parent.parent.parent / "storage" / "integracion_test"

def run_integration_3x3x6():
    logger.info("🚀 INICIANDO PRUEBA DE INTEGRACIÓN 3x3x6 (R.A.L.F.T.H)")
    logger.info(f"📂 Output: {OUTPUT_BASE}")
    
    os.makedirs(OUTPUT_BASE, exist_ok=True)
    
    total_files = 0
    errors = 0
    
    # TRIPLE LOOP: USER -> CLIENT -> MODEL
    for user in USERS:
        user_dir = OUTPUT_BASE / f"{user['id']}_{user['name'].replace(' ', '_')}"
        os.makedirs(user_dir, exist_ok=True)
        
        logger.info(f"👤 Procesando Usuario: {user['name']} ({user['id']})")
        
        for client in CLIENTS:
            logger.info(f"  🏢 Cliente: {client['nombre']}")
            
            for model in MODELS:
                # We need 3 formats: XLSX, DOCX, PDF
                formats = ["XLSX", "DOCX", "PDF"]
                
                for fmt in formats:
                    # Construct Request Payload for N06
                    payload = {
                        "client_info": client,
                        "service_request": {
                            "service_key": model["key"],
                            "document_model_id": model["id"],
                            "quantity": 1
                        },
                        "user_context": {
                            "user_id": user["id"],
                            "branding": user["branding"]
                        },
                        "emisor": { # Simulate Frontend Form Data
                            "nombre": "TESLA PROYECTOS Y MANTENIMIENTO S.C.R.L.",
                            "ruc": "20601138787",
                            "direccion": "Calle Los Negocios 123",
                            "logo": None, # Default
                            "color_hex": user["branding"]["color_hex"]
                        },
                        "output_format": fmt
                    }
                    
                    try:
                        # 💥 FIRE DISPATCH 💥
                        response = integrator_node.dispatch(payload)
                        
                        if response["success"]:
                            # Save file from B64
                            import base64
                            file_data = base64.b64decode(response["document"]["b64_preview"])
                            
                            # Naming Convention: CLIENT_MODEL_USER.fmt
                            # e.g. BAMBAS_Cotizacion_Simple_USR001.xlsx
                            # Use filename from N04 (via N06 document.url) if available (Strict Naming)
                            n06_doc = response.get("document", {})
                            if n06_doc.get("url"):
                                filename = n06_doc["url"]
                            else:
                                safe_client = client["nombre"].split()[0]
                                filename = f"{safe_client}_{model['name']}_{fmt}.{fmt.lower()}"
                            
                            file_path = user_dir / filename
                            
                            with open(file_path, "wb") as f:
                                f.write(file_data)
                                
                            total_files += 1
                            # logger.info(f"    ✅ Generated: {filename}") # Reduce noise
                        else:
                            print(f"❌ ERROR {model['name']} {fmt}: {response.get('error')}")
                            logger.error(f"    ❌ Failed {model['name']} {fmt}: {response.get('error')}")
                            errors += 1
                            
                    except Exception as e:
                        print(f"❌ EXCEPTION {model['name']} {fmt}: {e}")
                        logger.error(f"    ❌ Exception {model['name']} {fmt}: {e}")
                        errors += 1
                        
    logger.info("========================================")
    logger.info(f"🏁 PRUEBA COMPLETADA")
    logger.info(f"📄 Archivos Generados: {total_files}/54 Esperados")
    logger.info(f"❌ Errores: {errors}")
    logger.info("========================================")

if __name__ == "__main__":
    run_integration_3x3x6()
