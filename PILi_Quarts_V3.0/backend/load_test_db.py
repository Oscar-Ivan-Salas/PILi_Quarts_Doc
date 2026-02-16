"""
Database Load Testing Script
Generates 50 users with complete realistic data
"""
import sys
sys.path.insert(0, 'e:/PILi_Quarts/workspace-modern/backend')

from modules.pili.db.database import SessionLocal
from modules.pili.db.models import User, Client, Project, DocumentType, ProjectItem, PriceReference
from decimal import Decimal
from datetime import datetime, timedelta
import random
import uuid

# Realistic data pools
NOMBRES_EMPRESAS = [
    "Constructora", "Ingenieria", "Servicios", "Tecnologia", "Consultoria",
    "Desarrollo", "Infraestructura", "Proyectos", "Soluciones", "Sistemas"
]

APELLIDOS_EMPRESAS = [
    "del Norte", "del Sur", "del Este", "del Oeste", "Central",
    "Asociados", "y Cia", "Group", "Internacional", "Peru",
    "SAC", "EIRL", "SRL", "SA", "Ingenieros"
]

CIUDADES_PERU = [
    "Lima", "Arequipa", "Cusco", "Trujillo", "Chiclayo",
    "Piura", "Iquitos", "Huancayo", "Tacna", "Pucallpa",
    "Callao", "Cajamarca", "Ayacucho", "Juliaca", "Ica"
]

INDUSTRIAS = [
    "construccion", "industrial", "comercial", "mineria", "energia",
    "telecomunicaciones", "educacion", "salud", "retail", "manufactura"
]

NOMBRES_PERSONAS = [
    "Carlos", "Maria", "Juan", "Ana", "Luis", "Rosa", "Pedro", "Carmen",
    "Jorge", "Patricia", "Miguel", "Laura", "Ricardo", "Sofia", "Fernando"
]

APELLIDOS_PERSONAS = [
    "Garcia", "Rodriguez", "Martinez", "Lopez", "Gonzalez", "Perez",
    "Sanchez", "Ramirez", "Torres", "Flores", "Rivera", "Gomez"
]

TITULOS_PROFESIONALES = [
    "Ing. Electrico", "Ing. Civil", "Ing. Industrial", "Ing. Mecanico",
    "Arq.", "Ing. Sistemas", "Ing. Electronico", "MBA"
]

SERVICIOS = [
    "Instalacion Electrica", "Sistema de Iluminacion", "Tableros Electricos",
    "Puesta a Tierra", "Sistema de Emergencia", "Automatizacion Industrial",
    "Mantenimiento Electrico", "Auditoria Energetica"
]

def generate_ruc():
    """Generate realistic Peruvian RUC (11 digits)"""
    return f"20{random.randint(100000000, 999999999)}"

def generate_email(nombre, empresa):
    """Generate realistic email"""
    dominios = ["gmail.com", "hotmail.com", "outlook.com", "empresa.pe", "corp.pe"]
    nombre_clean = nombre.lower().replace(" ", "")
    return f"{nombre_clean}@{random.choice(dominios)}"

def generate_phone():
    """Generate Peruvian phone number"""
    return f"+51 9{random.randint(10000000, 99999999)}"

