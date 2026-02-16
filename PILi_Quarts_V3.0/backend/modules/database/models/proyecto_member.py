"""
Proyecto Member Model - Team member assignment
Following clean-code principles
"""
from sqlalchemy import Column, String, DateTime, ForeignKey, JSONB, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime

from ..base import Base


class ProyectoMember(Base):
    """
    Represents a user's membership in a project.
    Includes role (project_manager, ingeniero, supervisor).
    """
    
    __tablename__ = 'proyecto_members'
    __table_args__ = (
        PrimaryKeyConstraint('proyecto_id', 'user_id'),
    )

    # Foreign keys
    proyecto_id = Column(UUID(as_uuid=True), ForeignKey('proyectos.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    
    # Role and permissions
    rol = Column(String(50), nullable=False)
    permisos = Column(JSONB, default={})
    
    # Timestamp
    joined_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    proyecto = relationship('Proyecto', back_populates='members')
    user = relationship('User', back_populates='proyecto_memberships')

    def __repr__(self) -> str:
        return f"<ProyectoMember(proyecto_id={self.proyecto_id}, user_id={self.user_id}, rol={self.rol})>"

    @property
    def is_manager(self) -> bool:
        return self.rol == 'project_manager'
