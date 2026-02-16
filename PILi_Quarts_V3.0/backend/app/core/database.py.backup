"""
Configuración de base de datos con SQLAlchemy - VERSIÓN CORREGIDA
"""
from sqlalchemy import create_engine, event, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# =======================================
# CREAR ENGINE DE SQLALCHEMY
# =======================================

# Preparamos los argumentos de conexión
connect_args = {}

# Configuración específica para SQLite
if settings.DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False
    logger.info("Configurando SQLite con check_same_thread=False.")

# Creamos el engine
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DATABASE_ECHO,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    pool_recycle=3600,
    connect_args=connect_args
)

# =======================================
# SESSION LOCAL
# =======================================

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# =======================================
# BASE PARA MODELOS
# =======================================

Base = declarative_base()

# =======================================
# DEPENDENCY PARA FASTAPI
# =======================================

def get_db() -> Session:
    """
    Dependency que proporciona una sesión de base de datos.
    Maneja la apertura y cierre de la sesión.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# =======================================
# FUNCIONES HELPER
# =======================================

def init_db():
    """
    Crear todas las tablas en la base de datos
    """
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Base de datos inicializada con éxito.")
    except Exception as e:
        logger.error(f"Error al inicializar la base de datos: {str(e)}")
        raise

def drop_db():
    """
    CUIDADO: Elimina todas las tablas
    Solo usar en desarrollo
    """
    if settings.ENVIRONMENT == "production":
        raise Exception("No se puede eliminar base de datos en producción")
    
    Base.metadata.drop_all(bind=engine)
    logger.warning("Todas las tablas han sido eliminadas")

def check_db_connection() -> bool:
    """
    Verificar conexión a base de datos
    """
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return True
    except Exception as e:
        logger.error(f"Error de conexión a base de datos: {str(e)}")
        return False

# =======================================
# CONTEXT MANAGER PARA SESIONES
# =======================================

class DatabaseSession:
    """
    Context manager para manejar sesiones de base de datos
    
    Uso:
    with DatabaseSession() as db:
        user = db.query(User).first()
    """
    
    def __enter__(self) -> Session:
        self.db = SessionLocal()
        return self.db
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.db.rollback()
        self.db.close()