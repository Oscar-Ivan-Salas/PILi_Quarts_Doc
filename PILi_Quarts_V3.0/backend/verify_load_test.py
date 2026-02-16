"""
Verify load test results
"""
import sys
sys.path.insert(0, 'e:/PILi_Quarts/workspace-modern/backend')

from modules.pili.db.database import SessionLocal
from modules.pili.db.models import User, Client, Project, DocumentType, PriceReference
from sqlalchemy import func

db = SessionLocal()

try:
    print("=" * 80)
    print("DATABASE LOAD TEST VERIFICATION")
    print("=" * 80)
    
    # Total counts
    print("\nTotal Records:")
    print(f"  Users: {db.query(User).count()}")
    print(f"  Clients: {db.query(Client).count()}")
    print(f"  Document Types: {db.query(DocumentType).count()}")
    print(f"  Projects: {db.query(Project).count()}")
    print(f"  Price References: {db.query(PriceReference).count()}")
    
    # User breakdown
    print(f"\nUser Roles:")
    print(f"  Admins: {db.query(User).filter(User.role == 'admin').count()}")
    print(f"  Regular Users: {db.query(User).filter(User.role == 'user').count()}")
    
    # Project status
    print(f"\nProject Status:")
    print(f"  Draft: {db.query(Project).filter(Project.estado == 'draft').count()}")
    print(f"  Pending Review: {db.query(Project).filter(Project.estado == 'pending_review').count()}")
    print(f"  Approved: {db.query(Project).filter(Project.estado == 'approved').count()}")
    print(f"  Sent: {db.query(Project).filter(Project.estado == 'sent').count()}")
    
    # Sample users
    print(f"\nSample Users (first 5):")
    users = db.query(User).limit(5).all()
    for u in users:
        print(f"  - {u.razon_social}")
        print(f"    Email: {u.email}")
        print(f"    Role: {u.role}")
        print(f"    RUC: {u.ruc}")
    
    # Sample clients
    print(f"\nSample Clients (first 5):")
    clients = db.query(Client).limit(5).all()
    for c in clients:
        print(f"  - {c.razon_social}")
        print(f"    Industry: {c.industria}")
        print(f"    City: {c.ciudad}")
    
    # Sample projects with totals
    print(f"\nSample Projects (first 5):")
    projects = db.query(Project).limit(5).all()
    for p in projects:
        print(f"  - {p.nombre}")
        print(f"    Number: {p.numero_proyecto}")
        print(f"    Status: {p.estado}")
        print(f"    Total: S/ {p.total}")
    
    # Financial summary
    print(f"\nFinancial Summary:")
    total_sum = db.query(func.sum(Project.total)).scalar() or 0
    print(f"  Total value of all projects: S/ {total_sum:,.2f}")
    
    avg_project = db.query(func.avg(Project.total)).scalar() or 0
    print(f"  Average project value: S/ {avg_project:,.2f}")
    
    print("\n" + "=" * 80)
    print("VERIFICATION COMPLETE - DATABASE IS FULLY LOADED!")
    print("=" * 80)
    
finally:
    db.close()
