"""
Folder Model - Document organization
Following clean-code: KISS principle
"""
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from ..base import Base


class Folder(Base):
    """
    Represents a folder for organizing documents within a project.
    Supports nested folders (tree structure).
    """
    
    __tablename__ = 'folders'

    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Project relationship
    proyecto_id = Column(UUID(as_uuid=True), ForeignKey('proyectos.id', ondelete='CASCADE'), nullable=False, index=True)
    
    # Parent folder (for nesting)
    parent_folder_id = Column(UUID(as_uuid=True), ForeignKey('folders.id', ondelete='CASCADE'))
    
    # Folder info
    nombre = Column(String(255), nullable=False)
    tipo = Column(String(50))  # cotizaciones, planos, informes, custom
    color = Column(String(7), default='#6b7280')  # Hex color
    icono = Column(String(50), default='Folder')  # Lucide icon name
    orden = Column(Integer, default=0)  # Display order
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    proyecto = relationship('Proyecto', back_populates='folders')
    parent_folder = relationship('Folder', remote_side=[id], backref='subfolders')
    documentos = relationship('Documento', back_populates='folder', cascade='all, delete-orphan')

    def __repr__(self) -> str:
        return f"<Folder(id={self.id}, nombre={self.nombre}, tipo={self.tipo})>"

    @property
    def is_root(self) -> bool:
        """Check if folder is at root level"""
        return self.parent_folder_id is None

    @property
    def depth(self) -> int:
        """Calculate folder depth in tree"""
        depth = 0
        current = self
        while current.parent_folder_id is not None:
            depth += 1
            current = current.parent_folder
        return depth
