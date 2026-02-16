"""
Modelos SQLAlchemy para el Nodo N08 (Gestión de Identidad).
"""
from sqlalchemy import Column, Integer, String, ForeignKey, Text, JSON, DateTime
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class UsuarioEjecutor(Base):
    __tablename__ = 'usuarios_ejecutores'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_key = Column(String, unique=True, index=True) # ID único sistema (e.g. USER_001)
    
    # Perfil Profesional
    nombre_completo = Column(String, nullable=False)
    empresa = Column(String)
    ruc_dni = Column(String, nullable=False)
    direccion = Column(String)
    
    # Activos de Marca (Rutas a archivos o B64)
    logo_path = Column(String) 
    firma_path = Column(String)
    
    # Preferencias
    colores_hex = Column(JSON) # {"primary": "#CC0000", "secondary": "#000000"}
    
    # Relaciones
    proyectos = relationship("ProyectoActivo", back_populates="ejecutor")

class ClienteFinal(Base):
    __tablename__ = 'clientes_finales'

    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Identidad
    razon_social = Column(String, nullable=False)
    ruc_dni = Column(String, nullable=False)
    direccion = Column(String)
    persona_contacto = Column(String)
    
    # Relaciones
    proyectos = relationship("ProyectoActivo", back_populates="cliente")

class ProyectoActivo(Base):
    __tablename__ = 'proyectos_activos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_code = Column(String, unique=True, index=True) # e.g. PROJ_2026_001
    
    # Vinculación
    usuario_id = Column(Integer, ForeignKey('usuarios_ejecutores.id'))
    cliente_id = Column(Integer, ForeignKey('clientes_finales.id'))
    
    # Matriz 10x10 Reference
    service_id = Column(Integer) # 1-10 (Electricidad, etc.)
    document_type_id = Column(Integer) # 1-6
    industry_sector = Column(String) # Mineria, Residencial, etc.
    
    # Estado
    status = Column(String, default="DRAFT") # DRAFT, GENERATED, SENT
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relaciones
    ejecutor = relationship("UsuarioEjecutor", back_populates="proyectos")
    cliente = relationship("ClienteFinal", back_populates="proyectos")

# Configuración SQLite N08
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = f"sqlite:///{os.path.join(BASE_DIR, 'identity.db')}"
engine = create_engine(DB_PATH, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas de Identidad N08 creadas.")
