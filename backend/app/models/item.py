"""
Modelo: Item (items de cotización)
"""
from sqlalchemy import Column, Integer, Text, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Item(Base):
    """
    Modelo de Item
    Representa un item individual dentro de una cotización
    """
    __tablename__ = "items"
    
    # Campos principales
    id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(Text, nullable=False)
    cantidad = Column(Numeric(10, 2), nullable=False, default=1.0)
    precio_unitario = Column(Numeric(10, 2), nullable=False)
    total = Column(Numeric(10, 2), nullable=False)
    
    # Relación con cotización
    cotizacion_id = Column(
        Integer,
        ForeignKey("cotizaciones.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    cotizacion = relationship("Cotizacion", back_populates="items_rel")
    
    def __repr__(self):
        return f"<Item(id={self.id}, descripcion='{self.descripcion[:30]}...', total={self.total})>"
    
    def calcular_total(self):
        """Calcular el total del item"""
        self.total = round(float(self.cantidad) * float(self.precio_unitario), 2)
    
    def to_dict(self):
        """Convertir a diccionario"""
        return {
            "id": self.id,
            "descripcion": self.descripcion,
            "cantidad": float(self.cantidad) if self.cantidad else 0.00,
            "precio_unitario": float(self.precio_unitario) if self.precio_unitario else 0.00,
            "total": float(self.total) if self.total else 0.00,
            "cotizacion_id": self.cotizacion_id,
        }