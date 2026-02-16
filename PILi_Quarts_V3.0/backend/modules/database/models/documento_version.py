"""
Documento Version Model - File version history
Following clean-code: Single Responsibility
"""
from sqlalchemy import Column, String, Text, Integer, BigInteger, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from ..base import Base


class DocumentoVersion(Base):
    """
    Represents a specific version of a document.
    Stores file URL, size, and change description.
    """
    
    __tablename__ = 'documento_versiones'
    __table_args__ = (
        UniqueConstraint('documento_id', 'version', name='uq_documento_version'),
    )

    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Document relationship
    documento_id = Column(UUID(as_uuid=True), ForeignKey('documentos.id', ondelete='CASCADE'), nullable=False, index=True)
    
    # Version info
    version = Column(Integer, nullable=False)
    file_url = Column(Text, nullable=False)  # S3/Cloud storage URL
    file_size = Column(BigInteger)  # Size in bytes
    cambios = Column(Text)  # Description of changes
    
    # Creator
    created_by = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    
    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    documento = relationship('Documento', back_populates='versiones')
    creator = relationship('User')

    def __repr__(self) -> str:
        return f"<DocumentoVersion(documento_id={self.documento_id}, version={self.version})>"

    @property
    def file_size_mb(self) -> float:
        """Get file size in megabytes"""
        if not self.file_size:
            return 0.0
        return self.file_size / (1024 * 1024)

    @property
    def file_size_human(self) -> str:
        """Get human-readable file size"""
        if not self.file_size:
            return "0 B"
        
        size = self.file_size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"
