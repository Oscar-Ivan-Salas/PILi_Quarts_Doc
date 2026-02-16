"""
Create project manually with complete data
"""
import sys
sys.path.insert(0, 'e:/PILi_Quarts/workspace-modern/backend')

from modules.pili.db.database import SessionLocal
from modules.pili.db.models import Project
from decimal import Decimal
from datetime import datetime, timedelta

db = SessionLocal()

try:
    # Check if project exists
    project = db.query(Project).filter(Project.id == "default-project-1").first()
    
    if project:
        print(f"Project already exists: {project.nombre}")
    else:
        print("Creating project 'default-project-1'...")
        
        project = Project(
            id="default-project-1",
            user_id="b2289941-d90c-4d48-b8c2-6e3fafe88944",
            client_id="client-001",
            document_type_id="cotizacion_simple",
            numero_proyecto="COT-2026-001",
            nombre="Instalacion Electrica Oficinas",
            descripcion="Instalacion electrica completa para oficinas administrativas",
            tipo_documento="cotizacion_simple",
            estado="draft",
            prioridad="normal",
            subtotal=Decimal("5615.00"),
            monto_igv=Decimal("1010.70"),
            total=Decimal("6625.70"),
            fecha_emision=datetime.now(),
            fecha_vigencia=datetime.now() + timedelta(days=30),
            created_by="b2289941-d90c-4d48-b8c2-6e3fafe88944",
            state_json={
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
        )
        
        db.add(project)
        db.commit()
        print("SUCCESS! Project created with complete state_json.")
        
        # Verify
        db.refresh(project)
        print(f"\nVerification:")
        print(f"  ID: {project.id}")
        print(f"  Name: {project.nombre}")
        print(f"  Has state_json: {project.state_json is not None}")
        if project.state_json:
            print(f"  Has 'cliente': {'cliente' in project.state_json}")
            print(f"  Has 'items': {'items' in project.state_json}")
            print(f"  Items count: {len(project.state_json.get('items', []))}")
            print(f"  Total: {project.state_json.get('total', 0)}")

finally:
    db.close()
