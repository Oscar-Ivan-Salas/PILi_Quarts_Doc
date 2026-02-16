"""
═══════════════════════════════════════════════════════════════
TESLA COTIZADOR V3.0 - CONFIGURACIÓN ACTUALIZADA
═══════════════════════════════════════════════════════════════
Configuración de la aplicación con integración Gemini
"""
from pydantic_settings import BaseSettings
from pydantic import Field, validator
from typing import List, Optional
import os
from pathlib import Path
import logging
import sys
from logging.handlers import RotatingFileHandler

# =======================================
# DEFINICIÓN DE RUTAS (CORREGIDO)
# =======================================

# BASE_DIR apunta a tu_proyecto/backend
BASE_DIR = Path(__file__).resolve().parent.parent
# PROJECT_ROOT apunta a tu_proyecto (La raíz real del proyecto)
PROJECT_ROOT = BASE_DIR.parent.parent

# =======================================
# CONFIGURACIÓN DE LOGGING
# =======================================
LOG_DIR = BASE_DIR / "logs" # Los logs SÍ van dentro de backend/logs
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "app.log"
LOG_LEVEL_DEFAULT = os.getenv("LOG_LEVEL", "INFO").upper()

logging.basicConfig(
    level=LOG_LEVEL_DEFAULT,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.StreamHandler(sys.stdout),
        RotatingFileHandler(
            LOG_FILE, 
            maxBytes=10*1024*1024, # 10MB
            backupCount=5,
            encoding='utf-8'
        )
    ]
)
logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
logging.getLogger('uvicorn.access').setLevel(logging.WARNING)
logging.getLogger('watchfiles').setLevel(logging.WARNING)
logger = logging.getLogger(__name__)
logger.info("==================================================")
logger.info("Sistema de Logging inicializado.")
logger.info(f"Logs de archivo en: {LOG_FILE}")
logger.info("==================================================")


# =======================================
# CLASE DE CONFIGURACIÓN (SETTINGS)
# =======================================

