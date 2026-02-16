"""
Proyecto Model - Construction/Engineering project
Following architecture and database-design skills
"""
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, JSONB
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from ..base import Base


class Proyecto(Base):
    """
    Represents a construction or engineering project.
    Contains folders, documents, and team members.
    """
    
    __tablename__ = 'proyectos'

    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Workspace relationship
    workspace_id = Column(UUID(as_uuid=True), ForeignKey('workspaces.id', ondelete='CASCADE'), nullable=False, index=True)
    
    # Basic info
    nombre = Column(String(255), nullable=False)
    codigo = Column(String(100), unique=True, index=True)
    descripcion = Column(Text)
    
    # Classification
    tipo = Column(String(50))  # residencial, comercial, industrial
    estado = Column(String(50), default='activo')  # activo, pausado, completado, archivado
    
    # Location (JSON)
    ubicacion = Column(JSONB, default={})  # {direccion, ciudad, pais, coordenadas}
    
    # Client (JSON)
    cliente = Column(JSONB, default={})  # {nombre, contacto, email}
    
    # Dates (JSON)
    fechas = Column(JSONB, default={})  # {inicio, fin_estimado, fin_real}
    
    # Budget (JSON)
    presupuesto = Column(JSONB, default={})  # {total, gastado, moneda}
    
    # Additional metadata
    metadata = Column(JSONB, default={})
    
    # Creator
    created_by = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    workspace = relationship('Workspace', back_populates='proyectos')
    creator = relationship('User')
    members = relationship('ProyectoMember', back_populates='proyecto', cascade='all, delete-orphan')
    folders = relationship('Folder', back_populates='proyecto', cascade='all, delete-orphan')
    documentos = relationship('Documento', back_populates='proyecto', cascade='all, delete-orphan')
    actividades = relationship('Actividad', back_populates='proyecto')

    def __repr__(self) -> str:
        return f"<Proyecto(id={self.id}, nombre={self.nombre}, estado={self.estado})>"

    @property
    def is_active(self) -> bool:
        return self.estado == 'activo'

    @property
    def is_completed(self) -> bool:
        return self.estado == 'completado'

    @property
    def budget_percentage(self) -> float:
        """Calculate budget usage percentage"""
        if not self.presupuesto or 'total' not in self.presupuesto:
            return 0.0
        total = self.presupuesto.get('total', 0)
        gastado = self.presupuesto.get('gastado', 0)
        if total == 0:
            return 0.0
        return (gastado / total) * 100
