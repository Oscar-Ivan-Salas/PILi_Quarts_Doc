"""
PILi Database Models - Production Ready Architecture
Following database-design skill: Proper normalization, indexes, constraints
"""
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, JSON, Boolean, Float, Index, DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base
import uuid

def generate_uuid():
    return str(uuid.uuid4())


class User(Base):
    """
    Users table - System users with business profiles
    Multi-tenant ready with organization_id (future)
    """
    __tablename__ = "users"

    # Primary Key
    id = Column(String, primary_key=True, default=generate_uuid)
    
    # Authentication
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=True)  # Nullable for passwordless/magic links
    
    # Business Profile (Executor Identity)
    razon_social = Column(String, nullable=True)
    ruc = Column(String, nullable=True, index=True)  # Tax ID
    direccion = Column(String, nullable=True)
    telefono = Column(String, nullable=True)
    
    # Professional Profile (for document signatures)
    professional_title = Column(String, nullable=True)  # "Ing. Eléctrico"
    license_number = Column(String, nullable=True)  # Colegiatura
    
    # Assets
    logo_path = Column(String, nullable=True)
    signature_path = Column(String, nullable=True)
    
    # Permissions & Status
    role = Column(String, default='user')  # admin, user, viewer
    is_active = Column(Boolean, default=True, index=True)
    last_login = Column(DateTime(timezone=True), nullable=True)
    
    # Meta
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    projects = relationship("Project", back_populates="user", foreign_keys="Project.user_id")
    created_projects = relationship("Project", back_populates="creator", foreign_keys="Project.created_by")


class Client(Base):
    """
    Clients table - Customer information
    Normalized client data with full contact details
    """
    __tablename__ = "clients"

    # Primary Key
    id = Column(String, primary_key=True, default=generate_uuid)
    
    # Fiscal Data
    ruc = Column(String, unique=True, index=True, nullable=True)  # Tax ID (11 digits)
    razon_social = Column(String, nullable=False)  # Legal name
    nombre_comercial = Column(String, nullable=True)  # Commercial name
    
    # Contact Information
    direccion = Column(String, nullable=True)
    ciudad = Column(String, nullable=True)
    pais = Column(String, default='Perú')
    email = Column(String, nullable=True)
    telefono = Column(String, nullable=True)
    website = Column(String, nullable=True)
    
    # Secondary Contact
    contacto_persona = Column(String, nullable=True)  # Contact person
    contacto_email = Column(String, nullable=True)
    contacto_telefono = Column(String, nullable=True)
    
    # Classification
    industria = Column(String, nullable=True, index=True)  # construcción, industrial, comercial
    tipo_cliente = Column(String, default='empresa')  # empresa, persona
    
    # Business Terms
    limite_credito = Column(DECIMAL(12, 2), nullable=True)
    terminos_pago = Column(Integer, default=30)  # días
    
    # Status
    is_active = Column(Boolean, default=True, index=True)
    notas = Column(Text, nullable=True)
    
    # Meta
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    projects = relationship("Project", back_populates="client")


class DocumentType(Base):
    """
    Document Types catalog - Centralized document type definitions
    Makes it easy to add new document types without code changes
    """
    __tablename__ = "document_types"
    
    # Primary Key
    id = Column(String, primary_key=True)  # cotizacion-simple, proyecto-complejo-pmi
    
    # Identification
    nombre = Column(String, nullable=False)
    descripcion = Column(Text, nullable=True)
    categoria = Column(String, nullable=True, index=True)  # cotizacion, proyecto, informe
    
    # Templates
    template_html_path = Column(String, nullable=True)
    template_word_path = Column(String, nullable=True)
    
    # Requirements
    requiere_cliente = Column(Boolean, default=True)
    requiere_items = Column(Boolean, default=True)
    requiere_cronograma = Column(Boolean, default=False)
    
    # Defaults
    validez_dias = Column(Integer, default=30)
    
    # Status
    is_active = Column(Boolean, default=True, index=True)
    orden_visualizacion = Column(Integer, default=0)
    
    # Meta
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    projects = relationship("Project", back_populates="document_type")


