from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict, Any, Optional

from .service import document_service

router = APIRouter(prefix="/documents", tags=["Documents"])

class DocRequest(BaseModel):
    client_info: Dict[str, Any]
    service_request: Dict[str, Any]
    user_context: Optional[Dict[str, Any]] = {}
    output_format: str = "XLSX"

@router.post("/generate")
async def generate_document_endpoint(req: DocRequest):
    """
    Unified Endpoint: Generates a document based on service and model.
    Returns JSON with download URL (or Base64 for now).
    """
    result = document_service.generate_document(req.dict())
    
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))
        
    return result
