"""
Modelo: Documento
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON, SmallInteger
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Documento(Base):
    """
    Modelo de Documento
    Representa un documento subido y procesado
    """
    __tablename__ = "documentos"
    
    # Campos principales
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(200), nullable=False)
    nombre_original = Column(String(200), nullable=False)
    ruta_archivo = Column(String(500), nullable=False)
    tipo_mime = Column(String(100), nullable=False)
    tamano = Column(Integer, nullable=False)
    
    # Contenido extraído
    contenido_texto = Column(Text, nullable=True)
    metadata_extraida = Column(JSON, nullable=True)
    
    # Estado de procesamiento
    # 0: pendiente, 1: procesado, 2: error
    procesado = Column(SmallInteger, default=0, index=True)
    mensaje_error = Column(Text, nullable=True)
    
    # Timestamps
    fecha_subida = Column(DateTime(timezone=True), server_default=func.now())
    fecha_procesamiento = Column(DateTime(timezone=True), nullable=True)
    
    # Relación con proyecto
    proyecto_id = Column(
        Integer,
        ForeignKey("proyectos.id", ondelete="CASCADE"),
        nullable=True,
        index=True
    )
    proyecto = relationship("Proyecto", back_populates="documentos")
    
    def __repr__(self):
        return f"<Documento(id={self.id}, nombre='{self.nombre}', procesado={self.procesado})>"
    
    def marcar_como_procesado(self, contenido: str = None):
        """Marcar documento como procesado"""
        self.procesado = 1
        self.fecha_procesamiento = func.now()
        if contenido:
            self.contenido_texto = contenido
    
    def marcar_como_error(self, mensaje: str):
        """Marcar documento con error"""
        self.procesado = 2
        self.mensaje_error = mensaje
        self.fecha_procesamiento = func.now()
    
    def to_dict(self):
        """Convertir a diccionario"""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "nombre_original": self.nombre_original,
            "ruta_archivo": self.ruta_archivo,
            "tipo_mime": self.tipo_mime,
            "tamano": self.tamano,
            "contenido_texto": self.contenido_texto,
            "metadata_extraida": self.metadata_extraida,
            "procesado": self.procesado,
            "mensaje_error": self.mensaje_error,
            "fecha_subida": self.fecha_subida.isoformat() if self.fecha_subida else None,
            "fecha_procesamiento": self.fecha_procesamiento.isoformat() if self.fecha_procesamiento else None,
            "proyecto_id": self.proyecto_id,
        }