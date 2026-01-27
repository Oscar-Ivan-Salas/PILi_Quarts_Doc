"""
🤖 MULTI-IA SERVICE - Soporte para múltiples proveedores de IA
📁 RUTA: backend/app/services/multi_ia_service.py

Sistema que permite usar múltiples IAs con fallback automático:
- Google Gemini
- OpenAI (ChatGPT)
- Anthropic (Claude)
- Groq (Llama gratuito)
- Together AI (gratuito)
- Cohere (gratuito)
- Fallback a PILIBrain (100% offline)

Solo necesitas agregar las API keys en .env
"""

import os
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
import asyncio

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════
# 🔧 CONFIGURACIÓN DE PROVEEDORES DE IA
# ═══════════════════════════════════════════════════════════════

class MultiIAProvider:
    """
    Gestor de múltiples proveedores de IA con fallback automático

    Uso:
    1. Agrega API keys en .env:
       GEMINI_API_KEY=tu_key_aqui
       OPENAI_API_KEY=tu_key_aqui
       ANTHROPIC_API_KEY=tu_key_aqui
       GROQ_API_KEY=tu_key_aqui

    2. El sistema intentará usar las IAs en orden de prioridad
    3. Si todas fallan, usa PILIBrain (offline)
    """

    def __init__(self):
        """Inicializa proveedores disponibles"""
        self.providers = self._detect_available_providers()
        self.fallback_to_pili = True

        logger.info(f"🤖 Multi-IA inicializado con {len(self.providers)} proveedores")
        for provider in self.providers:
            logger.info(f"   ✅ {provider['nombre']}")

    def _detect_available_providers(self) -> List[Dict[str, Any]]:
        """Detecta qué proveedores están configurados"""
        available = []

        # 1. Google Gemini (PRIORIDAD 1)
        if os.getenv("GEMINI_API_KEY"):
            available.append({
                "nombre": "Google Gemini 1.5 Pro",
                "tipo": "gemini",
                "prioridad": 1,
                "costo": "Bajo",
                "limite": "60 req/min"
            })

        # 2. OpenAI GPT-4 (PRIORIDAD 2)
        if os.getenv("OPENAI_API_KEY"):
            available.append({
                "nombre": "OpenAI GPT-4",
                "tipo": "openai",
                "prioridad": 2,
                "costo": "Alto",
                "limite": "10000 tokens/min"
            })

        # 3. Anthropic Claude (PRIORIDAD 3)
        if os.getenv("ANTHROPIC_API_KEY"):
            available.append({
                "nombre": "Anthropic Claude 3",
                "tipo": "anthropic",
                "prioridad": 3,
                "costo": "Medio",
                "limite": "50 req/min"
            })

        # 4. Groq (GRATUITO - PRIORIDAD 4)
        if os.getenv("GROQ_API_KEY"):
            available.append({
                "nombre": "Groq Llama 3 70B",
                "tipo": "groq",
                "prioridad": 4,
                "costo": "Gratis",
                "limite": "30 req/min"
            })

        # 5. Together AI (GRATUITO - PRIORIDAD 5)
        if os.getenv("TOGETHER_API_KEY"):
            available.append({
                "nombre": "Together AI Mixtral",
                "tipo": "together",
                "prioridad": 5,
                "costo": "Gratis",
                "limite": "60 req/min"
            })

        # 6. Cohere (GRATUITO - PRIORIDAD 6)
        if os.getenv("COHERE_API_KEY"):
            available.append({
                "nombre": "Cohere Command",
                "tipo": "cohere",
                "prioridad": 6,
                "costo": "Gratis",
                "limite": "100 req/min"
            })

        # Ordenar por prioridad
        available.sort(key=lambda x: x["prioridad"])

        return available

    async def generar_respuesta(
        self,
        prompt: str,
        tipo_servicio: str = "cotizacion-simple",
        temperatura: float = 0.3,
        max_tokens: int = 4000
    ) -> Dict[str, Any]:
        """
        Genera respuesta usando la mejor IA disponible con fallback automático

        Args:
            prompt: Prompt para la IA
            tipo_servicio: Tipo de servicio PILI
            temperatura: Creatividad (0.0-1.0)
            max_tokens: Máximo de tokens

        Returns:
            Respuesta de la IA con metadata
        """

        # Si no hay proveedores, usar PILIBrain directamente
        if not self.providers:
            logger.info("🧠 Sin APIs configuradas, usando PILIBrain offline")
            return await self._usar_pili_brain(prompt, tipo_servicio)

        # Intentar con cada proveedor en orden
        for provider in self.providers:
            try:
                logger.info(f"🤖 Intentando con {provider['nombre']}...")

                if provider["tipo"] == "gemini":
                    resultado = await self._usar_gemini(prompt, temperatura, max_tokens)
                elif provider["tipo"] == "openai":
                    resultado = await self._usar_openai(prompt, temperatura, max_tokens)
                elif provider["tipo"] == "anthropic":
                    resultado = await self._usar_anthropic(prompt, temperatura, max_tokens)
                elif provider["tipo"] == "groq":
                    resultado = await self._usar_groq(prompt, temperatura, max_tokens)
                elif provider["tipo"] == "together":
                    resultado = await self._usar_together(prompt, temperatura, max_tokens)
                elif provider["tipo"] == "cohere":
                    resultado = await self._usar_cohere(prompt, temperatura, max_tokens)
                else:
                    continue

                # Si funcionó, retornar
                if resultado.get("exito"):
                    resultado["ia_utilizada"] = provider["nombre"]
                    resultado["costo"] = provider["costo"]
                    logger.info(f"✅ Respuesta exitosa de {provider['nombre']}")
                    return resultado

            except Exception as e:
                logger.warning(f"⚠️ {provider['nombre']} falló: {e}")
                continue

        # Si todos fallaron, usar PILIBrain
        logger.warning("⚠️ Todas las IAs fallaron, usando PILIBrain offline")
        return await self._usar_pili_brain(prompt, tipo_servicio)

    async def _usar_gemini(self, prompt: str, temp: float, max_tok: int) -> Dict[str, Any]:
        """Usa Google Gemini"""
        try:
            import google.generativeai as genai

            genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
            model = genai.GenerativeModel("gemini-1.5-pro")

            response = model.generate_content(
                prompt,
                generation_config={
                    "temperature": temp,
                    "max_output_tokens": max_tok
                }
            )

            return {
                "exito": True,
                "respuesta": response.text,
                "tokens_usados": len(response.text.split())
            }
        except Exception as e:
            raise Exception(f"Gemini error: {e}")

    async def _usar_openai(self, prompt: str, temp: float, max_tok: int) -> Dict[str, Any]:
        """Usa OpenAI GPT-4"""
        try:
            import openai

            openai.api_key = os.getenv("OPENAI_API_KEY")

            response = openai.ChatCompletion.create(
                model="gpt-4-turbo-preview",
                messages=[{"role": "user", "content": prompt}],
                temperature=temp,
                max_tokens=max_tok
            )

            return {
                "exito": True,
                "respuesta": response.choices[0].message.content,
                "tokens_usados": response.usage.total_tokens
            }
        except Exception as e:
            raise Exception(f"OpenAI error: {e}")

    async def _usar_anthropic(self, prompt: str, temp: float, max_tok: int) -> Dict[str, Any]:
        """Usa Anthropic Claude"""
        try:
            import anthropic

            client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

            response = client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=max_tok,
                temperature=temp,
                messages=[{"role": "user", "content": prompt}]
            )

            return {
                "exito": True,
                "respuesta": response.content[0].text,
                "tokens_usados": response.usage.input_tokens + response.usage.output_tokens
            }
        except Exception as e:
            raise Exception(f"Anthropic error: {e}")

    async def _usar_groq(self, prompt: str, temp: float, max_tok: int) -> Dict[str, Any]:
        """Usa Groq (Llama 3 - GRATUITO)"""
        try:
            from groq import Groq

            client = Groq(api_key=os.getenv("GROQ_API_KEY"))

            response = client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[{"role": "user", "content": prompt}],
                temperature=temp,
                max_tokens=max_tok
            )

            return {
                "exito": True,
                "respuesta": response.choices[0].message.content,
                "tokens_usados": response.usage.total_tokens
            }
        except Exception as e:
            raise Exception(f"Groq error: {e}")

    async def _usar_together(self, prompt: str, temp: float, max_tok: int) -> Dict[str, Any]:
        """Usa Together AI (GRATUITO)"""
        try:
            import together

            together.api_key = os.getenv("TOGETHER_API_KEY")

            response = together.Complete.create(
                model="mistralai/Mixtral-8x7B-Instruct-v0.1",
                prompt=prompt,
                temperature=temp,
                max_tokens=max_tok
            )

            return {
                "exito": True,
                "respuesta": response['output']['choices'][0]['text'],
                "tokens_usados": len(response['output']['choices'][0]['text'].split())
            }
        except Exception as e:
            raise Exception(f"Together error: {e}")

    async def _usar_cohere(self, prompt: str, temp: float, max_tok: int) -> Dict[str, Any]:
        """Usa Cohere (GRATUITO)"""
        try:
            import cohere

            client = cohere.Client(os.getenv("COHERE_API_KEY"))

            response = client.generate(
                model="command",
                prompt=prompt,
                temperature=temp,
                max_tokens=max_tok
            )

            return {
                "exito": True,
                "respuesta": response.generations[0].text,
                "tokens_usados": len(response.generations[0].text.split())
            }
        except Exception as e:
            raise Exception(f"Cohere error: {e}")

    async def _usar_pili_brain(self, prompt: str, tipo_servicio: str) -> Dict[str, Any]:
        """Usa PILIBrain como fallback (100% offline)"""
        try:
            from app.services.pili_brain import pili_brain

            # Detectar servicio del prompt
            servicio = pili_brain.detectar_servicio(prompt)

            # Determinar complejidad
            complejidad = "complejo" if "complejo" in tipo_servicio else "simple"

            # Generar según tipo
            if "cotizacion" in tipo_servicio:
                resultado = pili_brain.generar_cotizacion(prompt, servicio, complejidad)
            elif "proyecto" in tipo_servicio:
                resultado = pili_brain.generar_proyecto(prompt, servicio, complejidad)
            elif "informe" in tipo_servicio:
                resultado = pili_brain.generar_informe(prompt, servicio, complejidad)
            else:
                resultado = pili_brain.generar_cotizacion(prompt, servicio, complejidad)

            return {
                "exito": True,
                "respuesta": resultado["conversacion"]["mensaje_pili"],
                "datos_estructurados": resultado["datos"],
                "ia_utilizada": "PILIBrain (Offline)",
                "costo": "Gratis",
                "tokens_usados": 0
            }
        except Exception as e:
            raise Exception(f"PILIBrain error: {e}")

    def obtener_estado_proveedores(self) -> Dict[str, Any]:
        """Obtiene el estado de todos los proveedores"""
        return {
            "total_proveedores": len(self.providers),
            "proveedores_activos": [p["nombre"] for p in self.providers],
            "fallback_disponible": True,  # PILIBrain siempre disponible
            "configuracion": {
                "gemini": bool(os.getenv("GEMINI_API_KEY")),
                "openai": bool(os.getenv("OPENAI_API_KEY")),
                "anthropic": bool(os.getenv("ANTHROPIC_API_KEY")),
                "groq": bool(os.getenv("GROQ_API_KEY")),
                "together": bool(os.getenv("TOGETHER_API_KEY")),
                "cohere": bool(os.getenv("COHERE_API_KEY"))
            }
        }


# ═══════════════════════════════════════════════════════════════
# 🏭 INSTANCIA SINGLETON
# ═══════════════════════════════════════════════════════════════

multi_ia = MultiIAProvider()

logger.info("🤖 Multi-IA Service listo")
