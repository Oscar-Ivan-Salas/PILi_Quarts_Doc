"""
Workspace Model - Organization/Company workspace
Following clean-code and architecture skills
"""
from sqlalchemy import Column, String, BigInteger, DateTime, ForeignKey, JSONB
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from ..base import Base


class Workspace(Base):
    """
    Workspace represents an organization or company.
    Contains projects, members, and settings.
    """
    
    __tablename__ = 'workspaces'

    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Basic info
    nombre = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=False, index=True)
    tipo = Column(String(50), default='empresa')  # empresa, personal
    
    # Plan and storage
    plan = Column(String(50), default='free')  # free, pro, enterprise
    storage_usado = Column(BigInteger, default=0)  # bytes
    storage_limite = Column(BigInteger, default=107374182400)  # 100GB default
    
    # Owner
    owner_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    
    # Settings (JSON)
    settings = Column(JSONB, default={})
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    owner = relationship('User', back_populates='workspaces_owned')
    members = relationship('WorkspaceMember', back_populates='workspace', cascade='all, delete-orphan')
    proyectos = relationship('Proyecto', back_populates='workspace', cascade='all, delete-orphan')
    actividades = relationship('Actividad', back_populates='workspace')

    def __repr__(self) -> str:
        return f"<Workspace(id={self.id}, nombre={self.nombre}, plan={self.plan})>"

    @property
    def storage_percentage(self) -> float:
        """Calculate storage usage percentage"""
        if self.storage_limite == 0:
            return 0.0
        return (self.storage_usado / self.storage_limite) * 100

    @property
    def is_storage_full(self) -> bool:
        """Check if storage is at capacity"""
        return self.storage_usado >= self.storage_limite

    def can_add_storage(self, size_bytes: int) -> bool:
        """Check if workspace can add more storage"""
        return (self.storage_usado + size_bytes) <= self.storage_limite
