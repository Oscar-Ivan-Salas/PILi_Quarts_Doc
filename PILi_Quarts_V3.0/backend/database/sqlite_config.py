"""
SQLite Database Configuration for Local Development
Compatible with PostgreSQL/Supabase for easy migration
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# SQLite database file
SQLITE_DATABASE_URL = "sqlite:///./pili_quarts_local.db"

# Create engine
engine = create_engine(
    SQLITE_DATABASE_URL,
    connect_args={"check_same_thread": False},  # Needed for SQLite
    echo=True  # Log SQL queries for debugging
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency for FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize database
def init_db():
    """Create all tables"""
    Base.metadata.create_all(bind=engine)
    print("✅ SQLite database initialized")

# Drop all tables (for testing)
def drop_db():
    """Drop all tables"""
    Base.metadata.drop_all(bind=engine)
    print("❌ SQLite database dropped")
