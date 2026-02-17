"""
Script de Verificación N02 - List All Services.
"""
import sys
import os
from pathlib import Path

# Setup paths
current_dir = Path(__file__).parent
backend_dir = current_dir.parent.parent
sys.path.append(str(backend_dir))

from modules.N02_Pili_Logic.knowledge_db import SessionLocal, PiliService, PiliKnowledgeItem

def list_services():
    session = SessionLocal()
    try:
        services = session.query(PiliService).all()
        print("📋 SERVICIOS EN BD:")
        for s in services:
            count = session.query(PiliKnowledgeItem).filter_by(service_id=s.id).count()
            print(f"   - Key: '{s.service_key}' | ID: {s.id} | Name: {s.display_name} | Items: {count}")
            
    finally:
        session.close()

if __name__ == "__main__":
    list_services()
