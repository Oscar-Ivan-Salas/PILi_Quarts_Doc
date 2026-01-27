"""
Schemas de Proyecto
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum

class EstadoProyecto(str, Enum):
    """Estados posibles de un proyecto"""
    PLANIFICACION = "planificacion"
    EN_PROGRESO = "en_progreso"
    COMPLETADO = "completado"
    CANCELADO = "cancelado"

class ProyectoBase(BaseModel):
    """Schema base de Proyecto"""
    nombre: str = Field(..., min_length=3, max_length=200, description="Nombre del proyecto")
    descripcion: Optional[str] = Field(None, description="Descripción del proyecto")
    cliente: str = Field(..., min_length=3, max_length=200, description="Nombre del cliente")
    estado: EstadoProyecto = Field(default=EstadoProyecto.PLANIFICACION, description="Estado del proyecto")
    
    # ✅ CAMPOS PMI
    servicio: Optional[str] = Field(None, max_length=50, description="Servicio del proyecto")
    industria: Optional[str] = Field(None, max_length=50, description="Industria del proyecto")
    presupuesto: Optional[float] = Field(None, description="Presupuesto estimado")
    moneda: Optional[str] = Field('PEN', max_length=3, description="Moneda (PEN, USD, EUR)")
    duracion_total: Optional[int] = Field(None, description="Duración total en días")
    tipo_dias: Optional[str] = Field('habiles', max_length=20, description="Tipo de días (habiles, calendario)")
    area_m2: Optional[float] = Field(None, description="Área del proyecto en m²")
    tiene_area: Optional[bool] = Field(False, description="Si el proyecto tiene área definida")
    alcance_proyecto: Optional[str] = Field(None, description="Alcance del proyecto")
    ubicacion: Optional[str] = Field(None, max_length=200, description="Ubicación del proyecto")
    normativa: Optional[str] = Field(None, max_length=200, description="Normativa aplicable")
    
    metadata_adicional: Optional[Dict[str, Any]] = Field(None, description="Metadata adicional en formato JSON")

class ProyectoCreate(ProyectoBase):
    """Schema para crear un proyecto"""
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None

class ProyectoUpdate(BaseModel):
    """Schema para actualizar un proyecto"""
    nombre: Optional[str] = Field(None, min_length=3, max_length=200)
    descripcion: Optional[str] = None
    cliente: Optional[str] = Field(None, min_length=3, max_length=200)
    estado: Optional[EstadoProyecto] = None
    
    # ✅ CAMPOS PMI
    servicio: Optional[str] = None
    industria: Optional[str] = None
    presupuesto: Optional[float] = None
    moneda: Optional[str] = None
    duracion_total: Optional[int] = None
    tipo_dias: Optional[str] = None
    area_m2: Optional[float] = None
    tiene_area: Optional[bool] = None
    alcance_proyecto: Optional[str] = None
    ubicacion: Optional[str] = None
    normativa: Optional[str] = None
    
    metadata_adicional: Optional[Dict[str, Any]] = None
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None

class ProyectoResponse(ProyectoBase):
    """Schema de respuesta de Proyecto"""
    id: int
    fecha_creacion: datetime
    fecha_modificacion: datetime
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    
    
    model_config = ConfigDict(from_attributes=True)

class ProyectoDraftCreate(BaseModel):
    """Schema para crear un borrador de proyecto (todo opcional menos cliente/nombre sugerido)"""
    # Al crear un draft inicial, puede que ni siquiera tengamos nombre
    nombre: Optional[str] = Field("Nuevo Proyecto (Borrador)", max_length=200)
    cliente: Optional[str] = Field("Cliente Sin Asignar", max_length=200)
    estado: EstadoProyecto = Field(default=EstadoProyecto.PLANIFICACION)
    
    # Metadata es el rey en los drafts
    metadata_adicional: Optional[Dict[str, Any]] = Field(default_factory=dict)
    
class ProyectoDraftUpdate(BaseModel):
    """Schema para actualizar un borrador (Patch flexible)"""
    nombre: Optional[str] = None
    cliente: Optional[str] = None
    estado: Optional[EstadoProyecto] = None
    
    # Campos PMI específicos que podrían venir
    servicio: Optional[str] = None
    industria: Optional[str] = None
    duracion_total: Optional[int] = None
    fecha_inicio: Optional[datetime] = None
    
    # Payload completo para guardar estado de la UI
    metadata_adicional: Optional[Dict[str, Any]] = None
