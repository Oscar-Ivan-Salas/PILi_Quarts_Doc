"""
Script N06 - EXECUTE_BATCH_PRODUCTION.py
Ejecuta la producción masiva de documentos inyectando datos reales de N08 (Identidad) y N02 (Conocimiento)
en la Fábrica Binaria N04.

Misión: Validar "De la BD al Documento".
"""
import sys
import os
import logging
from pathlib import Path
import random

# Setup paths to allow imports from backend root
# Assuming script is run from project root (e.g. python backend/EXECUTE_BATCH_PRODUCTION.py)
# so backend/ is in path.
BASE_DIR = Path(__file__).resolve().parent.parent # e:\PILi_Quarts\workspace-modern\backend
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

# Config Logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("N06_MASS_PROD")

from modules.N08_User_Management.identity_db import SessionLocal as IdentitySession, UsuarioEjecutor, ClienteFinal
from modules.N02_Pili_Logic.knowledge_db import SessionLocal as KnowledgeSession, PiliKnowledgeItem, PiliService
from modules.N04_Binary_Factory.index import binary_factory

OUTPUT_DIR = Path("output/GENERACION_VALIDADA")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def run_mass_production():
    logger.info("🏭 INICIANDO PRODUCCIÓN MASIVA N06...")
    
    # 1. Extracción de Datos (N08)
    logger.info("🔍 Extrayendo datos de Identidad (N08)...")
    id_db = IdentitySession()
    users = id_db.query(UsuarioEjecutor).limit(5).all()
    clients = id_db.query(ClienteFinal).limit(5).all()
    id_db.close()
    
    if not users or not clients:
        logger.error("❌ No se encontraron usuarios o clientes en N08. Ejecuta el seed primero.")
        return

    logger.info(f"✅ Encontrados: {len(users)} Usuarios, {len(clients)} Clientes.")

    # 2. Extracción de Conocimiento (N02)
    logger.info("🧠 Extrayendo items de Electricidad (N02)...")
    kn_db = KnowledgeSession()
    # Find electricity service
    elec_service = kn_db.query(PiliService).filter(PiliService.service_key.like("%electricidad%")).first()
    
    if not elec_service:
        # Fallback to any service
        elec_service = kn_db.query(PiliService).first()
        
    items = []
    if elec_service:
        items = kn_db.query(PiliKnowledgeItem).filter(PiliKnowledgeItem.service_id == elec_service.id).limit(10).all()
    
    kn_db.close()
    
    if not items:
        logger.warning("⚠️ No items en N02. Usando Mock Data.")
        items_data = [
            {"descripcion": "Instalación de Punto de Luz (Mock)", "cantidad": 10, "precio_unitario": 80.0, "unidad": "und"},
            {"descripcion": "Tablero General (Mock)", "cantidad": 1, "precio_unitario": 1500.0, "unidad": "glb"}
        ]
    else:
        logger.info(f"✅ Encontrados {len(items)} items de {elec_service.display_name}")
        items_data = []
        for i in items:
            items_data.append({
                "descripcion": i.item_description,
                "cantidad": random.randint(1, 20),
                "precio_unitario": i.unit_price,
                "unidad": i.unit_measure,
                # Calculate total later
            })

    # 3. Ciclo de Producción
    generated_count = 0
    
    for user_idx, user in enumerate(users):
        client = clients[user_idx % len(clients)] # Round robin clients
        
        logger.info(f"🔨 Procesando: {user.user_key} -> {client.razon_social}")
        
        # Prepare Payload
        current_items = []
        subtotal = 0
        for item in items_data:
            qty = item["cantidad"]
            price = item["precio_unitario"]
            total = qty * price
            subtotal += total
            
            p_item = item.copy()
            p_item["total"] = total
            current_items.append(p_item)
            
        igv = subtotal * 0.18
        total_doc = subtotal + igv
        
        payload = {
            "items": current_items,
            "totals": {
                "subtotal": subtotal,
                "igv": igv,
                "total": total_doc,
                "currency": "PEN"
            },
            "client_info": {
                "nombre": client.razon_social,
                "ruc": client.ruc_dni,
                "direccion": client.direccion,
                "fecha": "2026-02-13"
            },
            "technical_notes": "Generado automáticamente por N06 Integrator."
        }
        
        branding = {
            "color_hex": getattr(user, "colores_hex", {}).get("primary", "#CC0000") if user.colores_hex else "#CC0000",
            # Logo logic could go here
        }
        
        # Requests
        # 1. Cotizacion Simple (PDF) - ID 1
        # 2. Cotizacion Compleja (DOCX) - ID 2 / Template "COTIZACION_MODELO_A"
        
        requests = [
            # PDF Format
            {
                "header": {"user_id": user.user_key, "service_id": 1, "document_type": "ELECTRICIDAD_COTIZACION_SIMPLE"}, 
                "branding": branding,
                "payload": payload,
                "output_format": "PDF"
            },
             # Word Format
            {
                "header": {"user_id": user.user_key, "service_id": 1, "document_type": "ELECTRICIDAD_COT_COMPLEJA"},
                "branding": branding,
                "payload": payload,
                "output_format": "DOCX"
            },
            # Excel Format
            {
                 "header": {"user_id": user.user_key, "service_id": 3, "document_type": "ELECTRICIDAD_CUADRO_CARGAS"},
                 "branding": branding,
                 "payload": payload,
                 "output_format": "XLSX"
            }
        ]
        
        import time
        timestamp = int(time.time())
        
        for req in requests:
            res = binary_factory.process_request(req)
            if res.get("success"):
                filename = f"{user.user_key}_{client.ruc_dni}_{res.get('filename').replace('.', f'_{timestamp}.')}"
                filepath = OUTPUT_DIR / filename
                
                try:
                    with open(filepath, "wb") as f:
                        f.write(base64.b64decode(res.get("file_b64")))
                    
                    logger.info(f"   💾 Generado: {filename}")
                    generated_count += 1
                except Exception as e:
                    logger.error(f"   ❌ Error Guardando {filename}: {e}")
            else:
                logger.error(f"   ❌ Fallo: {res.get('error')}")

    logger.info(f"🏁 Producción Finalizada. Total Documentos: {generated_count}")
    logger.info(f"📂 Ubicación: {OUTPUT_DIR.resolve()}")

if __name__ == "__main__":
    run_mass_production()
