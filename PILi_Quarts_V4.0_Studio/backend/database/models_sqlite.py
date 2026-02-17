"""
Document Models for SQLite
Compatible with PostgreSQL/Supabase
"""
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, JSON
from sqlalchemy.sql import func
from database.sqlite_config import Base

class Document(Base):
    """Document model - stores all document types"""
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(50), nullable=False)  # 'proyecto-simple', 'cotizacion-simple', etc.
    title = Column(String(200), nullable=False)
    data = Column(JSON, nullable=False)  # Document data as JSON
    color_scheme = Column(String(50), default='azul-tesla')
    logo = Column(Text, nullable=True)  # Base64 logo
    font = Column(String(50), default='Calibri')
    user_id = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class PILIConversation(Base):
    """PILI Chat Conversations"""
    __tablename__ = "pili_conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(100), nullable=False)
    chat_type = Column(String(50), nullable=False)  # 'electricidad', 'puesta-tierra', etc.
    messages = Column(JSON, nullable=False)  # Array of messages
    extracted_data = Column(JSON, nullable=True)  # Extracted structured data
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Project(Base):
    """Project model"""
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    type = Column(String(20), nullable=False)  # 'simple', 'complex'
    status = Column(String(20), default='active')  # 'active', 'pending', 'completed'
    progress = Column(Integer, default=0)  # 0-100
    budget = Column(Float, default=0.0)
    data = Column(JSON, nullable=True)  # Additional project data
    user_id = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Quote(Base):
    """Quote/Cotización model"""
    __tablename__ = "quotes"
    
    id = Column(Integer, primary_key=True, index=True)
    quote_id = Column(String(50), unique=True, nullable=False)  # COT-1001, etc.
    client_name = Column(String(200), nullable=False)
    project_name = Column(String(200), nullable=False)
    type = Column(String(20), nullable=False)  # 'simple', 'complex'
    amount = Column(Float, nullable=False)
    status = Column(String(20), default='draft')  # 'draft', 'pending', 'approved'
    data = Column(JSON, nullable=True)  # Full quote data
    user_id = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Report(Base):
    """Report/Informe model"""
    __tablename__ = "reports"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    type = Column(String(20), nullable=False)  # 'technical', 'executive'
    description = Column(Text, nullable=True)
    data = Column(JSON, nullable=True)  # Report data
    user_id = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
