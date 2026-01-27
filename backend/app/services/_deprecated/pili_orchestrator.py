"""
🎯 PILI ORCHESTRATOR LITE - INTEGRACIÓN CON ESTRUCTURA EXISTENTE
📁 RUTA: services/pili_orchestrator.py

INTEGRA CON TUS SERVICIOS EXISTENTES SIN TOCARLOS:
✅ file_processor.py (tu versión)
✅ gemini_service.py (tu versión) 
✅ rag_service.py (tu versión)
✅ template_processor.py (tu versión)
✅ word_generator.py (tu versión)
✅ pdf_generator.py (tu versión)

ESTE ARCHIVO ES EL COORDINADOR QUE UNE TODO TU SISTEMA EXISTENTE.
"""

import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
import asyncio
import json

# Imports de tus servicios existentes
try:
    from .gemini_service import gemini_service
    from .file_processor import file_processor
    from .rag_service import rag_service
    from .template_processor import template_processor
    from .word_generator import word_generator
    from .pdf_generator import pdf_generator
except ImportError as e:
    logging.warning(f"Importing with fallback: {e}")
    # Fallback imports
    try:
        import sys
        import os
        sys.path.append(os.path.dirname(__file__))
        
        import gemini_service
        import file_processor
        import rag_service
        import template_processor
        import word_generator
        import pdf_generator
    except:
        logging.error("Could not import services")

logger = logging.getLogger(__name__)

