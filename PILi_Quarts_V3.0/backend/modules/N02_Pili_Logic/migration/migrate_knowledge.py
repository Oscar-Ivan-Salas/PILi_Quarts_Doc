
"""
Script de Migración de Conocimiento (ETL).
Extrae el conocimiento hardcodeado de pili_local_specialists.py y lo carga en SQLite.
"""
import sys
import os
import logging
from pathlib import Path

# Setup paths
current_dir = Path(__file__).parent
n02_dir = current_dir.parent
backend_dir = n02_dir.parent.parent
sys.path.append(str(backend_dir))

# Config logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("N02_Migration")

# Import DB models
from modules.N02_Pili_Logic.knowledge_db import init_db, SessionLocal, PiliService, PiliKnowledgeItem, PiliRule

# Import Legacy Data Source (The Tumor) via File Path (Robust)
try:
    backup_path = backend_dir / "modules" / "pili" / "legacy" / "quarantine" / "pili_local_specialists_backup.py"
    if not backup_path.exists():
        logger.error(f"❌ Backup file not found at: {backup_path}")
        sys.exit(1)
        
    # Load file content
    with open(backup_path, "r", encoding="utf-8") as f:
        code = f.read()
        
    # Execute safely to extract KNOWLEDGE_BASE
    context = {}
    try:
        exec(code, context)
    except Exception as exec_error:
        # Ignore errors regarding missing imports inside the backup file (like 'import re')
        # We only care about KNOWLEDGE_BASE definition
        logger.warning(f"⚠️ Warning during exec (might be benign): {exec_error}")
    
    if "KNOWLEDGE_BASE" in context:
        KNOWLEDGE_BASE = context["KNOWLEDGE_BASE"]
        logger.info(f"✅ KNOWLEDGE_BASE (Backup) cargada vía exec. Tamaño: {len(KNOWLEDGE_BASE)} claves de primer nivel.")
    else:
        logger.error("❌ KNOWLEDGE_BASE not found in backup file execution.")
        sys.exit(1)

except Exception as e:
    logger.error(f"❌ Critical Error loading backup: {e}")
    sys.exit(1)

