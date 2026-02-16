"""
Script de Sembrado Manual para Pozo a Tierra (N02).
Restaura o inicializa los precios base para el servicio de Pozo a Tierra.
"""
import sys
import os
from pathlib import Path

# Setup paths
current_dir = Path(__file__).parent
backend_dir = current_dir.parent.parent
sys.path.append(str(backend_dir))

from modules.N02_Pili_Logic.knowledge_db import SessionLocal, PiliService, PiliKnowledgeItem

def seed_pozo_tierra():
    session = SessionLocal()
    try:
        # 1. Get Service
        service_key = "pozo-tierra"
        service = session.query(PiliService).filter_by(service_key=service_key).first()
        
        if not service:
            print(f"⚠️ Service {service_key} not found. Creating...")
            service = PiliService(
                service_key=service_key, 
                display_name="Pozo a Tierra", 
                normativa_referencia="CNE Utilización 060-712",
                descripcion="Sistemas de Puesta a Tierra Vertical y Horizontal"
            )
            session.add(service)
            session.commit()
        
        print(f"✅ Service: {service.display_name} (ID: {service.id}) using Key: {service.service_key}")

        # 2. Define Items (Standard Market Prices)
        items_to_seed = [
            {"key": "varilla_cobre_3_4", "desc": "Varilla de Cobre 3/4 x 2.40m", "unit": "und", "price": 280.00},
            {"key": "cemento_conductivo", "desc": "Saco de Cemento Conductivo 25kg", "unit": "sco", "price": 120.00},
            {"key": "caja_registro", "desc": "Caja de Registro de Concreto con Tapa", "unit": "und", "price": 85.00},
            {"key": "conector_ab", "desc": "Conector AB de Bronce 3/4", "unit": "und", "price": 25.00},
            {"key": "dosis_quimica", "desc": "Dosis Química (Thor Gel / Similar)", "unit": "kit", "price": 180.00},
            {"key": "tierra_cultivo", "desc": "Tierra de Cultivo Zarandeada", "unit": "m3", "price": 150.00},
            {"key": "mano_obra_pozo", "desc": "Mano de Obra Especializada (Excavación e Instalación)", "unit": "glba", "price": 600.00},
            {"key": "protocolo", "desc": "Protocolo de Medición y Certificado Firmado", "unit": "und", "price": 350.00},
            {"key": "cable_desnudo_35mm", "desc": "Cable de Cobre Desnudo 35mm2", "unit": "m", "price": 35.00},
        ]

        # 3. Insert Items
        added_count = 0
        for item_data in items_to_seed:
            # Check exist
            unique_key = f"GLOBAL_{item_data['key']}"
            existing = session.query(PiliKnowledgeItem).filter_by(service_id=service.id, item_key=unique_key).first()
            
            if not existing:
                new_item = PiliKnowledgeItem(
                    service_id=service.id,
                    category="MATERIAL",
                    item_key=unique_key,
                    item_description=item_data["desc"],
                    unit_measure=item_data["unit"],
                    unit_price=item_data["price"],
                    currency="PEN"
                )
                session.add(new_item)
                added_count += 1
                print(f"   + Added: {item_data['desc']}")
            else:
                # Update price just in case
                existing.unit_price = item_data["price"]
                print(f"   . Updated: {item_data['desc']}")
        
        session.commit()
        print(f"🎉 Seeding Complete. Added {added_count} items to Pozo a Tierra.")

    except Exception as e:
        print(f"❌ Error seeding: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    seed_pozo_tierra()