def load_test_database():
    db = SessionLocal()
    
    try:
        print("=" * 80)
        print("DATABASE LOAD TEST - Generating 50 Users with Complete Data")
        print("=" * 80)
        
        # Get existing document types
        doc_types = db.query(DocumentType).all()
        if not doc_types:
            print("ERROR: No document types found. Run seed_db.py first!")
            return
        
        # Get existing price references
        price_refs = db.query(PriceReference).all()
        if not price_refs:
            print("WARNING: No price references found. Projects will have minimal items.")
        
        users_created = 0
        clients_created = 0
        projects_created = 0
        items_created = 0
        
        for i in range(1, 51):
            print(f"\n[{i}/50] Creating user and associated data...")
            
            # 1. CREATE USER
            nombre_empresa = f"{random.choice(NOMBRES_EMPRESAS)} {random.choice(APELLIDOS_EMPRESAS)}"
            ruc_user = generate_ruc()
            
            user = User(
                id=str(uuid.uuid4()),
                email=generate_email(f"user{i}", nombre_empresa),
                password_hash=f"hash_{i}",
                razon_social=nombre_empresa,
                ruc=ruc_user,
                direccion=f"Av. {random.choice(['Los Pinos', 'Las Flores', 'Industrial', 'Comercial'])} {random.randint(100, 9999)}, {random.choice(CIUDADES_PERU)}",
                telefono=generate_phone(),
                professional_title=random.choice(TITULOS_PROFESIONALES),
                license_number=f"CIP {random.randint(100000, 999999)}",
                logo_path=f"/static/logos/user_{i}.png",
                signature_path=f"/static/signatures/user_{i}.png",
                role="user" if i > 5 else "admin",  # First 5 are admins
                is_active=True
            )
            db.add(user)
            users_created += 1
            
            # 2. CREATE 2-5 CLIENTS PER USER
            num_clients = random.randint(2, 5)
            user_clients = []
            
            for j in range(num_clients):
                nombre_cliente = f"{random.choice(NOMBRES_EMPRESAS)} {random.choice(APELLIDOS_EMPRESAS)} {random.choice(['SAC', 'EIRL', 'SRL'])}"
                contacto_nombre = f"{random.choice(NOMBRES_PERSONAS)} {random.choice(APELLIDOS_PERSONAS)}"
                
                client = Client(
                    id=str(uuid.uuid4()),
                    ruc=generate_ruc(),
                    razon_social=nombre_cliente,
                    nombre_comercial=nombre_cliente.split()[0],
                    direccion=f"Calle {random.choice(['Principal', 'Comercial', 'Industrial'])} {random.randint(100, 999)}",
                    ciudad=random.choice(CIUDADES_PERU),
                    pais="Peru",
                    email=generate_email(nombre_cliente.split()[0], "empresa"),
                    telefono=generate_phone(),
                    website=f"www.{nombre_cliente.split()[0].lower()}.com.pe",
                    contacto_persona=contacto_nombre,
                    contacto_email=generate_email(contacto_nombre.split()[0], "empresa"),
                    contacto_telefono=generate_phone(),
                    industria=random.choice(INDUSTRIAS),
                    tipo_cliente="empresa",
                    limite_credito=Decimal(random.randint(10000, 200000)),
                    terminos_pago=random.choice([15, 30, 45, 60]),
                    is_active=True,
                    notas=f"Cliente generado para pruebas de carga - Usuario {i}"
                )
                db.add(client)
                user_clients.append(client)
                clients_created += 1
            
            # 3. CREATE 3-8 PROJECTS PER USER
            num_projects = random.randint(3, 8)
            
            for k in range(num_projects):
                client = random.choice(user_clients)
                doc_type = random.choice(doc_types)
                
                # Generate project data
                servicio = random.choice(SERVICIOS)
                area = random.randint(50, 1000)
                num_items = random.randint(3, 10)
                
                # Generate items
                items_data = []
                subtotal_proyecto = 0
                
                for item_num in range(1, num_items + 1):
                    if price_refs:
                        price_ref = random.choice(price_refs)
                        cantidad = random.randint(1, 50)
                        precio_unit = float(price_ref.precio_sugerido or price_ref.precio_base)
                        subtotal_item = cantidad * precio_unit
                        
                        items_data.append({
                            "item": f"{item_num:02d}",
                            "descripcion": price_ref.nombre_item,
                            "unidad": price_ref.unidad,
                            "cantidad": cantidad,
                            "precio_unitario": precio_unit,
                            "subtotal": subtotal_item
                        })
                        subtotal_proyecto += subtotal_item
                
                igv = subtotal_proyecto * 0.18
                total = subtotal_proyecto + igv
                
                # Create project
                project_id = str(uuid.uuid4())
                project = Project(
                    id=project_id,
                    user_id=user.id,
                    client_id=client.id,
                    document_type_id=doc_type.id,
                    numero_proyecto=f"COT-{datetime.now().year}-{i:03d}-{k:02d}",
                    nombre=f"{servicio} - {client.razon_social[:30]}",
                    descripcion=f"{servicio} para {client.razon_social}. Area: {area}m2",
                    tipo_documento=doc_type.id,
                    estado=random.choice(["draft", "pending_review", "approved", "sent"]),
                    prioridad=random.choice(["normal", "normal", "normal", "high", "low"]),
                    subtotal=Decimal(str(round(subtotal_proyecto, 2))),
                    monto_igv=Decimal(str(round(igv, 2))),
                    total=Decimal(str(round(total, 2))),
                    moneda="PEN",
                    fecha_emision=datetime.now() - timedelta(days=random.randint(0, 90)),
                    fecha_vigencia=datetime.now() + timedelta(days=random.randint(15, 60)),
                    created_by=user.id,
                    state_json={
                        "cliente": {
                            "nombre": client.razon_social,
                            "ruc": client.ruc,
                            "direccion": client.direccion,
                            "contacto": client.contacto_persona,
                            "telefono": client.telefono,
                            "email": client.email
                        },
                        "proyecto": f"{servicio} - {client.razon_social[:30]}",
                        "numero": f"COT-{datetime.now().year}-{i:03d}-{k:02d}",
                        "fecha": datetime.now().strftime("%Y-%m-%d"),
                        "vigencia": f"{random.choice([15, 30, 45, 60])} dias calendario",
                        "area_m2": str(area),
                        "servicio": servicio,
                        "servicio_nombre": servicio,
                        "descripcion": f"{servicio} completo para area de {area}m2",
                        "items": items_data,
                        "subtotal": round(subtotal_proyecto, 2),
                        "igv": round(igv, 2),
                        "total": round(total, 2),
                        "normativa": "CNE Suministro 2011, NTP 370.252",
                        "observaciones": f"Proyecto generado para pruebas de carga. Usuario: {user.razon_social}"
                    }
                )
                db.add(project)
                projects_created += 1
                items_created += len(items_data)
            
            # Commit every 10 users to avoid memory issues
            if i % 10 == 0:
                db.commit()
                print(f"  Committed batch {i//10}")
        
        # Final commit
        db.commit()
        
        # Summary
        print("\n" + "=" * 80)
        print("LOAD TEST COMPLETE!")
        print("=" * 80)
        print(f"Users created: {users_created}")
        print(f"Clients created: {clients_created}")
        print(f"Projects created: {projects_created}")
        print(f"Items created: {items_created}")
        print(f"\nTotal records in database:")
        print(f"  Users: {db.query(User).count()}")
        print(f"  Clients: {db.query(Client).count()}")
        print(f"  Projects: {db.query(Project).count()}")
        print("=" * 80)
        
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    load_test_database()
