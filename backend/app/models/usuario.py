"""
Modelo: Usuario
Usuarios del sistema con planes de suscripción y límites de tokens
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime, timedelta
from app.core.database import Base


class Usuario(Base):
    """
    Modelo de Usuario del Sistema
    Gestiona usuarios con planes de suscripción (free, pro, enterprise)
    y límites de tokens para uso de IAs
    """
    __tablename__ = "usuarios"

    # Campos principales
    id = Column(Integer, primary_key=True, index=True)

    # Información personal
    nombre = Column(String(200), nullable=False, index=True)
    apellido = Column(String(200), nullable=False)
    email = Column(String(200), unique=True, nullable=False, index=True)
    telefono = Column(String(20), nullable=True)

    # Información profesional
    empresa = Column(String(200), nullable=True)
    cargo = Column(String(100), nullable=True)
    departamento = Column(String(100), nullable=True, default="Junín")
    ciudad = Column(String(100), nullable=True, default="Huancayo")

    # Autenticación (simplificada - mejorar en futuro con hash)
    password_hash = Column(String(500), nullable=True)
    activo = Column(Boolean, default=True, index=True)

    # Plan de suscripción
    plan = Column(String(50), default="free", index=True)  # free, pro, enterprise
    fecha_inicio_plan = Column(DateTime(timezone=True), server_default=func.now())
    fecha_fin_plan = Column(DateTime(timezone=True), nullable=True)

    # Sistema de tokens
    tokens_mensuales = Column(Integer, default=1000)  # Límite mensual según plan
    tokens_usados = Column(Integer, default=0)
    tokens_extra = Column(Integer, default=0)  # Tokens comprados adicionales
    fecha_reset_tokens = Column(DateTime(timezone=True), nullable=True)

    # Preferencias de IA
    ia_preferida = Column(String(50), default="gemini")  # gemini, claude, gpt-4, groq
    temperatura_ia = Column(Float, default=0.3)  # Temperatura para generación (0.0-1.0)

    # Estadísticas de uso
    total_cotizaciones = Column(Integer, default=0)
    total_proyectos = Column(Integer, default=0)
    total_documentos = Column(Integer, default=0)
    total_tokens_historico = Column(Integer, default=0)

    # Timestamps
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_modificacion = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
    ultimo_acceso = Column(DateTime(timezone=True), nullable=True)

    # Relaciones (para implementar en futuro)
    # cotizaciones = relationship("Cotizacion", back_populates="usuario")
    # proyectos = relationship("Proyecto", back_populates="usuario")

    def __repr__(self):
        return f"<Usuario(id={self.id}, nombre='{self.nombre}', email='{self.email}', plan='{self.plan}')>"

    def to_dict(self):
        """Convertir a diccionario"""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "email": self.email,
            "telefono": self.telefono,
            "empresa": self.empresa,
            "cargo": self.cargo,
            "departamento": self.departamento,
            "ciudad": self.ciudad,
            "activo": self.activo,
            "plan": self.plan,
            "tokens_mensuales": self.tokens_mensuales,
            "tokens_usados": self.tokens_usados,
            "tokens_disponibles": self.tokens_disponibles(),
            "ia_preferida": self.ia_preferida,
            "total_cotizaciones": self.total_cotizaciones,
            "total_proyectos": self.total_proyectos,
            "total_documentos": self.total_documentos,
            "fecha_creacion": self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            "ultimo_acceso": self.ultimo_acceso.isoformat() if self.ultimo_acceso else None,
        }

    def tokens_disponibles(self) -> int:
        """Calcula tokens disponibles del usuario"""
        # Verificar si hay que resetear tokens (nuevo mes)
        ahora = datetime.now()
        if self.fecha_reset_tokens and self.fecha_reset_tokens < ahora:
            return self.tokens_mensuales + self.tokens_extra

        disponibles = (self.tokens_mensuales + self.tokens_extra) - self.tokens_usados
        return max(0, disponibles)

    def necesita_reset_tokens(self) -> bool:
        """Verifica si necesita resetear tokens (nuevo mes)"""
        if not self.fecha_reset_tokens:
            return True
        return self.fecha_reset_tokens < datetime.now()

    def consumir_tokens(self, cantidad: int) -> bool:
        """
        Intenta consumir tokens
        Retorna True si hay suficientes, False si no
        """
        if self.tokens_disponibles() >= cantidad:
            self.tokens_usados += cantidad
            self.total_tokens_historico += cantidad
            return True
        return False

    def resetear_tokens(self):
        """Resetea los tokens usados (nuevo mes)"""
        self.tokens_usados = 0
        self.fecha_reset_tokens = datetime.now() + timedelta(days=30)

    def cambiar_plan(self, nuevo_plan: str):
        """Cambia el plan del usuario y ajusta tokens"""
        planes = {
            "free": 1000,
            "pro": 10000,
            "enterprise": 100000
        }

        if nuevo_plan in planes:
            self.plan = nuevo_plan
            self.tokens_mensuales = planes[nuevo_plan]
            self.fecha_inicio_plan = datetime.now()
            self.fecha_fin_plan = datetime.now() + timedelta(days=30)
            self.resetear_tokens()

    @staticmethod
    def get_plan_info(plan: str) -> dict:
        """Retorna información del plan"""
        planes = {
            "free": {
                "nombre": "Free",
                "tokens_mensuales": 1000,
                "ia_disponible": ["gemini", "groq"],
                "precio": 0,
                "descripcion": "Plan básico con IAs gratuitas"
            },
            "pro": {
                "nombre": "Pro",
                "tokens_mensuales": 10000,
                "ia_disponible": ["gemini", "claude", "gpt-4", "groq"],
                "precio": 29.99,
                "descripcion": "Plan profesional con todas las IAs"
            },
            "enterprise": {
                "nombre": "Enterprise",
                "tokens_mensuales": 100000,
                "ia_disponible": ["gemini", "claude", "gpt-4", "groq", "together", "cohere"],
                "precio": 299.99,
                "descripcion": "Plan empresarial sin límites"
            }
        }
        return planes.get(plan, planes["free"])
