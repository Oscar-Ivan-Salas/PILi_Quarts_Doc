"""
Script de Verificación N02 - Deep Dive.
Lista las claves almacenadas para diagnóstico.
"""
import sys
import os
from pathlib import Path

# Setup paths
current_dir = Path(__file__).parent
backend_dir = current_dir.parent.parent
sys.path.append(str(backend_dir))

from modules.N02_Pili_Logic.knowledge_db import SessionLocal, PiliService, PiliKnowledgeItem

def deep_verify():
    session = SessionLocal()
    try:
        service_key = "puesta_tierra"
        service = session.query(PiliService).filter(PiliService.service_key.like(f"%{service_key}%")).first()
        
        if service:
            print(f"✅ Servicio Encontrado: {service.display_name} (ID: {service.id})")
            items = session.query(PiliKnowledgeItem).filter_by(service_id=service.id).all()
            print(f"📦 Items encontrados: {len(items)}")
            for item in items:
                print(f"   - Key: '{item.item_key}' | Price: {item.unit_price}")
        else:
            print(f"❌ Servicio '{service_key}' NO encontrado.")
            
    finally:
        session.close()

if __name__ == "__main__":
    deep_verify()