class Settings(BaseSettings):
    """
    Configuración general de la aplicación
    Carga variables desde .env
    """
    
    # =======================================
    # INFORMACIÓN DE LA APP
    # =======================================
    APP_NAME: str = "Tesla Cotizador"
    VERSION: str = "3.0.0"
    
    # =======================================
    # LÓGICA DE BD INTELIGENTE
    # =======================================
    ENVIRONMENT: str = Field(default="development", env="ENVIRONMENT")
    DEBUG: bool = Field(default=True, env="DEBUG")
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    
    # 1. URL de Producción (Leída desde .env)
    PROD_DATABASE_URL: Optional[str] = Field(None, env="PROD_DATABASE_URL")
    
    # 2. URL de Desarrollo (SQLite) - ✅ APUNTA A LA RAÍZ /database/
    # 2. URL de Desarrollo (SQLite) - ✅ APUNTA A LA RAÍZ /database/
    # Usar ruta absoluta con forward slashes para Windows
    DEV_DATABASE_URL: str = f"sqlite:///{(PROJECT_ROOT / 'database' / 'tesla_cotizador.db').as_posix()}"

    # 3. Esta será la variable final que usará la app
    DATABASE_URL: Optional[str] = None
    DATABASE_ECHO: bool = False

    @validator("DATABASE_URL", pre=False, always=True)
    def set_database_url(cls, v, values):
        """
        Elige la URL de la base de datos correcta basándose en el ENTORNO.
        """
        env = values.get("ENVIRONMENT", "development")
        logger = logging.getLogger(__name__)
        
        if env == "production":
            logger.info("Usando configuración de Base de Datos de PRODUCCIÓN (PostgreSQL).")
            prod_url = values.get("PROD_DATABASE_URL")
            if not prod_url:
                logger.error("¡ERROR CRÍTICO! ENTORNO=production pero PROD_DATABASE_URL no está definida en .env")
                raise ValueError("PROD_DATABASE_URL es requerida en entorno de producción")
            return prod_url
        else:
            # Modo Development (SQLite)
            logger.info("Usando configuración de Base de Datos de DESARROLLO (SQLite).")
            sqlite_url = values.get("DEV_DATABASE_URL")
            db_path_str = sqlite_url.split("///")[1]
            db_path = Path(db_path_str)
            db_path.parent.mkdir(parents=True, exist_ok=True)
            logger.info(f"Ruta de base de datos SQLite: {sqlite_url}")
            return sqlite_url

    # =======================================
    # RUTAS DE ARCHIVOS - ✅ TODO EN LA RAÍZ /storage/
    # =======================================
    UPLOAD_DIR: Path = PROJECT_ROOT / "storage" / "documentos"
    GENERATED_DIR: Path = PROJECT_ROOT / "storage" / "generados"
    TEMPLATES_DIR: Path = PROJECT_ROOT / "storage" / "templates"
    CHROMA_PERSIST_DIRECTORY: Path = PROJECT_ROOT / "storage" / "chroma_db"
    
    ALLOWED_EXTENSIONS: str = Field(default="pdf,docx,xlsx,png,jpg,jpeg", env="ALLOWED_EXTENSIONS")
    MAX_UPLOAD_SIZE_MB: int = Field(default=10, env="MAX_UPLOAD_SIZE_MB")
    
    # ✅ CORREGIDO - Apuntan a las rutas correctas
    STORAGE_PATH: str = str(PROJECT_ROOT / "storage")
    TEMPLATES_PATH: str = str(PROJECT_ROOT / "storage" / "templates")
    
    # Computed property para MAX_FILE_SIZE (usado por file_processor)
    @property
    def MAX_FILE_SIZE(self) -> int:
        """Tamaño máximo de archivo en bytes"""
        return self.MAX_UPLOAD_SIZE_MB * 1024 * 1024

    # =======================================
    # GEMINI AI - CONFIGURACIÓN FLEXIBLE
    # =======================================
    GEMINI_API_KEY: str = Field(default="", env="GEMINI_API_KEY")
    GEMINI_MODEL: str = Field(default="gemini-1.5-pro", env="GEMINI_MODEL")
    EMBEDDING_MODEL: str = Field(default="models/embedding-001", env="EMBEDDING_MODEL")
    TEMPERATURE: float = Field(default=0.3, env="TEMPERATURE")
    MAX_TOKENS: int = Field(default=4000, env="MAX_TOKENS")
    
    # =======================================
    # MÓDULOS DE SERVICIO
    # =======================================
    @property
    def WORD_TEMPLATE_PATH(self) -> str:
        return str(self.TEMPLATES_DIR / "plantilla_cotizacion.docx")
    
    @property
    def PDF_TEMPLATE_PATH(self) -> str:
        return str(self.TEMPLATES_DIR / "plantilla_informe_pdf.html")
    
    @property
    def PDF_LOGO_PATH(self) -> str:
        return str(self.TEMPLATES_DIR / "logo_tesla.png")
    
    # =======================================
    # SEGURIDAD - CON DEFAULTS SEGUROS
    # =======================================
    SECRET_KEY: str = Field(default="tesla-secret-key-change-in-production", env="SECRET_KEY")
    ALGORITHM: str = Field(default="HS256", env="ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")

    # =======================================
    # SERVIDOR Y CORS
    # =======================================
    FRONTEND_URL: str = Field(default="http://localhost:3000", env="FRONTEND_URL")
    BACKEND_HOST: str = Field(default="0.0.0.0", env="BACKEND_HOST")
    BACKEND_PORT: int = Field(default=8000, env="BACKEND_PORT")
    
    # =======================================
    # CONFIGURACIÓN DE PYDANTIC
    # =======================================
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        arbitrary_types_allowed = True
        extra = 'ignore'

# Instancia única de la configuración
settings = Settings()


# =======================================
# FUNCIONES HELPER
# =======================================

