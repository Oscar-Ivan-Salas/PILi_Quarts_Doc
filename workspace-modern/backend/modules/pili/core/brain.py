import logging
import json
import time
from datetime import datetime
from typing import Dict, Any, Optional

from modules.pili.config.settings import settings
from modules.pili.legacy.pili_integrator import PILIIntegrator

logger = logging.getLogger(__name__)

class PILIBrain:
    """
    Core PILI AI logic adapter.
    Delegates processing to the Legacy Integrator (pili_integrator.py)
    to support offline logic and rule-based specialists.
    """
    
    def __init__(self):
        self.settings = settings
        # Initialize Legacy Integrator
        try:
            self.integrator = PILIIntegrator()
            logger.info("✅ PILI Legacy Integrator connected")
        except Exception as e:
            logger.error(f"❌ Failed to load Legacy Integrator: {e}")
            self.integrator = None

    async def process_message(self, message: str, user_id: str, context: dict = None) -> dict:
        """
        Process message using the Legacy Logic (PILIIntegrator)
        """
        start_time = time.time()
        context = context or {}
        
        try:
            if not self.integrator:
                return {
                    "type": "error",
                    "content": "Sistema en mantenimiento (Integrador no disponible).",
                    "timestamp": "now"
                }

            # Map inputs to Legacy format
            # tipo_flujo defaults to 'consulta-general' or extracts from context
            tipo_flujo = context.get("tipo_flujo", "consulta-general")
            historial = context.get("history", []) # Expected list of dicts

            # Call Legacy Integrator
            # We use 'datos_acumulados' to pass context if needed
            resultado = await self.integrator.procesar_solicitud_completa(
                mensaje=message,
                tipo_flujo=tipo_flujo,
                historial=historial,
                generar_documento=False, # Default to false for chat
                datos_acumulados=context.get("data", {})
            )

            # Map Output
            response_text = resultado.get("respuesta", "Lo siento, no pude procesar eso.")
            
            # Map Buttons (Botones sugeridos)
            suggestions = []
            botones = resultado.get("botones", [])
            # Also check 'botones_sugeridos' from legacy integrator
            if not botones and "botones_sugeridos" in resultado:
                botones = resultado["botones_sugeridos"]

            if botones:
                for btn in botones:
                    if isinstance(btn, dict):
                        suggestions.append({
                            "label": btn.get("texto", "Opción"),
                            "action": "message", # or whatever frontend expects
                            "payload": btn.get("valor", "")
                        })
                    elif isinstance(btn, str):
                         suggestions.append({
                            "label": btn,
                            "action": "message",
                            "payload": btn
                        })

            # Check for generated data
            metadata = {}
            if "datos_generados" in resultado:
                metadata["generated_data"] = resultado["datos_generados"]
            
            if "servicio" in resultado:
                metadata["service_detected"] = resultado["servicio"]
                
            if "stage" in resultado:
                 metadata["stage"] = resultado["stage"]

            return {
                "response": response_text,
                "timestamp": datetime.utcnow().isoformat(),
                "suggestions": suggestions,
                "extracted_data": metadata,
                "user_id": user_id
            }

        except Exception as e:
            import traceback
            serialized_tb = traceback.format_exc()
            logger.error(f"Error processing message: {str(e)}")
            with open("e:\\PILi_Quarts\\backend_error.log", "w", encoding="utf-8") as f:
                f.write(f"Error: {str(e)}\nTraceback:\n{serialized_tb}")
                
            return {
                "type": "error",
                "response": "Lo siento, hubo un error interno en mi lógica local.",
                "timestamp": datetime.utcnow().isoformat()
            }