def migrate_data():
    session = SessionLocal()
    
    try:
        # 1. Initialize DB
        init_db()
        
        # 2. Iterate Services
        print(f"DEBUG: Processing {len(KNOWLEDGE_BASE)} services...")
        for service_key, service_data in KNOWLEDGE_BASE.items():
            print(f"Processing Service: {service_key}")
            display_name = service_key.replace("_", " ").title()
            normativa = service_data.get("normativa", "N/A")
            
            # Check structure keys
            print(f"   Keys found: {list(service_data.keys())}")
            
            # Check if exists
            service = session.query(PiliService).filter_by(service_key=service_key).first()
            if not service:
                service = PiliService(
                    service_key=service_key,
                    display_name=display_name,
                    normativa_referencia=normativa,
                    descripcion=f"Servicio especializado: {display_name}"
                )
                session.add(service)
                session.commit()
                logger.info(f"➕ Servicio creado: {display_name}")
            else:
                service.normativa_referencia = normativa # Update metadata just in case
                session.commit()

            # 3. Extract Knowledge Items (Prices/Materials)
            
            # Structure A: 'tipos' -> 'SUBTYPE' -> 'precios'
            if "tipos" in service_data:
                types_dict = service_data["tipos"]
                if isinstance(types_dict, dict):
                    for subtype_key, subtype_data in types_dict.items():
                        if isinstance(subtype_data, dict) and "precios" in subtype_data:
                             precios = subtype_data["precios"]
                             for item_key, price in precios.items():
                                 desc = f"{subtype_key} - {item_key.replace('_', ' ').capitalize()}"
                                 
                                 # Unique constraint check (service_id + item_key)
                                 # We define item_key as 'SUBTYPE_KEY' for A
                                 unique_key = f"{subtype_key}_{item_key}"
                                 
                                 existing_item = session.query(PiliKnowledgeItem).filter_by(
                                     service_id=service.id, 
                                     item_key=unique_key
                                 ).first()
                                 
                                 if not existing_item:
                                     item = PiliKnowledgeItem(
                                         service_id=service.id,
                                         category="GENERAL", 
                                         item_key=unique_key,
                                         item_description=desc,
                                         unit_measure="und", 
                                         unit_price=float(price),
                                         currency="PEN" if "sol" not in str(price).lower() else "PEN"
                                     )
                                     session.add(item)
            
            # Structure B: 'precios_municipales' (ITSE)
            if "precios_municipales" in service_data:
                 precios = service_data["precios_municipales"]
                 for item_key, item_data in precios.items():
                      if isinstance(item_data, dict) and "precio" in item_data:
                           price = item_data["precio"]
                           desc = f"ITSE Municipal - {item_data.get('descripcion', item_key)}"
                           unique_key = f"GLOBAL_{item_key}"
                           
                           existing_item = session.query(PiliKnowledgeItem).filter_by(
                                     service_id=service.id, 
                                     item_key=unique_key
                                 ).first()
                           
                           if not existing_item:
                                 item = PiliKnowledgeItem(
                                     service_id=service.id,
                                     category="TASA_MUNICIPAL",
                                     item_key=unique_key,
                                     item_description=desc,
                                     unit_measure="glba",
                                     unit_price=float(price),
                                     currency="PEN"
                                 )
                                 session.add(item)

            # Structure C: Root level 'precios' (Pozo Tierra, etc.)
            if "precios" in service_data:
                 precios = service_data["precios"]
                 if isinstance(precios, dict):
                     for item_key, price in precios.items():
                         # For root items, we prefix with GLOBAL or similar to avoid collision? 
                         # Or just use key. Let's use GLOBAL_ if not colliding.
                         # Actually for pozo-tierra it's unique enough.
                         desc = f"{display_name} - {item_key.replace('_', ' ').capitalize()}"
                         unique_key = f"GLOBAL_{item_key}"

                         existing_item = session.query(PiliKnowledgeItem).filter_by(
                                     service_id=service.id, 
                                     item_key=unique_key
                                 ).first()
                         
                         if not existing_item:
                                 item = PiliKnowledgeItem(
                                     service_id=service.id,
                                     category="GENERAL",
                                     item_key=unique_key,
                                     item_description=desc,
                                     unit_measure="und",
                                     unit_price=float(price),
                                     currency="PEN"
                                 )
                                 session.add(item)

            # Structure D: 'sistemas' with nested 'precios'
            if "sistemas" in service_data:
                 sistemas_dict = service_data["sistemas"]
                 if isinstance(sistemas_dict, dict):
                    for subt_key, subt_data in sistemas_dict.items():
                         if isinstance(subt_data, dict) and "precios" in subt_data:
                             precios = subt_data["precios"]
                             for item_key, price in precios.items():
                                 desc = f"{subt_key} - {item_key.replace('_', ' ').capitalize()}"
                                 unique_key = f"{subt_key}_{item_key}"
                                 
                                 existing_item = session.query(PiliKnowledgeItem).filter_by(
                                     service_id=service.id, item_key=unique_key).first()
                                 if not existing_item:
                                     item = PiliKnowledgeItem(
                                         service_id=service.id,
                                         category="SISTEMA",
                                         item_key=unique_key,
                                         item_description=desc,
                                         unit_measure="und",
                                         unit_price=float(price),
                                         currency="PEN"
                                     )
                                     session.add(item)

            session.commit()
            logger.info(f"✅ Datos migrados para servicio: {service_key}")

    except Exception as e:
        session.rollback()
        logger.error(f"❌ Error crítico en migración: {e}", exc_info=True)
    finally:
        session.close()

if __name__ == "__main__":
    logger.info("🚀 Iniciando migración de conocimiento a SQLite...")
    migrate_data()
    logger.info("🏁 Migración finalizada.")
