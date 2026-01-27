"""
Schemas de Pydantic para validación de datos
"""
from app.schemas.proyecto import (
    ProyectoBase,
    ProyectoCreate,
    ProyectoUpdate,
    ProyectoResponse
)
from app.schemas.cotizacion import (
    ItemBase,
    ItemCreate,
    CotizacionBase,
    CotizacionCreate,
    CotizacionUpdate,
    CotizacionResponse
)
from app.schemas.documento import (
    DocumentoBase,
    DocumentoResponse
)
from app.schemas.cliente import (
    ClienteBase,
    ClienteCreate,
    ClienteUpdate,
    ClienteResponse,
    ClienteListResponse
)

__all__ = [
    # Proyecto
    "ProyectoBase",
    "ProyectoCreate",
    "ProyectoUpdate",
    "ProyectoResponse",

    # Cotización
    "ItemBase",
    "ItemCreate",
    "CotizacionBase",
    "CotizacionCreate",
    "CotizacionUpdate",
    "CotizacionResponse",

    # Documento
    "DocumentoBase",
    "DocumentoResponse",

    # Cliente
    "ClienteBase",
    "ClienteCreate",
    "ClienteUpdate",
    "ClienteResponse",
    "ClienteListResponse",
]