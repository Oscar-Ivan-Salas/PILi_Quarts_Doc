import logging
import time
from typing import Dict, Any, List

# --- INTERNAL MODULES (The Nodes) ---
from modules.N02_Pili_Logic.index import logic_node
from modules.N04_Binary_Factory.index import binary_factory
from modules.N06_Integrator.index import integrator_node # We reuse N06 logic or wrap it?
# The user said: "1. Implementación del Orquestador (N06 Modificado) Carpeta: backend/modules/documents/"
# So this IS the new home for N06 logic, or at least the Service Layer.

logger = logging.getLogger("UnifiedDocumentService")

class DocumentService:
    def generate_document(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Unified Entry Point for Document Generation.
        Orchestrates N02 -> Logic -> N04.
        """
        start_time = time.time()
        try:
            # 1. Validation & Usage of N06 Integrator Logic
            # The N06 Integrator fully implements the dispatch logic.
            # So this Service is just a wrapper or interface for the API Router?
            # Yes. "El Frontend solo ve un endpoint limpio: /api/documents/generate."
            
            logger.info(f"📄 Document Generation Requested: {request_data.get('service_request', {}).get('service_key')}")
            
            # Delegate to N06 Integrator (The Brain)
            response = integrator_node.dispatch(request_data)
            
            if response.get("success"):
                logger.info("✅ Generation Success")
                return response
            else:
                 logger.error(f"❌ Generation Failed: {response.get('error')}")
                 return response
                 
        except Exception as e:
            logger.error(f"Service Error: {e}", exc_info=True)
            return {"success": False, "error": str(e)}

    def get_available_templates(self, service_key: str) -> List[Dict[str, Any]]:
        """
        Helper to list templates for a service (for Frontend dropdown).
        """
        # Call N02 to get templates?
        # N02 logic_node.process_intention returns templates in logic_result.
        # But we need a simpler call.
        # For now, return hardcoded or seed based.
        return [] # Implement if needed

document_service = DocumentService()