class Project(Base):
    """
    Projects table - Main document/project entity
    Stores all project data with flexible JSON state
    """
    __tablename__ = "projects"

    # Primary Key
    id = Column(String, primary_key=True, default=generate_uuid)
    
    # Foreign Keys
    user_id = Column(String, ForeignKey("users.id"), nullable=True, index=True)
    client_id = Column(String, ForeignKey("clients.id"), nullable=True, index=True)
    document_type_id = Column(String, ForeignKey("document_types.id"), nullable=True, index=True)
    
    # Identification
    numero_proyecto = Column(String, unique=True, index=True, nullable=True)  # COT-2026-001
    nombre = Column(String, nullable=True)
    descripcion = Column(Text, nullable=True)
    
    # Legacy field (backward compatibility)
    tipo_documento = Column(String, nullable=False, default="cotizacion")
    
    # Status & Priority
    estado = Column(String, default="draft", index=True)  # draft, pending_review, approved, sent, accepted, rejected
    prioridad = Column(String, default="normal")  # low, normal, high, urgent
    
    # Core Data (Flexible JSON for dynamic fields)
    state_json = Column(JSON, nullable=True)
    
    # Personalization
    esquema_color = Column(String, default="azul-tesla")
    logo_personalizado_url = Column(String, nullable=True)
    fuente_personalizada = Column(String, default="Calibri")
    
    # Financial (denormalized for performance)
    subtotal = Column(DECIMAL(12, 2), nullable=True)
    monto_igv = Column(DECIMAL(12, 2), nullable=True)
    total = Column(DECIMAL(12, 2), nullable=True, index=True)
    moneda = Column(String, default="PEN")
    
    # Dates
    fecha_emision = Column(DateTime(timezone=True), nullable=True)
    fecha_vigencia = Column(DateTime(timezone=True), nullable=True)
    fecha_envio = Column(DateTime(timezone=True), nullable=True)
    fecha_aceptacion = Column(DateTime(timezone=True), nullable=True)
    
    # Generated Files
    archivo_generado_path = Column(String, nullable=True)
    archivo_generado_url = Column(String, nullable=True)
    archivo_pdf_path = Column(String, nullable=True)
    archivo_pdf_url = Column(String, nullable=True)
    
    # Meta
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(String, ForeignKey("users.id"), nullable=True)
    
    # Soft Delete
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="projects", foreign_keys=[user_id])
    client = relationship("Client", back_populates="projects")
    document_type = relationship("DocumentType", back_populates="projects")
    creator = relationship("User", back_populates="created_projects", foreign_keys=[created_by])
    items = relationship("ProjectItem", back_populates="project", cascade="all, delete-orphan")

    # Indexes
    __table_args__ = (
        Index('idx_projects_status_created', 'estado', 'created_at'),
        Index('idx_projects_deleted', 'deleted_at'),
    )


class ProjectItem(Base):
    """
    Project Items - Normalized items/partidas for projects
    Allows complex queries across all project items
    """
    __tablename__ = "project_items"
    
    # Primary Key
    id = Column(String, primary_key=True, default=generate_uuid)
    
    # Foreign Key
    project_id = Column(String, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Identification
    numero_item = Column(String, nullable=True)  # 01, 02, 03
    descripcion = Column(Text, nullable=False)
    
    # Quantities
    cantidad = Column(DECIMAL(10, 2), nullable=False)
    unidad = Column(String, nullable=False)  # und, m, m2, glb
    
    # Prices
    precio_unitario = Column(DECIMAL(12, 2), nullable=False)
    subtotal = Column(DECIMAL(12, 2), nullable=False)
    descuento_porcentaje = Column(DECIMAL(5, 2), default=0)
    descuento_monto = Column(DECIMAL(12, 2), default=0)
    total = Column(DECIMAL(12, 2), nullable=False)
    
    # Classification
    categoria = Column(String, nullable=True, index=True)  # electricidad, obra civil
    es_opcional = Column(Boolean, default=False)
    
    # Order
    orden_visualizacion = Column(Integer, default=0)
    
    # Meta
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    project = relationship("Project", back_populates="items")


class PriceReference(Base):
    """
    Price References - Market price catalog
    Centralized pricing information for items
    """
    __tablename__ = "price_references"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Classification
    categoria = Column(String, index=True, nullable=False)  # electricidad, dry-wall, pintura
    subcategoria = Column(String, nullable=True)
    
    # Description
    nombre_item = Column(String, nullable=False, index=True)
    descripcion = Column(Text, nullable=True)
    especificaciones_tecnicas = Column(Text, nullable=True)
    
    # Unit
    unidad = Column(String, nullable=False)  # und, m, m2, kg
    
    # Prices
    precio_base = Column(DECIMAL(12, 2), nullable=False)
    precio_mercado = Column(DECIMAL(12, 2), nullable=True)
    precio_sugerido = Column(DECIMAL(12, 2), nullable=True)
    moneda = Column(String, default="PEN")
    
    # Supplier
    proveedor_preferido = Column(String, nullable=True)
    codigo_proveedor = Column(String, nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True, index=True)
    ultima_actualizacion_precio = Column(DateTime(timezone=True), nullable=True)
    
    # Meta
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Indexes
    __table_args__ = (
        Index('idx_price_refs_category_active', 'categoria', 'is_active'),
    )
