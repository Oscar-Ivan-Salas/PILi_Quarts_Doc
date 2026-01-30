"""
Actividad Model - Activity/Audit log
Following clean-code and architecture principles
"""
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, JSONB
from sqlalchemy.dialects.postgresql import UUID, INET
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from ..base import Base


class Actividad(Base):
    """
    Represents an activity/action in the system.
    Used for audit logs and activity feeds.
    """
    
    __tablename__ = 'actividad'

    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # User who performed the action
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='SET NULL'))
    
    # Context (where the action happened)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey('workspaces.id', ondelete='CASCADE'), index=True)
    proyecto_id = Column(UUID(as_uuid=True), ForeignKey('proyectos.id', ondelete='CASCADE'), index=True)
    documento_id = Column(UUID(as_uuid=True), ForeignKey('documentos.id', ondelete='CASCADE'))
    
    # Action details
    accion = Column(String(50), nullable=False)  # created, updated, deleted, commented, approved
    detalles = Column(JSONB, default={})  # Additional details
    
    # Request metadata
    ip_address = Column(INET)
    user_agent = Column(Text)
    
    # Timestamp
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    # Relationships
    user = relationship('User', back_populates='actividades')
    workspace = relationship('Workspace', back_populates='actividades')
    proyecto = relationship('Proyecto', back_populates='actividades')
    documento = relationship('Documento', back_populates='actividades')

    def __repr__(self) -> str:
        return f"<Actividad(id={self.id}, accion={self.accion}, timestamp={self.timestamp})>"

    @property
    def is_recent(self) -> bool:
        """Check if activity is from last 24 hours"""
        if not self.timestamp:
            return False
        delta = datetime.utcnow() - self.timestamp
        return delta.total_seconds() < 86400  # 24 hours
