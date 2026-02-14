"""
PILI API Router - FastAPI Endpoints
Enterprise-grade REST API with OpenAPI documentation
Following api-patterns, python-patterns, and clean-code skills
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse, FileResponse
from typing import Optional
from uuid import UUID
import logging

# HTML-to-Word generator that preserves custom template designs
# from app.services.html_to_word_generator import HTMLToWordGenerator # MISSING

from .schemas import (
    ChatMessageRequest,
    ChatMessageResponse,
    ConversationHistoryResponse,
    PILIStatsResponse,
    ErrorResponse,
    GenerateDocumentRequest,
    GenerateDocumentResponse
)
from ..core.brain import PILIBrain
from ..core.gemini import GeminiService
from ..config.settings import get_settings
from ..db.models import Project, User
import os
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..db.database import get_db
from ..db.models import Project
import json

logger = logging.getLogger(__name__)
settings = get_settings()

# Create router with prefix and tags
router = APIRouter(
    prefix="/api/pili/v2",
    tags=["PILI AI"],
    responses={
        500: {"model": ErrorResponse, "description": "Internal server error"},
        429: {"model": ErrorResponse, "description": "Rate limit exceeded"},
    }
)

# Dependency: Get PILI Brain instance (singleton pattern)
_pili_brain: Optional[PILIBrain] = None
_gemini_service: Optional[GeminiService] = None


def get_pili_brain() -> PILIBrain:
    """
    Dependency injection for PILI Brain.
    
    Following python-patterns: Dependency Injection
    Following clean-code: Single Responsibility
    """
    global _pili_brain, _gemini_service
    
    if _pili_brain is None:
        logger.info("Initializing PILI Brain singleton")
        _gemini_service = GeminiService()
        _pili_brain = PILIBrain()
    
    return _pili_brain


@router.post(
    "/chat",
    response_model=ChatMessageResponse,
    status_code=status.HTTP_200_OK,
    summary="Send message to PILI AI",
    description="Process user message and get AI response with extracted data and suggestions",
    responses={
        200: {"description": "Successful response"},
        400: {"model": ErrorResponse, "description": "Invalid request"},
        408: {"model": ErrorResponse, "description": "Request timeout"},
    }
)
async def chat(
    request: ChatMessageRequest,
    pili: PILIBrain = Depends(get_pili_brain),
    db: Session = Depends(get_db)  # NEW: Inject DB Session
) -> ChatMessageResponse:
    """
    Chat endpoint - Process user message.
    
    Following api-patterns:
    - Clear endpoint naming
    - Proper status codes
    - OpenAPI documentation
    - Error handling
    """
    try:
        logger.info(f"Chat request from user {request.user_id}")
        
        # Process message
        result = await pili.process_message(
            user_id=str(request.user_id),
            message=request.message,
            context=request.context
        )
        
        # === SKILL 06 & 03: PERSISTENCE LAYER ===
        try:
            # 1. Extract State (Prioritize extracted_data from result, fallback to context)
            final_state = result.get("extracted_data")
            if not final_state and request.context:
                 final_state = request.context.get("data")
            
            if final_state:
                # 2. Find or Create Project (Draft) for this user
                # In a real scenario, we might use a specific Project ID from context
                project_id = final_state.get("project_id")
                
                project = None
                if project_id:
                    project = db.query(Project).filter(Project.id == project_id).first()
                
                if not project:
                     # Find latest draft
                    project = db.query(Project).filter(
                        Project.user_id == str(request.user_id),
                        Project.estado == "draft"
                    ).order_by(Project.updated_at.desc()).first()
                
                if not project:
                    # Create new draft
                    project = Project(
                        user_id=str(request.user_id),
                        tipo_documento="general", # Will be updated by brain logic later
                        state_json=final_state,
                        estado="draft"
                    )
                    db.add(project)
                    db.commit() # Commit to get ID
                    
                    # Inject project_id back to state
                    final_state["project_id"] = project.id
                    # Update result to reflect new ID in frontend
                    result["extracted_data"] = final_state
                else:
                    # Update existing
                    project.state_json = final_state
                    # Update timestamp
                    project.updated_at = func.now()
                    
                    if "tipo_documento" in final_state:
                         project.tipo_documento = final_state["tipo_documento"]
                         
                    db.commit()
                    
                logger.info(f"💾 State persisted for Project {project.id}")
                
        except Exception as db_e:
            logger.error(f"❌ Failed to persist state to DB: {db_e}")
            db.rollback()
            # Do not fail the request, just log error
            
        return ChatMessageResponse(**result)
        
    except ValueError as e:
        logger.warning(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "ValidationError", "message": str(e)}
        )
    
    except TimeoutError as e:
        logger.error(f"Timeout error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_408_REQUEST_TIMEOUT,
            detail={"error": "TimeoutError", "message": "AI response took too long"}
        )
    
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "InternalError", "message": "An unexpected error occurred"}
        )


@router.get(
    "/history/{user_id}",
    response_model=ConversationHistoryResponse,
    summary="Get conversation history",
    description="Retrieve conversation history for a specific user",
    responses={
        200: {"description": "Conversation history"},
        404: {"model": ErrorResponse, "description": "User not found"},
    }
)
async def get_history(
    user_id: UUID,
    pili: PILIBrain = Depends(get_pili_brain)
) -> ConversationHistoryResponse:
    """
    Get conversation history endpoint.
    
    Following api-patterns: RESTful resource naming
    """
    try:
        history = pili._get_history(str(user_id))
        
        return ConversationHistoryResponse(
            user_id=user_id,
            messages=history,
            total_messages=len(history)
        )
        
    except Exception as e:
        logger.error(f"Error retrieving history: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "InternalError", "message": str(e)}
        )


@router.delete(
    "/history/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Clear conversation history",
    description="Delete all conversation history for a specific user",
    responses={
        204: {"description": "History cleared successfully"},
    }
)
async def clear_history(
    user_id: UUID,
    pili: PILIBrain = Depends(get_pili_brain)
):
    """
    Clear history endpoint.
    
    Following api-patterns: DELETE for resource deletion
    """
    try:
        pili.clear_history(str(user_id))
        return JSONResponse(
            status_code=status.HTTP_204_NO_CONTENT,
            content=None
        )
        
    except Exception as e:
        logger.error(f"Error clearing history: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "InternalError", "message": str(e)}
        )


@router.get(
    "/stats",
    response_model=PILIStatsResponse,
    summary="Get PILI statistics",
    description="Retrieve PILI service statistics and metrics",
    responses={
        200: {"description": "Service statistics"},
    }
)
async def get_stats(
    pili: PILIBrain = Depends(get_pili_brain)
) -> PILIStatsResponse:
    """
    Stats endpoint - Service health and metrics.
    
    Following api-patterns: Monitoring endpoint
    """
    try:
        brain_stats = pili.get_stats()
        gemini_metrics = _gemini_service.get_metrics() if _gemini_service else {}
        
        return PILIStatsResponse(
            active_conversations=brain_stats["active_conversations"],
            total_messages=brain_stats["total_messages"],
            gemini_metrics=gemini_metrics,
            settings=brain_stats["settings"]
        )
        
    except Exception as e:
        logger.error(f"Error retrieving stats: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "InternalError", "message": str(e)}
        )


@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    summary="Health check",
    description="Check if PILI service is healthy",
    responses={
        200: {"description": "Service is healthy"},
        503: {"description": "Service unavailable"},
    }
)
@router.post(
    "/generate",
    response_model=GenerateDocumentResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate professional document",
    description="Generate Word/PDF document from project state with Identity Injection",
    responses={
        200: {"description": "Document generated successfully"},
        404: {"model": ErrorResponse, "description": "Project or User not found"},
    }
)
async def generate_document(
    request: GenerateDocumentRequest,
    db: Session = Depends(get_db)
) -> GenerateDocumentResponse:
    raise HTTPException(status_code=501, detail="Endpoit Migrated to N04 Use N06")
    # """
    # Generate document endpoint - Skill 02 & 09.
    # 
    # 1. Fetches Project State (Skill 03)
    # 2. Fetches User Identity (Skill 09)
    # 3. Invokes WordGenerator (Skill 02)
    # """
    # try:
    #     # 1. Fetch Project
    #     project = db.query(Project).filter(
    #         Project.id == request.project_id,
    #         Project.user_id == str(request.user_id)
    #     ).first()
    #     
    #     if not project:
    #         raise HTTPException(
    #             status_code=status.HTTP_404_NOT_FOUND,
    #             detail={"error": "NotFound", "message": "Project not found"}
    #         )
    #         
    #     # 2. Fetch User Identity (Executor)
    #     user = db.query(User).filter(User.id == str(request.user_id)).first()
    #     if not user:
    #          raise HTTPException(
    #             status_code=status.HTTP_404_NOT_FOUND,
    #             detail={"error": "NotFound", "message": "User profile not found"}
    #         )
    #         
    #     # 3. Merge Data (State + Identity)
    #     # Prepare data for generator
    #     # Priority: Request Data (Real-time edits) > DB State (Saved) > Empty
    #     logger.info(f"🔍 DEBUG X - request.data type: {type(request.data)}")
    #     logger.info(f"🔍 DEBUG Y - request.data value: {request.data}")
    #     logger.info(f"🔍 DEBUG Z - project.state_json type: {type(project.state_json)}")
    #     
    #     # CRITICAL FIX: Ensure we always have a dict, never a Project object
    #     if request.data:
    #         # Use request data if provided (from frontend)
    #         pili_data = dict(request.data) if isinstance(request.data, dict) else {}
    #         logger.info("✅ Using request.data from frontend")
    #     elif project.state_json:
    #         # Fallback to saved state
    #         pili_data = dict(project.state_json) if isinstance(project.state_json, dict) else {}
    #         logger.info("✅ Using project.state_json from database")
    #     else:
    #         # Last resort: empty dict
    #         pili_data = {}
    #         logger.info("⚠️ Using empty dict (no data available)")
    #     
    #     # Inject Identity (Executor Profile)
    #     pili_data["_opciones_personalizacion"] = request.options or {}
    #     
    #     # Inject Executor Info directly into data if needed by template
    #     pili_data["executor_info"] = {
    #         "razon_social": user.razon_social,
    #         "ruc": user.ruc,
    #         "direccion": user.direccion,
    #         "telefono": user.telefono,
    #         "email": user.email
    #     }
    #     
    #     logger.info(f"🔍 DEBUG A - After executor_info injection")
    #     logger.info(f"🔍 DEBUG B - pili_data type: {type(pili_data)}")
    #     logger.info(f"🔍 DEBUG C - pili_data keys: {list(pili_data.keys()) if isinstance(pili_data, dict) else 'NOT A DICT'}")
    #     
    #     # 4. Invoke Professional Generator
    #     # Determine document type to select appropriate generator
    #     try:
    #         tipo_documento = project.tipo_documento.lower() if project.tipo_documento else "cotizacion_simple"
    #         logger.info(f"🔍 DEBUG 1 - tipo_documento: {tipo_documento}")
    #         logger.info(f"🔍 DEBUG 2 - project type: {type(project)}")
    #         logger.info(f"🔍 DEBUG 3 - pili_data type: {type(pili_data)}")
    #         
    #         # Generate output file path
    #         import datetime
    #         timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    #         
    #         # Extract client name from data
    #         cliente_data = pili_data.get("cliente", {})
    #         cliente_nombre = cliente_data.get("nombre", "cliente") if isinstance(cliente_data, dict) else str(cliente_data)
    #         # Sanitize filename
    #         cliente_nombre = "".join(c for c in cliente_nombre if c.isalnum() or c in (' ', '-', '_')).strip()[:30]
    #         
    #         filename = f"cotizacion_{cliente_nombre}_{timestamp}.docx"
    #         
    #         # Ensure storage directory exists
    #         base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    #         storage_dir = os.path.join(base_dir, "storage", "generados")
    #         os.makedirs(storage_dir, exist_ok=True)
    #         
    #         file_path = os.path.join(storage_dir, filename)
    #         logger.info(f"📁 Output file path: {file_path}")
    #         
    #         # Prepare data for HTML-to-Word generator
    #         # The generator expects specific variable names matching the HTML templates
    #         datos_generacion = {
    #             "cliente": pili_data.get("cliente", {}),
    #             "proyecto": pili_data.get("proyecto", "Proyecto"),
    #             "items": pili_data.get("items", []),
    #             "numero": pili_data.get("numero", f"COT-{project.id}"),
    #             "fecha": pili_data.get("fecha", ""),
    #             "vigencia": pili_data.get("vigencia", "30 días"),
    #             "servicio_nombre": pili_data.get("servicio", "Instalaciones Eléctricas"),
    #             "area_m2": pili_data.get("area_m2", "0"),
    #             "descripcion": pili_data.get("descripcion", ""),
    #             "normativa": pili_data.get("normativa", "CNE Suministro 2011"),
    #         }
    #         
    #         # Calculate totals from items if available
    #         items = datos_generacion.get("items", [])
    #         if items:
    #             subtotal = sum(
    #                 float(item.get("cantidad", 0)) * float(item.get("precio_unitario", 0))
    #                 for item in items
    #             )
    #             igv = subtotal * 0.18
    #             total = subtotal + igv
    #             
    #             datos_generacion["subtotal"] = subtotal
    #             datos_generacion["igv"] = igv
    #             datos_generacion["total"] = total
    #         else:
    #             datos_generacion["subtotal"] = 0
    #             datos_generacion["igv"] = 0
    #             datos_generacion["total"] = 0
    #         
    #         # Create HTML-to-Word generator instance
    #         html_generator = HTMLToWordGenerator()
    #         
    #         # Select and invoke appropriate generator based on document type
    #         from pathlib import Path
    #         file_path_obj = Path(file_path)
    #         
    #         if "compleja" in tipo_documento or "complejo" in tipo_documento:
    #             logger.info(f"🎨 Using HTML template: COTIZACION_COMPLEJA")
    #             file_path_obj = html_generator.generar_cotizacion_compleja(
    #                 datos=datos_generacion,
    #                 ruta_salida=file_path_obj
    #             )
    #         else:
    #             logger.info(f"🎨 Using HTML template: COTIZACION_SIMPLE")
    #             logger.info(f"🔍 DEBUG - Type of datos_generacion: {type(datos_generacion)}")
    #             logger.info(f"🔍 DEBUG - datos_generacion keys: {list(datos_generacion.keys()) if isinstance(datos_generacion, dict) else 'NOT A DICT'}")
    #             logger.info(f"🔍 DEBUG - datos_generacion['cliente']: {datos_generacion.get('cliente', 'NO CLIENTE KEY')}")
    #             file_path_obj = html_generator.generar_cotizacion_simple(
    #                 datos=datos_generacion,
    #                 ruta_salida=file_path_obj
    #             )
    #         
    #         # Convert Path back to string
    #         file_path = str(file_path_obj)
    #         
    #         # Verify file was created
    #         if not os.path.exists(file_path):
    #             raise Exception(f"Generator did not create file at {file_path}")
    #         
    #         logger.info(f"✅ Professional document generated: {os.path.basename(file_path)}")
    #         
    #         # Construct download URL
    #         filename = os.path.basename(file_path)
    #         download_url = f"/api/pili/v2/download/{filename}"
    #         
    #         # Update Project State
    #         project.estado = "generated"
    #         db.commit()
    #
    #         return GenerateDocumentResponse(
    #             success=True,
    #             message="Document generated successfully",
    #             file_path=file_path,
    #             download_url=download_url,
    #             document_type=request.format
    #         )
    #
    #     except ImportError:
    #          raise HTTPException(
    #             status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
    #             detail={"error": "ServiceUnavailable", "message": "WordGenerator not available"}
    #         )
    #         
    # except HTTPException:
    #     raise
    # except Exception as e:
    #     import traceback
    #     import sys
    #     error_traceback = traceback.format_exc()
    #     
    #     # Print to console (stderr) so we can see it
    #     print("=" * 80, file=sys.stderr)
    #     print("🚨 ERROR IN DOCUMENT GENERATION:", file=sys.stderr)
    #     print("=" * 80, file=sys.stderr)
    #     print(error_traceback, file=sys.stderr)
    #     print("=" * 80, file=sys.stderr)
    #     
    #     logger.error(f"Error generating document: {str(e)}")
    #     logger.error(f"Full traceback:\n{error_traceback}")
    #     raise HTTPException(
    #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #         detail={"error": "InternalError", "message": str(e), "traceback": error_traceback.split('\n')[:10]}
    #     )


@router.get(
    "/download/{filename}",
    summary="Download generated document",
    description="Download a previously generated document file",
    responses={
        200: {"description": "File download"},
        404: {"description": "File not found"},
    }
)
async def download_document(filename: str):
    """
    Download endpoint for generated documents.
    Serves files from storage/generados directory.
    """
    try:
        # Construct file path
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        file_path = os.path.join(base_dir, "storage", "generados", filename)
        
        # Security: Prevent directory traversal
        if ".." in filename or "/" in filename or "\\" in filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"error": "InvalidFilename", "message": "Invalid filename"}
            )
        
        # Check if file exists
        if not os.path.exists(file_path):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": "FileNotFound", "message": f"File {filename} not found"}
            )
        
        # Determine media type
        media_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        if filename.endswith(".pdf"):
            media_type = "application/pdf"
        elif filename.endswith(".xlsx"):
            media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        
        # Return file with proper headers for download
        return FileResponse(
            path=file_path,
            media_type=media_type,
            filename=filename,
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error downloading file: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "InternalError", "message": str(e)}
        )
