"""
Modelo: Cotizacion
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Numeric, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Cotizacion(Base):
    """
    Modelo de Cotización
    Representa una cotización generada para un proyecto
    """
    __tablename__ = "cotizaciones"
    
    # Campos principales
    id = Column(Integer, primary_key=True, index=True)
    numero = Column(String(50), unique=True, nullable=False, index=True)
    cliente = Column(String(200), nullable=False, index=True)
    proyecto = Column(String(200), nullable=False)
    descripcion = Column(Text, nullable=True)
    
    # Totales
    subtotal = Column(Numeric(10, 2), default=0.00)
    igv = Column(Numeric(10, 2), default=0.00)
    total = Column(Numeric(10, 2), default=0.00)
    
    # ✅ CAMPOS QUE FALTABAN (AHORA EN EL LUGAR CORRECTO)
    observaciones = Column(Text, nullable=True)
    vigencia = Column(String(100), nullable=True, default="30 días")
    
    # Estado
    estado = Column(String(50), default="borrador", index=True)
    
    # Datos estructurados
    items = Column(JSON, nullable=True)
    metadata_adicional = Column(JSON, nullable=True)
    
    # Timestamps
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_modificacion = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
    
    # Relación con proyecto
    proyecto_id = Column(Integer, ForeignKey("proyectos.id", ondelete="SET NULL"), nullable=True)
    proyecto_rel = relationship("Proyecto", back_populates="cotizaciones")
    
    # Relación con items
    items_rel = relationship(
        "Item",
        back_populates="cotizacion",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self):
        return f"<Cotizacion(id={self.id}, numero='{self.numero}', cliente='{self.cliente}', total={self.total})>"
    
    def calcular_totales(self):
        """
        Calcular subtotal, IGV y total desde los items
        """
        if self.items_rel:
            self.subtotal = sum(item.total for item in self.items_rel)
        elif self.items and isinstance(self.items, list):
            self.subtotal = sum(
                float(item.get("cantidad", 0)) * float(item.get("precio_unitario", 0))
                for item in self.items
            )
        else:
            self.subtotal = 0.00
        
        self.igv = round(self.subtotal * 0.18, 2)
        self.total = round(self.subtotal + self.igv, 2)
    
    def to_dict(self):
        """Convertir a diccionario"""
        return {
            "id": self.id,
            "numero": self.numero,
            "cliente": self.cliente,
            "proyecto": self.proyecto,
            "descripcion": self.descripcion,
            "subtotal": float(self.subtotal) if self.subtotal else 0.00,
            "igv": float(self.igv) if self.igv else 0.00,
            "total": float(self.total) if self.total else 0.00,
            "estado": self.estado,
            "items": self.items,
            "metadata_adicional": self.metadata_adicional,
            "fecha_creacion": self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            "fecha_modificacion": self.fecha_modificacion.isoformat() if self.fecha_modificacion else None,
            "proyecto_id": self.proyecto_id,
            "observaciones": self.observaciones,
            "vigencia": self.vigencia,
        }