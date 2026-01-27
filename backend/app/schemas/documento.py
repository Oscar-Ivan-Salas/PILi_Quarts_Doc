"""
Schemas de Documento
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict, Any
from datetime import datetime

class DocumentoBase(BaseModel):
    """Schema base de Documento"""
    nombre: str = Field(..., description="Nombre del documento")
    proyecto_id: Optional[int] = Field(None, description="ID del proyecto relacionado")

class DocumentoResponse(DocumentoBase):
    """Schema de respuesta de Documento"""
    id: int
    nombre_original: str
    ruta_archivo: str
    tipo_mime: str
    tamano: int
    contenido_texto: Optional[str] = None
    metadata_extraida: Optional[Dict[str, Any]] = None
    procesado: int
    mensaje_error: Optional[str] = None
    fecha_subida: datetime
    fecha_procesamiento: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

class DocumentoUploadResponse(BaseModel):
    """Schema de respuesta al subir documento"""
    success: bool
    message: str
    documento: Optional[DocumentoResponse] = None
    contenido_extraido: Optional[str] = None

class BusquedaSemanticaRequest(BaseModel):
    """Schema para búsqueda semántica en documentos"""
    query: str = Field(..., min_length=3, description="Texto a buscar")
    limite: int = Field(5, ge=1, le=20, description="Número máximo de resultados")
    proyecto_id: Optional[int] = Field(None, description="Filtrar por proyecto")

class ResultadoBusqueda(BaseModel):
    """Schema de resultado de búsqueda"""
    documento_id: int
    nombre_documento: str
    fragmento: str
    score: float
    metadata: Optional[Dict[str, Any]] = None