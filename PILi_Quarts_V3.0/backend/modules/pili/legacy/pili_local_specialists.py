import logging
import re
import math
from typing import Dict, Optional

logger = logging.getLogger(__name__)

# ══════════════════════════════════════════════════════════════════════════════
# 💰 KNOWLEDGE BASES PROFESIONALES - NODO N02 (PILI LOGIC)
# ══════════════════════════════════════════════════════════════════════════════

# Importar N02 Logic Node
try:
    from modules.N02_Pili_Logic.index import logic_node
    # Definir clase de error personalizada para fallo de conexión N02
    class NodeConnectionError(Exception):
        pass
except ImportError:
    logger.error("❌ CRITICAL: N02 Logic Node not found. Legacy fallback unavailable.")
    logic_node = None

# Eliminado KNOWLEDGE_BASE hardcoded (155KB)
# Ahora se consulta dinámicamente vía logic_node.process_intention()

def _query_n02(service_key: str, subtype: Optional[str] = None) -> Dict:
    """Helper para consultar N02 con caché simple o manejo de errores"""
    if not logic_node:
        logger.error("N02 Node not available")
        return {}
    
    response = logic_node.process_intention({
        "service": service_key,
        "subtype": "*" # Request all items to reconstruct legacy dict
    })
    
    if response.get("success"):
        return response.get("logic_result", {})
    else:
        logger.warning(f"N02 Query Failed: {response.get('error')}")
        return {}

# ⚠️ MANTENEMOS LA VARIABLE KNOWLEDGE_BASE COMO UN PROXY DINÁMICO
# Para no romper el código legacy que hace KNOWLEDGE_BASE['electricidad']...
# Usamos una clase dict-like que intercepta los accesos.

class KnowledgeBaseProxy(dict):
    def __getitem__(self, key):
        # Mapeo de claves legacy a service_keys de N02
        # 'electricidad' -> 'electricidad'
        # 'itse' -> 'itse'
        # etc.
        
        # Consultamos N02. Como el código legacy espera un dict anidado gigante,
        # tendremos que reconstruir UNA PARTE de ese dict on-demand o 
        # refactorizar los consumidores.
        # DADO EL PEDIDO DE "CASCARON VACIO", lo ideal es refactorizar los consumidores.
        # PERO para esta fase "quirúrgica", devolvemos una estructura mínima compatible
        # basada en lo que devuelve N02.
        
        # NOTA: N02 devuelve una lista plana de items. Legacy espera 'precios': {...}
        # Hacemos un adaptador al vuelo.
        
        data = _query_n02(key)
        
        # Transformar respuesta N02 a estructura Legacy (Adapter Pattern)
        legacy_structure = {
            "tipos": {},
            "etapas": ["initial", "quotation"] # Default
        }
        
        # Reconstruir precios
        items = data.get("items", [])
        precios_dict = {item["key"].split("_", 1)[1] if "_" in item["key"] else item["key"]: item["price"] for item in items}
        
        # Mockear estructura para que el código legacy no explote inmediatamente
        # Esto es temporal hasta refactorizar la lógica de conversación.
        # Por ahora, devolvemos un objeto que loguea el acceso.
        logger.info(f"🐢 Legacy Access to KNOWLEDGE_BASE['{key}'] - Redirecting to N02")
        
        # Retornamos un dict CONSTRUÍDO desde N02 para este servicio
        # Esto permite que `service_data = KNOWLEDGE_BASE[service]` funcione
        
        return {
            "tipos": {
                "STANDARD": {
                    "nombre": data.get("service_info", {}).get("name", key),
                    "precios": precios_dict,
                    "normativa": data.get("service_info", {}).get("normativa", "")
                }
            },
            "normativa": data.get("service_info", {}).get("normativa", "")
        }

    def get(self, key, default=None):
        try:
            return self[key]
        except:
            return default

KNOWLEDGE_BASE = KnowledgeBaseProxy()
