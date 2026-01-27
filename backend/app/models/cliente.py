"""
Modelo: Cliente
Gestión de clientes para cotizaciones y proyectos
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Cliente(Base):
    """
    Modelo de Cliente
    Almacena información de clientes para reutilizar en cotizaciones y proyectos
    """
    __tablename__ = "clientes"

    # Campos principales
    id = Column(Integer, primary_key=True, index=True)

    # Información básica
    nombre = Column(String(200), nullable=False, index=True)  # Nombre o Razón Social
    ruc = Column(String(11), unique=True, nullable=False, index=True)  # RUC peruano (11 dígitos)
    telefono = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True, index=True)

    # Dirección
    direccion = Column(String(500), nullable=True)
    ciudad = Column(String(100), nullable=True, default="Huancayo")
    departamento = Column(String(100), nullable=True, default="Junín")

    # Web y branding
    web = Column(String(200), nullable=True)
    logo_base64 = Column(Text, nullable=True)

    # Clasificación
    industria = Column(String(50), nullable=True, index=True)  # Construcción, Minería, etc.
    tipo_cliente = Column(String(50), default="empresa", index=True)  # empresa, persona, gobierno

    # Contacto
    persona_contacto = Column(String(200), nullable=True)
    cargo_contacto = Column(String(100), nullable=True)
    telefono_contacto = Column(String(20), nullable=True)
    email_contacto = Column(String(100), nullable=True)

    # Notas
    notas = Column(Text, nullable=True)

    # Estado
    activo = Column(String(10), default="activo", index=True)  # activo, inactivo

    # Datos adicionales
    metadata_adicional = Column(JSON, nullable=True)

    # Timestamps
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_modificacion = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    fecha_ultima_cotizacion = Column(DateTime(timezone=True), nullable=True)

    # Relaciones (cuando se implementen)
    # cotizaciones = relationship("Cotizacion", back_populates="cliente_rel")
    # proyectos = relationship("Proyecto", back_populates="cliente_rel")

    def __repr__(self):
        return f"<Cliente(id={self.id}, nombre='{self.nombre}', ruc='{self.ruc}')>"

    def to_dict(self):
        """Convertir a diccionario"""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "ruc": self.ruc,
            "telefono": self.telefono,
            "email": self.email,
            "direccion": self.direccion,
            "ciudad": self.ciudad,
            "departamento": self.departamento,
            "web": self.web,
            "industria": self.industria,
            "tipo_cliente": self.tipo_cliente,
            "persona_contacto": self.persona_contacto,
            "cargo_contacto": self.cargo_contacto,
            "telefono_contacto": self.telefono_contacto,
            "email_contacto": self.email_contacto,
            "notas": self.notas,
            "activo": self.activo,
            "metadata_adicional": self.metadata_adicional,
            "fecha_creacion": self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            "fecha_modificacion": self.fecha_modificacion.isoformat() if self.fecha_modificacion else None,
            "fecha_ultima_cotizacion": self.fecha_ultima_cotizacion.isoformat() if self.fecha_ultima_cotizacion else None,
        }
