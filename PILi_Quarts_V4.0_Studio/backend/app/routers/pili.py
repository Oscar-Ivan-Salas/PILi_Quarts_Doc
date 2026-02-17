from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel
from typing import Optional, Dict, Any, List

import logging

router = APIRouter(
    prefix="/api/pili",
    tags=["pili"]
)

logger = logging.getLogger(__name__)

# --- REQUEST MODELS ---
class ChatRequest(BaseModel):
    user_id: str
    message: str
    context: Optional[Dict[str, Any]] = {}

class ChatResponse(BaseModel):
    response: str
    suggestions: List[Dict[str, str]] = []
    extracted_data: Optional[Dict[str, Any]] = None

# --- ENDPOINTS ---

@router.post("/chat", response_model=ChatResponse)
async def chat_with_pili(request: ChatRequest):
    """
    Endpoint principal para conversar con PILi (Universal Specialist).
    Detecta el servicio del contexto y enruta al especialista adecuado.
    """
    try:
        # 1. Determinar el servicio y tipo de documento del contexto
        context = request.context or {}
        service_name = context.get('service_id') or context.get('servicio', 'general').lower()
        
        # Mapeo simple de nombres de servicio si es necesario
        # (El frontend manda 'electricidad', 'itse', etc.)
        
        # 2. Instanciar el CEREBRO (PILIBrain Core)
        # Usamos el brain que envuelve al integrador legacy para tener toda la inteligencia
        from modules.pili.core.brain import PILIBrain
        brain = PILIBrain()
        
        # 3. Procesar el mensaje
        # El brain espera: message, user_id, context
        
        # Preparar contexto para el brain
        brain_context = {
            "service_id": service_name,
            "tipo_flujo": context.get('tipo_documento', 'cotizacion-simple'), # Default mapping
            "data": context.get('data', {}),
            "history": context.get('history', [])
        }

        # Procesar
        result = await brain.process_message(
            message=request.message,
            user_id=request.user_id,
            context=brain_context
        )
        
        # 4. Formatear respuesta
        # El brain devuelve un dict estructurado: {response, suggestions, extracted_data, ...}
        
        response_text = result.get('response', 'Lo siento, no pude procesar tu mensaje.')
        suggestions = result.get('suggestions', [])
        extracted_data = result.get('extracted_data', {})
        
        # Mapear botones a suggestions
        suggestions = []
        if 'botones' in result:
            suggestions = [
                {'label': btn['text'], 'payload': btn['value']} 
                for btn in result['botones']
            ]
            
        # Empaquetamos todo el estado nuevo en extracted_data para que el frontend lo persista
        extracted_data = result.get('state', {})
        # Tambien agregamos si se generó algo específico
        if 'datos_generados' in result:
            extracted_data['generated_data'] = result['datos_generados']

        return ChatResponse(
            response=response_text,
            suggestions=suggestions,
            extracted_data=extracted_data
        )

    except Exception as e:
        logger.error(f"Error en PILi Chat: {str(e)}")
        # Fallback elegante
        return ChatResponse(
            response=f"Ocurrió un error interno en mi cerebro: {str(e)}",
            suggestions=[],
            extracted_data=None
        )
