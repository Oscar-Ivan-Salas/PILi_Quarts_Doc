"""
Workspace Member Model - Many-to-many relationship
Following clean-code: Single Responsibility
"""
from sqlalchemy import Column, String, DateTime, ForeignKey, JSONB, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime

from ..base import Base


class WorkspaceMember(Base):
    """
    Represents a user's membership in a workspace.
    Includes role and permissions.
    """
    
    __tablename__ = 'workspace_members'
    __table_args__ = (
        PrimaryKeyConstraint('workspace_id', 'user_id'),
    )

    # Foreign keys
    workspace_id = Column(UUID(as_uuid=True), ForeignKey('workspaces.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    
    # Role and permissions
    rol = Column(String(50), nullable=False)  # owner, admin, editor, viewer
    permisos = Column(JSONB, default={})
    
    # Timestamp
    joined_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    workspace = relationship('Workspace', back_populates='members')
    user = relationship('User', back_populates='workspace_memberships')

    def __repr__(self) -> str:
        return f"<WorkspaceMember(workspace_id={self.workspace_id}, user_id={self.user_id}, rol={self.rol})>"

    @property
    def is_owner(self) -> bool:
        return self.rol == 'owner'

    @property
    def is_admin(self) -> bool:
        return self.rol in ['owner', 'admin']

    @property
    def can_edit(self) -> bool:
        return self.rol in ['owner', 'admin', 'editor']
