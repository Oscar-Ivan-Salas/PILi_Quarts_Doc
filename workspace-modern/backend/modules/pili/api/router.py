"""
PILI API Router - FastAPI Endpoints
Enterprise-grade REST API with OpenAPI documentation
Following api-patterns, python-patterns, and clean-code skills
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from typing import Optional
from uuid import UUID
import logging

from .schemas import (
    ChatMessageRequest,
    ChatMessageResponse,
    ConversationHistoryResponse,
    PILIStatsResponse,
    ErrorResponse
)
from ..core.brain import PILIBrain
from ..core.gemini import GeminiService
from ..config.settings import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

# Create router with prefix and tags
router = APIRouter(
    prefix="/api/pili",
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
    pili: PILIBrain = Depends(get_pili_brain)
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
async def health_check():
    """
    Health check endpoint.
    
    Following deployment-procedures: Health monitoring
    """
    try:
        # Basic health check
        if _pili_brain is None or _gemini_service is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail={"error": "ServiceUnavailable", "message": "PILI not initialized"}
            )
        
        return {
            "status": "healthy",
            "service": "PILI AI",
            "version": "1.0.0"
        }
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"error": "ServiceUnavailable", "message": str(e)}
        )
