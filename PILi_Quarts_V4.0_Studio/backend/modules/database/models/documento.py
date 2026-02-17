"""
Documento Model - File/Document with versioning
Following architecture and database-design skills
"""
from sqlalchemy import Column, String, Text, Integer, DateTime, ForeignKey, JSONB, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from ..base import Base


class Documento(Base):
    """
    Represents a document/file in the system.
    Supports versioning through DocumentoVersion relationship.
    """
    
    __tablename__ = 'documentos'

    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Relationships
    folder_id = Column(UUID(as_uuid=True), ForeignKey('folders.id', ondelete='CASCADE'), nullable=False, index=True)
    proyecto_id = Column(UUID(as_uuid=True), ForeignKey('proyectos.id', ondelete='CASCADE'), nullable=False, index=True)
    
    # Document info
    nombre = Column(String(255), nullable=False)
    tipo_documento = Column(String(50))  # cotizacion, plano, informe, contrato
    formato = Column(String(10))  # pdf, docx, xlsx, dwg
    
    # Versioning
    version_actual = Column(Integer, default=1)
    
    # Metadata and tags
    metadata = Column(JSONB, default={})
    tags = Column(ARRAY(Text), default=[])
    
    # Status
    estado = Column(String(50), default='borrador')  # borrador, revision, aprobado
    
    # Creator
    created_by = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    folder = relationship('Folder', back_populates='documentos')
    proyecto = relationship('Proyecto', back_populates='documentos')
    creator = relationship('User', back_populates='documentos_created')
    versiones = relationship('DocumentoVersion', back_populates='documento', cascade='all, delete-orphan', order_by='DocumentoVersion.version.desc()')
    actividades = relationship('Actividad', back_populates='documento')

    def __repr__(self) -> str:
        return f"<Documento(id={self.id}, nombre={self.nombre}, version={self.version_actual})>"

    @property
    def is_draft(self) -> bool:
        return self.estado == 'borrador'

    @property
    def is_approved(self) -> bool:
        return self.estado == 'aprobado'

    @property
    def latest_version(self):
        """Get the latest version object"""
        return self.versiones[0] if self.versiones else None

    def increment_version(self) -> int:
        """Increment version number and return new version"""
        self.version_actual += 1
        return self.version_actual
