"""
Quick verification and fix script for project state_json
"""
import sys
sys.path.insert(0, 'e:/PILi_Quarts/workspace-modern/backend')

from modules.pili.db.database import SessionLocal
from modules.pili.db.models import Project
from decimal import Decimal
from datetime import datetime, timedelta

db = SessionLocal()

try:
    # Get project
    project = db.query(Project).filter(Project.id == "default-project-1").first()
    
    if not project:
        print("ERROR: Project not found!")
        sys.exit(1)
    
    print(f"Project found: {project.nombre}")
    print(f"Has state_json: {project.state_json is not None}")
    
    if project.state_json:
        print(f"state_json keys: {list(project.state_json.keys())}")
        print(f"Has 'cliente': {'cliente' in project.state_json}")
        print(f"Has 'items': {'items' in project.state_json}")
    else:
        print("\nWARNING: state_json is None! Fixing...")
        
        # Fix it
        project.state_json = {
            "cliente": {
                "nombre": "Constructora Los Andes S.A.C.",
                "ruc": "20123456789",
                "direccion": "Av. Javier Prado 456, San Isidro, Lima",
                "contacto": "Ing. Carlos Mendoza",
                "telefono": "+51 987 654 321",
                "email": "contacto@losandes.com"
            },
            "proyecto": "Instalacion Electrica para Oficinas Administrativas",
            "numero": "COT-2026-001",
            "fecha": datetime.now().strftime("%Y-%m-%d"),
            "vigencia": "30 dias calendario",
            "area_m2": "150",
            "servicio": "Instalaciones Electricas",
            "servicio_nombre": "Instalacion Electrica Completa",
            "descripcion": "Instalacion electrica completa para oficinas administrativas de 150m2, incluyendo tableros, circuitos, iluminacion y tomacorrientes.",
            "items": [
                {
                    "item": "01",
                    "descripcion": "Tablero electrico trifasico 380V",
                    "unidad": "und",
                    "cantidad": 1,
                    "precio_unitario": 850.00,
                    "subtotal": 850.00
                },
                {
                    "item": "02",
                    "descripcion": "Circuitos derivados (iluminacion y tomacorrientes)",
                    "unidad": "pto",
                    "cantidad": 12,
                    "precio_unitario": 120.00,
                    "subtotal": 1440.00
                },
                {
                    "item": "03",
                    "descripcion": "Luminarias LED 36W empotradas",
                    "unidad": "und",
                    "cantidad": 20,
                    "precio_unitario": 85.00,
                    "subtotal": 1700.00
                },
                {
                    "item": "04",
                    "descripcion": "Tomacorrientes dobles con linea a tierra",
                    "unidad": "und",
                    "cantidad": 15,
                    "precio_unitario": 45.00,
                    "subtotal": 675.00
                },
                {
                    "item": "05",
                    "descripcion": "Sistema de puesta a tierra",
                    "unidad": "glb",
                    "cantidad": 1,
                    "precio_unitario": 950.00,
                    "subtotal": 950.00
                }
            ],
            "subtotal": 5615.00,
            "igv": 1010.70,
            "total": 6625.70,
            "normativa": "CNE Suministro 2011, NTP 370.252",
            "observaciones": "Incluye materiales, mano de obra y pruebas de funcionamiento. No incluye obra civil."
        }
        
        db.commit()
        print("FIXED! state_json updated and committed.")
        
        # Verify
        db.refresh(project)
        print(f"\nVerification:")
        print(f"Has state_json: {project.state_json is not None}")
        if project.state_json:
            print(f"Has 'cliente': {'cliente' in project.state_json}")
            print(f"Has 'items': {'items' in project.state_json}")
            print(f"Items count: {len(project.state_json.get('items', []))}")

finally:
    db.close()
