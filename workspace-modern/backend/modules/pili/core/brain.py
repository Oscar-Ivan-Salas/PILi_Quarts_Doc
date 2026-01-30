"""
PILI Brain - Core AI Logic
Enterprise-grade AI service with error handling and logging
Following clean-code, python-patterns, and architecture skills
"""
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import asyncio

from ..config.settings import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class PILIBrain:
    """
    Core PILI AI logic.
    Handles chat interactions, data extraction, and context management.
    
    Principles:
    - Single Responsibility: AI chat logic only
    - Dependency Injection: Gemini service injected
    - Error Handling: Graceful degradation
    - Logging: Comprehensive for debugging
    """
    
    def __init__(self, gemini_service):
        """
        Initialize PILI Brain with dependencies.
        
        Args:
            gemini_service: Gemini AI service instance
        """
        self.gemini = gemini_service
        self.conversation_history: Dict[str, List[Dict]] = {}
        logger.info("PILI Brain initialized")
    
    async def process_message(
        self,
        user_id: str,
        message: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Process user message and generate response.
        
        Args:
            user_id: Unique user identifier
            message: User's message
            context: Additional context (proyecto_id, tipo_servicio, etc.)
        
        Returns:
            Dict with response, extracted_data, and suggestions
        
        Raises:
            ValueError: If message is empty
            TimeoutError: If AI response takes too long
        """
        if not message or not message.strip():
            raise ValueError("Message cannot be empty")
        
        logger.info(f"Processing message for user {user_id}")
        
        try:
            # Get conversation history
            history = self._get_history(user_id)
            
            # Build prompt with context
            prompt = self._build_prompt(message, history, context)
            
            # Call Gemini AI with timeout
            response = await asyncio.wait_for(
                self.gemini.generate_response(prompt),
                timeout=settings.pili_timeout_seconds
            )
            
            # Extract structured data
            extracted_data = self._extract_data(response)
            
            # Generate suggestions
            suggestions = self._generate_suggestions(context, extracted_data)
            
            # Update history
            self._update_history(user_id, message, response)
            
            logger.info(f"Successfully processed message for user {user_id}")
            
            return {
                "response": response,
                "extracted_data": extracted_data,
                "suggestions": suggestions,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except asyncio.TimeoutError:
            logger.error(f"Timeout processing message for user {user_id}")
            raise TimeoutError("AI response took too long")
        
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}", exc_info=True)
            # Graceful degradation
            return {
                "response": "Lo siento, tuve un problema procesando tu mensaje. ¿Puedes intentar de nuevo?",
                "extracted_data": None,
                "suggestions": [],
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def _get_history(self, user_id: str) -> List[Dict]:
        """Get conversation history for user"""
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = []
        
        # Return last N messages (context window)
        return self.conversation_history[user_id][-settings.pili_context_window:]
    
    def _build_prompt(
        self,
        message: str,
        history: List[Dict],
        context: Optional[Dict] = None
    ) -> str:
        """
        Build AI prompt with message, history, and context.
        
        Following clean-code: Single Level of Abstraction
        """
        prompt_parts = [
            "Eres PILI, un asistente experto en ingeniería eléctrica y construcción.",
            "Tu objetivo es ayudar a crear cotizaciones y proyectos profesionales.",
            ""
        ]
        
        # Add context if provided
        if context:
            prompt_parts.append("Contexto actual:")
            for key, value in context.items():
                prompt_parts.append(f"- {key}: {value}")
            prompt_parts.append("")
        
        # Add conversation history
        if history:
            prompt_parts.append("Historial de conversación:")
            for msg in history:
                prompt_parts.append(f"Usuario: {msg['user']}")
                prompt_parts.append(f"PILI: {msg['assistant']}")
            prompt_parts.append("")
        
        # Add current message
        prompt_parts.append(f"Usuario: {message}")
        prompt_parts.append("PILI:")
        
        return "\n".join(prompt_parts)
    
    def _extract_data(self, response: str) -> Optional[Dict[str, Any]]:
        """
        Extract structured data from AI response.
        
        This is a simplified version. In production, use:
        - Function calling (Gemini)
        - JSON mode
        - Structured output parsing
        """
        # TODO: Implement proper data extraction
        # For now, return None
        return None
    
    def _generate_suggestions(
        self,
        context: Optional[Dict],
        extracted_data: Optional[Dict]
    ) -> List[str]:
        """
        Generate contextual suggestions for user.
        
        Following YAGNI: Simple implementation for now
        """
        suggestions = []
        
        if context and context.get("tipo_servicio") == "electricidad":
            suggestions.extend([
                "¿Necesitas incluir puesta a tierra?",
                "¿El proyecto requiere tablero eléctrico?",
                "¿Cuál es la potencia total estimada?"
            ])
        
        return suggestions[:3]  # Max 3 suggestions
    
    def _update_history(self, user_id: str, user_msg: str, assistant_msg: str):
        """
        Update conversation history.
        
        Following clean-code: Keep it simple
        """
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = []
        
        self.conversation_history[user_id].append({
            "user": user_msg,
            "assistant": assistant_msg,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        # Trim history if too long
        max_history = settings.pili_max_history
        if len(self.conversation_history[user_id]) > max_history:
            self.conversation_history[user_id] = self.conversation_history[user_id][-max_history:]
    
    def clear_history(self, user_id: str):
        """Clear conversation history for user"""
        if user_id in self.conversation_history:
            del self.conversation_history[user_id]
            logger.info(f"Cleared history for user {user_id}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get PILI Brain statistics"""
        return {
            "active_conversations": len(self.conversation_history),
            "total_messages": sum(len(h) for h in self.conversation_history.values()),
            "settings": {
                "model": settings.gemini_model,
                "max_history": settings.pili_max_history,
                "context_window": settings.pili_context_window
            }
        }
