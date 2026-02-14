from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any, Union

# ══════════════════════════════════════════════════════════════════════════════
# 🛡️ INPUT MODELS (Strict Contract)
# ══════════════════════════════════════════════════════════════════════════════

class Header(BaseModel):
    user_id: str
    service_id: int = Field(..., ge=1, le=10, description="Service ID 1-10")
    document_type: Union[int, str] = Field(..., description="Document Type ID (1-6) or Template Name")

class Branding(BaseModel):
    logo_b64: Optional[str] = None
    color_hex: str = "#0052A3" # Default Tesla Blue

class Payload(BaseModel):
    items: List[Dict[str, Any]] = []
    totals: Dict[str, Any] = {}
    technical_notes: Optional[str] = ""
    client_info: Optional[Dict[str, Any]] = {} # Added for generated docs context

class BinaryFactoryInput(BaseModel):
    header: Header
    branding: Branding
    payload: Payload
    output_format: str = Field(..., pattern="^(XLSX|DOCX|PDF)$")

    @validator('output_format')
    def validate_format(cls, v):
        return v.upper()
