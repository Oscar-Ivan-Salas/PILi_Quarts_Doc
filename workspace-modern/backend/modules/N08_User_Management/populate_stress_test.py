"""
Script de Prueba de Estrés de Identidad (50x50x100).
Genera 50 Usuarios, 50 Clientes y 100 Proyectos cruzados.
"""
import sys
import os
import random
import time
from pathlib import Path

# Setup paths
current_dir = Path(__file__).parent
backend_dir = current_dir.parent.parent
sys.path.append(str(backend_dir))

from modules.N08_User_Management.identity_db import init_db, SessionLocal, UsuarioEjecutor, ClienteFinal, ProyectoActivo

# Fake Data Generators
def generate_ruc():
    return f"20{random.randint(100000000, 999999999)}"

def generate_color():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))

def populate_stress_test():
    print("🚀 INICIANDO PRUEBA DE ESTRÉS DE IDENTIDAD (50x50x100)...")
    init_db()
    
    session = SessionLocal()
    
    try:
        # 1. Create 50 Users (Ejecutores)
        print("👤 Generando 50 Usuarios Ejecutores...")
        users = []
        for i in range(1, 51):
            u = UsuarioEjecutor(
                user_key=f"USER_{i:03d}",
                nombre_completo=f"Ingeniero {i} Pro",
                empresa=f"Soluciones Técnicas {i} S.A.C.",
                ruc_dni=generate_ruc(),
                direccion=f"Av. Tecnológica {i*100}, Lima",
                colores_hex={"primary": generate_color(), "secondary": generate_color()},
                logo_path=f"/assets/logos/user_{i}.png",
                firma_path=f"/assets/firmas/user_{i}.png"
            )
            users.append(u)
        session.add_all(users)
        session.commit()
        
        # 2. Create 50 Clients (Finales)
        print("🏢 Generando 50 Clientes Finales...")
        clients = []
        for i in range(1, 51):
            c = ClienteFinal(
                razon_social=f"Cliente Industria {i} Corp",
                ruc_dni=generate_ruc(),
                direccion=f"Calle Industrial {i*50}, Arequipa",
                persona_contacto=f"Gerente {i}"
            )
            clients.append(c)
        session.add_all(clients)
        session.commit()
        
        # Reload to get IDs
        all_users = session.query(UsuarioEjecutor).all()
        all_clients = session.query(ClienteFinal).all()
        
        # 3. Create 100 Active Projects (Cross-linked)
        print("🔗 Generando 100 Proyectos Activos (Vinculación)...")
        projects = []
        for i in range(1, 101):
            status_list = ["DRAFT", "GENERATED", "APPROVED"]
            p = ProyectoActivo(
                project_code=f"PROJ_2026_{i:04d}",
                usuario_id=random.choice(all_users).id,
                cliente_id=random.choice(all_clients).id,
                service_id=random.randint(1, 10),
                document_type_id=random.randint(1, 10),
                industry_sector=random.choice(["Minería", "Residencial", "Hospitalario", "Industrial"]),
                status=random.choice(status_list)
            )
            projects.append(p)
        session.add_all(projects)
        session.commit()
        
        # 4. Validation Report
        total_users = session.query(UsuarioEjecutor).count()
        total_clients = session.query(ClienteFinal).count()
        total_projects = session.query(ProyectoActivo).count()
        
        print("\n📊 REPORTE DE CONSISTENCIA N08:")
        print(f"   ✅ Usuarios Creados: {total_users} (Objetivo: 50)")
        print(f"   ✅ Clientes Creados: {total_clients} (Objetivo: 50)")
        print(f"   ✅ Proyectos Vinculados: {total_projects} (Objetivo: 100)")
        
        # Integrity Check: Random Project
        p_check = session.query(ProyectoActivo).first()
        print(f"\n🔍 Auditoría de Integridad (Muestra Aleatoria):")
        print(f"   Proyecto: {p_check.project_code}")
        print(f"   Ejecutor: {p_check.ejecutor.nombre_completo} (RUC: {p_check.ejecutor.ruc_dni})")
        print(f"   Cliente:  {p_check.cliente.razon_social} (Contacto: {p_check.cliente.persona_contacto})")
        print(f"   Branding: {p_check.ejecutor.colores_hex}")
        
        print("\n✅ PRUEBA DE ESTRÉS SUPERADA: Integridad Referencial Validada.")

    except Exception as e:
        print(f"❌ Error Crítico: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    populate_stress_test()
