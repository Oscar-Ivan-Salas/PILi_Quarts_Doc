"""
PILI API Schemas - Pydantic Models
Enterprise-grade request/response validation
Following api-patterns and clean-code skills
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, List, Any, Union
from datetime import datetime
from uuid import UUID


class ChatMessageRequest(BaseModel):
    """
    Chat message request schema.
    
    Following api-patterns: Clear request validation
    """
    user_id: str = Field(..., description="Unique user identifier")
    message: str = Field(..., min_length=1, max_length=5000, description="User message")
    context: Optional[Dict[str, Any]] = Field(None, description="Additional context")
    
    @validator('message')
    def message_not_empty(cls, v):
        """Ensure message is not just whitespace"""
        if not v.strip():
            raise ValueError("Message cannot be empty or whitespace")
        return v.strip()
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "123e4567-e89b-12d3-a456-426614174000",
                "message": "Necesito cotización para instalación eléctrica trifásica",
                "context": {
                    "proyecto_id": "123e4567-e89b-12d3-a456-426614174001",
                    "tipo_servicio": "electricidad"
                }
            }
        }


class ChatMessageResponse(BaseModel):
    """
    Chat message response schema.
    
    Following api-patterns: Consistent response format
    """
    response: str = Field(..., description="AI generated response")
    extracted_data: Optional[Dict[str, Any]] = Field(None, description="Extracted structured data")
    suggestions: List[Any] = Field(default_factory=list, description="Contextual suggestions")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Response timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "response": "Claro, voy a ayudarte con la cotización...",
                "extracted_data": {
                    "tipo_instalacion": "trifásica",
                    "potencia": "50kW"
                },
                "suggestions": [
                    "¿Necesitas incluir puesta a tierra?",
                    "¿El proyecto requiere tablero eléctrico?"
                ],
                "timestamp": "2026-01-29T14:30:00Z"
            }
        }


class ConversationHistoryResponse(BaseModel):
    """Conversation history response"""
    user_id: UUID
    messages: List[Dict[str, Any]]
    total_messages: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "123e4567-e89b-12d3-a456-426614174000",
                "messages": [
                    {
                        "user": "Hola PILI",
                        "assistant": "¡Hola! ¿En qué puedo ayudarte?",
                        "timestamp": "2026-01-29T14:00:00Z"
                    }
                ],
                "total_messages": 1
            }
        }


class PILIStatsResponse(BaseModel):
    """PILI service statistics"""
    active_conversations: int
    total_messages: int
    gemini_metrics: Dict[str, Any]
    settings: Dict[str, Any]
    
    class Config:
        json_schema_extra = {
            "example": {
                "active_conversations": 42,
                "total_messages": 1337,
                "gemini_metrics": {
                    "total_requests": 1000,
                    "total_errors": 5,
                    "error_rate": 0.005
                },
                "settings": {
                    "model": "gemini-2.0-flash-exp",
                    "max_history": 50
                }
            }
        }


class ErrorResponse(BaseModel):
    """
    Standard error response.
    
    Following api-patterns: Consistent error format
    """
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Human-readable error message")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_schema_extra = {
            "example": {
                "error": "ValidationError",
                "message": "Message cannot be empty",
                "details": {"field": "message"},
                "timestamp": "2026-01-29T14:30:00Z"
            }
        }


class GenerateDocumentRequest(BaseModel):
    """
    Request to generate a document from a project state.
    """
    user_id: Union[str, int, UUID] = Field(..., description="User ID requesting generation")
    project_id: Union[str, int, UUID] = Field(..., description="Project ID to generate document for")
    format: str = Field("docx", description="Output format (docx, pdf)")
    options: Optional[Dict[str, Any]] = Field(None, description="Customization options")
    data: Optional[Dict[str, Any]] = Field(None, description="Optional state data override")


class GenerateDocumentResponse(BaseModel):
    """
    Response with generated document information.
    """
    success: bool
    message: str
    file_path: Optional[str] = None
    download_url: Optional[str] = None
    document_type: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

