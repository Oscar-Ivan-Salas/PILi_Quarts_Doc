"""
Multi-IA Orchestrator - Orquestador de múltiples IAs
Gestiona Gemini, Claude, GPT-4, Groq según el plan del usuario
"""
import logging
from typing import Optional, Dict, Any
from app.core.features import FeatureFlags
from app.models.usuario import Usuario

logger = logging.getLogger(__name__)


class MultiIAOrchestrator:
    """
    Orquestador de múltiples IAs

    Selecciona la IA apropiada según:
    - Plan del usuario (Free, Pro, Enterprise)
    - Tipo de operación
    - Disponibilidad de APIs
    """

    def __init__(self, usuario: Optional[Usuario] = None):
        self.usuario = usuario

        # Importar servicios de IA (lazy loading)
        try:
            from app.services.gemini_service import GeminiService
            self.gemini = GeminiService()
            logger.info("✅ Gemini disponible")
        except Exception as e:
            self.gemini = None
            logger.warning(f"⚠️ Gemini no disponible: {e}")

        # Claude (Anthropic)
        try:
            # from langchain_anthropic import ChatAnthropic
            # self.claude = ChatAnthropic(...)
            self.claude = None  # Por implementar
            if self.claude:
                logger.info("✅ Claude disponible")
        except Exception as e:
            self.claude = None
            logger.warning(f"⚠️ Claude no disponible: {e}")

        # GPT-4 (OpenAI)
        try:
            # from langchain_openai import ChatOpenAI
            # self.gpt4 = ChatOpenAI(...)
            self.gpt4 = None  # Por implementar
            if self.gpt4:
                logger.info("✅ GPT-4 disponible")
        except Exception as e:
            self.gpt4 = None
            logger.warning(f"⚠️ GPT-4 no disponible: {e}")

        # Groq (gratis)
        try:
            # from langchain_groq import ChatGroq
            # self.groq = ChatGroq(...)
            self.groq = None  # Por implementar
            if self.groq:
                logger.info("✅ Groq disponible")
        except Exception as e:
            self.groq = None
            logger.warning(f"⚠️ Groq no disponible: {e}")

    async def procesar(
        self,
        solicitud: str,
        tipo_operacion: str = "chat",
        contexto: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Procesa una solicitud con la IA apropiada

        Args:
            solicitud: Texto de la solicitud del usuario
            tipo_operacion: chat, cotizacion, proyecto, informe
            contexto: Contexto adicional (opcional)

        Returns:
            dict: Respuesta de la IA
        """
        # Si el feature flag está OFF, usar solo Gemini (fallback)
        if not FeatureFlags.MULTI_IA:
            logger.info("🔓 Multi-IA OFF - Usando solo Gemini")
            return await self._procesar_con_gemini(solicitud, tipo_operacion, contexto)

        # Seleccionar IA según plan del usuario
        ia_seleccionada = self._seleccionar_ia(tipo_operacion)

        logger.info(f"🤖 IA seleccionada: {ia_seleccionada} | Plan: {self.usuario.plan if self.usuario else 'N/A'}")

        # Procesar según IA seleccionada
        if ia_seleccionada == "gemini":
            return await self._procesar_con_gemini(solicitud, tipo_operacion, contexto)
        elif ia_seleccionada == "claude":
            return await self._procesar_con_claude(solicitud, tipo_operacion, contexto)
        elif ia_seleccionada == "gpt4":
            return await self._procesar_con_gpt4(solicitud, tipo_operacion, contexto)
        elif ia_seleccionada == "groq":
            return await self._procesar_con_groq(solicitud, tipo_operacion, contexto)
        else:
            # Fallback a Gemini
            return await self._procesar_con_gemini(solicitud, tipo_operacion, contexto)

    def _seleccionar_ia(self, tipo_operacion: str) -> str:
        """
        Selecciona la IA apropiada según el plan y operación

        Estrategia:
        - Free: Solo Gemini (gratis) o Groq (gratis)
        - Pro: Gemini para creatividad, Claude para razonamiento
        - Enterprise: Routing inteligente según operación
        """
        if not self.usuario:
            return "gemini"

        plan = self.usuario.plan
        ia_preferida = self.usuario.ia_preferida if hasattr(self.usuario, 'ia_preferida') else "gemini"

        # Plan Free: Solo IAs gratuitas
        if plan == "free":
            if self.gemini:
                return "gemini"
            elif self.groq:
                return "groq"
            else:
                return "gemini"  # Fallback

        # Plan Pro: IAs según preferencia y disponibilidad
        elif plan == "pro":
            # Usar IA preferida si está disponible
            if ia_preferida == "claude" and self.claude:
                return "claude"
            elif ia_preferida == "gpt-4" and self.gpt4:
                return "gpt4"
            elif ia_preferida == "gemini" and self.gemini:
                return "gemini"
            else:
                # Fallback inteligente según operación
                if tipo_operacion in ["proyecto", "informe"]:
                    return "claude" if self.claude else "gemini"
                else:
                    return "gemini"

        # Plan Enterprise: Routing inteligente
        elif plan == "enterprise":
            # Routing por tipo de operación
            routing = {
                "chat": ia_preferida,  # Usar preferencia del usuario
                "cotizacion": "gemini",  # Gemini es bueno en generación
                "proyecto": "claude",  # Claude es bueno en razonamiento
                "informe": "gpt4",  # GPT-4 es bueno en escritura formal
                "analisis": "claude"  # Claude es bueno en análisis
            }

            ia_sugerida = routing.get(tipo_operacion, ia_preferida)

            # Verificar disponibilidad
            if ia_sugerida == "claude" and self.claude:
                return "claude"
            elif ia_sugerida == "gpt4" and self.gpt4:
                return "gpt4"
            elif ia_sugerida == "gemini" and self.gemini:
                return "gemini"
            elif ia_sugerida == "groq" and self.groq:
                return "groq"
            else:
                return "gemini"  # Fallback final

        return "gemini"

    async def _procesar_con_gemini(
        self,
        solicitud: str,
        tipo_operacion: str,
        contexto: Optional[str]
    ) -> Dict[str, Any]:
        """Procesa con Gemini"""
        if not self.gemini:
            return {"error": "Gemini no disponible", "ia_usada": "ninguna"}

        try:
            # Usar el servicio de Gemini existente
            if tipo_operacion == "chat":
                response = await self.gemini.chat_conversacional(
                    mensaje=solicitud,
                    contexto=contexto or "",
                    historial=[]
                )
            else:
                # Para otras operaciones, usar método general
                response = await self.gemini.generar_cotizacion_estructurada(
                    descripcion=solicitud,
                    archivos_contexto=[]
                )

            return {
                **response,
                "ia_usada": "gemini",
                "tokens_estimados": len(solicitud.split()) * 1.5  # Estimación
            }

        except Exception as e:
            logger.error(f"❌ Error en Gemini: {e}")
            return {"error": str(e), "ia_usada": "gemini"}

    async def _procesar_con_claude(
        self,
        solicitud: str,
        tipo_operacion: str,
        contexto: Optional[str]
    ) -> Dict[str, Any]:
        """Procesa con Claude (Anthropic)"""
        if not self.claude:
            logger.warning("⚠️ Claude no disponible, fallback a Gemini")
            return await self._procesar_con_gemini(solicitud, tipo_operacion, contexto)

        try:
            # TODO: Implementar cuando se agregue Claude API
            # response = await self.claude.invoke(solicitud)
            return {
                "respuesta": "Claude API por implementar",
                "ia_usada": "claude",
                "tokens_estimados": len(solicitud.split()) * 1.5
            }
        except Exception as e:
            logger.error(f"❌ Error en Claude: {e}")
            return await self._procesar_con_gemini(solicitud, tipo_operacion, contexto)

    async def _procesar_con_gpt4(
        self,
        solicitud: str,
        tipo_operacion: str,
        contexto: Optional[str]
    ) -> Dict[str, Any]:
        """Procesa con GPT-4 (OpenAI)"""
        if not self.gpt4:
            logger.warning("⚠️ GPT-4 no disponible, fallback a Gemini")
            return await self._procesar_con_gemini(solicitud, tipo_operacion, contexto)

        try:
            # TODO: Implementar cuando se agregue OpenAI API
            # response = await self.gpt4.invoke(solicitud)
            return {
                "respuesta": "GPT-4 API por implementar",
                "ia_usada": "gpt-4",
                "tokens_estimados": len(solicitud.split()) * 1.5
            }
        except Exception as e:
            logger.error(f"❌ Error en GPT-4: {e}")
            return await self._procesar_con_gemini(solicitud, tipo_operacion, contexto)

    async def _procesar_con_groq(
        self,
        solicitud: str,
        tipo_operacion: str,
        contexto: Optional[str]
    ) -> Dict[str, Any]:
        """Procesa con Groq (Llama - gratis)"""
        if not self.groq:
            logger.warning("⚠️ Groq no disponible, fallback a Gemini")
            return await self._procesar_con_gemini(solicitud, tipo_operacion, contexto)

        try:
            # TODO: Implementar cuando se agregue Groq API
            # response = await self.groq.invoke(solicitud)
            return {
                "respuesta": "Groq API por implementar",
                "ia_usada": "groq",
                "tokens_estimados": len(solicitud.split()) * 1.5
            }
        except Exception as e:
            logger.error(f"❌ Error en Groq: {e}")
            return await self._procesar_con_gemini(solicitud, tipo_operacion, contexto)

    def get_ias_disponibles(self) -> Dict[str, bool]:
        """Retorna qué IAs están disponibles"""
        return {
            "gemini": self.gemini is not None,
            "claude": self.claude is not None,
            "gpt4": self.gpt4 is not None,
            "groq": self.groq is not None
        }