def get_database_url() -> str:
    return settings.DATABASE_URL

def is_debug_mode() -> bool:
    return settings.DEBUG

def get_upload_directory() -> Path:
    settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    return settings.UPLOAD_DIR

def get_generated_directory() -> Path:
    settings.GENERATED_DIR.mkdir(parents=True, exist_ok=True)
    return settings.GENERATED_DIR

def validate_file_extension(filename: str) -> bool:
    extension = filename.split('.')[-1].lower()
    allowed_list = [ext.strip() for ext in settings.ALLOWED_EXTENSIONS.split(',')]
    return extension in allowed_list

def get_word_template_path() -> Path:
    path = Path(settings.WORD_TEMPLATE_PATH)
    if not path.exists():
        logging.error(f"No se encontró la plantilla de Word en: {path}")
        raise FileNotFoundError(f"No se encontró la plantilla de Word en: {path}")
    return path

def get_pdf_template_path() -> Path:
    path = Path(settings.PDF_TEMPLATE_PATH)
    if not path.exists():
        logging.error(f"No se encontró la plantilla de PDF en: {path}")
        raise FileNotFoundError(f"No se encontró la plantilla de PDF en: {path}")
    return path

def get_pdf_logo_path() -> Path:
    path = Path(settings.PDF_LOGO_PATH)
    if not path.exists():
        logging.warning(f"No se encontró el logo de PDF en: {path}. El PDF se generará sin logo.")
        return None
    return path

def get_chroma_persist_directory() -> str:
    settings.CHROMA_PERSIST_DIRECTORY.mkdir(parents=True, exist_ok=True)
    return str(settings.CHROMA_PERSIST_DIRECTORY)

def get_embedding_model_name() -> str:
    return settings.EMBEDDING_MODEL

def get_secret_key() -> str:
    if settings.SECRET_KEY == "tesla-secret-key-change-in-production":
        logging.warning("Estás usando la SECRET_KEY por defecto. ¡Cámbiala en producción!")
    return settings.SECRET_KEY

def get_jwt_algorithm() -> str:
    return settings.ALGORITHM

def get_access_token_expire_minutes() -> int:
    return settings.ACCESS_TOKEN_EXPIRE_MINUTES

def get_frontend_url() -> str:
    return settings.FRONTEND_URL

def get_max_upload_size_bytes() -> int:
    return settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024

# =======================================
# FUNCIONES GEMINI - NUEVAS
# =======================================

def validate_gemini_key() -> bool:
    """Valida si la API key de Gemini está configurada"""
    try:
        api_key = settings.GEMINI_API_KEY
        return api_key and api_key != "" and api_key != "tu_gemini_api_key_aqui"
    except:
        return False

def get_gemini_api_key() -> str:
    """Obtiene la API key de Gemini"""
    return settings.GEMINI_API_KEY

def get_gemini_model() -> str:
    """Obtiene el modelo de Gemini a usar"""
    return settings.GEMINI_MODEL

# =======================================
# CONFIGURACIÓN DE LOGGING ESPECÍFICA
# =======================================

def setup_tesla_logging():
    """Configura logging específico para Tesla"""
    tesla_logger = logging.getLogger("tesla")
    tesla_logger.setLevel(logging.INFO)
    
    # Handler específico para Tesla
    tesla_handler = RotatingFileHandler(
        LOG_DIR / "tesla.log",
        maxBytes=5*1024*1024,  # 5MB
        backupCount=3,
        encoding='utf-8'
    )
    tesla_handler.setFormatter(
        logging.Formatter('%(asctime)s - TESLA - %(levelname)s - %(message)s')
    )
    tesla_logger.addHandler(tesla_handler)
    
    return tesla_logger

# Configurar logging de Tesla
tesla_logger = setup_tesla_logging()
tesla_logger.info("🚀 Sistema Tesla inicializado")
# tesla_logger.info(f"🤖 Gemini configurado: {validate_gemini_key()}")