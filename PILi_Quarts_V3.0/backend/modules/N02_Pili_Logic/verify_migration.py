"""
Script de Verificación N02.
Verifica que la base de datos ha sido poblada correctamente.
"""
import sys
import os
from pathlib import Path

# Setup paths
current_dir = Path(__file__).parent
backend_dir = current_dir.parent.parent
sys.path.append(str(backend_dir))

from modules.N02_Pili_Logic.knowledge_db import SessionLocal, PiliService, PiliKnowledgeItem

def verify():
    session = SessionLocal()
    try:
        n_services = session.query(PiliService).count()
        n_items = session.query(PiliKnowledgeItem).count()
        
        print(f"✅ SERVICIOS: {n_services}")
        print(f"✅ ITEMS DE CONOCIMIENTO: {n_items}")
        
        if n_services > 0 and n_items > 0:
            print("🎉 Verificación Exitosa: La base de datos contiene conocimiento.")
            
            # Muestra un ejemplo
            example = session.query(PiliKnowledgeItem).first()
            print(f"🔍 Ejemplo: {example.item_description} = {example.unit_price} {example.currency}")
            
        else:
            print("⚠️ ADVERTENCIA: Base de datos vacía o incompleta.")
            
    finally:
        session.close()

if __name__ == "__main__":
    verify()
