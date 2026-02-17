"""
Quick summary of load test results
"""
import sys
sys.path.insert(0, 'e:/PILi_Quarts/workspace-modern/backend')

from modules.pili.db.database import SessionLocal
from modules.pili.db.models import User, Client, Project

db = SessionLocal()
print(f"Users: {db.query(User).count()}")
print(f"Clients: {db.query(Client).count()}")
print(f"Projects: {db.query(Project).count()}")
db.close()
