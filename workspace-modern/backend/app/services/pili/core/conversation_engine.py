"""
🎯 CONVERSATION ENGINE - Motor de Conversación Reutilizable
Maneja toda la lógica de generación de mensajes y respuestas
"""

import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)


class ConversationEngine:
    """Motor de conversación reutilizable para todos los especialistas"""
    
    def __init__(self):
        """Inicializa el motor y carga plantillas de mensajes"""
        self.templates = self._load_templates()
    
    def _load_templates(self) -> Dict:
        """Carga todas las plantillas de mensajes desde YAML"""
        try:
            templates_path = Path(__file__).parent.parent / "templates" / "messages.yaml"
            
            if not templates_path.exists():
                logger.warning(f"Archivo de templates no encontrado: {templates_path}")
                return {}
            
            with open(templates_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        
        except Exception as e:
            logger.error(f"Error cargando templates: {e}")
            return {}
    
    def render_message(
        self,
        service: str,
        template_name: str,
        **kwargs
    ) -> str:
        """
        Renderiza un mensaje desde template
        
        Args:
            service: Nombre del servicio (itse, electricidad, etc.)
            template_name: Nombre del template (presentacion, confirm_categoria, etc.)
            **kwargs: Variables para reemplazar en el template
        
        Returns:
            Mensaje formateado
        """
        # Obtener template
        service_templates = self.templates.get(service, {})
        template = service_templates.get(template_name, "")
        
        if not template:
            logger.warning(f"Template no encontrado: {service}.{template_name}")
            return f"Mensaje no disponible ({service}.{template_name})"
        
        # Reemplazar variables
        try:
            return template.format(**kwargs)
        except KeyError as e:
            logger.warning(f"Variable faltante en template: {e}")
            return template
        except Exception as e:
            logger.error(f"Error renderizando template: {e}")
            return template
    
    def create_buttons_response(
        self,
        service: str,
        template_name: str,
        buttons: List[Dict],
        next_stage: str,
        progress: str = "",
        **template_vars
    ) -> Dict[str, Any]:
        """
        Crea respuesta con botones
        
        Args:
            service: Nombre del servicio
            template_name: Nombre del template de mensaje
            buttons: Lista de botones [{"text": "...", "value": "..."}]
            next_stage: Siguiente stage
            progress: Progreso (ej: "2/5")
            **template_vars: Variables para el template
        
        Returns:
            Diccionario con respuesta completa
        """
        # Renderizar mensaje
        text = self.render_message(service, template_name, **template_vars)
        
        # Crear respuesta
        response = {
            "texto": text,
            "botones": buttons,
            "stage": next_stage
        }
        
        if progress:
            response["progreso"] = progress
        
        return response
    
    def create_input_response(
        self,
        service: str,
        template_name: str,
        next_stage: str,
        progress: str = "",
        **template_vars
    ) -> Dict[str, Any]:
        """
        Crea respuesta que espera input del usuario
        
        Args:
            service: Nombre del servicio
            template_name: Nombre del template
            next_stage: Siguiente stage
            progress: Progreso
            **template_vars: Variables para el template
        
        Returns:
            Diccionario con respuesta
        """
        text = self.render_message(service, template_name, **template_vars)
        
        response = {
            "texto": text,
            "stage": next_stage
        }
        
        if progress:
            response["progreso"] = progress
        
        return response
    
    def create_quote_response(
        self,
        service: str,
        template_name: str,
        quote_data: Dict[str, Any],
        actions: List[Dict] = None
    ) -> Dict[str, Any]:
        """
        Crea respuesta con cotización
        
        Args:
            service: Nombre del servicio
            template_name: Nombre del template
            quote_data: Datos de la cotización
            actions: Botones de acción
        
        Returns:
            Diccionario con respuesta completa
        """
        # Renderizar mensaje con datos de cotización
        text = self.render_message(service, template_name, **quote_data)
        
        response = {
            "texto": text,
            "datos_generados": quote_data,
            "stage": "completed"
        }
        
        if actions:
            response["botones"] = actions
        
        if "progreso" in quote_data:
            response["progreso"] = quote_data["progreso"]
        
        return response
    
    def create_error_response(
        self,
        error_message: str,
        current_stage: str
    ) -> Dict[str, Any]:
        """
        Crea respuesta de error
        
        Args:
            error_message: Mensaje de error
            current_stage: Stage actual (para mantener al usuario en el mismo lugar)
        
        Returns:
            Diccionario con respuesta de error
        """
        return {
            "texto": error_message,
            "stage": current_stage
        }
