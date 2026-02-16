"""
N02 Pili Logic - Entry Point (Logic Controller)
Responsable de orquestar la lógica de negocio y recuperar conocimiento.
"""
import logging
from typing import Dict, Any, List, Optional
from .knowledge_db import SessionLocal, PiliService, PiliKnowledgeItem, PiliRule, PiliTemplateConfig

logger = logging.getLogger("N02_Pili_Logic")

class PiliLogicNode:
    def __init__(self):
        self.db = SessionLocal()

    def process_intention(self, intention_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Procesa una intención de usuario y retorna estructura para N04 o Frontend.
        
        Args:
            intention_data: {
                "service": "electricidad",
                "subtype": "RESIDENCIAL",
                "parameters": {"area": 100, ...}
            }
        """
        try:
            service_slug = intention_data.get("service")
            subtype = intention_data.get("subtype", "RESIDENCIAL") # Opcional
            
            # 1. Recuperar Servicio
            service = self.db.query(PiliService).filter(
                PiliService.service_key.like(f"%{service_slug}%")
            ).first()
            
            if not service:
                return {"error": f"Servicio no encontrado: {service_slug}"}

            # 2. Recuperar Conocimiento (Items)
            query = self.db.query(PiliKnowledgeItem).filter_by(service_id=service.id)
            
            # Filtro opcional por subtipo
            if subtype and subtype != "*": 
                query = query.filter(PiliKnowledgeItem.item_description.like(f"%{subtype}%"))
            
            items = query.all()
            
            # 3. Estructurar Datos
            knowledge_data = {
                "service_info": {
                    "id": service.id,
                    "name": service.display_name,
                    "normativa": service.normativa_referencia
                },
                "items": [
                    {
                        "key": item.item_key,
                        "description": item.item_description,
                        "unit": item.unit_measure,
                        "price": item.unit_price,
                        "currency": item.currency
                    }
                    for item in items
                ]
            }

            # 4. Enriquecer con Reglas de Plantilla (R.A.L.F.)
            # Retrieve all template configs for this service to map doc_type -> template_ref
            # Or just return raw configs for N06 to decide. 
            # Better: N06 sends doc_model_id, we return the specific template ref for THAT id if possible?
            # But process_intention input doesn't always have doc_type.
            # Let's return a map of available templates.
            template_configs = self.db.query(PiliTemplateConfig).filter_by(service_id=service.id).all()
            knowledge_data["templates"] = {
                t.document_type_id: t.template_ref for t in template_configs
            }
            
            return {
                "success": True,
                "node": "N02",
                "logic_result": knowledge_data
            }

        except Exception as e:
            logger.error(f"Error en N02 Logic: {e}", exc_info=True)
            return {"success": False, "error": str(e)}
        finally:
            self.db.close() # Ensure connection is closed per request (simple pattern)
            self.db = SessionLocal() # Re-open for next? Better separate lifecycle. 
            # For this MVP class, re-init is safer or use context manager in method.

    def __del__(self):
        self.db.close()

# Singleton
logic_node = PiliLogicNode()
