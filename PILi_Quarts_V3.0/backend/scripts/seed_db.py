"""
Database Seed Script
Populate database with initial data for development
Following database-design and deployment-procedures
"""
import asyncio
import uuid
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession

from modules.database.base import get_db, init_db
from modules.database.models import (
    User,
    Workspace,
    WorkspaceMember,
    Proyecto,
    ProyectoMember,
    Folder,
)
from modules.integration.auth.jwt import hash_password


async def seed_database():
    """Seed database with initial data"""
    print("=" * 60)
    print("SEEDING DATABASE")
    print("=" * 60)
    
    # Initialize database
    await init_db()
    
    async for db in get_db():
        try:
            # Create admin user
            print("\n📝 Creating admin user...")
            admin_user = User(
                id=str(uuid.uuid4()),
                email="admin@piliquarts.com",
                nombre="Admin User",
                password_hash=hash_password("admin123"),
                rol_global="admin",
                email_verified=True,
            )
            db.add(admin_user)
            
            # Create test user
            print("📝 Creating test user...")
            test_user = User(
                id=str(uuid.uuid4()),
                email="test@piliquarts.com",
                nombre="Test User",
                password_hash=hash_password("test123"),
                rol_global="member",
                email_verified=True,
            )
            db.add(test_user)
            
            await db.commit()
            await db.refresh(admin_user)
            await db.refresh(test_user)
            
            # Create workspace
            print("📝 Creating workspace...")
            workspace = Workspace(
                id=str(uuid.uuid4()),
                nombre="Demo Workspace",
                slug="demo-workspace",
                descripcion="Workspace de demostración para PILi Quarts",
                owner_id=admin_user.id,
                plan="pro",
            )
            db.add(workspace)
            await db.commit()
            await db.refresh(workspace)
            
            # Add members to workspace
            print("📝 Adding workspace members...")
            admin_member = WorkspaceMember(
                id=str(uuid.uuid4()),
                workspace_id=workspace.id,
                user_id=admin_user.id,
                rol="owner",
            )
            test_member = WorkspaceMember(
                id=str(uuid.uuid4()),
                workspace_id=workspace.id,
                user_id=test_user.id,
                rol="member",
            )
            db.add_all([admin_member, test_member])
            
            # Create projects
            print("📝 Creating projects...")
            proyecto1 = Proyecto(
                id=str(uuid.uuid4()),
                nombre="Instalación Eléctrica Residencial",
                workspace_id=workspace.id,
                descripcion="Proyecto de instalación eléctrica para casa habitación",
                tipo="residencial",
                estado="activo",
                fecha_inicio=datetime.now().date(),
                presupuesto=150000.00,
            )
            
            proyecto2 = Proyecto(
                id=str(uuid.uuid4()),
                nombre="Sistema de Iluminación Comercial",
                workspace_id=workspace.id,
                descripcion="Diseño e instalación de sistema de iluminación LED",
                tipo="comercial",
                estado="activo",
                fecha_inicio=datetime.now().date(),
                presupuesto=250000.00,
            )
            
            db.add_all([proyecto1, proyecto2])
            await db.commit()
            await db.refresh(proyecto1)
            await db.refresh(proyecto2)
            
            # Add project members
            print("📝 Adding project members...")
            proj1_admin = ProyectoMember(
                id=str(uuid.uuid4()),
                proyecto_id=proyecto1.id,
                user_id=admin_user.id,
                rol="gerente",
            )
            proj1_test = ProyectoMember(
                id=str(uuid.uuid4()),
                proyecto_id=proyecto1.id,
                user_id=test_user.id,
                rol="ingeniero",
            )
            proj2_admin = ProyectoMember(
                id=str(uuid.uuid4()),
                proyecto_id=proyecto2.id,
                user_id=admin_user.id,
                rol="gerente",
            )
            
            db.add_all([proj1_admin, proj1_test, proj2_admin])
            
            # Create folders
            print("📝 Creating folders...")
            folder1 = Folder(
                id=str(uuid.uuid4()),
                nombre="Cotizaciones",
                proyecto_id=proyecto1.id,
                path="/Cotizaciones",
            )
            folder2 = Folder(
                id=str(uuid.uuid4()),
                nombre="Planos",
                proyecto_id=proyecto1.id,
                path="/Planos",
            )
            folder3 = Folder(
                id=str(uuid.uuid4()),
                nombre="Documentos",
                proyecto_id=proyecto2.id,
                path="/Documentos",
            )
            
            db.add_all([folder1, folder2, folder3])
            
            await db.commit()
            
            print("\n" + "=" * 60)
            print("✅ DATABASE SEEDED SUCCESSFULLY!")
            print("=" * 60)
            print("\n📊 Created:")
            print(f"  - 2 users (admin@piliquarts.com / test@piliquarts.com)")
            print(f"  - 1 workspace (Demo Workspace)")
            print(f"  - 2 projects")
            print(f"  - 3 folders")
            print("\n🔑 Login credentials:")
            print(f"  Admin: admin@piliquarts.com / admin123")
            print(f"  Test:  test@piliquarts.com / test123")
            
        except Exception as e:
            print(f"\n❌ Error seeding database: {e}")
            await db.rollback()
            raise
        finally:
            break


def main():
    """Main entry point"""
    asyncio.run(seed_database())


if __name__ == "__main__":
    main()
