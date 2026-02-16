"""
Modelos SQLAlchemy para el conocimiento de PILi (N02).
"""
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

Base = declarative_base()

class PiliService(Base):
    __tablename__ = 'pili_services'

    id = Column(Integer, primary_key=True, autoincrement=True)
    service_key = Column(String, unique=True, nullable=False, index=True) # ej: 'electricidad_residencial'
    display_name = Column(String, nullable=False)
    normativa_referencia = Column(String)
    descripcion = Column(Text)
    
    # Relaciones
    knowledge_items = relationship("PiliKnowledgeItem", back_populates="service", cascade="all, delete-orphan")
    rules = relationship("PiliRule", back_populates="service", cascade="all, delete-orphan")
    template_configs = relationship("PiliTemplateConfig", back_populates="service", cascade="all, delete-orphan")

class PiliKnowledgeItem(Base):
    __tablename__ = 'pili_knowledge_base'

    id = Column(Integer, primary_key=True, autoincrement=True)
    service_id = Column(Integer, ForeignKey('pili_services.id'), nullable=False)
    
    category = Column(String) # 'MATERIAL', 'MANO_OBRA', 'EQUIPO', 'GENERAL'
    item_key = Column(String) # Clave interna del item ej: 'punto_luz_empotrado'
    item_description = Column(String, nullable=False)
    unit_measure = Column(String) # 'm2', 'und', 'glba'
    unit_price = Column(Float, nullable=False)
    currency = Column(String, default="PEN") # 'PEN', 'USD'
    
    service = relationship("PiliService", back_populates="knowledge_items")

class PiliRule(Base):
    __tablename__ = 'pili_rules'

    id = Column(Integer, primary_key=True)
    service_id = Column(Integer, ForeignKey('pili_services.id'))
    
    rule_key = Column(String)
    rule_value = Column(String)
    rule_type = Column(String) # CALCULATION, CONSTRAINT, WARNING
    
    service = relationship("PiliService", back_populates="rules")

class PiliTemplateConfig(Base):
    __tablename__ = 'pili_template_configs'
    id = Column(Integer, primary_key=True)
    service_id = Column(Integer, ForeignKey('pili_services.id'))
    document_type_id = Column(Integer) # 1-6
    template_ref = Column(String) # Folder name in N04/templates
    logic_class = Column(String)  # Python class for special calcs
    css_ref = Column(String)      # Shared CSS file

    service = relationship("PiliService", back_populates="template_configs")


# Configuración de BD SQLite local para este módulo
# Usamos una BD separada para conocimiento o la integramos a la principal?
# Por aislamiento, mejor su propia BD de conocimiento 'pili_knowledge.db'
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = f"sqlite:///{os.path.join(BASE_DIR, 'pili_knowledge.db')}"

engine = create_engine(DB_PATH, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas de conocimiento N02 creadas/verificadas.")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
