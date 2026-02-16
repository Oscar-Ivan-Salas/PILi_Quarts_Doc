"""
Database Module - Base Configuration
Following clean-code and database-design skills
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
import os

# Database URL from environment
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/pili_quarts"
)

# Create engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


def get_session() -> Generator[Session, None, None]:
    """
    Dependency for FastAPI endpoints.
    Yields a database session and ensures it's closed after use.
    """
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def init_db() -> None:
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)