class PILIOrchestrator:
    """
    🎯 ORQUESTADOR LITE - Se integra con tu estructura existente
    
    NO modifica tus archivos existentes.
    SOLO los coordina para crear flujos end-to-end.
    """
    
    def __init__(self):
        """Inicializa con tus servicios existentes"""
        
        self.servicios = {}
        self.modo_demo = False
        
        # Conectar con tus servicios existentes
        self._conectar_servicios_existentes()
        
        logger.info("✅ PILI Orchestrator conectado con tus servicios existentes")
    
    def _conectar_servicios_existentes(self):
        """Conecta con tus servicios sin modificarlos"""
        
        # Conectar Gemini Service (tu versión)
        try:
            if 'gemini_service' in globals():
                self.servicios['gemini'] = gemini_service
                logger.info("✅ Conectado con tu GeminiService")
            else:
                self.servicios['gemini'] = None
                self.modo_demo = True
                logger.info("⚠️ GeminiService no disponible - modo demo")
        except Exception as e:
            logger.warning(f"GeminiService error: {e}")
            self.servicios['gemini'] = None
            self.modo_demo = True
        
        # Conectar File Processor (tu versión)
        try:
            if 'file_processor' in globals():
                self.servicios['file_processor'] = file_processor
                logger.info("✅ Conectado con tu FileProcessor")
            else:
                self.servicios['file_processor'] = None
        except Exception as e:
            logger.warning(f"FileProcessor error: {e}")
            self.servicios['file_processor'] = None
        
        # Conectar RAG Service (tu versión)
        try:
            if 'rag_service' in globals():
                self.servicios['rag'] = rag_service
                logger.info("✅ Conectado con tu RAGService")
            else:
                self.servicios['rag'] = None
        except Exception as e:
            logger.warning(f"RAGService error: {e}")
            self.servicios['rag'] = None
        
        # Conectar Template Processor (tu versión)
        try:
            if 'template_processor' in globals():
                self.servicios['template'] = template_processor
                logger.info("✅ Conectado con tu TemplateProcessor")
            else:
                self.servicios['template'] = None
        except Exception as e:
            logger.warning(f"TemplateProcessor error: {e}")
            self.servicios['template'] = None
        
        # Conectar Word Generator (tu versión)
        try:
            if 'word_generator' in globals():
                self.servicios['word'] = word_generator
                logger.info("✅ Conectado con tu WordGenerator")
            else:
                self.servicios['word'] = None
        except Exception as e:
            logger.warning(f"WordGenerator error: {e}")
            self.servicios['word'] = None
        
        # Conectar PDF Generator (tu versión)
        try:
            if 'pdf_generator' in globals():
                self.servicios['pdf'] = pdf_generator
                logger.info("✅ Conectado con tu PDFGenerator")
            else:
                self.servicios['pdf'] = None
        except Exception as e:
            logger.warning(f"PDFGenerator error: {e}")
            self.servicios['pdf'] = None

    # ═══════════════════════════════════════════════════════════════
    # 🎯 MÉTODOS PRINCIPALES - USAN TUS SERVICIOS EXISTENTES
    # ═══════════════════════════════════════════════════════════════
    
    async def procesar_cotizacion_completa(
        self,
        descripcion: str,
        archivos: Optional[List] = None,
        tipo_salida: str = "word",  # "word" o "pdf"
        cliente: str = "Cliente",
        usar_plantilla: bool = False,
        logo_base64: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        🎯 FLUJO COTIZACIÓN COMPLETA usando tus servicios existentes
        
        1. Procesa archivos (si hay) con TU file_processor
        2. Genera respuesta con TU gemini_service  
        3. Crea documento con TU word_generator o pdf_generator
        """
        
        try:
            resultado = {
                "exito": True,
                "timestamp": datetime.now().isoformat(),
                "tipo_procesamiento": "cotizacion_completa",
                "pasos_realizados": []
            }
            
            # PASO 1: Procesar archivos (si hay)
            contenido_archivos = ""
            if archivos and len(archivos) > 0 and self.servicios['file_processor']:
                logger.info("📄 Procesando archivos con tu FileProcessor...")
                
                for archivo in archivos:
                    try:
                        # Usar TU file_processor existente
                        resultado_archivo = await self.servicios['file_processor'].procesar_archivo(
                            archivo['path'], archivo['nombre']
                        )
                        
                        if resultado_archivo.get('exito'):
                            contenido_archivos += f"\n--- {archivo['nombre']} ---\n"
                            contenido_archivos += resultado_archivo.get('contenido_texto', '')
                            
                    except Exception as e:
                        logger.warning(f"Error procesando archivo: {e}")
                
                resultado["pasos_realizados"].append("procesar_archivos")
            
            # PASO 2: Generar cotización con IA (tu Gemini)
            if self.servicios['gemini']:
                logger.info("🤖 Generando cotización con tu GeminiService...")
                
                try:
                    # Usar TU gemini_service existente
                    prompt_completo = f"""
Descripción del proyecto: {descripcion}

Cliente: {cliente}

Archivos analizados:
{contenido_archivos}

Genera una cotización profesional para instalación eléctrica en Perú.
"""
                    
                    respuesta_ia = await self.servicios['gemini'].generar_cotizacion(
                        descripcion_proyecto=prompt_completo,
                        contexto_documentos=[contenido_archivos] if contenido_archivos else None,
                        historial_chat=[]
                    )
                    
                    resultado["respuesta_ia"] = respuesta_ia
                    resultado["pasos_realizados"].append("generar_ia")
                    
                except Exception as e:
                    logger.error(f"Error con Gemini: {e}")
                    # Fallback a respuesta demo
                    respuesta_ia = self._generar_cotizacion_demo(descripcion, cliente)
                    resultado["respuesta_ia"] = respuesta_ia
                    resultado["modo_demo"] = True
            else:
                # Modo demo
                respuesta_ia = self._generar_cotizacion_demo(descripcion, cliente)
                resultado["respuesta_ia"] = respuesta_ia
                resultado["modo_demo"] = True
            
            # PASO 3: Generar documento final
            if respuesta_ia.get('exito') and respuesta_ia.get('cotizacion'):
                logger.info(f"📄 Generando documento {tipo_salida} con tus generadores...")
                
                datos_cotizacion = respuesta_ia['cotizacion']
                
                if tipo_salida == "pdf" and self.servicios['pdf']:
                    # Usar TU pdf_generator
                    try:
                        documento_resultado = self.servicios['pdf'].generar_cotizacion(
                            datos_cotizacion=datos_cotizacion,
                            opciones={"cliente": cliente},
                            logo_base64=logo_base64
                        )
                        resultado["documento_generado"] = documento_resultado
                        resultado["pasos_realizados"].append("generar_pdf")
                    except Exception as e:
                        logger.error(f"Error generando PDF: {e}")
                        resultado["error_documento"] = str(e)
                        
                elif self.servicios['word']:
                    # Usar TU word_generator (default)
                    try:
                        documento_resultado = self.servicios['word'].generar_cotizacion(
                            datos_cotizacion=datos_cotizacion,
                            opciones={"cliente": cliente},
                            logo_base64=logo_base64
                        )
                        resultado["documento_generado"] = documento_resultado
                        resultado["pasos_realizados"].append("generar_word")
                    except Exception as e:
                        logger.error(f"Error generando Word: {e}")
                        resultado["error_documento"] = str(e)
                
                else:
                    resultado["error_documento"] = f"Generador {tipo_salida} no disponible"
            
            return resultado
            
        except Exception as e:
            logger.error(f"Error en procesamiento completo: {e}")
            return {
                "exito": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    async def procesar_proyecto_completo(
        self,
        descripcion: str,
        cliente: str = "Cliente",
        tipo_salida: str = "word"
    ) -> Dict[str, Any]:
        """
        🎯 FLUJO PROYECTO COMPLETO usando tus servicios existentes
        """
        
        try:
            # Similar al de cotización pero usando métodos de proyecto
            if self.servicios['word'] and hasattr(self.servicios['word'], 'generar_informe_proyecto'):
                
                datos_proyecto = {
                    "cliente": cliente,
                    "descripcion": descripcion,
                    "fecha": datetime.now().strftime("%d/%m/%Y"),
                    "tipo": "Proyecto Eléctrico"
                }
                
                resultado_doc = self.servicios['word'].generar_informe_proyecto(
                    datos_proyecto=datos_proyecto
                )
                
                return {
                    "exito": True,
                    "tipo_procesamiento": "proyecto_completo",
                    "documento_generado": resultado_doc,
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {
                    "exito": False,
                    "error": "WordGenerator no tiene método generar_informe_proyecto",
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            return {
                "exito": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    async def chat_inteligente(
        self,
        mensaje: str,
        contexto: Optional[Dict[str, Any]] = None,
        historial: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """
        🎯 CHAT INTELIGENTE usando tu GeminiService existente
        """
        
        if self.servicios['gemini']:
            try:
                respuesta = await self.servicios['gemini'].chat_conversacional(
                    mensaje=mensaje,
                    historial=historial or [],
                    contexto=contexto
                )
                
                return {
                    "exito": True,
                    "respuesta": respuesta.get('respuesta', ''),
                    "timestamp": datetime.now().isoformat()
                }
                
            except Exception as e:
                logger.error(f"Error en chat: {e}")
                return {
                    "exito": False,
                    "error": str(e),
                    "respuesta": "Error en el chat. Verifica tu configuración de Gemini.",
                    "timestamp": datetime.now().isoformat()
                }
        else:
            # Modo demo
            return {
                "exito": True,
                "respuesta": f"DEMO: Recibí tu mensaje '{mensaje[:50]}...' - Configura GEMINI_API_KEY para chat real.",
                "modo_demo": True,
                "timestamp": datetime.now().isoformat()
            }
    
    def _generar_cotizacion_demo(self, descripcion: str, cliente: str) -> Dict[str, Any]:
        """Genera cotización demo cuando Gemini no está disponible"""
        
        return {
            "exito": True,
            "cotizacion": {
                "cliente": cliente,
                "proyecto": f"Proyecto para {descripcion[:30]}...",
                "numero": f"DEMO-{datetime.now().strftime('%Y%m%d')}-001",
                "fecha": datetime.now().strftime("%d/%m/%Y"),
                "items": [
                    {
                        "id": 1,
                        "descripcion": f"Instalación eléctrica - {descripcion[:40]}",
                        "cantidad": 1,
                        "precio_unitario": 1500.00,
                        "total": 1500.00
                    }
                ],
                "subtotal": 1500.00,
                "igv": 270.00,
                "total": 1770.00,
                "observaciones": "Cotización DEMO - Configura GEMINI_API_KEY para cotizaciones reales con IA",
                "vigencia": "30 días"
            },
            "modo_demo": True
        }

    # ═══════════════════════════════════════════════════════════════
    # 🎯 MÉTODOS UTILITARIOS
    # ═══════════════════════════════════════════════════════════════
    
    def obtener_estado(self) -> Dict[str, Any]:
        """Obtiene estado de todos tus servicios"""
        
        estado = {
            "pili_orchestrator": "✅ ACTIVO",
            "modo_demo": self.modo_demo,
            "servicios_conectados": {},
            "total_servicios": len(self.servicios)
        }
        
        for nombre, servicio in self.servicios.items():
            if servicio is not None:
                estado["servicios_conectados"][nombre] = "✅ CONECTADO"
            else:
                estado["servicios_conectados"][nombre] = "❌ NO DISPONIBLE"
        
        return estado
    
    def listar_capacidades(self) -> Dict[str, Any]:
        """Lista qué puede hacer con tus servicios actuales"""
        
        capacidades = {
            "flujos_completos": [],
            "generadores_disponibles": [],
            "procesadores_disponibles": []
        }
        
        # Verificar flujos completos disponibles
        if self.servicios['gemini'] and self.servicios['word']:
            capacidades["flujos_completos"].append("cotizacion_completa_word")
        
        if self.servicios['gemini'] and self.servicios['pdf']:
            capacidades["flujos_completos"].append("cotizacion_completa_pdf")
        
        if self.servicios['word']:
            capacidades["generadores_disponibles"].append("word_documents")
        
        if self.servicios['pdf']:
            capacidades["generadores_disponibles"].append("pdf_documents")
        
        if self.servicios['file_processor']:
            capacidades["procesadores_disponibles"].append("file_analysis")
        
        if self.servicios['template']:
            capacidades["procesadores_disponibles"].append("template_processing")
        
        return capacidades

# ═══════════════════════════════════════════════════════════════
# 🎯 INSTANCIA GLOBAL PARA TU SISTEMA
# ═══════════════════════════════════════════════════════════════

# Crear instancia que se conecta con tus servicios
try:
    pili_orchestrator = PILIOrchestrator()
    logger.info("✅ PILI Orchestrator conectado con tu sistema existente")
except Exception as e:
    logger.error(f"❌ Error conectando PILI Orchestrator: {e}")
    pili_orchestrator = None

def get_pili_orchestrator():
    """Obtiene el orquestrador conectado con tu sistema"""
    global pili_orchestrator
    if pili_orchestrator is None:
        try:
            pili_orchestrator = PILIOrchestrator()
        except Exception as e:
            logger.error(f"Error creando PILIOrchestrator: {e}")
    return pili_orchestrator

# ═══════════════════════════════════════════════════════════════
# 🎯 EJEMPLO DE USO CON TUS SERVICIOS
# ═══════════════════════════════════════════════════════════════

"""
EJEMPLO DE CÓMO USARLO:

from services.pili_orchestrator import get_pili_orchestrator

# Crear instancia que usa TUS servicios existentes
orchestrator = get_pili_orchestrator()

# Ver estado de TUS servicios
print(orchestrator.obtener_estado())

# Procesar cotización usando TODO TU STACK existente
resultado = await orchestrator.procesar_cotizacion_completa(
    descripcion="Instalación casa 120m²",
    cliente="Juan Pérez",
    tipo_salida="word"  # usa TU word_generator.py
)

# Chat usando TU gemini_service.py
chat = await orchestrator.chat_inteligente(
    mensaje="¿Cuánto cuesta instalar 10 puntos de luz?"
)
"""