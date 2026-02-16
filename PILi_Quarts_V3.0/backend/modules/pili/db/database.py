
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Create directory for SQLite DB if it doesn't exist
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "pili.db")

# SQLite URL
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

# Engine creation
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

def get_db():
    """Dependency for FastAPI"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
