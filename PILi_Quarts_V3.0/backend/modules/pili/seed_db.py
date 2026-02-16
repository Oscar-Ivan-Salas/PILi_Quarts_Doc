"""
PILi Database Seed Script - Production Ready
Comprehensive seed data for all tables
"""
from db.database import SessionLocal
from db.models import User, Client, Project, DocumentType, ProjectItem, PriceReference
from decimal import Decimal
from datetime import datetime, timedelta
import uuid

def seed_db():
    db = SessionLocal()
    try:
        print("=" * 80)
        print("SEEDING DATABASE - Production Ready Data")
        print("=" * 80)
        
        # ============================================================
        # 1. DOCUMENT TYPES (Catalog)
        # ============================================================
        print("\nCreating Document Types...")
        
        doc_types = [
            {
                "id": "cotizacion_simple",
                "nombre": "Cotización Simple",
                "descripcion": "Cotización básica para servicios eléctricos estándar",
                "categoria": "cotizacion",
                "template_html_path": "templates/html/COTIZACION_SIMPLE.html",
                "requiere_cliente": True,
                "requiere_items": True,
                "requiere_cronograma": False,
                "validez_dias": 30
            },
            {
                "id": "cotizacion_compleja",
                "nombre": "Cotización Compleja",
                "descripcion": "Cotización detallada con cronograma y especificaciones técnicas",
                "categoria": "cotizacion",
                "template_html_path": "templates/html/COTIZACION_COMPLEJA.html",
                "requiere_cliente": True,
                "requiere_items": True,
                "requiere_cronograma": True,
                "validez_dias": 45
            },
            {
                "id": "proyecto_pmi",
                "nombre": "Proyecto PMI",
                "descripcion": "Proyecto completo siguiendo metodología PMI",
                "categoria": "proyecto",
                "template_html_path": "templates/html/PROYECTO_PMI.html",
                "requiere_cliente": True,
                "requiere_items": True,
                "requiere_cronograma": True,
                "validez_dias": 60
            }
        ]
        
        for dt_data in doc_types:
            existing = db.query(DocumentType).filter(DocumentType.id == dt_data["id"]).first()
            if not existing:
                doc_type = DocumentType(**dt_data)
                db.add(doc_type)
                print(f"  ✅ Created: {dt_data['nombre']}")
        
        db.commit()
        
        # ============================================================
        # 2. USER (Tesla Electricidad)
        # ============================================================
        print("\n👤 Creating User...")
        
        user_id = "b2289941-d90c-4d48-b8c2-6e3fafe88944"
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            user = User(
                id=user_id,
                email="admin@tesla.com",
                password_hash="dummy_hash",  # In production, use proper hashing
                razon_social="Tesla Electricidad y Automatización S.A.C.",
                ruc="20601138787",
                direccion="Av. Los Ingenieros 123, San Isidro, Lima",
                telefono="+51 999 888 777",
                professional_title="Ing. Eléctrico",
                license_number="CIP 123456",
                logo_path="/static/logos/tesla.png",
                signature_path="/static/signatures/tesla_signature.png",
                role="admin",
                is_active=True
            )
            db.add(user)
            db.commit()
            print(f"  ✅ Created: {user.razon_social}")
        else:
            print(f"  ℹ️  User already exists: {user.razon_social}")
        
        # ============================================================
        # 3. CLIENTS (3 clients)
        # ============================================================
        print("\n🏢 Creating Clients...")
        
        clients_data = [
            {
                "id": "client-001",
                "ruc": "20123456789",
                "razon_social": "Constructora Los Andes S.A.C.",
                "nombre_comercial": "Los Andes",
                "direccion": "Av. Javier Prado 456, San Isidro, Lima",
                "ciudad": "Lima",
                "pais": "Perú",
                "email": "contacto@losandes.com",
                "telefono": "+51 987 654 321",
                "website": "www.losandes.com",
                "contacto_persona": "Ing. Carlos Mendoza",
                "contacto_email": "cmendoza@losandes.com",
                "contacto_telefono": "+51 987 654 322",
                "industria": "construccion",
                "tipo_cliente": "empresa",
                "limite_credito": Decimal("50000.00"),
                "terminos_pago": 30,
                "is_active": True,
                "notas": "Cliente preferencial - Proyectos de construcción"
            },
            {
                "id": "client-002",
                "ruc": "20987654321",
                "razon_social": "Industrias del Pacífico S.A.",
                "nombre_comercial": "Pacífico Industrial",
                "direccion": "Av. Argentina 789, Callao",
                "ciudad": "Callao",
                "pais": "Perú",
                "email": "ventas@pacifico.com",
                "telefono": "+51 976 543 210",
                "website": "www.pacifico.com.pe",
                "contacto_persona": "Ing. María Torres",
                "contacto_email": "mtorres@pacifico.com",
                "contacto_telefono": "+51 976 543 211",
                "industria": "industrial",
                "tipo_cliente": "empresa",
                "limite_credito": Decimal("100000.00"),
                "terminos_pago": 45,
                "is_active": True,
                "notas": "Proyectos industriales de gran escala"
            },
            {
                "id": "client-003",
                "ruc": "20555666777",
                "razon_social": "Comercial Lima Norte E.I.R.L.",
                "nombre_comercial": "Lima Norte",
                "direccion": "Av. Túpac Amaru 321, Lima",
                "ciudad": "Lima",
                "pais": "Perú",
                "email": "info@limanorte.com",
                "telefono": "+51 965 432 109",
                "contacto_persona": "Sr. Juan Pérez",
                "contacto_email": "jperez@limanorte.com",
                "contacto_telefono": "+51 965 432 110",
                "industria": "comercial",
                "tipo_cliente": "empresa",
                "limite_credito": Decimal("30000.00"),
                "terminos_pago": 15,
                "is_active": True,
                "notas": "Cliente comercial - Pagos rápidos"
            }
        ]
        
        for client_data in clients_data:
            existing = db.query(Client).filter(Client.id == client_data["id"]).first()
            if not existing:
                client = Client(**client_data)
                db.add(client)
                print(f"  ✅ Created: {client_data['razon_social']}")
        
        db.commit()
        
        # ============================================================
        # 4. PRICE REFERENCES (20+ items)
        # ============================================================
        print("\n💰 Creating Price References...")
        
        price_refs = [
            # Electricidad
            {"categoria": "electricidad", "subcategoria": "tableros", "nombre_item": "Tablero eléctrico trifásico 380V", "unidad": "und", "precio_base": Decimal("850.00"), "precio_mercado": Decimal("900.00"), "precio_sugerido": Decimal("1050.00")},
            {"categoria": "electricidad", "subcategoria": "tableros", "nombre_item": "Tablero general trifásico 1000A", "unidad": "und", "precio_base": Decimal("3500.00"), "precio_mercado": Decimal("3700.00"), "precio_sugerido": Decimal("4200.00")},
            {"categoria": "electricidad", "subcategoria": "circuitos", "nombre_item": "Circuito derivado (iluminación/tomacorrientes)", "unidad": "pto", "precio_base": Decimal("120.00"), "precio_mercado": Decimal("130.00"), "precio_sugerido": Decimal("150.00")},
            {"categoria": "electricidad", "subcategoria": "circuitos", "nombre_item": "Circuito de fuerza para maquinaria", "unidad": "pto", "precio_base": Decimal("250.00"), "precio_mercado": Decimal("270.00"), "precio_sugerido": Decimal("310.00")},
            {"categoria": "electricidad", "subcategoria": "iluminacion", "nombre_item": "Luminaria LED 36W empotrada", "unidad": "und", "precio_base": Decimal("85.00"), "precio_mercado": Decimal("95.00"), "precio_sugerido": Decimal("110.00")},
            {"categoria": "electricidad", "subcategoria": "iluminacion", "nombre_item": "Luminaria LED 72W industrial", "unidad": "und", "precio_base": Decimal("150.00"), "precio_mercado": Decimal("165.00"), "precio_sugerido": Decimal("190.00")},
            {"categoria": "electricidad", "subcategoria": "tomacorrientes", "nombre_item": "Tomacorriente doble con línea a tierra", "unidad": "und", "precio_base": Decimal("45.00"), "precio_mercado": Decimal("50.00"), "precio_sugerido": Decimal("60.00")},
            {"categoria": "electricidad", "subcategoria": "tomacorrientes", "nombre_item": "Tomacorriente industrial trifásico", "unidad": "und", "precio_base": Decimal("180.00"), "precio_mercado": Decimal("200.00"), "precio_sugerido": Decimal("230.00")},
            {"categoria": "electricidad", "subcategoria": "puesta_tierra", "nombre_item": "Sistema de puesta a tierra completo", "unidad": "glb", "precio_base": Decimal("950.00"), "precio_mercado": Decimal("1050.00"), "precio_sugerido": Decimal("1200.00")},
            {"categoria": "electricidad", "subcategoria": "puesta_tierra", "nombre_item": "Pozo a tierra con varilla copperweld", "unidad": "und", "precio_base": Decimal("450.00"), "precio_mercado": Decimal("500.00"), "precio_sugerido": Decimal("580.00")},
            
            # Cableado
            {"categoria": "electricidad", "subcategoria": "cableado", "nombre_item": "Cable NYY 3x10 mm²", "unidad": "m", "precio_base": Decimal("12.50"), "precio_mercado": Decimal("14.00"), "precio_sugerido": Decimal("16.50")},
            {"categoria": "electricidad", "subcategoria": "cableado", "nombre_item": "Cable NYY 3x25 mm²", "unidad": "m", "precio_base": Decimal("28.00"), "precio_mercado": Decimal("31.00"), "precio_sugerido": Decimal("36.00")},
            {"categoria": "electricidad", "subcategoria": "cableado", "nombre_item": "Cable THW 12 AWG", "unidad": "m", "precio_base": Decimal("3.50"), "precio_mercado": Decimal("4.00"), "precio_sugerido": Decimal("4.80")},
            
            # Conduit
            {"categoria": "electricidad", "subcategoria": "conduit", "nombre_item": "Tubería PVC-P 20mm (3/4\")", "unidad": "m", "precio_base": Decimal("5.50"), "precio_mercado": Decimal("6.00"), "precio_sugerido": Decimal("7.20")},
            {"categoria": "electricidad", "subcategoria": "conduit", "nombre_item": "Tubería PVC-P 40mm (1 1/2\")", "unidad": "m", "precio_base": Decimal("12.00"), "precio_mercado": Decimal("13.50"), "precio_sugerido": Decimal("16.00")},
            
            # Automatización
            {"categoria": "automatizacion", "subcategoria": "control", "nombre_item": "Contactor trifásico 25A", "unidad": "und", "precio_base": Decimal("120.00"), "precio_mercado": Decimal("135.00"), "precio_sugerido": Decimal("160.00")},
            {"categoria": "automatizacion", "subcategoria": "control", "nombre_item": "Relé térmico 16-25A", "unidad": "und", "precio_base": Decimal("85.00"), "precio_mercado": Decimal("95.00"), "precio_sugerido": Decimal("115.00")},
            {"categoria": "automatizacion", "subcategoria": "sensores", "nombre_item": "Sensor de movimiento PIR", "unidad": "und", "precio_base": Decimal("45.00"), "precio_mercado": Decimal("50.00"), "precio_sugerido": Decimal("60.00")},
            
            # Servicios
            {"categoria": "servicios", "subcategoria": "mano_obra", "nombre_item": "Mano de obra electricista especializado", "unidad": "hr", "precio_base": Decimal("35.00"), "precio_mercado": Decimal("40.00"), "precio_sugerido": Decimal("50.00")},
            {"categoria": "servicios", "subcategoria": "pruebas", "nombre_item": "Pruebas eléctricas y puesta en servicio", "unidad": "glb", "precio_base": Decimal("500.00"), "precio_mercado": Decimal("550.00"), "precio_sugerido": Decimal("650.00")},
        ]
        
        for pr_data in price_refs:
            existing = db.query(PriceReference).filter(
                PriceReference.nombre_item == pr_data["nombre_item"]
            ).first()
            if not existing:
                price_ref = PriceReference(
                    **pr_data,
                    descripcion=f"Precio de referencia para {pr_data['nombre_item']}",
                    is_active=True,
                    ultima_actualizacion_precio=datetime.now()
                )
                db.add(price_ref)
        
        db.commit()
        print(f"  ✅ Created {len(price_refs)} price references")
        
        # ============================================================
        # 5. PROJECTS with COMPLETE state_json
        # ============================================================
        print("\n📁 Creating Projects...")
        
        # Project 1: Cotización Simple (default-project-1)
        project1_id = "default-project-1"
        project1 = db.query(Project).filter(Project.id == project1_id).first()
        
        if project1:
            # Update existing project with complete data
            project1.client_id = "client-001"
            project1.document_type_id = "cotizacion_simple"
            project1.numero_proyecto = "COT-2026-001"
            project1.nombre = "Instalación Eléctrica Oficinas"
            project1.descripcion = "Instalación eléctrica completa para oficinas administrativas"
            project1.estado = "draft"
            project1.prioridad = "normal"
            project1.subtotal = Decimal("5615.00")
            project1.monto_igv = Decimal("1010.70")
            project1.total = Decimal("6625.70")
            project1.fecha_emision = datetime.now()
            project1.fecha_vigencia = datetime.now() + timedelta(days=30)
            project1.created_by = user_id
            
            project1.state_json = {
                "cliente": {
                    "nombre": "Constructora Los Andes S.A.C.",
                    "ruc": "20123456789",
                    "direccion": "Av. Javier Prado 456, San Isidro, Lima",
                    "contacto": "Ing. Carlos Mendoza",
                    "telefono": "+51 987 654 321",
                    "email": "contacto@losandes.com"
                },
                "proyecto": "Instalación Eléctrica para Oficinas Administrativas",
                "numero": "COT-2026-001",
                "fecha": datetime.now().strftime("%Y-%m-%d"),
                "vigencia": "30 días calendario",
                "area_m2": "150",
                "servicio": "Instalaciones Eléctricas",
                "servicio_nombre": "Instalación Eléctrica Completa",
                "descripcion": "Instalación eléctrica completa para oficinas administrativas de 150m², incluyendo tableros, circuitos, iluminación y tomacorrientes.",
                "items": [
                    {
                        "item": "01",
                        "descripcion": "Tablero eléctrico trifásico 380V",
                        "unidad": "und",
                        "cantidad": 1,
                        "precio_unitario": 850.00,
                        "subtotal": 850.00
                    },
                    {
                        "item": "02",
                        "descripcion": "Circuitos derivados (iluminación y tomacorrientes)",
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
                        "descripcion": "Tomacorrientes dobles con línea a tierra",
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
            
            print(f"  ✅ Updated: {project1.nombre}")
        
        db.commit()
        
        # Project 2: Cotización Compleja
        project2_id = "project-002"
        project2 = db.query(Project).filter(Project.id == project2_id).first()
        
        if not project2:
            project2 = Project(
                id=project2_id,
                user_id=user_id,
                client_id="client-002",
                document_type_id="cotizacion_compleja",
                numero_proyecto="COT-2026-002",
                nombre="Proyecto Industrial Completo",
                descripcion="Instalación eléctrica industrial para planta de producción",
                tipo_documento="cotizacion_compleja",
                estado="draft",
                prioridad="high",
                subtotal=Decimal("13300.00"),
                monto_igv=Decimal("2394.00"),
                total=Decimal("15694.00"),
                fecha_emision=datetime.now(),
                fecha_vigencia=datetime.now() + timedelta(days=45),
                created_by=user_id,
                state_json={
                    "cliente": {
                        "nombre": "Industrias del Pacífico S.A.",
                        "ruc": "20987654321",
                        "direccion": "Av. Argentina 789, Callao",
                        "contacto": "Ing. María Torres",
                        "telefono": "+51 976 543 210",
                        "email": "ventas@pacifico.com"
                    },
                    "proyecto": "Instalación Eléctrica Industrial - Planta de Producción",
                    "numero": "COT-2026-002",
                    "fecha": datetime.now().strftime("%Y-%m-%d"),
                    "vigencia": "45 días calendario",
                    "area_m2": "500",
                    "servicio_nombre": "Instalación Eléctrica Industrial Completa",
                    "items": [
                        {
                            "item": "01",
                            "descripcion": "Tablero general trifásico 1000A",
                            "unidad": "und",
                            "cantidad": 1,
                            "precio_unitario": 3500.00,
                            "subtotal": 3500.00
                        },
                        {
                            "item": "02",
                            "descripcion": "Tableros de distribución 380V",
                            "unidad": "und",
                            "cantidad": 4,
                            "precio_unitario": 1200.00,
                            "subtotal": 4800.00
                        },
                        {
                            "item": "03",
                            "descripcion": "Circuitos de fuerza para maquinaria",
                            "unidad": "pto",
                            "cantidad": 20,
                            "precio_unitario": 250.00,
                            "subtotal": 5000.00
                        }
                    ],
                    "cronograma": {
                        "dias_ingenieria": 7,
                        "dias_adquisiciones": 10,
                        "dias_instalacion": 20,
                        "dias_pruebas": 5,
                        "dias_total": 42
                    },
                    "subtotal": 13300.00,
                    "igv": 2394.00,
                    "total": 15694.00,
                    "normativa": "CNE Suministro 2011, CNE Utilización 2006"
                }
            )
            db.add(project2)
            print(f"  ✅ Created: {project2.nombre}")
        
        db.commit()
        
        # ============================================================
        # SUMMARY
        # ============================================================
        print("\n" + "=" * 80)
        print("📊 DATABASE SEEDING COMPLETE!")
        print("=" * 80)
        print(f"  👤 Users: {db.query(User).count()}")
        print(f"  🏢 Clients: {db.query(Client).count()}")
        print(f"  📋 Document Types: {db.query(DocumentType).count()}")
        print(f"  📁 Projects: {db.query(Project).count()}")
        print(f"  💰 Price References: {db.query(PriceReference).count()}")
        print("=" * 80)
        
        # Verify project data
        project = db.query(Project).filter(Project.id == "default-project-1").first()
        if project and project.state_json:
            print(f"\n✅ Project 'default-project-1' state_json keys: {list(project.state_json.keys())}")
            print(f"✅ Items count: {len(project.state_json.get('items', []))}")
            print(f"✅ Total: {project.state_json.get('total', 0)}")
        
    except Exception as e:
        print(f"\n❌ Error seeding DB: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_db()
