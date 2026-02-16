"""
User Model - Following clean-code principles
Single Responsibility: Represents a user in the system
"""
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from ..base import Base


class User(Base):
    """User model with authentication and profile data"""
    
    __tablename__ = 'users'

    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Authentication
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    email_verified = Column(Boolean, default=False)
    
    # Profile
    nombre = Column(String(255), nullable=False)
    avatar_url = Column(String)
    rol_global = Column(String(50), default='member')
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    workspaces_owned = relationship('Workspace', back_populates='owner', cascade='all, delete-orphan')
    workspace_memberships = relationship('WorkspaceMember', back_populates='user', cascade='all, delete-orphan')
    proyecto_memberships = relationship('ProyectoMember', back_populates='user', cascade='all, delete-orphan')
    documentos_created = relationship('Documento', back_populates='creator')
    actividades = relationship('Actividad', back_populates='user')

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email}, nombre={self.nombre})>"

    @property
    def is_verified(self) -> bool:
        """Check if user email is verified"""
        return self.email_verified

    @property
    def is_admin(self) -> bool:
        """Check if user has global admin role"""
        return self.rol_global == 'admin'
