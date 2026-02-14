"""
Script de Sembrado R.A.L.F. - Electricidad.
Configura Lógica y Plantillas para la Prueba de Hipótesis N04.
"""
import sys
import os
from pathlib import Path

# Setup paths
current_dir = Path(__file__).parent
backend_dir = current_dir.parent.parent
sys.path.append(str(backend_dir))

from modules.N02_Pili_Logic.knowledge_db import init_db, SessionLocal, PiliService, PiliKnowledgeItem, PiliTemplateConfig

def seed_ralf():
    print("🌱 Iniciando Sembrado R.A.L.F. (Electricidad)...")
    init_db() # Ensure tables exist
    
    session = SessionLocal()
    try:
        # 1. Service: Electricidad
        service_key = "electricidad"
        service = session.query(PiliService).filter_by(service_key=service_key).first()
        
        if not service:
            service = PiliService(
                service_key=service_key,
                display_name="Electricidad Industrial",
                normativa_referencia="CNE Suministro 2011",
                descripcion="Instalaciones Eléctricas de Alta Demanda"
            )
            session.add(service)
            session.commit()
            print(f"   ✅ Servicio Creado: {service.display_name}")
        else:
            print(f"   ℹ️ Servicio Existente: {service.display_name}")

        # 2. Template Config (The Hypothesys)
        # Service 1 (Electricidad) + Doc 2 (Cotizacion Compleja) -> Template "ELECTRICIDAD_COT_COMPLEJA"
        doc_type = 2
        template_ref = "ELECTRICIDAD_COT_COMPLEJA"
        
        config = session.query(PiliTemplateConfig).filter_by(service_id=service.id, document_type_id=doc_type).first()
        if not config:
            config = PiliTemplateConfig(
                service_id=service.id,
                document_type_id=doc_type,
                template_ref=template_ref,
                logic_class="ElectricidadLogic",
                css_ref="style.css"
            )
            session.add(config)
            print(f"   ✅ Regla de Negocio Agregada: {template_ref} -> ID {doc_type}")
        else:
            config.template_ref = template_ref
            print(f"   ℹ️ Regla Actualizada: {template_ref}")
            
        # 3. Items (Data for the test)
        items_data = [
            {"key": "tablero_industrial", "desc": "Tablero General Autosoportado", "unit": "und", "price": 4500.00},
            {"key": "cable_35mm_lshf", "desc": "Cable N2XOH 35mm2 (Libre Halógenos)", "unit": "m", "price": 45.50},
            {"key": "interruptor_3x100a", "desc": "Interruptor Termomagnético 3x100A 35kA", "unit": "und", "price": 850.00},
            {"key": "mano_obra_calificada", "desc": "Servicio de Instalación y Peinado de Tablero", "unit": "glba", "price": 1200.00}
        ]
        
        for i_data in items_data:
            ukey = f"GLOBAL_{i_data['key']}"
            existing = session.query(PiliKnowledgeItem).filter_by(service_id=service.id, item_key=ukey).first()
            if not existing:
                item = PiliKnowledgeItem(
                    service_id=service.id,
                    category="MATERIAL",
                    item_key=ukey,
                    item_description=i_data["desc"],
                    unit_measure=i_data["unit"],
                    unit_price=i_data["price"],
                    currency="PEN"
                )
                session.add(item)
                print(f"   + Item: {i_data['desc']}")
        
        session.commit()
        print("🏁 Sembrado Completo.")

    except Exception as e:
        print(f"❌ Error: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    seed_ralf()
