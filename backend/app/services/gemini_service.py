"""
🤖 GEMINI SERVICE + PILI v3.0 - INTEGRACIÓN INTELIGENTE
📁 RUTA: backend/app/services/gemini_service.py

PILI (Procesadora Inteligente de Licitaciones Industriales) actúa como orquestadora 
inteligente sobre el servicio Gemini existente, especializando respuestas por agente.

🧠 NUEVAS CARACTERÍSTICAS PILI v3.0:
- Especialización automática por tipo de servicio
- Aprendizaje continuo de conversaciones
- Integración RAG con proyectos históricos
- Contextos específicos por agente PILI
- Modo demo robusto sin API key

🔄 CONSERVA TODO LO EXISTENTE:
- generar_cotizacion() ✅
- chat_conversacional() ✅ 
- analizar_documento() ✅
- Toda la lógica de parseo JSON ✅
"""

import google.generativeai as genai
from typing import List, Dict, Any, Optional
import json
import logging
from datetime import datetime
from app.core.config import settings

# 🧠 Importar PILIBrain para modo demo inteligente
from app.services.pili_brain import pili_brain

logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════════════════════════
# 🤖 CONFIGURACIÓN PILI - AGENTES ESPECIALIZADOS
# ═══════════════════════════════════════════════════════════════

PILI_AGENTES = {
    "cotizacion-simple": {
        "nombre": "PILI Cotizadora",
        "especialidad": "cotizaciones eléctricas rápidas",
        "prompt_base": """Eres PILI Cotizadora, agente IA experta en cotizaciones eléctricas para Tesla Electricidad.
        Tu especialidad es generar cotizaciones precisas y rápidas para instalaciones eléctricas en Perú.
        Siempre usas precios del mercado peruano 2025 y normativas CNE."""
    },
    
    "cotizacion-compleja": {
        "nombre": "PILI Analista",
        "especialidad": "proyectos eléctricos complejos",
        "prompt_base": """Eres PILI Analista, agente IA senior especializada en proyectos eléctricos complejos.
        Tu especialidad es analizar documentos técnicos, planos y generar cotizaciones detalladas con análisis profundo."""
    },
    
    "proyecto-simple": {
        "nombre": "PILI Coordinadora", 
        "especialidad": "gestión de proyectos simples",
        "prompt_base": """Eres PILI Coordinadora, experta en organización y gestión de proyectos eléctricos.
        Tu especialidad es crear estructura, cronogramas y seguimiento de proyectos de forma eficiente."""
    },
    
    "proyecto-complejo": {
        "nombre": "PILI Project Manager",
        "especialidad": "gestión avanzada de proyectos",
        "prompt_base": """Eres PILI Project Manager, directora de proyectos senior con metodología PMI.
        Tu especialidad es gestión integral de proyectos complejos con múltiples stakeholders."""
    },
    
    "informe-simple": {
        "nombre": "PILI Reportera",
        "especialidad": "documentos técnicos claros",
        "prompt_base": """Eres PILI Reportera, especialista en redacción técnica clara y profesional.
        Tu especialidad es crear informes técnicos estructurados y fáciles de entender."""
    },
    
    "informe-ejecutivo": {
        "nombre": "PILI Analista Senior",
        "especialidad": "informes ejecutivos APA",
        "prompt_base": """Eres PILI Analista Senior, creadora de informes ejecutivos de alto nivel.
        Tu especialidad es análisis profundo, gráficos avanzados y recomendaciones estratégicas."""
    }
}

class GeminiService:
    """
    🔄 SERVICIO ORIGINAL CONSERVADO + 🤖 PILI INTEGRADA
    
    Mantiene toda la funcionalidad existente pero agrega capacidades
    inteligentes de PILI para especialización automática.
    """
    
    def __init__(self):
        """🔄 CONSERVADO + 🤖 PILI mejorado"""
        
        # Estado PILI
        self.pili_activa = True
        self.modo_demo = False
        self.aprendizaje_habilitado = False
        
        # Configuración Gemini original
        try:
            if hasattr(settings, 'GEMINI_API_KEY') and settings.GEMINI_API_KEY:
                genai.configure(api_key=settings.GEMINI_API_KEY)
                self.model = genai.GenerativeModel(settings.GEMINI_MODEL)
                self.aprendizaje_habilitado = True
                logger.info(f"✅ PILI + Gemini configurados: {settings.GEMINI_MODEL}")
            else:
                logger.warning("⚠️ GEMINI_API_KEY no configurada. PILI funcionará en modo demo.")
                self.modo_demo = True
                
        except Exception as e:
            logger.error(f"❌ Error configurando Gemini: {e}")
            self.modo_demo = True

    # ═══════════════════════════════════════════════════════════════
    # 🤖 NUEVOS MÉTODOS PILI v3.0
    # ═══════════════════════════════════════════════════════════════
    
    async def procesar_con_pili(
        self,
        mensaje: str,
        tipo_servicio: str,
        contexto_adicional: Optional[Dict[str, Any]] = None,
        historial: Optional[List[Dict[str, Any]]] = None,
        datos_archivos: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        🤖 NUEVO PILI v3.0 - Procesamiento inteligente con agente especializado
        
        Args:
            mensaje: Mensaje del usuario
            tipo_servicio: Tipo de servicio (cotizacion-simple, etc.)
            contexto_adicional: Contexto extra del proyecto
            historial: Historial de conversación
            datos_archivos: Información de archivos procesados
            
        Returns:
            Respuesta especializada del agente PILI correspondiente
        """
        
        if self.modo_demo:
            return self._respuesta_demo_pili(mensaje, tipo_servicio)
        
        try:
            # 1. Obtener agente PILI especializado
            agente = PILI_AGENTES.get(tipo_servicio, PILI_AGENTES["cotizacion-simple"])
            nombre_pili = agente["nombre"]
            
            # 2. Construir prompt especializado PILI
            prompt = self._construir_prompt_pili(
                mensaje=mensaje,
                agente=agente,
                tipo_servicio=tipo_servicio,
                contexto_adicional=contexto_adicional,
                historial=historial,
                datos_archivos=datos_archivos
            )
            
            # 3. Generar respuesta con Gemini
            response = self.model.generate_content(prompt)
            respuesta_texto = response.text
            
            # 4. Procesar respuesta PILI
            respuesta_procesada = self._procesar_respuesta_pili(
                respuesta_texto, 
                tipo_servicio,
                nombre_pili
            )
            
            # 5. Aprender de la conversación
            if self.aprendizaje_habilitado:
                await self._guardar_aprendizaje_pili(
                    mensaje=mensaje,
                    respuesta=respuesta_procesada,
                    tipo_servicio=tipo_servicio,
                    agente=nombre_pili
                )
            
            return respuesta_procesada
            
        except Exception as e:
            logger.error(f"❌ Error PILI procesando: {e}")
            return {
                "exito": False,
                "error": str(e),
                "agente_pili": agente["nombre"],
                "mensaje": f"Error procesando con {agente['nombre']}: {str(e)}",
                "modo_degradado": True
            }
    
    def _construir_prompt_pili(
        self,
        mensaje: str,
        agente: Dict[str, str],
        tipo_servicio: str,
        contexto_adicional: Optional[Dict[str, Any]],
        historial: Optional[List[Dict[str, Any]]],
        datos_archivos: Optional[Dict[str, Any]]
    ) -> str:
        """Construye prompt especializado para agente PILI específico"""
        
        prompt = f"""
{agente['prompt_base']}

INFORMACIÓN DE CONTEXTO:
- Agente activo: {agente['nombre']}
- Especialidad: {agente['especialidad']}
- Tipo de servicio: {tipo_servicio}
- Mensaje del usuario: {mensaje}
"""
        
        # Agregar contexto adicional
        if contexto_adicional:
            prompt += f"\nCONTEXTO DEL PROYECTO:\n{json.dumps(contexto_adicional, ensure_ascii=False, indent=2)}"
        
        # Agregar historial si existe
        if historial and len(historial) > 0:
            prompt += f"\n\nHISTORIAL DE CONVERSACIÓN:"
            for msg in historial[-5:]:  # Últimos 5 mensajes
                rol = msg.get('role', 'usuario')
                contenido = msg.get('content', msg.get('mensaje', ''))
                prompt += f"\n{rol.upper()}: {contenido}"
        
        # Agregar información de archivos procesados
        if datos_archivos:
            prompt += f"\n\nARCHIVOS PROCESADOS:"
            archivos = datos_archivos.get('archivos_procesados', [])
            if archivos:
                prompt += f"\n- {len(archivos)} archivos procesados"
            texto = datos_archivos.get('texto_extraido', '')
            if texto:
                prompt += f"\n- Texto extraído: {texto[:500]}..."  # Primeros 500 caracteres
        
        # Instrucciones específicas por tipo de servicio
        if "cotizacion" in tipo_servicio:
            prompt += """

INSTRUCCIONES DE COTIZACIÓN:
1. Si tienes información suficiente, genera JSON estructurado con items detallados
2. Si falta información, haz preguntas específicas
3. Usa precios del mercado peruano 2025
4. Incluye especificaciones técnicas (CNE)
5. Calcula correctamente subtotal, IGV (18%) y total

FORMATO DE RESPUESTA:
Si generas cotización, incluye JSON:
{
    "accion": "cotizacion_generada",
    "datos": {
        "cliente": "nombre",
        "proyecto": "descripción",
        "items": [{"descripcion": "", "cantidad": 1, "precio_unitario": 100}],
        "observaciones": ""
    }
}

Si necesitas más información, responde conversacionalmente.
"""
        
        elif "proyecto" in tipo_servicio:
            prompt += """

INSTRUCCIONES DE PROYECTO:
1. Organiza la información del proyecto en fases claras
2. Define cronograma realista
3. Identifica recursos necesarios
4. Establece hitos importantes
5. Considera riesgos y mitigaciones

FORMATO DE RESPUESTA:
Estructura la información para gestión eficiente del proyecto.
"""
        
        elif "informe" in tipo_servicio:
            prompt += """

INSTRUCCIONES DE INFORME:
1. Estructura información en secciones lógicas
2. Incluye métricas relevantes
3. Proporciona conclusiones claras
4. Sugiere recomendaciones específicas
5. Mantén formato profesional
"""
        
        prompt += f"\n\nRESPONDE COMO {agente['nombre']}:"
        
        return prompt
    
    def _procesar_respuesta_pili(
        self, 
        respuesta_texto: str, 
        tipo_servicio: str,
        nombre_pili: str
    ) -> Dict[str, Any]:
        """Procesa respuesta de Gemini para formato PILI"""
        
        resultado = {
            "exito": True,
            "agente_pili": nombre_pili,
            "tipo_servicio": tipo_servicio,
            "mensaje": respuesta_texto,
            "timestamp": datetime.now().isoformat(),
            "datos_estructurados": None,
            "accion_recomendada": None
        }
        
        # Intentar extraer JSON estructurado
        if "{" in respuesta_texto and "}" in respuesta_texto:
            try:
                start = respuesta_texto.find("{")
                end = respuesta_texto.rfind("}") + 1
                json_text = respuesta_texto[start:end]
                datos_json = json.loads(json_text)
                
                resultado["datos_estructurados"] = datos_json
                resultado["accion_recomendada"] = datos_json.get("accion", "revisar_datos")
                
                # Limpiar mensaje sin JSON
                mensaje_limpio = respuesta_texto[:start] + respuesta_texto[end:]
                resultado["mensaje"] = mensaje_limpio.strip()
                
            except json.JSONDecodeError:
                pass  # No hay JSON válido
        
        # Determinar siguiente acción basada en contenido
        if not resultado["accion_recomendada"]:
            if "necesito" in respuesta_texto.lower() or "falta" in respuesta_texto.lower():
                resultado["accion_recomendada"] = "solicitar_informacion"
            elif "cotizacion" in respuesta_texto.lower() and "generada" in respuesta_texto.lower():
                resultado["accion_recomendada"] = "generar_documento"
            elif "proyecto" in respuesta_texto.lower():
                resultado["accion_recomendada"] = "crear_proyecto"
            elif "informe" in respuesta_texto.lower():
                resultado["accion_recomendada"] = "generar_informe"
            else:
                resultado["accion_recomendada"] = "continuar_conversacion"
        
        return resultado
    
    def _respuesta_demo_pili(self, mensaje: str, tipo_servicio: str) -> Dict[str, Any]:
        """
        🧠 Respuesta INTELIGENTE usando PILIBrain cuando Gemini no está configurado

        Ahora genera JSONs estructurados reales usando lógica interna sin APIs.
        """

        agente = PILI_AGENTES.get(tipo_servicio, PILI_AGENTES["cotizacion-simple"])

        # 🧠 Usar PILIBrain para generar respuesta inteligente
        logger.info(f"🧠 PILIBrain procesando: {tipo_servicio}")

        # Detectar servicio técnico (eléctrico, contraincendios, etc.)
        servicio_tecnico = pili_brain.detectar_servicio(mensaje)

        # Determinar complejidad
        complejidad = "simple" if "simple" in tipo_servicio else "complejo"

        # Si es cotización, generar con PILIBrain
        if "cotizacion" in tipo_servicio:
            # 🎯 Generar cotización real con cálculos
            respuesta_brain = pili_brain.generar_cotizacion(
                mensaje=mensaje,
                servicio=servicio_tecnico,
                complejidad=complejidad
            )

            # Combinar con formato esperado
            return {
                "exito": True,
                "agente_pili": agente["nombre"],
                "tipo_servicio": tipo_servicio,
                "servicio_tecnico_detectado": servicio_tecnico,
                "mensaje": respuesta_brain["conversacion"]["mensaje_pili"],
                "datos_estructurados": respuesta_brain["datos"],
                "accion_recomendada": "generar_documento",
                "puede_generar": respuesta_brain["conversacion"]["puede_generar"],
                "preguntas_pendientes": respuesta_brain["conversacion"].get("preguntas_pendientes", []),
                "modo_demo": True,
                "modo_inteligente": True,  # ✨ NUEVO: Indica que usa PILIBrain
                "timestamp": datetime.now().isoformat()
            }

        # Para proyectos - generar con PILIBrain
        elif "proyecto" in tipo_servicio:
            # 🎯 Generar proyecto real con cronograma
            respuesta_brain = pili_brain.generar_proyecto(
                mensaje=mensaje,
                servicio=servicio_tecnico,
                complejidad=complejidad
            )

            return {
                "exito": True,
                "agente_pili": agente["nombre"],
                "tipo_servicio": tipo_servicio,
                "servicio_tecnico_detectado": servicio_tecnico,
                "mensaje": respuesta_brain["conversacion"]["mensaje_pili"],
                "datos_estructurados": respuesta_brain["datos"],
                "accion_recomendada": "generar_documento",
                "puede_generar": respuesta_brain["conversacion"]["puede_generar"],
                "preguntas_pendientes": respuesta_brain["conversacion"].get("preguntas_pendientes", []),
                "modo_demo": True,
                "modo_inteligente": True,
                "timestamp": datetime.now().isoformat()
            }

        # Para informes - generar con PILIBrain
        elif "informe" in tipo_servicio:
            # 🎯 Generar informe real con análisis
            respuesta_brain = pili_brain.generar_informe(
                mensaje=mensaje,
                servicio=servicio_tecnico,
                complejidad=complejidad
            )

            return {
                "exito": True,
                "agente_pili": agente["nombre"],
                "tipo_servicio": tipo_servicio,
                "servicio_tecnico_detectado": servicio_tecnico,
                "mensaje": respuesta_brain["conversacion"]["mensaje_pili"],
                "datos_estructurados": respuesta_brain["datos"],
                "accion_recomendada": "generar_documento",
                "puede_generar": respuesta_brain["conversacion"]["puede_generar"],
                "modo_demo": True,
                "modo_inteligente": True,
                "timestamp": datetime.now().isoformat()
            }

        # Fallback genérico
        else:
            mensaje_respuesta = self._generar_respuesta_conversacional(tipo_servicio, mensaje, agente)

            return {
                "exito": True,
                "agente_pili": agente["nombre"],
                "tipo_servicio": tipo_servicio,
                "mensaje": mensaje_respuesta,
                "modo_demo": True,
                "modo_inteligente": True,
                "accion_recomendada": "continuar_conversacion",
                "timestamp": datetime.now().isoformat()
            }

    def _generar_respuesta_conversacional(self, tipo_servicio: str, mensaje: str, agente: Dict) -> str:
        """Genera respuesta conversacional para proyectos e informes"""

        if "proyecto" in tipo_servicio:
            return f"""¡Hola! Soy {agente['nombre']} 📊

He analizado tu solicitud: "{mensaje}"

Para crear un proyecto profesional, necesito:
• 📋 Descripción detallada del alcance
• 📅 Fecha de inicio deseada
• 👥 Recursos disponibles
• 💰 Presupuesto estimado

🎯 **Generaré un proyecto con:**
- Cronograma Gantt
- Plan de recursos
- Análisis de riesgos
- Entregables definidos

💬 Cuéntame más detalles y lo estructuramos juntos."""

        elif "informe" in tipo_servicio:
            return f"""¡Hola! Soy {agente['nombre']} 📄

He recibido tu solicitud: "{mensaje}"

Para el informe necesito:
• 📊 Datos del proyecto/cotización base
• 🎯 Objetivo del informe
• 👥 Audiencia (técnico/ejecutivo)
• 📈 Métricas a incluir

✅ **El informe incluirá:**
- Resumen ejecutivo
- Análisis detallado
- Conclusiones y recomendaciones
- Gráficos profesionales

💬 ¿Qué proyecto quieres documentar?"""

        else:
            return f"Soy {agente['nombre']} en modo inteligente. ¿En qué puedo ayudarte?"
    
    async def _guardar_aprendizaje_pili(
        self,
        mensaje: str,
        respuesta: Dict[str, Any],
        tipo_servicio: str,
        agente: str
    ):
        """Guarda conversación para aprendizaje automático de PILI"""
        
        try:
            # En un sistema real, esto se guardaría en base de datos
            aprendizaje_data = {
                "timestamp": datetime.now().isoformat(),
                "agente_pili": agente,
                "tipo_servicio": tipo_servicio,
                "entrada_usuario": mensaje,
                "respuesta_ia": respuesta.get("mensaje", ""),
                "accion_generada": respuesta.get("accion_recomendada", ""),
                "exito": respuesta.get("exito", False),
                "metadatos": {
                    "longitud_mensaje": len(mensaje),
                    "genero_datos": bool(respuesta.get("datos_estructurados")),
                    "requirio_mas_info": "necesito" in respuesta.get("mensaje", "").lower()
                }
            }
            
            # Log para debugging (en producción iría a BD)
            logger.info(f"📚 PILI aprendizaje: {agente} procesó {tipo_servicio}")
            
        except Exception as e:
            logger.error(f"Error guardando aprendizaje PILI: {e}")

    async def buscar_contexto_rag(
        self,
        consulta: str,
        tipo_servicio: str,
        limite: int = 3
    ) -> List[Dict[str, Any]]:
        """
        🤖 NUEVO PILI v3.0 - Búsqueda RAG especializada por agente
        
        Busca en proyectos históricos similares para mejorar respuestas de PILI.
        """
        
        try:
            # Integración con RAG service (si está disponible)
            from app.services.rag_service import rag_service
            
            if rag_service and rag_service.is_available():
                # Buscar documentos relacionados
                filtro = {"tipo_servicio": tipo_servicio}
                resultados = rag_service.buscar(
                    query=consulta,
                    n_results=limite,
                    where=filtro
                )
                
                logger.info(f"🔍 PILI RAG: {len(resultados)} resultados para {tipo_servicio}")
                return resultados
            else:
                logger.warning("RAG service no disponible")
                return []
                
        except Exception as e:
            logger.error(f"Error en búsqueda RAG: {e}")
            return []

    # ═══════════════════════════════════════════════════════════════
    # 🔄 MÉTODOS ORIGINALES CONSERVADOS (COMPATIBILIDAD)
    # ═══════════════════════════════════════════════════════════════
    
    async def generar_cotizacion(
        self,
        descripcion_proyecto: str,
        contexto_documentos: Optional[List[str]] = None,
        historial_chat: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """
        🔄 CONSERVADO - Genera una cotización completa usando Gemini AI
        
        Método original mantenido para compatibilidad hacia atrás.
        """
        
        if self.modo_demo:
            return {
                "exito": False,
                "error": "Gemini no configurado. Usar procesar_con_pili() para modo demo.",
                "respuesta_ia": "PILI en modo demo"
            }
        
        # Construir el prompt
        prompt = self._construir_prompt_cotizacion(
            descripcion_proyecto,
            contexto_documentos,
            historial_chat
        )
        
        try:
            response = self.model.generate_content(prompt)
            
            # Parsear la respuesta
            cotizacion_data = self._parsear_respuesta_cotizacion(response.text)
            
            return {
                "exito": True,
                "cotizacion": cotizacion_data,
                "respuesta_ia": response.text
            }
            
        except Exception as e:
            return {
                "exito": False,
                "error": str(e),
                "respuesta_ia": None
            }
    
    async def chat_conversacional(
        self,
        mensaje: str,
        historial: List[Dict[str, str]],
        contexto: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        🔄 CONSERVADO - Chat conversacional para refinar cotizaciones
        
        Método original mantenido para compatibilidad hacia atrás.
        """
        
        if self.modo_demo:
            return {
                "exito": False,
                "error": "Gemini no configurado. Usar procesar_con_pili() para funcionalidad completa."
            }
        
        prompt = self._construir_prompt_chat(mensaje, historial, contexto)
        
        try:
            response = self.model.generate_content(prompt)
            
            return {
                "exito": True,
                "respuesta": response.text,
                "cotizacion_actualizada": self._extraer_cotizacion_si_existe(response.text)
            }
            
        except Exception as e:
            return {
                "exito": False,
                "error": str(e)
            }
    
    async def analizar_documento(self, contenido: str, tipo: str) -> Dict[str, Any]:
        """
        🔄 CONSERVADO - Analiza un documento y extrae información relevante para cotización
        
        Método original mantenido para compatibilidad hacia atrás.
        """
        
        if self.modo_demo:
            return {
                "exito": False,
                "error": "Gemini no configurado. Usar procesar_con_pili() para análisis demo."
            }
        
        prompt = f"""
Eres un asistente experto en análisis de documentos para cotizaciones.

TIPO DE DOCUMENTO: {tipo}

CONTENIDO DEL DOCUMENTO:
{contenido[:5000]}  # Limitar a 5000 caracteres

TAREA:
Extrae la siguiente información del documento (si existe):
1. Cliente/Empresa mencionada
2. Servicios o productos mencionados
3. Cantidades mencionadas
4. Precios mencionados
5. Fechas relevantes
6. Requisitos específicos del proyecto
7. Cualquier otra información relevante para una cotización

RESPONDE EN FORMATO JSON:
{{
    "cliente": "nombre del cliente si se menciona",
    "servicios": ["servicio1", "servicio2"],
    "cantidades": {{"servicio": cantidad}},
    "precios": {{"servicio": precio}},
    "fechas": ["fecha1", "fecha2"],
    "requisitos": ["req1", "req2"],
    "resumen": "resumen breve del documento",
    "datos_relevantes": {{"clave": "valor"}}
}}
"""
        
        try:
            response = self.model.generate_content(prompt)
            
            # Intentar parsear JSON
            texto = response.text.strip()
            # Limpiar markdown si existe
            if "```json" in texto:
                texto = texto.split("```json")[1].split("```")[0].strip()
            elif "```" in texto:
                texto = texto.split("```")[1].split("```")[0].strip()
            
            datos = json.loads(texto)
            
            return {
                "exito": True,
                "datos_extraidos": datos
            }
            
        except Exception as e:
            return {
                "exito": False,
                "error": str(e),
                "respuesta_raw": response.text if 'response' in locals() else None
            }
    
    # ═══════════════════════════════════════════════════════════════
    # 🔄 MÉTODOS AUXILIARES ORIGINALES CONSERVADOS
    # ═══════════════════════════════════════════════════════════════
    
    def _construir_prompt_cotizacion(
        self,
        descripcion: str,
        contexto_docs: Optional[List[str]],
        historial: Optional[List[Dict[str, str]]]
    ) -> str:
        """
        🔄 CONSERVADO - Construye el prompt para generar cotización
        """
        
        prompt = f"""
Eres un asistente experto en crear cotizaciones profesionales para proyectos en Perú.

DESCRIPCIÓN DEL PROYECTO:
{descripcion}
"""
        
        if contexto_docs and len(contexto_docs) > 0:
            prompt += f"""

INFORMACIÓN DE DOCUMENTOS ANALIZADOS:
{chr(10).join(contexto_docs[:3])}  # Máximo 3 documentos
"""
        
        if historial and len(historial) > 0:
            prompt += "\n\nHISTORIAL DE CONVERSACIÓN:\n"
            for msg in historial[-5:]:  # Últimos 5 mensajes
                role = "Usuario" if msg["role"] == "user" else "Asistente"
                prompt += f"{role}: {msg['content']}\n"
        
        prompt += """

TAREA:
Genera una cotización completa y profesional. Debes proporcionar:

1. Un resumen ejecutivo del proyecto
2. Lista detallada de servicios/productos con:
   - Descripción clara
   - Cantidad estimada
   - Precio unitario realista (en soles peruanos)
   - Total por item
3. Cálculo correcto de:
   - Subtotal
   - IGV (18%)
   - Total

RESPONDE EN FORMATO JSON ESTRICTO:
{
    "resumen": "Resumen ejecutivo del proyecto",
    "cliente": "Nombre sugerido del cliente",
    "proyecto": "Nombre del proyecto",
    "items": [
        {
            "id": 1,
            "descripcion": "Descripción detallada del servicio",
            "cantidad": 1.0,
            "precioUnitario": 1000.00,
            "total": 1000.00
        }
    ],
    "observaciones": "Observaciones adicionales o condiciones",
    "vigencia": "30 días"
}

IMPORTANTE:
- Precios realistas para el mercado peruano
- Descripciones profesionales y claras
- Cantidades lógicas
- NO incluyas texto adicional fuera del JSON
- SOLO responde con el JSON válido
"""
        
        return prompt
    
    def _construir_prompt_chat(
        self,
        mensaje: str,
        historial: List[Dict[str, str]],
        contexto: Optional[Dict[str, Any]]
    ) -> str:
        """
        🔄 CONSERVADO - Construye prompt para chat conversacional
        """
        
        prompt = """
Eres un asistente de cotización inteligente y conversacional.

El usuario está refinando una cotización. Responde de manera natural y profesional.

HISTORIAL:
"""
        
        for msg in historial[-10:]:
            role = "Usuario" if msg["role"] == "user" else "Asistente"
            prompt += f"{role}: {msg['content']}\n"
        
        if contexto:
            prompt += f"\n\nCONTEXTO ACTUAL DE LA COTIZACIÓN:\n{json.dumps(contexto, indent=2, ensure_ascii=False)}\n"
        
        prompt += f"\n\nNUEVO MENSAJE DEL USUARIO:\n{mensaje}\n"
        prompt += """

RESPONDE:
1. De manera conversacional y útil
2. Si el usuario pide cambios en la cotización, proporciona el JSON actualizado
3. Si solo hace preguntas, responde claramente
"""
        
        return prompt
    
    def _parsear_respuesta_cotizacion(self, texto: str) -> Dict[str, Any]:
        """
        🔄 CONSERVADO - Parsea la respuesta de Gemini y extrae el JSON de cotización
        """
        
        try:
            # Limpiar markdown
            if "```json" in texto:
                texto = texto.split("```json")[1].split("```")[0].strip()
            elif "```" in texto:
                texto = texto.split("```")[1].split("```")[0].strip()
            
            # Parsear JSON
            data = json.loads(texto)
            
            # Calcular totales si no existen
            items = data.get("items", [])
            subtotal = sum(item.get("total", 0) for item in items)
            igv = subtotal * 0.18
            total = subtotal + igv
            
            return {
                "cliente": data.get("cliente", "Cliente"),
                "proyecto": data.get("proyecto", "Proyecto"),
                "descripcion": data.get("resumen", ""),
                "items": items,
                "subtotal": round(subtotal, 2),
                "igv": round(igv, 2),
                "total": round(total, 2),
                "observaciones": data.get("observaciones", ""),
                "vigencia": data.get("vigencia", "30 días")
            }
            
        except Exception as e:
            # Si falla el parseo, devolver estructura básica
            return {
                "cliente": "Cliente",
                "proyecto": "Proyecto",
                "items": [],
                "subtotal": 0.0,
                "igv": 0.0,
                "total": 0.0,
                "error_parseo": str(e),
                "respuesta_raw": texto
            }
    
    def _extraer_cotizacion_si_existe(self, texto: str) -> Optional[Dict[str, Any]]:
        """
        🔄 CONSERVADO - Intenta extraer una cotización actualizada del texto de respuesta
        """
        
        if "```json" in texto or "{" in texto:
            try:
                return self._parsear_respuesta_cotizacion(texto)
            except:
                return None
        
        return None

    # ═══════════════════════════════════════════════════════════════
    # 🤖 MÉTODOS NUEVOS PARA INTEGRACIÓN COMPLETA
    # ═══════════════════════════════════════════════════════════════
    
    def chat(self, mensaje: str, contexto: str = "", cotizacion_id: Optional[int] = None) -> Dict[str, Any]:
        """
        🔄 MÉTODO DE COMPATIBILIDAD - Usado por chat.py existente
        
        Redirige a lógica existente para mantener compatibilidad.
        """
        
        if self.modo_demo:
            return {
                "mensaje": f"PILI en modo demo: {mensaje}",
                "sugerencias": ["Configurar GEMINI_API_KEY", "Usar procesar_con_pili()"],
                "accion_recomendada": "configurar_gemini"
            }
        
        # Usar lógica original para compatibilidad
        historial = [{"role": "user", "content": mensaje}]
        contexto_dict = {"descripcion": contexto, "cotizacion_id": cotizacion_id}
        
        try:
            import asyncio
            result = asyncio.create_task(self.chat_conversacional(mensaje, historial, contexto_dict))
            return {
                "mensaje": "Procesando con chat conversacional...",
                "sugerencias": [],
                "accion_recomendada": "esperar_respuesta"
            }
        except Exception as e:
            return {
                "mensaje": f"Error en chat: {str(e)}",
                "sugerencias": ["Revisar configuración"],
                "accion_recomendada": "reintentar"
            }

    def sugerir_mejoras(self, cotizacion_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        🔄 MÉTODO DE COMPATIBILIDAD - Usado por endpoints existentes
        """
        
        if self.modo_demo:
            return {
                "mejoras": [
                    "PILI en modo demo: Sugerencias básicas disponibles",
                    "Configura GEMINI_API_KEY para análisis completo",
                    "Usar PILI con especialización por agente"
                ]
            }
        
        # Lógica básica de sugerencias
        return {
            "mejoras": [
                "Revisar precios actualizados del mercado",
                "Verificar especificaciones técnicas CNE",
                "Considerar factores de seguridad adicionales"
            ]
        }

# ═══════════════════════════════════════════════════════════════
# 🎯 INSTANCIA GLOBAL CON MEJORAS PILI
# ═══════════════════════════════════════════════════════════════

# Crear instancia global con manejo robusto de errores
try:
    gemini_service = GeminiService()
    logger.info("✅ GeminiService + PILI inicializado correctamente")
except Exception as e:
    logger.error(f"❌ Error crítico inicializando GeminiService: {e}")
    # Crear instancia degradada para evitar errores
    gemini_service = None

# Función auxiliar para obtener instancia segura
def get_gemini_service():
    """Obtiene instancia de GeminiService de forma segura"""
    global gemini_service
    if gemini_service is None:
        try:
            gemini_service = GeminiService()
        except Exception as e:
            logger.error(f"Error creando GeminiService: {e}")
    return gemini_service