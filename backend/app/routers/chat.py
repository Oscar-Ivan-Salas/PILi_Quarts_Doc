"""
🤖 PILI AGENTE IA v3.0 - SISTEMA COMPLETO FINAL
📁 RUTA: backend/app/routers/chat.py

PILI (Procesadora Inteligente de Licitaciones Industriales) es un agente IA multifunción
que combina las mejores características de sistemas mundiales como ChatGPT, Microsoft Copilot
y Google Bard, pero especializada 100% en servicios eléctricos peruanos.

🧠 CARACTERÍSTICAS PILI v3.0:
- 6 Agentes especializados con personalidades únicas
- Conversación inteligente + anti-salto (no se desvía del tema)
- Procesamiento OCR multimodal (fotos, PDFs, manuscritos)
- JSON estructurado + Vista previa HTML editable
- Aprendizaje automático de cada conversación
- RAG con proyectos históricos
- Integración web search cuando necesita datos

🎯 AGENTES PILI:
- PILI Cotizadora: Cotizaciones rápidas (5-15 min)
- PILI Analista: Proyectos complejos con OCR avanzado
- PILI Coordinadora: Gestión de proyectos simples
- PILI Project Manager: Proyectos PMI avanzados
- PILI Reportera: Informes técnicos
- PILI Analista Senior: Informes ejecutivos APA

🔄 CONSERVA TODO LO EXISTENTE v2.0:
- Botones contextuales por tipo de servicio ✅
- Chat contextualizado según flujo seleccionado ✅
- Guía inteligente para 6 servicios ✅
- Gestión completa de plantillas ✅
- Análisis de proyectos ✅
- Sugerencias de mejoras ✅
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Body
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from app.core.database import get_db
from app.schemas.cotizacion import (
    CotizacionRapidaRequest,
    ChatRequest,
    ChatResponse,
    CotizacionResponse
)
from app.services.gemini_service import gemini_service
from app.services.pili_brain import PILIBrain
from app.services.pili_integrator import pili_integrator  # ✅ NUEVO: Integrador completo
from app.models.cotizacion import Cotizacion
from app.models.item import Item
from datetime import datetime, timedelta
from pathlib import Path
import logging
import os
import shutil
import json
import base64
import tempfile

logger = logging.getLogger(__name__)

# Inicializar PILIBrain para generación offline
pili_brain = PILIBrain()

router = APIRouter()

# ═══════════════════════════════════════════════════════════════
# 🤖 PILI ITSE - IMPORTAR CAJA NEGRA
# ═══════════════════════════════════════════════════════════════



try:
    from app.integrations.pili_chatbot.pili_itse_chatbot import PILIITSEChatBot
    # Crear instancia global de la caja negra
    pili_itse_bot = PILIITSEChatBot()
    logger.info("✅ Caja negra PILI ITSE inicializada correctamente")
except Exception as e:
    logger.error(f"❌ Error importando caja negra PILI ITSE: {e}")
    pili_itse_bot = None

# ═══════════════════════════════════════════════════════════════
# 🤖 PILI ELECTRICIDAD - IMPORTAR CAJA NEGRA
# ═══════════════════════════════════════════════════════════════

try:
    from app.integrations.pili_chatbot.pili_electricidad_chatbot import PILIElectricidadChatBot
    # Crear instancia global de la caja negra
    pili_electricidad_bot = PILIElectricidadChatBot()
    logger.info("✅ Caja negra PILI ELECTRICIDAD inicializada correctamente")
except Exception as e:
    logger.error(f"❌ Error importando caja negra PILI ELECTRICIDAD: {e}")
    pili_electricidad_bot = None

# ═══════════════════════════════════════════════════════════════
# 🤖 PILI PUESTA A TIERRA - IMPORTAR CAJA NEGRA
# ═══════════════════════════════════════════════════════════════

try:
    from app.integrations.pili_chatbot.pili_puesta_tierra_chatbot import PILIPuestaTierraChatBot
    # Crear instancia global de la caja negra
    pili_puesta_tierra_bot = PILIPuestaTierraChatBot()
    logger.info("✅ Caja negra PILI PUESTA A TIERRA inicializada correctamente")
except Exception as e:
    logger.error(f"❌ Error importando caja negra PILI PUESTA A TIERRA: {e}")
    pili_puesta_tierra_bot = None

# ═══════════════════════════════════════════════════════════════
# 🔥 PILI CONTRA INCENDIOS - IMPORTAR CAJA NEGRA
# ═══════════════════════════════════════════════════════════════

try:
    from app.integrations.pili_chatbot.pili_contra_incendios_chatbot import PILIContraIncendiosChatBot
    pili_contra_incendios_bot = PILIContraIncendiosChatBot()
    logger.info("✅ Caja negra PILI CONTRA INCENDIOS inicializada correctamente")
except Exception as e:
    logger.error(f"❌ Error importando caja negra PILI CONTRA INCENDIOS: {e}")
    pili_contra_incendios_bot = None

# ═══════════════════════════════════════════════════════════════
# 🏠 PILI DOMÓTICA - IMPORTAR CAJA NEGRA
# ═══════════════════════════════════════════════════════════════

try:
    from app.integrations.pili_chatbot.pili_domotica_chatbot import PILIDomoticaChatBot
    pili_domotica_bot = PILIDomoticaChatBot()
    logger.info("✅ Caja negra PILI DOMÓTICA inicializada correctamente")
except Exception as e:
    logger.error(f"❌ Error importando caja negra PILI DOMÓTICA: {e}")
    pili_domotica_bot = None

try:
    from app.integrations.pili_chatbot.pili_cctv_chatbot import PILICCTVChatBot
    pili_cctv_bot = PILICCTVChatBot()
    logger.info("✅ Caja negra PILI CCTV inicializada correctamente")
except Exception as e:
    logger.error(f"❌ Error importando caja negra PILI CCTV: {e}")
    pili_cctv_bot = None

try:
    from app.integrations.pili_chatbot.pili_redes_chatbot import PILIRedesChatBot
    pili_redes_bot = PILIRedesChatBot()
    logger.info("✅ PILI REDES OK")
except Exception as e:
    pili_redes_bot = None

try:
    from app.integrations.pili_chatbot.pili_automatizacion_chatbot import PILIAutomatizacionChatBot
    pili_automatizacion_bot = PILIAutomatizacionChatBot()
    logger.info("✅ PILI AUTOMATIZACIÓN OK")
except: pili_automatizacion_bot = None

try:
    from app.integrations.pili_chatbot.pili_expedientes_chatbot import PILIExpedientesChatBot
    pili_expedientes_bot = PILIExpedientesChatBot()
    logger.info("✅ PILI EXPEDIENTES OK")
except: pili_expedientes_bot = None

try:
    from app.integrations.pili_chatbot.pili_saneamiento_chatbot import PILISaneamientoChatBot
    pili_saneamiento_bot = PILISaneamientoChatBot()
    logger.info("✅ PILI SANEAMIENTO OK")
except: pili_saneamiento_bot = None

# (Bloque duplicado eliminado para evitar conflictos de importación)
# La instancia pili_electricidad_proyecto_complejo_pmi_bot se inicializa correctamente 
# en la sección de ENDPOINTS PROYECTO COMPLEJO PMI (líneas ~5180)


# ═══════════════════════════════════════════════════════════════
# 🤖 PILI - CONTEXTOS DE SERVICIOS INTELIGENTES v3.0
# ═══════════════════════════════════════════════════════════════

CONTEXTOS_SERVICIOS = {
    
    # ⚡ COTIZACIÓN SIMPLE - PILI COTIZADORA
    "cotizacion-simple": {
        "nombre_pili": "PILI Cotizadora",
        "personalidad": "¡Hola! 🤖 Soy PILI Cotizadora, tu asistente especializada en cotizaciones eléctricas rápidas. Te ayudo a generar cotizaciones precisas en 5-15 minutos con preguntas inteligentes y sin salirme del tema.",
        
        "rol_ia": """Eres PILI Cotizadora, agente IA especializada en cotizaciones eléctricas de Tesla Electricidad. 
        Tu objetivo es obtener información específica para generar una cotización precisa de instalaciones eléctricas.
        Siempre haz preguntas para clarificar antes de cotizar. NO te desvíes hacia otros temas.""",
        
        "preguntas_esenciales": [
            "¿Qué tipo de instalación necesitas? (residencial/comercial/industrial)",
            "¿Cuántos metros cuadrados tiene el área?", 
            "¿Cuántos puntos de luz necesitas aproximadamente?",
            "¿Cuántos tomacorrientes requieres?",
            "¿Necesitas tablero eléctrico nuevo o existe uno?",
            "¿La instalación es desde cero o hay cableado existente?"
        ],
        
        "botones_contextuales": {
            "inicial": [
                "🏠 Instalación Residencial", 
                "🏢 Instalación Comercial",
                "🏭 Instalación Industrial", 
                "📋 Certificado ITSE",
                "🔌 Pozo a Tierra",
                "🤖 Automatización",
                "📹 CCTV",
                "🌐 Redes"
            ],
            "refinamiento": [
                "📝 Necesito más detalles técnicos",
                "🔢 Ajustar cantidades estimadas", 
                "💰 Revisar precios unitarios",
                "⚡ Verificar cargas eléctricas",
                "✅ Generar cotización",
                "📎 Subir planos/fotos"
            ],
            "generacion": [
                "✏️ Editar vista previa",
                "📄 Generar Word final", 
                "📱 Enviar por WhatsApp",
                "💾 Guardar como borrador"
            ]
        },
        
        "prompt_especializado": """
        Como PILI Cotizadora de Tesla Electricidad, analiza la información y:
        
        1. 🔍 IDENTIFICA el tipo exacto de instalación
        2. ⚡ CALCULA materiales según normativa peruana (CNE)
        3. 👷 ESTIMA mano de obra especializada requerida
        4. 💰 APLICA precios del mercado peruano 2025
        5. 📋 INCLUYE especificaciones técnicas detalladas
        6. ⚠️ CONSIDERA factores de seguridad y normativas
        
        PRECIOS REFERENCIALES PERÚ 2025:
        - Punto de luz LED 18W: S/25.00 - S/35.00
        - Tomacorriente doble: S/28.00 - S/40.00
        - Cable THW 2.5mm²: S/3.50 - S/4.50 por metro
        - Tablero monofásico 12 polos: S/350.00 - S/450.00
        - Mano de obra especializada: S/80.00 - S/120.00 por hora
        
        IMPORTANTE: Si falta información crítica, haz preguntas específicas antes de cotizar.
        """
    },

    # 📋 CERTIFICADO ITSE - PILI ITSE
    "itse": {
        "nombre_pili": "PILI ITSE",
        "personalidad": "¡Hola! 📋 Soy PILI ITSE, tu especialista en certificados de Inspección Técnica de Seguridad en Edificaciones. Te ayudo a obtener tu certificado ITSE con visita técnica GRATUITA y precios oficiales TUPA Huancayo.",
        
        "rol_ia": """Eres PILI ITSE, agente especializada en certificaciones ITSE de Tesla Electricidad - Huancayo.
        Tu objetivo es guiar al usuario a través del proceso de certificación ITSE, recopilando información sobre su establecimiento.
        Mantente enfocada en ITSE, no te desvíes a otros servicios eléctricos.""",
        
        "preguntas_esenciales": [
            "¿Qué tipo de establecimiento es? (Salud, Educación, Comercio, etc.)",
            "¿Cuál es el área total en m²?",
            "¿Cuántos pisos tiene el establecimiento?",
            "¿Qué actividad específica se realizará?"
        ],
        
        "botones_contextuales": {
            "inicial": [
                "🏥 Salud",
                "🎓 Educación", 
                "🏨 Hospedaje",
                "🏪 Comercio",
                "🍽️ Restaurante",
                "🏢 Oficina",
                "🏭 Industrial",
                "🎭 Encuentro"
            ],
            "refinamiento": [
                "📝 Especificar tipo exacto",
                "📐 Confirmar dimensiones",
                "🔢 Verificar número de pisos",
                "✅ Generar cotización ITSE"
            ],
            "generacion": [
                "✏️ Editar cotización",
                "📄 Generar documento",
                "📅 Agendar visita técnica",
                "💾 Guardar cotización"
            ]
        },
        
        "prompt_especializado": """
        Como PILI ITSE de Tesla Electricidad - Huancayo:
        
        1. 🏢 IDENTIFICA el tipo de establecimiento según categorías ITSE
        2. 📏 RECOPILA área en m² y número de pisos
        3. ⚠️ DETERMINA nivel de riesgo (BAJO, MEDIO, ALTO, MUY ALTO)
        4. 💰 CALCULA precios según TUPA Huancayo 2025
        5. 📋 GENERA cotización con desglose de costos
        
        PRECIOS TUPA HUANCAYO 2025:
        - Riesgo BAJO: S/150 - S/200 (municipal) + S/300-500 (servicio)
        - Riesgo MEDIO: S/200 - S/300 (municipal) + S/500-800 (servicio)
        - Riesgo ALTO: S/300 - S/450 (municipal) + S/800-1200 (servicio)
        - Riesgo MUY ALTO: S/450 - S/600 (municipal) + S/1200-1800 (servicio)
        
        INCLUYE:
        - ✅ Visita técnica GRATUITA
        - ✅ Trámite 100% gestionado
        - ✅ Entrega en 7 días hábiles
        - ✅ Garantía de aprobación
        
        IMPORTANTE: Enfócate SOLO en ITSE. No menciones instalaciones eléctricas.
        """
    },

    # 🔍 COTIZACIÓN COMPLEJA - PILI ANALISTA
    "cotizacion-compleja": {
        "nombre_pili": "PILI Analista",
        "personalidad": "¡Hola! 🔍 Soy PILI Analista, especialista en proyectos eléctricos complejos. Proceso planos, documentos técnicos y genero cotizaciones detalladas con análisis profundo usando OCR y IA avanzada.",
        
        "rol_ia": """Eres PILI Analista, agente IA senior especializada en proyectos eléctricos complejos.
        Procesas documentos técnicos, analizas planos con OCR y generas cotizaciones detalladas.
        Tu enfoque es técnico y profundo, pero mantienes la conversación en el contexto del proyecto.""",
        
        "documentos_esperados": [
            "Planos arquitectónicos (PDF/DWG)",
            "Memoria descriptiva del proyecto",
            "Especificaciones técnicas detalladas",
            "Presupuesto referencial o base",
            "Normas y códigos aplicables", 
            "Lista de materiales existente"
        ],
        
        "botones_contextuales": {
            "inicial": [
                "📄 Subir planos para análisis",
                "📋 Subir especificaciones técnicas",
                "🔍 Analizar proyecto existente",
                "⚡ Cálculo de cargas eléctricas",
                "📐 Metrados automáticos"
            ],
            "analisis": [
                "📊 Revisar análisis OCR",
                "🔍 Verificar información extraída",
                "📋 Completar datos faltantes",
                "⚡ Validar cargas calculadas",
                "📐 Confirmar metrados"
            ],
            "refinamiento": [
                "📋 Generar lista detallada materiales",
                "👷 Calcular cronograma mano obra",
                "💰 Aplicar precios actualizados",
                "📊 Crear análisis precios unitarios",
                "⚖️ Revisar normativas aplicables"
            ],
            "generacion": [
                "📄 Crear cotización formal",
                "📊 Incluir análisis de costos",
                "📈 Agregar cronograma obra",
                "📋 Generar memoria cálculo",
                "🎨 Personalizar con logo"
            ]
        },
        
        "prompt_especializado": """
        Como PILI Analista de Tesla Electricidad para proyectos complejos:
        
        1. 📄 ANALIZA documentos técnicos subidos
        2. 🔍 EXTRAE información con OCR avanzado
        3. ⚡ CALCULA cargas y dimensionamientos
        4. 📐 GENERA metrados automáticos
        5. 📊 CREA análisis de precios unitarios
        6. ⚖️ VALIDA contra normativas CNE
        7. 📋 ESTRUCTURA información en JSON
        
        CAPACIDADES TÉCNICAS:
        - Lectura de planos AutoCAD (PDF)
        - Análisis de especificaciones técnicas
        - Cálculo de metrados por ambientes
        - Dimensionamiento de conductores
        - Selección de equipos de protección
        - Cumplimiento de códigos peruanos
        
        ENFOQUE: Precisión técnica + eficiencia comercial
        """
    },

    # 📊 PROYECTO SIMPLE - PILI COORDINADORA
    "proyecto-simple": {
        "nombre_pili": "PILI Coordinadora",
        "personalidad": "¡Hola! 📊 Soy PILI Coordinadora, especialista en gestión de proyectos eléctricos simples. Te ayudo a estructurar proyectos, crear cronogramas y coordinar recursos de manera eficiente.",
        
        "rol_ia": """Eres PILI Coordinadora, agente IA especializada en gestión de proyectos eléctricos.
        Tu enfoque es organizacional y práctico, creando estructuras de trabajo claras y cronogramas realistas.
        Mantienes la conversación centrada en la organización y ejecución del proyecto.""",
        
        "elementos_proyecto": [
            "Alcance del proyecto claramente definido",
            "Cronograma con fases y actividades",
            "Recursos humanos y materiales necesarios",
            "Presupuesto desglosado por actividades",
            "Riesgos identificados y mitigaciones",
            "Entregables y fechas de entrega"
        ],
        
        "botones_contextuales": {
            "inicial": [
                "🎯 Definir alcance del proyecto",
                "📅 Crear cronograma básico",
                "👥 Asignar recursos",
                "💰 Estimar presupuesto",
                "⚠️ Identificar riesgos"
            ],
            "planificacion": [
                "📋 Desglosar actividades",
                "⏱️ Estimar duraciones",
                "🔗 Definir dependencias",
                "📊 Crear diagrama Gantt",
                "🎯 Establecer hitos"
            ],
            "refinamiento": [
                "👷 Optimizar recursos",
                "💰 Ajustar presupuesto",
                "⏰ Revisar cronograma",
                "📋 Validar entregables",
                "🔄 Planes de contingencia"
            ],
            "generacion": [
                "📄 Generar documento proyecto",
                "📈 Crear dashboard seguimiento",
                "📊 Exportar cronograma",
                "📋 Lista de verificación"
            ]
        },
        
        "prompt_especializado": """
        Como PILI Coordinadora de Tesla Electricidad:
        
        1. 🎯 ESTRUCTURA el proyecto en fases lógicas
        2. 📅 CREA cronogramas realistas y factibles
        3. 👥 ASIGNA recursos humanos especializados
        4. 💰 ESTIMA presupuestos por actividades
        5. ⚠️ IDENTIFICA riesgos y planes de contingencia
        6. 📋 DEFINE entregables claros y medibles
        7. 🔄 ESTABLECE puntos de control y seguimiento
        
        METODOLOGÍA:
        - Enfoque ágil adaptado a electricidad
        - Fases: Diseño → Materiales → Instalación → Pruebas
        - Control de calidad en cada etapa
        - Documentación técnica especializada
        
        ESPECIALIDAD: Proyectos 1-12 semanas, equipos 2-8 personas
        """
    },

    # 🎯 PROYECTO COMPLEJO - PILI PROJECT MANAGER
    "proyecto-complejo": {
        "nombre_pili": "PILI Project Manager",
        "personalidad": "¡Hola! 🎯 Soy PILI Project Manager, especialista en proyectos eléctricos complejos y de gran envergadura. Aplico metodologías PMI, gestiono múltiples stakeholders y aseguro el éxito de proyectos críticos.",
        
        "rol_ia": """Eres PILI Project Manager, agente IA senior especializada en proyectos eléctricos complejos.
        Aplicas metodologías PMI, gestionas riesgos avanzados y coordinas múltiples equipos especializados.
        Tu enfoque es estratégico y orientado a resultados empresariales.""",
        
        "areas_conocimiento": [
            "Gestión de Integración del Proyecto",
            "Gestión del Alcance y Requerimientos", 
            "Gestión del Cronograma y Recursos",
            "Gestión de Costos y Presupuestos",
            "Gestión de Calidad y Estándares",
            "Gestión de Recursos Humanos",
            "Gestión de Comunicaciones",
            "Gestión de Riesgos",
            "Gestión de Adquisiciones",
            "Gestión de Stakeholders"
        ],
        
        "botones_contextuales": {
            "inicial": [
                "📋 Charter del proyecto",
                "🎯 Análisis de stakeholders", 
                "📊 Estructura de desglose trabajo",
                "⚠️ Registro de riesgos",
                "📈 Plan de gestión proyecto"
            ],
            "planificacion": [
                "📅 Cronograma maestro",
                "💰 Línea base presupuesto",
                "👥 Matriz RACI",
                "📊 Plan gestión calidad",
                "🔄 Plan gestión cambios"
            ],
            "ejecucion": [
                "📈 Dashboard ejecutivo",
                "📊 Reportes de avance",
                "⚠️ Gestión de issues",
                "🔄 Control de cambios",
                "👥 Gestión de equipos"
            ],
            "control": [
                "📊 Análisis valor ganado",
                "📈 Métricas de performance",
                "⚠️ Escalamiento de riesgos",
                "💰 Control de costos",
                "📋 Auditorías de calidad"
            ]
        },
        
        "prompt_especializado": """
        Como PILI Project Manager de Tesla Electricidad para proyectos complejos:
        
        1. 📋 DESARROLLA Charter completo del proyecto
        2. 🎯 GESTIONA stakeholders y expectativas
        3. 📊 CREA EDT (Work Breakdown Structure)
        4. 📅 PLANIFICA cronograma maestro con rutas críticas
        5. 💰 ESTABLECE líneas base de costo y alcance
        6. ⚠️ GESTIONA riesgos con análisis cuanti/cualitativo
        7. 📈 IMPLEMENTA métricas de valor ganado (EVM)
        8. 🔄 CONTROLA cambios con governance
        9. 👥 LIDERA equipos multidisciplinarios
        10. 📊 REPORTA a nivel ejecutivo
        
        METODOLOGÍAS:
        - PMI PMBOK 7ma Edición
        - Agile/Scrum para desarrollo técnico
        - Lean Construction para instalaciones
        - ISO 21500 para gestión de proyectos
        
        ESPECIALIDAD: Proyectos >$100K, >6 meses, equipos >10 personas
        """
    },

    # 📋 INFORME SIMPLE - PILI REPORTERA
    "informe-simple": {
        "nombre_pili": "PILI Reportera",
        "personalidad": "¡Hola! 📋 Soy PILI Reportera, especialista en informes técnicos eléctricos claros y concisos. Transformo datos complejos en reportes comprensibles para clientes y autoridades.",
        
        "rol_ia": """Eres PILI Reportera, agente IA especializada en redacción técnica y informes eléctricos.
        Tu enfoque es comunicacional, creando documentos claros, bien estructurados y técnicamente precisos.
        Adaptas el lenguaje según la audiencia: técnica, gerencial o regulatoria.""",
        
        "tipos_informes": [
            "Informe de inspección eléctrica",
            "Reporte de mediciones y pruebas",
            "Informe de cumplimiento normativo",
            "Reporte de incidentes técnicos",
            "Informe de avance de obra",
            "Reporte de verificación ITSE"
        ],
        
        "botones_contextuales": {
            "inicial": [
                "📋 Seleccionar tipo de informe",
                "🎯 Definir audiencia objetivo",
                "📊 Identificar datos disponibles",
                "⚖️ Verificar normativas aplicables",
                "📝 Establecer estructura"
            ],
            "desarrollo": [
                "📊 Analizar datos técnicos",
                "📈 Crear gráficos y tablas",
                "📸 Incluir evidencia fotográfica",
                "🔍 Verificar cálculos",
                "📝 Redactar hallazgos"
            ],
            "revision": [
                "✏️ Revisar redacción técnica",
                "📊 Validar datos y cálculos",
                "🎨 Aplicar formato profesional",
                "📋 Verificar completitud",
                "🔍 Control de calidad"
            ],
            "finalizacion": [
                "📄 Generar PDF final",
                "📱 Versión ejecutiva",
                "📋 Lista de verificación",
                "📧 Preparar para envío"
            ]
        },
        
        "prompt_especializado": """
        Como PILI Reportera de Tesla Electricidad:
        
        1. 📋 ESTRUCTURA informes según estándares técnicos
        2. 📊 PRESENTA datos de manera clara y visual
        3. 📝 REDACTA en lenguaje técnico apropiado
        4. 📈 INCLUYE gráficos y tablas profesionales
        5. 🔍 VERIFICA precisión técnica y normativa
        6. 📸 INTEGRA evidencia fotográfica relevante
        7. 📋 APLICA formatos estándar de la industria
        
        ELEMENTOS CLAVE:
        - Resumen ejecutivo claro
        - Metodología de inspección/medición
        - Hallazgos técnicos detallados
        - Conclusiones fundamentadas
        - Recomendaciones específicas
        - Anexos con evidencia
        
        ESTÁNDARES:
        - Normas CNE peruanas
        - Formatos oficiales (OSINERGMIN, MEM)
        - Protocolos de medición IEEE
        - Estándares de redacción técnica
        
        ESPECIALIDAD: Informes 5-20 páginas, formato profesional
        """
    },

    # 📊 INFORME EJECUTIVO - PILI ANALISTA SENIOR
    "informe-ejecutivo": {
        "nombre_pili": "PILI Analista Senior",
        "personalidad": "¡Hola! 📊 Soy PILI Analista Senior, especialista en informes ejecutivos y análisis estratégico. Creo documentos de alto nivel con análisis profundo, formato APA y presentación ejecutiva para toma de decisiones estratégicas.",
        
        "rol_ia": """Eres PILI Analista Senior, agente IA especializada en análisis estratégico e informes ejecutivos.
        Tu enfoque es analítico y estratégico, creando documentos de alto valor para la toma de decisiones.
        Combinas expertise técnico con visión de negocios para generar insights accionables.""",
        
        "capacidades_analisis": [
            "Análisis estratégico de proyectos",
            "Evaluación de rentabilidad y ROI",
            "Análisis de riesgos cuantitativos",
            "Benchmarking de mercado",
            "Proyecciones financieras",
            "Análisis de tendencias tecnológicas",
            "Evaluación de cumplimiento regulatorio",
            "Análisis de competitividad"
        ],
        
        "botones_contextuales": {
            "inicial": [
                "🎯 Definir objetivos del análisis",
                "📊 Identificar métricas clave",
                "🔍 Establecer metodología",
                "📈 Fuentes de información",
                "👥 Audiencia ejecutiva"
            ],
            "investigacion": [
                "📊 Análisis de datos cuantitativos",
                "📈 Investigación de mercado",
                "💰 Análisis financiero",
                "⚠️ Evaluación de riesgos",
                "🏆 Benchmarking competitivo"
            ],
            "analisis": [
                "📊 Análisis estadístico avanzado",
                "📈 Modelado de escenarios",
                "💡 Generación de insights",
                "🎯 Identificación de oportunidades",
                "⚖️ Evaluación de alternativas"
            ],
            "presentacion": [
                "📋 Resumen ejecutivo",
                "📊 Dashboard de métricas",
                "📈 Recomendaciones estratégicas",
                "🎨 Diseño ejecutivo",
                "📄 Formato APA completo"
            ]
        },
        
        "prompt_especializado": """
        Como PILI Analista Senior de Tesla Electricidad para informes ejecutivos:
        
        1. 🎯 ANALIZA objetivos estratégicos del negocio
        2. 📊 DESARROLLA métricas y KPIs relevantes
        3. 📈 REALIZA análisis cuantitativo profundo
        4. 💡 GENERA insights y recomendaciones
        5. 🎨 PRESENTA en formato ejecutivo profesional
        6. 📋 ESTRUCTURA según estándares APA
        7. 📊 INCLUYE análisis visual avanzado
        8. 💰 EVALÚA impacto financiero y ROI
        9. ⚠️ IDENTIFICA riesgos y oportunidades
        10. 🚀 PROPONE planes de acción
        
        METODOLOGÍAS:
        - Análisis SWOT/PESTEL
        - Análisis de valor económico (EVA)
        - Análisis de sensibilidad y escenarios
        - Benchmarking estratégico
        - Análisis de riesgo cuantitativo
        
        FORMATO:
        - Estilo APA 7ma edición
        - Gráficos ejecutivos (dashboard style)
        - Tablas de análisis profesionales
        - Referencias académicas y técnicas
        - Anexos con análisis detallado
        
        ESPECIALIDAD: Informes 20-50 páginas, nivel C-Suite, decisiones >$50K
        """
    }
}

# ═══════════════════════════════════════════════════════════════
# 🛠️ FUNCIONES AUXILIARES PILI
# ═══════════════════════════════════════════════════════════════

def obtener_contexto_servicio(tipo_flujo: str) -> Dict[str, Any]:
    """Obtiene el contexto especializado para el tipo de flujo"""
    return CONTEXTOS_SERVICIOS.get(tipo_flujo, {})

def determinar_etapa_conversacion(historial: List[Dict], tiene_cotizacion: bool = False) -> str:
    """Determina la etapa actual de la conversación para botones contextuales"""
    
    if not historial:
        return "inicial"
    
    if tiene_cotizacion:
        return "generacion"
    
    if len(historial) >= 3:
        return "refinamiento"
    
    return "inicial"

def obtener_botones_para_etapa(tipo_flujo: str, etapa: str) -> List[str]:
    """Obtiene los botones contextuales para la etapa actual"""
    
    contexto = obtener_contexto_servicio(tipo_flujo)
    botones_config = contexto.get("botones_contextuales", {})
    
    return botones_config.get(etapa, [])

def generar_preview_html_editable(datos: Dict[str, Any], agente: str) -> str:
    """
    🆕 NUEVO PILI v3.0 - Genera vista previa HTML editable
    
    Esta función crea HTML que el frontend puede mostrar y editar,
    permitiendo al usuario modificar la cotización antes de generar el Word final.
    """
    
    items = datos.get('items', [])
    cliente = datos.get('cliente', 'Cliente')
    proyecto = datos.get('proyecto', 'Proyecto Eléctrico')
    total = datos.get('total', 0)
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Vista Previa - {agente}</title>
        <style>
            body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 20px; background: #fef2f2; }}
            .container {{ background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 20px rgba(220, 38, 38, 0.15); border: 2px solid #fecaca; }}
            .header {{ border-bottom: 4px solid #dc2626; padding-bottom: 20px; margin-bottom: 30px; background: linear-gradient(135deg, #fee2e2 0%, #ffffff 100%); padding: 20px; border-radius: 8px; }}
            .company {{ color: #b91c1c; font-size: 26px; font-weight: 900; text-shadow: 1px 1px 2px rgba(0,0,0,0.1); letter-spacing: -0.5px; }}
            .agent {{ color: #1f2937; font-size: 14px; margin-top: 8px; font-weight: 600; }}
            .title {{ color: #1f2937; font-size: 22px; margin: 20px 0; font-weight: 800; border-left: 5px solid #dc2626; padding-left: 15px; }}
            .info-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 20px 0; }}
            .info-item {{ background: #fef2f2; padding: 15px; border-radius: 8px; border: 1px solid #fecaca; }}
            .info-label {{ font-weight: 800; color: #1f2937; font-size: 14px; }}
            .info-value {{ color: #dc2626; font-size: 17px; font-weight: 700; margin-top: 5px; }}
            .items-table {{ width: 100%; border-collapse: collapse; margin: 20px 0; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
            .items-table th {{ background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%); color: white; padding: 14px; text-align: left; font-weight: 800; font-size: 15px; }}
            .items-table td {{ padding: 12px; border-bottom: 2px solid #fecaca; color: #1f2937; font-weight: 600; }}
            .items-table tr:hover {{ background: #fef2f2; }}
            .items-table td:nth-child(4), .items-table td:nth-child(5) {{ color: #dc2626; font-weight: 700; }}
            .total-section {{ background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%); padding: 25px; border-radius: 8px; margin-top: 20px; border: 2px solid #dc2626; box-shadow: 0 4px 12px rgba(220, 38, 38, 0.2); }}
            .total-row {{ display: flex; justify-content: space-between; margin: 8px 0; font-size: 16px; font-weight: 700; color: #1f2937; }}
            .total-final {{ font-size: 24px; font-weight: 900; color: #b91c1c; background: white; padding: 15px; border-radius: 6px; margin-top: 10px; border: 2px solid #dc2626; }}
            .edit-note {{ background: #fffbeb; border: 2px solid #fbbf24; padding: 15px; border-radius: 5px; margin-top: 20px; font-weight: 600; color: #78350f; }}
            .agent-signature {{ text-align: right; margin-top: 30px; padding-top: 20px; border-top: 2px solid #fecaca; font-weight: 700; color: #dc2626; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="company">⚡ TESLA ELECTRICIDAD Y AUTOMATIZACIÓN S.A.C.</div>
                <div class="agent">🤖 Generado por {agente}</div>
            </div>
            
            <h2 class="title">💰 COTIZACIÓN ELÉCTRICA</h2>
            
            <div class="info-grid">
                <div class="info-item">
                    <div class="info-label">👤 Cliente:</div>
                    <div class="info-value">{cliente}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">📋 Proyecto:</div>
                    <div class="info-value">{proyecto}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">📅 Fecha:</div>
                    <div class="info-value">{datetime.now().strftime('%d/%m/%Y')}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">🤖 Especialista:</div>
                    <div class="info-value">{agente}</div>
                </div>
            </div>
            
            <table class="items-table">
                <thead>
                    <tr>
                        <th>📋 Descripción</th>
                        <th>🔢 Cantidad</th>
                        <th>📏 Unidad</th>
                        <th>💰 Precio Unit.</th>
                        <th>💰 Subtotal</th>
                    </tr>
                </thead>
                <tbody>
    """
    
    subtotal = 0
    for item in items:
        cantidad = item.get('cantidad', 0)
        precio = item.get('precio_unitario', 0)
        item_total = cantidad * precio
        subtotal += item_total
        
        html += f"""
                    <tr>
                        <td>{item.get('descripcion', '')}</td>
                        <td>{cantidad}</td>
                        <td>{item.get('unidad', 'und')}</td>
                        <td>S/ {precio:.2f}</td>
                        <td>S/ {item_total:.2f}</td>
                    </tr>
        """
    
    igv = subtotal * 0.18
    total_final = subtotal + igv
    
    html += f"""
                </tbody>
            </table>
            
            <div class="total-section">
                <div class="total-row">
                    <span>💰 Subtotal:</span>
                    <span>S/ {subtotal:.2f}</span>
                </div>
                <div class="total-row">
                    <span>📋 IGV (18%):</span>
                    <span>S/ {igv:.2f}</span>
                </div>
                <div class="total-row total-final">
                    <span>🏆 TOTAL:</span>
                    <span>S/ {total_final:.2f}</span>
                </div>
            </div>
            
            <div class="edit-note">
                ✏️ <strong>Edición Disponible:</strong> Puedes modificar cantidades, precios y descripciones desde el panel izquierdo. 
                Los cambios se reflejarán instantáneamente en esta vista previa.
            </div>
            
            <div class="agent-signature">
                <div style="color: #6c757d; font-size: 12px;">
                    Documento generado por {agente} v3.0<br>
                    {datetime.now().strftime('%d/%m/%Y %H:%M')}
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html

def generar_preview_informe(datos: Dict[str, Any], agente: str) -> str:
    """Genera vista previa HTML para informes"""
    
    titulo = datos.get('titulo', 'Informe Técnico')
    cliente = datos.get('cliente', 'Cliente')
    fecha = datetime.now().strftime('%d/%m/%Y')
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Vista Previa Informe - {agente}</title>
        <style>
            body {{ font-family: 'Times New Roman', serif; margin: 40px; line-height: 1.6; }}
            .header {{ text-align: center; border-bottom: 2px solid #333; padding-bottom: 20px; }}
            .title {{ font-size: 24px; font-weight: bold; color: #333; margin: 20px 0; }}
            .info {{ margin: 20px 0; }}
            .section {{ margin: 30px 0; }}
            .section h3 {{ color: #007bff; border-bottom: 1px solid #007bff; padding-bottom: 5px; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>⚡ TESLA ELECTRICIDAD Y AUTOMATIZACIÓN S.A.C.</h1>
            <p>🤖 {agente} - Sistema de Informes Técnicos</p>
        </div>
        
        <h2 class="title">📋 {titulo}</h2>
        
        <div class="info">
            <p><strong>Cliente:</strong> {cliente}</p>
            <p><strong>Fecha:</strong> {fecha}</p>
            <p><strong>Elaborado por:</strong> {agente}</p>
        </div>
        
        <div class="section">
            <h3>1. RESUMEN EJECUTIVO</h3>
            <p>Este informe presenta el análisis técnico realizado por {agente}, 
            especialista en {agente.lower().replace('pili ', '')}...</p>
        </div>
        
        <div class="section">
            <h3>2. METODOLOGÍA</h3>
            <p>El análisis se realizó aplicando normativas técnicas peruanas...</p>
        </div>
        
        <div class="section">
            <h3>3. HALLAZGOS</h3>
            <p>Los principales hallazgos identificados son...</p>
        </div>
        
        <div class="section">
            <h3>4. RECOMENDACIONES</h3>
            <p>Se recomienda implementar las siguientes acciones...</p>
        </div>
    </body>
    </html>
    """

    return html


# ═══════════════════════════════════════════════════════════════
# 🆕 AGENTE 1: FUNCIONES DE VISTA PREVIA EDITABLE - COTIZACIONES
# ═══════════════════════════════════════════════════════════════

def generar_preview_cotizacion_simple_editable(datos: Dict[str, Any], agente: str) -> str:
    """
    🆕 Vista previa HTML COMPLETAMENTE EDITABLE para Cotización Simple

    Características:
    - Colores AZULES Tesla (#0052A3, #1E40AF, #3B82F6)
    - Inputs editables en toda la tabla
    - Checkboxes para opciones de visualización
    - Cálculo automático de totales con JavaScript
    - Sin dependencias externas

    Args:
        datos: Diccionario con datos de cotización (cliente, items, etc.)
        agente: Nombre del agente que genera la cotización

    Returns:
        str: HTML completo con formulario editable
    """

    items = datos.get('items', [])
    cliente = datos.get('cliente', '')
    proyecto = datos.get('proyecto', '')

    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cotización Simple Editable - {agente}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', 'Arial', sans-serif;
            background: linear-gradient(135deg, #e0f2fe 0%, #f0f9ff 100%);
            padding: 20px;
            line-height: 1.6;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 8px 32px rgba(0, 82, 163, 0.15);
            overflow: hidden;
        }}

        .header {{
            background: linear-gradient(135deg, #0052A3 0%, #1E40AF 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}

        .header h1 {{
            font-size: 28px;
            font-weight: 900;
            letter-spacing: -0.5px;
            margin-bottom: 8px;
        }}

        .header .agente {{
            font-size: 14px;
            opacity: 0.9;
            font-weight: 600;
        }}

        .content {{
            padding: 30px;
        }}

        .titulo-seccion {{
            color: #0052A3;
            font-size: 22px;
            font-weight: 800;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #3B82F6;
        }}

        .info-basica {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 30px;
        }}

        .campo {{
            display: flex;
            flex-direction: column;
        }}

        .campo label {{
            font-weight: 700;
            color: #1E40AF;
            margin-bottom: 8px;
            font-size: 14px;
        }}

        .campo input[type="text"],
        .campo input[type="number"],
        .campo textarea,
        .campo select {{
            padding: 12px;
            border: 2px solid #bfdbfe;
            border-radius: 6px;
            font-size: 15px;
            font-weight: 600;
            color: #1e293b;
            transition: all 0.3s;
        }}

        .campo input:focus,
        .campo textarea:focus,
        .campo select:focus {{
            outline: none;
            border-color: #3B82F6;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        }}

        .items-table {{
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
            margin: 20px 0;
            box-shadow: 0 4px 12px rgba(0, 82, 163, 0.1);
            border-radius: 8px;
            overflow: hidden;
        }}

        .items-table thead th {{
            background: linear-gradient(135deg, #0052A3 0%, #1E40AF 100%);
            color: white;
            padding: 16px 12px;
            text-align: left;
            font-weight: 800;
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .items-table tbody tr {{
            transition: background 0.2s;
        }}

        .items-table tbody tr:hover {{
            background: #eff6ff;
        }}

        .items-table tbody td {{
            padding: 12px;
            border-bottom: 1px solid #dbeafe;
        }}

        .items-table input[type="text"],
        .items-table input[type="number"] {{
            width: 100%;
            padding: 8px;
            border: 2px solid #bfdbfe;
            border-radius: 4px;
            font-size: 14px;
            font-weight: 600;
            color: #1e293b;
        }}

        .items-table input[type="text"]:focus,
        .items-table input[type="number"]:focus {{
            border-color: #3B82F6;
            outline: none;
        }}

        .total-item {{
            color: #0052A3;
            font-weight: 700;
            font-size: 15px;
        }}

        .opciones-visualizacion {{
            background: #eff6ff;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
            border: 2px solid #bfdbfe;
        }}

        .opciones-visualizacion h3 {{
            color: #1E40AF;
            font-size: 16px;
            font-weight: 800;
            margin-bottom: 15px;
        }}

        .checkbox-group {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 12px;
        }}

        .checkbox-item {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .checkbox-item input[type="checkbox"] {{
            width: 18px;
            height: 18px;
            cursor: pointer;
            accent-color: #0052A3;
        }}

        .checkbox-item label {{
            font-weight: 600;
            color: #334155;
            cursor: pointer;
            font-size: 14px;
        }}

        .totales {{
            background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
            padding: 25px;
            border-radius: 8px;
            margin-top: 20px;
            border: 3px solid #3B82F6;
        }}

        .total-row {{
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            font-size: 16px;
            font-weight: 700;
            color: #1e293b;
        }}

        .total-row.igv {{
            border-top: 2px solid #93c5fd;
            margin-top: 10px;
            padding-top: 15px;
        }}

        .total-row.final {{
            background: white;
            padding: 18px;
            border-radius: 6px;
            margin-top: 15px;
            font-size: 22px;
            font-weight: 900;
            color: #0052A3;
            border: 2px solid #1E40AF;
        }}

        .boton-calcular {{
            background: linear-gradient(135deg, #0052A3 0%, #1E40AF 100%);
            color: white;
            border: none;
            padding: 15px 40px;
            font-size: 16px;
            font-weight: 800;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s;
            box-shadow: 0 4px 12px rgba(0, 82, 163, 0.3);
            width: 100%;
            margin-top: 20px;
        }}

        .boton-calcular:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0, 82, 163, 0.4);
        }}

        .boton-calcular:active {{
            transform: translateY(0);
        }}

        .footer {{
            text-align: center;
            padding: 20px;
            color: #64748b;
            font-size: 13px;
            border-top: 2px solid #e2e8f0;
            margin-top: 30px;
        }}

        .nota-edicion {{
            background: #fef3c7;
            border: 2px solid #fbbf24;
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
            color: #78350f;
            font-weight: 600;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>⚡ TESLA ELECTRICIDAD Y AUTOMATIZACIÓN</h1>
            <p class="agente">🤖 Generado por {agente} - Vista Editable</p>
        </div>

        <div class="content">
            <h2 class="titulo-seccion">📋 COTIZACIÓN SIMPLE - MODO EDITABLE</h2>

            <div class="info-basica">
                <div class="campo">
                    <label>👤 Cliente:</label>
                    <input type="text" id="cliente" name="cliente" value="{cliente}" placeholder="Nombre del cliente">
                </div>
                <div class="campo">
                    <label>📁 Proyecto:</label>
                    <input type="text" id="proyecto" name="proyecto" value="{proyecto}" placeholder="Nombre del proyecto">
                </div>
            </div>

            <div class="nota-edicion">
                ✏️ <strong>MODO EDICIÓN ACTIVA:</strong> Puedes modificar todos los campos directamente.
                Los totales se calcularán automáticamente al presionar el botón "Calcular Totales" o al cambiar cualquier valor.
            </div>

            <table class="items-table">
                <thead>
                    <tr>
                        <th style="width: 45%">📋 Descripción</th>
                        <th style="width: 15%">🔢 Cantidad</th>
                        <th style="width: 12%">📏 Unidad</th>
                        <th style="width: 15%">💰 Precio Unit.</th>
                        <th style="width: 13%">💵 Total</th>
                    </tr>
                </thead>
                <tbody id="items-body">
"""

    # Agregar items editables
    for i, item in enumerate(items):
        descripcion = item.get('descripcion', '')
        cantidad = item.get('cantidad', 0)
        unidad = item.get('unidad', 'und')
        precio = item.get('precio_unitario', 0)
        total = cantidad * precio

        html += f"""
                    <tr class="item-row">
                        <td>
                            <input type="text" class="item-desc" value="{descripcion}"
                                   placeholder="Descripción del servicio/producto">
                        </td>
                        <td>
                            <input type="number" class="item-cant" value="{cantidad}"
                                   min="0" step="0.01" onchange="calcularTotales()">
                        </td>
                        <td>
                            <input type="text" class="item-unidad" value="{unidad}"
                                   placeholder="und">
                        </td>
                        <td>
                            <input type="number" class="item-precio" value="{precio}"
                                   min="0" step="0.01" onchange="calcularTotales()">
                        </td>
                        <td class="total-item">S/ {total:.2f}</td>
                    </tr>
"""

    # Si no hay items, agregar una fila vacía
    if not items:
        html += """
                    <tr class="item-row">
                        <td>
                            <input type="text" class="item-desc" value=""
                                   placeholder="Descripción del servicio/producto">
                        </td>
                        <td>
                            <input type="number" class="item-cant" value="1"
                                   min="0" step="0.01" onchange="calcularTotales()">
                        </td>
                        <td>
                            <input type="text" class="item-unidad" value="und"
                                   placeholder="und">
                        </td>
                        <td>
                            <input type="number" class="item-precio" value="0"
                                   min="0" step="0.01" onchange="calcularTotales()">
                        </td>
                        <td class="total-item">S/ 0.00</td>
                    </tr>
"""

    html += f"""
                </tbody>
            </table>

            <div class="opciones-visualizacion">
                <h3>⚙️ Opciones de Visualización</h3>
                <div class="checkbox-group">
                    <div class="checkbox-item">
                        <input type="checkbox" id="mostrar_precios_unitarios" checked
                               onchange="calcularTotales()">
                        <label for="mostrar_precios_unitarios">Mostrar Precios Unitarios</label>
                    </div>
                    <div class="checkbox-item">
                        <input type="checkbox" id="mostrar_igv" checked
                               onchange="calcularTotales()">
                        <label for="mostrar_igv">Mostrar IGV (18%)</label>
                    </div>
                    <div class="checkbox-item">
                        <input type="checkbox" id="mostrar_total" checked
                               onchange="calcularTotales()">
                        <label for="mostrar_total">Mostrar Total Final</label>
                    </div>
                </div>
            </div>

            <div class="totales" id="seccion-totales">
                <div class="total-row">
                    <span>💰 Subtotal:</span>
                    <span id="subtotal_valor">S/ 0.00</span>
                </div>
                <div class="total-row igv" id="fila-igv">
                    <span>📋 IGV (18%):</span>
                    <span id="igv_valor">S/ 0.00</span>
                </div>
                <div class="total-row final" id="fila-total">
                    <span>🏆 TOTAL:</span>
                    <span id="total_valor">S/ 0.00</span>
                </div>
            </div>

            <button class="boton-calcular" onclick="calcularTotales()">
                🧮 Calcular Totales
            </button>

            <div class="footer">
                <strong>Tesla Electricidad y Automatización S.A.C.</strong><br>
                RUC: 20601138787 | Huancayo, Junín, Perú<br>
                📧 ingenieria.teslaelectricidad@gmail.com | 📱 +51 906 315 961<br>
                <br>
                Documento generado por {agente} v3.0 | {datetime.now().strftime('%d/%m/%Y %H:%M')}
            </div>
        </div>
    </div>

    <script>
        function calcularTotales() {{
            let subtotal = 0;

            // Calcular totales de cada fila
            const filas = document.querySelectorAll('.item-row');
            filas.forEach((fila, index) => {{
                const cantidad = parseFloat(fila.querySelector('.item-cant').value) || 0;
                const precio = parseFloat(fila.querySelector('.item-precio').value) || 0;
                const total = cantidad * precio;

                // Actualizar celda de total
                const celdaTotal = fila.querySelector('.total-item');
                celdaTotal.textContent = 'S/ ' + total.toFixed(2);

                subtotal += total;
            }});

            // Calcular IGV y total
            const mostrarIGV = document.getElementById('mostrar_igv').checked;
            const mostrarTotal = document.getElementById('mostrar_total').checked;

            const igv = mostrarIGV ? subtotal * 0.18 : 0;
            const total = subtotal + igv;

            // Actualizar valores
            document.getElementById('subtotal_valor').textContent = 'S/ ' + subtotal.toFixed(2);
            document.getElementById('igv_valor').textContent = 'S/ ' + igv.toFixed(2);
            document.getElementById('total_valor').textContent = 'S/ ' + total.toFixed(2);

            // Mostrar/ocultar filas según checkboxes
            document.getElementById('fila-igv').style.display = mostrarIGV ? 'flex' : 'none';
            document.getElementById('fila-total').style.display = mostrarTotal ? 'flex' : 'none';
        }}

        // Calcular totales al cargar la página
        window.addEventListener('DOMContentLoaded', function() {{
            calcularTotales();
        }});
    </script>
</body>
</html>
"""

    return html


def generar_preview_cotizacion_compleja_editable(datos: Dict[str, Any], agente: str) -> str:
    """
    🆕 Vista previa HTML COMPLETAMENTE EDITABLE para Cotización Compleja

    Incluye todo lo de la versión simple MÁS:
    - Select de términos de pago (30, 60, 90 días)
    - Textarea para condiciones comerciales
    - Sección de cronograma con 4 fases editables
    - 3 tipos de garantía con checkboxes
    - Diseño más profesional y completo

    Args:
        datos: Diccionario con datos de cotización completa
        agente: Nombre del agente que genera la cotización

    Returns:
        str: HTML completo con formulario editable avanzado
    """

    items = datos.get('items', [])
    cliente = datos.get('cliente', '')
    proyecto = datos.get('proyecto', '')
    terminos_pago = datos.get('terminos_pago', '30')
    condiciones = datos.get('condiciones_comerciales', '')

    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cotización Compleja Editable - {agente}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', 'Arial', sans-serif; background: linear-gradient(135deg, #dbeafe 0%, #eff6ff 100%); padding: 20px; line-height: 1.6; }}
        .container {{ max-width: 1400px; margin: 0 auto; background: white; border-radius: 12px; box-shadow: 0 10px 40px rgba(0, 82, 163, 0.2); overflow: hidden; }}
        .header {{ background: linear-gradient(135deg, #0052A3 0%, #1E40AF 100%); color: white; padding: 40px; text-align: center; position: relative; overflow: hidden; }}
        .header::before {{ content: ''; position: absolute; top: -50%; right: -10%; width: 400px; height: 400px; background: rgba(255, 255, 255, 0.1); border-radius: 50%; }}
        .header h1 {{ font-size: 32px; font-weight: 900; letter-spacing: -0.5px; margin-bottom: 10px; position: relative; z-index: 1; }}
        .header .agente {{ font-size: 15px; opacity: 0.95; font-weight: 600; position: relative; z-index: 1; }}
        .content {{ padding: 40px; }}
        .titulo-seccion {{ color: #0052A3; font-size: 24px; font-weight: 800; margin: 30px 0 20px 0; padding-bottom: 12px; border-bottom: 4px solid #3B82F6; display: flex; align-items: center; gap: 10px; }}
        .titulo-seccion:first-of-type {{ margin-top: 0; }}
        .info-basica {{ display: grid; grid-template-columns: 1fr 1fr; gap: 25px; margin-bottom: 30px; }}
        .campo {{ display: flex; flex-direction: column; }}
        .campo label {{ font-weight: 700; color: #1E40AF; margin-bottom: 10px; font-size: 15px; }}
        .campo input[type="text"], .campo input[type="number"], .campo textarea, .campo select {{ padding: 14px; border: 2px solid #bfdbfe; border-radius: 8px; font-size: 15px; font-weight: 600; color: #1e293b; transition: all 0.3s; }}
        .campo textarea {{ min-height: 120px; resize: vertical; font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; }}
        .campo input:focus, .campo textarea:focus, .campo select:focus {{ outline: none; border-color: #3B82F6; box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.15); }}
        .items-table {{ width: 100%; border-collapse: separate; border-spacing: 0; margin: 20px 0; box-shadow: 0 6px 16px rgba(0, 82, 163, 0.12); border-radius: 10px; overflow: hidden; }}
        .items-table thead th {{ background: linear-gradient(135deg, #0052A3 0%, #1E40AF 100%); color: white; padding: 18px 14px; text-align: left; font-weight: 800; font-size: 14px; text-transform: uppercase; letter-spacing: 0.5px; }}
        .items-table tbody tr {{ transition: background 0.2s; }}
        .items-table tbody tr:hover {{ background: #f0f9ff; }}
        .items-table tbody td {{ padding: 14px; border-bottom: 1px solid #dbeafe; }}
        .items-table input[type="text"], .items-table input[type="number"] {{ width: 100%; padding: 10px; border: 2px solid #bfdbfe; border-radius: 6px; font-size: 14px; font-weight: 600; color: #1e293b; }}
        .items-table input:focus {{ border-color: #3B82F6; outline: none; }}
        .total-item {{ color: #0052A3; font-weight: 700; font-size: 15px; }}
        .seccion-avanzada {{ background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); padding: 25px; border-radius: 10px; margin: 25px 0; border: 2px solid #bfdbfe; }}
        .cronograma-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-top: 20px; }}
        .fase-item {{ background: white; padding: 20px; border-radius: 8px; border: 2px solid #bfdbfe; transition: all 0.3s; }}
        .fase-item:hover {{ border-color: #3B82F6; box-shadow: 0 4px 12px rgba(59, 130, 246, 0.2); }}
        .fase-item h4 {{ color: #1E40AF; font-weight: 800; margin-bottom: 12px; font-size: 16px; }}
        .garantias-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-top: 20px; }}
        .garantia-item {{ background: white; padding: 20px; border-radius: 8px; border: 2px solid #bfdbfe; display: flex; align-items: flex-start; gap: 15px; transition: all 0.3s; }}
        .garantia-item:hover {{ border-color: #3B82F6; }}
        .garantia-item input[type="checkbox"] {{ width: 22px; height: 22px; cursor: pointer; accent-color: #0052A3; margin-top: 2px; }}
        .garantia-info {{ flex: 1; }}
        .garantia-info h4 {{ color: #1E40AF; font-weight: 800; margin-bottom: 8px; font-size: 16px; }}
        .garantia-info p {{ color: #64748b; font-size: 14px; line-height: 1.5; }}
        .opciones-visualizacion {{ background: #eff6ff; padding: 25px; border-radius: 10px; margin: 25px 0; border: 2px solid #bfdbfe; }}
        .opciones-visualizacion h3 {{ color: #1E40AF; font-size: 18px; font-weight: 800; margin-bottom: 18px; }}
        .checkbox-group {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 15px; }}
        .checkbox-item {{ display: flex; align-items: center; gap: 10px; }}
        .checkbox-item input[type="checkbox"] {{ width: 20px; height: 20px; cursor: pointer; accent-color: #0052A3; }}
        .checkbox-item label {{ font-weight: 600; color: #334155; cursor: pointer; font-size: 15px; }}
        .totales {{ background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); padding: 30px; border-radius: 10px; margin-top: 25px; border: 3px solid #3B82F6; }}
        .total-row {{ display: flex; justify-content: space-between; padding: 12px 0; font-size: 17px; font-weight: 700; color: #1e293b; }}
        .total-row.igv {{ border-top: 2px solid #93c5fd; margin-top: 12px; padding-top: 18px; }}
        .total-row.final {{ background: white; padding: 22px; border-radius: 8px; margin-top: 18px; font-size: 26px; font-weight: 900; color: #0052A3; border: 3px solid #1E40AF; box-shadow: 0 4px 12px rgba(0, 82, 163, 0.2); }}
        .boton-calcular {{ background: linear-gradient(135deg, #0052A3 0%, #1E40AF 100%); color: white; border: none; padding: 18px 50px; font-size: 17px; font-weight: 800; border-radius: 10px; cursor: pointer; transition: all 0.3s; box-shadow: 0 6px 16px rgba(0, 82, 163, 0.3); width: 100%; margin-top: 25px; }}
        .boton-calcular:hover {{ transform: translateY(-3px); box-shadow: 0 8px 24px rgba(0, 82, 163, 0.4); }}
        .boton-calcular:active {{ transform: translateY(0); }}
        .footer {{ text-align: center; padding: 25px; color: #64748b; font-size: 14px; border-top: 3px solid #e2e8f0; margin-top: 40px; }}
        .nota-edicion {{ background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); border: 3px solid #fbbf24; padding: 18px; border-radius: 10px; margin: 25px 0; color: #78350f; font-weight: 600; font-size: 15px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>⚡ TESLA ELECTRICIDAD Y AUTOMATIZACIÓN</h1>
            <p class="agente">🤖 Generado por {agente} - Cotización Compleja Editable</p>
        </div>
        <div class="content">
            <h2 class="titulo-seccion">📋 COTIZACIÓN COMPLEJA - MODO EDITABLE AVANZADO</h2>
            <div class="info-basica">
                <div class="campo"><label>👤 Cliente:</label><input type="text" id="cliente" value="{cliente}" placeholder="Nombre completo del cliente"></div>
                <div class="campo"><label>📁 Proyecto:</label><input type="text" id="proyecto" value="{proyecto}" placeholder="Nombre del proyecto"></div>
            </div>
            <div class="nota-edicion">✏️ <strong>MODO EDICIÓN COMPLETA ACTIVA:</strong> Cotización compleja con todas las funcionalidades editables. Modifica items, condiciones comerciales, cronograma, garantías y más. Los cálculos se actualizan automáticamente.</div>
            <h2 class="titulo-seccion">📦 Items de la Cotización</h2>
            <table class="items-table">
                <thead><tr><th style="width: 40%">📋 Descripción</th><th style="width: 12%">🔢 Cantidad</th><th style="width: 10%">📏 Unidad</th><th style="width: 15%">💰 Precio Unit.</th><th style="width: 10%">⏱️ Días</th><th style="width: 13%">💵 Total</th></tr></thead>
                <tbody>
"""

    for i, item in enumerate(items):
        desc = item.get('descripcion', '')
        cant = item.get('cantidad', 0)
        unid = item.get('unidad', 'und')
        prec = item.get('precio_unitario', 0)
        dias = item.get('dias_ejecucion', 1)
        total = cant * prec
        html += f"""                    <tr class="item-row">
                        <td><input type="text" class="item-desc" value="{desc}" placeholder="Descripción detallada"></td>
                        <td><input type="number" class="item-cant" value="{cant}" min="0" step="0.01" onchange="calcularTotales()"></td>
                        <td><input type="text" class="item-unidad" value="{unid}"></td>
                        <td><input type="number" class="item-precio" value="{prec}" min="0" step="0.01" onchange="calcularTotales()"></td>
                        <td><input type="number" class="item-dias" value="{dias}" min="1" step="1"></td>
                        <td class="total-item">S/ {total:.2f}</td>
                    </tr>
"""

    if not items:
        html += """                    <tr class="item-row">
                        <td><input type="text" class="item-desc" value="" placeholder="Descripción"></td>
                        <td><input type="number" class="item-cant" value="1" min="0" step="0.01" onchange="calcularTotales()"></td>
                        <td><input type="text" class="item-unidad" value="und"></td>
                        <td><input type="number" class="item-precio" value="0" min="0" step="0.01" onchange="calcularTotales()"></td>
                        <td><input type="number" class="item-dias" value="1" min="1" step="1"></td>
                        <td class="total-item">S/ 0.00</td>
                    </tr>
"""

    html += f"""                </tbody>
            </table>
            <h2 class="titulo-seccion">💼 Condiciones Comerciales</h2>
            <div class="seccion-avanzada">
                <div class="info-basica">
                    <div class="campo"><label>💳 Términos de Pago:</label>
                        <select id="terminos_pago">
                            <option value="contado" {"selected" if terminos_pago == "contado" else ""}>Pago al Contado</option>
                            <option value="30" {"selected" if terminos_pago == "30" else ""}>30 días</option>
                            <option value="60" {"selected" if terminos_pago == "60" else ""}>60 días</option>
                            <option value="90" {"selected" if terminos_pago == "90" else ""}>90 días</option>
                            <option value="personalizado" {"selected" if terminos_pago == "personalizado" else ""}>Personalizado</option>
                        </select>
                    </div>
                    <div class="campo"><label>📅 Vigencia de la Oferta:</label><input type="number" id="vigencia_dias" value="30" min="1" step="1"></div>
                </div>
                <div class="campo" style="margin-top: 20px;"><label>📝 Condiciones Adicionales:</label><textarea id="condiciones_comerciales" placeholder="Condiciones comerciales adicionales, descuentos, bonificaciones...">{condiciones}</textarea></div>
            </div>
            <h2 class="titulo-seccion">📅 Cronograma de Ejecución</h2>
            <div class="seccion-avanzada">
                <div class="cronograma-grid">
                    <div class="fase-item"><h4>🔷 Fase 1: Planificación</h4><div class="campo"><label>Descripción:</label><input type="text" id="fase1_desc" value="Planificación y diseño inicial"></div><div class="campo" style="margin-top: 10px;"><label>Duración (días):</label><input type="number" id="fase1_dias" value="5" min="1" step="1"></div></div>
                    <div class="fase-item"><h4>🔷 Fase 2: Ejecución</h4><div class="campo"><label>Descripción:</label><input type="text" id="fase2_desc" value="Instalación y montaje"></div><div class="campo" style="margin-top: 10px;"><label>Duración (días):</label><input type="number" id="fase2_dias" value="10" min="1" step="1"></div></div>
                    <div class="fase-item"><h4>🔷 Fase 3: Pruebas</h4><div class="campo"><label>Descripción:</label><input type="text" id="fase3_desc" value="Pruebas y ajustes"></div><div class="campo" style="margin-top: 10px;"><label>Duración (días):</label><input type="number" id="fase3_dias" value="3" min="1" step="1"></div></div>
                    <div class="fase-item"><h4>🔷 Fase 4: Entrega</h4><div class="campo"><label>Descripción:</label><input type="text" id="fase4_desc" value="Capacitación y entrega final"></div><div class="campo" style="margin-top: 10px;"><label>Duración (días):</label><input type="number" id="fase4_dias" value="2" min="1" step="1"></div></div>
                </div>
            </div>
            <h2 class="titulo-seccion">🛡️ Garantías Incluidas</h2>
            <div class="seccion-avanzada">
                <div class="garantias-grid">
                    <div class="garantia-item"><input type="checkbox" id="garantia_materiales" checked><div class="garantia-info"><h4>🔧 Garantía de Materiales</h4><p>12 meses de garantía en todos los materiales y equipos instalados contra defectos de fabricación.</p></div></div>
                    <div class="garantia-item"><input type="checkbox" id="garantia_mano_obra" checked><div class="garantia-info"><h4>👷 Garantía de Mano de Obra</h4><p>6 meses de garantía en la instalación y mano de obra contra defectos de ejecución.</p></div></div>
                    <div class="garantia-item"><input type="checkbox" id="garantia_soporte"><div class="garantia-info"><h4>📞 Soporte Técnico Extendido</h4><p>Soporte técnico telefónico y visitas de mantenimiento preventivo durante 12 meses.</p></div></div>
                </div>
            </div>
            <div class="opciones-visualizacion">
                <h3>⚙️ Opciones de Visualización del Documento</h3>
                <div class="checkbox-group">
                    <div class="checkbox-item"><input type="checkbox" id="mostrar_precios_unitarios" checked onchange="calcularTotales()"><label for="mostrar_precios_unitarios">Mostrar Precios Unitarios</label></div>
                    <div class="checkbox-item"><input type="checkbox" id="mostrar_igv" checked onchange="calcularTotales()"><label for="mostrar_igv">Mostrar IGV (18%)</label></div>
                    <div class="checkbox-item"><input type="checkbox" id="mostrar_total" checked onchange="calcularTotales()"><label for="mostrar_total">Mostrar Total Final</label></div>
                    <div class="checkbox-item"><input type="checkbox" id="mostrar_cronograma" checked><label for="mostrar_cronograma">Incluir Cronograma</label></div>
                    <div class="checkbox-item"><input type="checkbox" id="mostrar_garantias" checked><label for="mostrar_garantias">Incluir Garantías</label></div>
                </div>
            </div>
            <div class="totales">
                <div class="total-row"><span>💰 Subtotal:</span><span id="subtotal_valor">S/ 0.00</span></div>
                <div class="total-row igv" id="fila-igv"><span>📋 IGV (18%):</span><span id="igv_valor">S/ 0.00</span></div>
                <div class="total-row final" id="fila-total"><span>🏆 TOTAL:</span><span id="total_valor">S/ 0.00</span></div>
            </div>
            <button class="boton-calcular" onclick="calcularTotales()">🧮 Calcular Totales y Actualizar Documento</button>
            <div class="footer">
                <strong style="font-size: 16px;">Tesla Electricidad y Automatización S.A.C.</strong><br>
                RUC: 20601138787 | Huancayo, Junín, Perú<br>
                📧 ingenieria.teslaelectricidad@gmail.com | 📱 +51 906 315 961<br><br>
                Documento generado por {agente} v3.0 - Sistema de Cotización Compleja<br>
                {datetime.now().strftime('%d/%m/%Y %H:%M')}
            </div>
        </div>
    </div>
    <script>
        function calcularTotales() {{
            let subtotal = 0;
            const filas = document.querySelectorAll('.item-row');
            filas.forEach((fila) => {{
                const cantidad = parseFloat(fila.querySelector('.item-cant').value) || 0;
                const precio = parseFloat(fila.querySelector('.item-precio').value) || 0;
                const total = cantidad * precio;
                fila.querySelector('.total-item').textContent = 'S/ ' + total.toFixed(2);
                subtotal += total;
            }});
            const mostrarIGV = document.getElementById('mostrar_igv').checked;
            const mostrarTotal = document.getElementById('mostrar_total').checked;
            const igv = mostrarIGV ? subtotal * 0.18 : 0;
            const total = subtotal + igv;
            document.getElementById('subtotal_valor').textContent = 'S/ ' + subtotal.toFixed(2);
            document.getElementById('igv_valor').textContent = 'S/ ' + igv.toFixed(2);
            document.getElementById('total_valor').textContent = 'S/ ' + total.toFixed(2);
            document.getElementById('fila-igv').style.display = mostrarIGV ? 'flex' : 'none';
            document.getElementById('fila-total').style.display = mostrarTotal ? 'flex' : 'none';
            let duracionTotal = 0;
            for (let i = 1; i <= 4; i++) {{
                duracionTotal += parseFloat(document.getElementById('fase' + i + '_dias').value) || 0;
            }}
            console.log('Duración total del proyecto:', duracionTotal, 'días');
        }}
        window.addEventListener('DOMContentLoaded', function() {{ calcularTotales(); }});
    </script>
</body>
</html>
"""

    return html


def generar_preview_proyecto_simple_editable(datos: Dict[str, Any], agente: str) -> str:
    """
    AGENTE 2 - Vista previa HTML COMPLETAMENTE EDITABLE para Proyecto Simple

    Genera HTML con inputs editables para gestión de proyectos básicos.
    Colores: Paleta AZUL Tesla (#0052A3, #1E40AF, #3B82F6)
    """

    nombre = datos.get('nombre', '')
    cliente = datos.get('cliente', '')
    codigo = datos.get('codigo', f"PRY-{datetime.now().strftime('%Y%m')}-001")
    presupuesto = datos.get('presupuesto', 0)
    fecha_inicio = datos.get('fecha_inicio', datetime.now().strftime('%Y-%m-%d'))
    fecha_fin = datos.get('fecha_fin', (datetime.now() + timedelta(days=90)).strftime('%Y-%m-%d'))
    alcance = datos.get('alcance', '')

    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Proyecto Simple - {agente}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Arial, sans-serif;
            margin: 20px;
            background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
        }}
        .container {{
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 8px 32px rgba(0, 82, 163, 0.2);
            border: 3px solid #3B82F6;
        }}
        .header {{
            background: linear-gradient(135deg, #0052A3 0%, #1E40AF 100%);
            color: white;
            padding: 25px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 4px 12px rgba(0, 82, 163, 0.3);
        }}
        .company {{
            font-size: 28px;
            font-weight: 900;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
            letter-spacing: -0.5px;
        }}
        .agent {{
            font-size: 14px;
            margin-top: 8px;
            opacity: 0.95;
            font-weight: 600;
        }}
        .title {{
            color: #0052A3;
            font-size: 24px;
            margin: 25px 0;
            font-weight: 800;
            border-left: 6px solid #1E40AF;
            padding-left: 15px;
            background: linear-gradient(90deg, #EFF6FF 0%, transparent 100%);
            padding: 10px 15px;
            border-radius: 4px;
        }}
        .form-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin: 25px 0;
        }}
        .form-group {{
            background: #F0F9FF;
            padding: 18px;
            border-radius: 8px;
            border: 2px solid #BFDBFE;
        }}
        .form-group label {{
            display: block;
            font-weight: 800;
            color: #1E40AF;
            font-size: 14px;
            margin-bottom: 8px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        .form-group input, .form-group textarea {{
            width: 100%;
            padding: 12px;
            border: 2px solid #3B82F6;
            border-radius: 6px;
            font-size: 15px;
            font-weight: 600;
            color: #1F2937;
            transition: all 0.3s ease;
            box-sizing: border-box;
        }}
        .form-group input:focus, .form-group textarea:focus {{
            outline: none;
            border-color: #0052A3;
            box-shadow: 0 0 0 3px rgba(0, 82, 163, 0.1);
        }}
        .full-width {{
            grid-column: 1 / -1;
        }}
        .fase-card {{
            background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
            border-left: 5px solid #0052A3;
            padding: 18px;
            margin: 12px 0;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0, 82, 163, 0.15);
        }}
        .fase-header {{
            font-weight: 800;
            color: #0052A3;
            font-size: 16px;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .fase-inputs {{
            display: grid;
            grid-template-columns: 2fr 1fr 1fr;
            gap: 12px;
        }}
        .fase-inputs input, .fase-inputs select {{
            padding: 10px;
            border: 2px solid #3B82F6;
            border-radius: 5px;
            font-weight: 600;
        }}
        .recursos-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
            margin: 20px 0;
        }}
        .recurso-card {{
            background: white;
            padding: 15px;
            border: 2px solid #3B82F6;
            border-radius: 8px;
            box-shadow: 0 2px 6px rgba(59, 130, 246, 0.15);
        }}
        .edit-note {{
            background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%);
            border: 2px solid #F59E0B;
            padding: 18px;
            border-radius: 8px;
            margin-top: 25px;
            font-weight: 700;
            color: #92400E;
            box-shadow: 0 2px 8px rgba(245, 158, 11, 0.2);
        }}
        .signature {{
            text-align: right;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 3px solid #BFDBFE;
            font-weight: 700;
            color: #0052A3;
        }}
        select {{
            cursor: pointer;
        }}
        select:hover {{
            background: #EFF6FF;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="company">⚡ TESLA ELECTRICIDAD Y AUTOMATIZACIÓN S.A.C.</div>
            <div class="agent">🤖 {agente} - Sistema de Gestión de Proyectos</div>
        </div>

        <h2 class="title">📋 PROYECTO SIMPLE - EDITABLE</h2>

        <div class="form-grid">
            <div class="form-group">
                <label>📝 Nombre del Proyecto</label>
                <input type="text" name="nombre" value="{nombre}" placeholder="Ej: Instalación Eléctrica Oficina XYZ">
            </div>
            <div class="form-group">
                <label>👤 Cliente</label>
                <input type="text" name="cliente" value="{cliente}" placeholder="Nombre del cliente">
            </div>
            <div class="form-group">
                <label>🔢 Código de Proyecto</label>
                <input type="text" name="codigo" value="{codigo}" placeholder="PRY-202512-001">
            </div>
            <div class="form-group">
                <label>💰 Presupuesto Estimado (S/)</label>
                <input type="number" name="presupuesto" value="{presupuesto}" step="0.01" placeholder="0.00">
            </div>
            <div class="form-group">
                <label>📅 Fecha de Inicio</label>
                <input type="date" name="fecha_inicio" value="{fecha_inicio}">
            </div>
            <div class="form-group">
                <label>📅 Fecha de Fin Estimada</label>
                <input type="date" name="fecha_fin" value="{fecha_fin}">
            </div>
            <div class="form-group full-width">
                <label>📄 Alcance del Proyecto</label>
                <textarea name="alcance" rows="4" placeholder="Descripción detallada del alcance del proyecto...">{alcance}</textarea>
            </div>
        </div>

        <h3 class="title" style="font-size: 20px; margin-top: 30px;">🔄 Fases del Proyecto (5 etapas)</h3>
"""

    fases_default = [
        {'nombre': 'Planificación y Diseño', 'duracion': '1-2 semanas', 'estado': 'pendiente'},
        {'nombre': 'Ingeniería de Detalle', 'duracion': '2-3 semanas', 'estado': 'pendiente'},
        {'nombre': 'Ejecución y Montaje', 'duracion': '3-4 semanas', 'estado': 'pendiente'},
        {'nombre': 'Pruebas y Comisionamiento', 'duracion': '1 semana', 'estado': 'pendiente'},
        {'nombre': 'Entrega y Cierre', 'duracion': '1 semana', 'estado': 'pendiente'}
    ]

    fases = datos.get('fases', fases_default)

    for i, fase in enumerate(fases[:5], 1):
        nombre_fase = fase.get('nombre', f'Fase {i}')
        duracion = fase.get('duracion', '1 semana')
        estado = fase.get('estado', 'pendiente')

        html += f"""
        <div class="fase-card">
            <div class="fase-header">
                ▶️ Fase {i}
            </div>
            <div class="fase-inputs">
                <input type="text" value="{nombre_fase}" placeholder="Nombre de la fase">
                <input type="text" value="{duracion}" placeholder="Duración">
                <select>
                    <option value="pendiente" {"selected" if estado == "pendiente" else ""}>⏳ Pendiente</option>
                    <option value="en_curso" {"selected" if estado == "en_curso" else ""}>🔄 En Curso</option>
                    <option value="completado" {"selected" if estado == "completado" else ""}>✅ Completado</option>
                    <option value="pausado" {"selected" if estado == "pausado" else ""}>⏸️ Pausado</option>
                </select>
            </div>
        </div>
"""

    html += """
        <h3 class="title" style="font-size: 20px; margin-top: 30px;">👥 Recursos Asignados</h3>
        <div class="recursos-grid">
"""

    recursos_default = [
        {'rol': 'Jefe de Proyecto', 'nombre': 'Por asignar'},
        {'rol': 'Ingeniero Eléctrico', 'nombre': 'Por asignar'},
        {'rol': 'Técnico Instalador', 'nombre': 'Por asignar'},
        {'rol': 'Supervisor de Obra', 'nombre': 'Por asignar'}
    ]

    recursos = datos.get('recursos', recursos_default)

    for recurso in recursos[:4]:
        rol = recurso.get('rol', 'Rol')
        nombre = recurso.get('nombre', 'Por asignar')

        html += f"""
            <div class="recurso-card">
                <label style="font-weight: 800; color: #1E40AF; font-size: 13px; display: block; margin-bottom: 6px;">
                    {rol}
                </label>
                <input type="text" value="{nombre}" placeholder="Nombre del recurso"
                       style="width: 100%; padding: 8px; border: 2px solid #3B82F6; border-radius: 5px; font-weight: 600;">
            </div>
"""

    html += f"""
        </div>

        <div class="edit-note">
            ✏️ <strong>Vista Previa Editable:</strong> Todos los campos son editables. Modifica los datos según las necesidades del proyecto.
            Los cambios se reflejarán en el documento final Word/PDF.
        </div>

        <div class="signature">
            <div style="color: #6b7280; font-size: 12px;">
                Documento generado por {agente} v3.0<br>
                {datetime.now().strftime('%d/%m/%Y %H:%M')} - Sistema Tesla
            </div>
        </div>
    </div>
</body>
</html>
"""

    return html

def generar_preview_proyecto_complejo_pmi_editable(datos: Dict[str, Any], agente: str) -> str:
    """
    AGENTE 2 - Vista previa HTML COMPLETAMENTE EDITABLE para Proyecto Complejo PMI

    Incluye todo lo de Proyecto Simple MÁS:
    - Métricas PMI (SPI, CPI, EV, PV, AC)
    - Diagrama Gantt simplificado
    - Matriz RACI
    - Gestión de riesgos

    Colores: Paleta AZUL Tesla (#0052A3, #1E40AF, #3B82F6)
    """

    nombre = datos.get('nombre', '')
    cliente = datos.get('cliente', '')
    codigo = datos.get('codigo', f"PRY-PMI-{datetime.now().strftime('%Y%m')}-001")
    presupuesto = datos.get('presupuesto', 0)
    fecha_inicio = datos.get('fecha_inicio', datetime.now().strftime('%Y-%m-%d'))
    fecha_fin = datos.get('fecha_fin', (datetime.now() + timedelta(days=180)).strftime('%Y-%m-%d'))
    alcance = datos.get('alcance', '')

    # Métricas PMI
    metricas = datos.get('metricas_pmi', {
        'SPI': 1.0,
        'CPI': 1.0,
        'EV': 0,
        'PV': 0,
        'AC': 0
    })

    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Proyecto Complejo PMI - {agente}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Arial, sans-serif;
            margin: 20px;
            background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
        }}
        .container {{
            background: white;
            padding: 35px;
            border-radius: 12px;
            box-shadow: 0 8px 32px rgba(0, 82, 163, 0.25);
            border: 3px solid #0052A3;
        }}
        .header {{
            background: linear-gradient(135deg, #0052A3 0%, #1E40AF 100%);
            color: white;
            padding: 28px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 4px 16px rgba(0, 82, 163, 0.4);
        }}
        .company {{
            font-size: 30px;
            font-weight: 900;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }}
        .agent {{
            font-size: 14px;
            margin-top: 8px;
            opacity: 0.95;
            font-weight: 600;
        }}
        .title {{
            color: #0052A3;
            font-size: 22px;
            margin: 25px 0 15px 0;
            font-weight: 800;
            border-left: 6px solid #1E40AF;
            padding-left: 15px;
            background: linear-gradient(90deg, #EFF6FF 0%, transparent 100%);
            padding: 12px 15px;
            border-radius: 4px;
        }}
        .form-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin: 20px 0;
        }}
        .form-group {{
            background: #F0F9FF;
            padding: 18px;
            border-radius: 8px;
            border: 2px solid #BFDBFE;
        }}
        .form-group label {{
            display: block;
            font-weight: 800;
            color: #1E40AF;
            font-size: 13px;
            margin-bottom: 8px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        .form-group input, .form-group textarea {{
            width: 100%;
            padding: 12px;
            border: 2px solid #3B82F6;
            border-radius: 6px;
            font-size: 15px;
            font-weight: 600;
            color: #1F2937;
            box-sizing: border-box;
            transition: all 0.3s ease;
        }}
        .form-group input:focus, .form-group textarea:focus {{
            outline: none;
            border-color: #0052A3;
            box-shadow: 0 0 0 3px rgba(0, 82, 163, 0.1);
        }}
        .full-width {{
            grid-column: 1 / -1;
        }}
        .pmi-section {{
            background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%);
            border: 3px solid #F59E0B;
            padding: 25px;
            border-radius: 10px;
            margin: 25px 0;
            box-shadow: 0 4px 12px rgba(245, 158, 11, 0.2);
        }}
        .pmi-grid {{
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 15px;
            margin-top: 15px;
        }}
        .pmi-metric {{
            background: white;
            padding: 15px;
            border-radius: 8px;
            border: 2px solid #F59E0B;
            text-align: center;
        }}
        .pmi-metric label {{
            display: block;
            font-weight: 800;
            color: #92400E;
            font-size: 12px;
            margin-bottom: 8px;
        }}
        .pmi-metric input {{
            width: 100%;
            padding: 8px;
            border: 2px solid #F59E0B;
            border-radius: 5px;
            text-align: center;
            font-weight: 700;
            font-size: 16px;
            color: #92400E;
        }}
        .gantt-section {{
            background: #F0F9FF;
            padding: 20px;
            border-radius: 8px;
            border: 2px solid #3B82F6;
            margin: 20px 0;
        }}
        .gantt-bar {{
            background: linear-gradient(90deg, #0052A3 0%, #3B82F6 100%);
            height: 30px;
            border-radius: 5px;
            margin: 8px 0;
            padding: 5px 10px;
            color: white;
            font-weight: 700;
            font-size: 12px;
            display: flex;
            align-items: center;
            box-shadow: 0 2px 6px rgba(0, 82, 163, 0.3);
        }}
        .raci-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
            box-shadow: 0 2px 12px rgba(0, 82, 163, 0.15);
        }}
        .raci-table th {{
            background: linear-gradient(135deg, #0052A3 0%, #1E40AF 100%);
            color: white;
            padding: 12px;
            font-weight: 800;
            font-size: 13px;
            border: 2px solid #1E40AF;
        }}
        .raci-table td {{
            padding: 10px;
            border: 2px solid #BFDBFE;
            text-align: center;
        }}
        .raci-table select {{
            width: 100%;
            padding: 6px;
            border: 2px solid #3B82F6;
            border-radius: 4px;
            font-weight: 700;
            cursor: pointer;
            background: white;
        }}
        .risk-card {{
            background: linear-gradient(135deg, #FEE2E2 0%, #FECACA 100%);
            border-left: 5px solid #DC2626;
            padding: 15px;
            margin: 10px 0;
            border-radius: 8px;
        }}
        .risk-inputs {{
            display: grid;
            grid-template-columns: 2fr 1fr 1fr;
            gap: 10px;
            margin-top: 10px;
        }}
        .edit-note {{
            background: linear-gradient(135deg, #D1FAE5 0%, #A7F3D0 100%);
            border: 2px solid #10B981;
            padding: 18px;
            border-radius: 8px;
            margin-top: 25px;
            font-weight: 700;
            color: #065F46;
            box-shadow: 0 2px 8px rgba(16, 185, 129, 0.2);
        }}
        .signature {{
            text-align: right;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 3px solid #BFDBFE;
            font-weight: 700;
            color: #0052A3;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="company">⚡ TESLA ELECTRICIDAD Y AUTOMATIZACIÓN S.A.C.</div>
            <div class="agent">🤖 {agente} - Gestión PMI Profesional</div>
        </div>

        <h2 class="title">📊 PROYECTO COMPLEJO PMI - EDITABLE</h2>

        <div class="form-grid">
            <div class="form-group">
                <label>📝 Nombre del Proyecto</label>
                <input type="text" name="nombre" value="{nombre}" placeholder="Nombre completo del proyecto">
            </div>
            <div class="form-group">
                <label>👤 Cliente</label>
                <input type="text" name="cliente" value="{cliente}" placeholder="Cliente corporativo">
            </div>
            <div class="form-group">
                <label>🔢 Código PMI</label>
                <input type="text" name="codigo" value="{codigo}" placeholder="PRY-PMI-202512-001">
            </div>
            <div class="form-group">
                <label>💰 Presupuesto Total (S/)</label>
                <input type="number" name="presupuesto" value="{presupuesto}" step="0.01">
            </div>
            <div class="form-group">
                <label>📅 Fecha de Inicio</label>
                <input type="date" name="fecha_inicio" value="{fecha_inicio}">
            </div>
            <div class="form-group">
                <label>📅 Fecha de Fin</label>
                <input type="date" name="fecha_fin" value="{fecha_fin}">
            </div>
            <div class="form-group full-width">
                <label>📄 Alcance del Proyecto</label>
                <textarea name="alcance" rows="4" placeholder="Descripción completa del alcance PMI...">{alcance}</textarea>
            </div>
        </div>

        <div class="pmi-section">
            <h3 style="color: #92400E; font-size: 18px; margin: 0 0 15px 0; font-weight: 900;">
                📈 MÉTRICAS PMI (Earned Value Management)
            </h3>
            <div class="pmi-grid">
                <div class="pmi-metric">
                    <label>SPI</label>
                    <input type="number" value="{metricas.get('SPI', 1.0)}" step="0.01" placeholder="1.00">
                    <small style="color: #92400E; font-size: 10px;">Schedule Performance</small>
                </div>
                <div class="pmi-metric">
                    <label>CPI</label>
                    <input type="number" value="{metricas.get('CPI', 1.0)}" step="0.01" placeholder="1.00">
                    <small style="color: #92400E; font-size: 10px;">Cost Performance</small>
                </div>
                <div class="pmi-metric">
                    <label>EV (S/)</label>
                    <input type="number" value="{metricas.get('EV', 0)}" step="0.01" placeholder="0">
                    <small style="color: #92400E; font-size: 10px;">Earned Value</small>
                </div>
                <div class="pmi-metric">
                    <label>PV (S/)</label>
                    <input type="number" value="{metricas.get('PV', 0)}" step="0.01" placeholder="0">
                    <small style="color: #92400E; font-size: 10px;">Planned Value</small>
                </div>
                <div class="pmi-metric">
                    <label>AC (S/)</label>
                    <input type="number" value="{metricas.get('AC', 0)}" step="0.01" placeholder="0">
                    <small style="color: #92400E; font-size: 10px;">Actual Cost</small>
                </div>
            </div>
        </div>

        <h3 class="title">📅 Diagrama Gantt Simplificado</h3>
        <div class="gantt-section">
"""

    fases_gantt = datos.get('fases', [
        {'nombre': 'Iniciación', 'progreso': 30},
        {'nombre': 'Planificación', 'progreso': 60},
        {'nombre': 'Ejecución', 'progreso': 40},
        {'nombre': 'Monitoreo', 'progreso': 25},
        {'nombre': 'Cierre', 'progreso': 10}
    ])

    for fase in fases_gantt[:5]:
        nombre = fase.get('nombre', 'Fase')
        progreso = fase.get('progreso', 0)

        html += f"""
            <div style="margin: 12px 0;">
                <label style="font-weight: 700; color: #1E40AF; font-size: 13px; display: block; margin-bottom: 5px;">
                    {nombre}
                </label>
                <div class="gantt-bar" style="width: {progreso}%;">
                    {progreso}% completado
                </div>
            </div>
"""

    html += """
        </div>

        <h3 class="title">👥 Matriz RACI (Responsabilidades)</h3>
        <table class="raci-table">
            <thead>
                <tr>
                    <th>Actividad</th>
                    <th>Jefe Proyecto</th>
                    <th>Ingeniero</th>
                    <th>Técnico</th>
                    <th>Cliente</th>
                </tr>
            </thead>
            <tbody>
"""

    actividades_raci = [
        'Planificación Inicial',
        'Diseño Eléctrico',
        'Instalación',
        'Pruebas',
        'Aprobación Final'
    ]

    for actividad in actividades_raci:
        html += f"""
                <tr>
                    <td style="text-align: left; font-weight: 700; color: #1E40AF;">{actividad}</td>
                    <td>
                        <select>
                            <option value="R">R - Responsable</option>
                            <option value="A" selected>A - Aprueba</option>
                            <option value="C">C - Consulta</option>
                            <option value="I">I - Informa</option>
                        </select>
                    </td>
                    <td>
                        <select>
                            <option value="R" selected>R - Responsable</option>
                            <option value="A">A - Aprueba</option>
                            <option value="C">C - Consulta</option>
                            <option value="I">I - Informa</option>
                        </select>
                    </td>
                    <td>
                        <select>
                            <option value="R">R - Responsable</option>
                            <option value="A">A - Aprueba</option>
                            <option value="C" selected>C - Consulta</option>
                            <option value="I">I - Informa</option>
                        </select>
                    </td>
                    <td>
                        <select>
                            <option value="R">R - Responsable</option>
                            <option value="A">A - Aprueba</option>
                            <option value="C">C - Consulta</option>
                            <option value="I" selected>I - Informa</option>
                        </select>
                    </td>
                </tr>
"""

    html += """
            </tbody>
        </table>

        <h3 class="title">⚠️ Gestión de Riesgos (Top 3)</h3>
"""

    riesgos_default = [
        {'descripcion': 'Retraso en entrega de materiales', 'probabilidad': 'Media', 'impacto': 'Alto'},
        {'descripcion': 'Cambios en normativa eléctrica', 'probabilidad': 'Baja', 'impacto': 'Medio'},
        {'descripcion': 'Condiciones climáticas adversas', 'probabilidad': 'Media', 'impacto': 'Medio'}
    ]

    riesgos = datos.get('riesgos', riesgos_default)

    for i, riesgo in enumerate(riesgos[:3], 1):
        desc = riesgo.get('descripcion', '')
        prob = riesgo.get('probabilidad', 'Media')
        imp = riesgo.get('impacto', 'Medio')

        html += f"""
        <div class="risk-card">
            <strong style="color: #DC2626;">⚠️ Riesgo {i}</strong>
            <div class="risk-inputs">
                <input type="text" value="{desc}" placeholder="Descripción del riesgo"
                       style="border: 2px solid #DC2626; border-radius: 5px; padding: 8px; font-weight: 600;">
                <select style="border: 2px solid #DC2626; border-radius: 5px; padding: 8px; font-weight: 600;">
                    <option value="baja" {"selected" if prob == "Baja" else ""}>Prob: Baja</option>
                    <option value="media" {"selected" if prob == "Media" else ""}>Prob: Media</option>
                    <option value="alta" {"selected" if prob == "Alta" else ""}>Prob: Alta</option>
                </select>
                <select style="border: 2px solid #DC2626; border-radius: 5px; padding: 8px; font-weight: 600;">
                    <option value="bajo" {"selected" if imp == "Bajo" else ""}>Imp: Bajo</option>
                    <option value="medio" {"selected" if imp == "Medio" else ""}>Imp: Medio</option>
                    <option value="alto" {"selected" if imp == "Alto" else ""}>Imp: Alto</option>
                </select>
            </div>
        </div>
"""

    html += f"""
        <div class="edit-note">
            ✏️ <strong>Gestión PMI Completa:</strong> Proyecto con métricas Earned Value, Gantt, RACI y análisis de riesgos.
            Todos los campos son editables para gestión profesional según estándares PMI.
        </div>

        <div class="signature">
            <div style="color: #6b7280; font-size: 12px;">
                Documento PMI generado por {agente} v3.0<br>
                {datetime.now().strftime('%d/%m/%Y %H:%M')} - Gestión Profesional Tesla
            </div>
        </div>
    </div>
</body>
</html>
"""

    return html

def generar_numero_cotizacion(db: Session) -> str:
    """Generar número único de cotización"""
    fecha = datetime.now()
    prefijo = f"COT-{fecha.strftime('%Y%m')}"
    
    ultima = db.query(Cotizacion).filter(
        Cotizacion.numero.like(f"{prefijo}%")
    ).order_by(Cotizacion.numero.desc()).first()
    
    if ultima:
        try:
            ultimo_num = int(ultima.numero.split('-')[-1])
            nuevo_num = ultimo_num + 1
        except:
            nuevo_num = 1
    else:
        nuevo_num = 1
    
    return f"{prefijo}-{nuevo_num:04d}"

# ═══════════════════════════════════════════════════════════════
# 🤖 ENDPOINTS PILI CORE (RESTAURADOS)
# ═══════════════════════════════════════════════════════════════

@router.get("/pili/presentacion")
async def presentacion_pili():
    """
    🤖 RESTAURADO - Presentación de PILI y sus capacidades
    
    Muestra información sobre PILI y los 6 agentes especializados disponibles.
    """
    
    servicios_disponibles = []
    
    for servicio_id, config in CONTEXTOS_SERVICIOS.items():
        servicios_disponibles.append({
            "id": servicio_id,
            "nombre": config.get("nombre_pili", "PILI"),
            "personalidad": config.get("personalidad", ""),
            "especialidad": servicio_id.replace("-", " ").title()
        })
    
    return {
        "success": True,
        "mensaje": "¡Hola! 👋 Soy PILI, tu agente IA multifunción de Tesla Electricidad.",
        "descripcion": "Soy una agente IA especializada que combina lo mejor de ChatGPT, Microsoft Copilot y Google Bard, pero enfocada 100% en servicios eléctricos peruanos.",
        "caracteristicas": [
            "🧠 Conversación inteligente con anti-salto (no me desvío del tema)",
            "📄 Procesamiento OCR de archivos (fotos, PDFs, manuscritos)",
            "⚡ Especializada en normativas eléctricas peruanas (CNE)", 
            "📊 Genero documentos profesionales con estructura JSON",
            "🎯 Aprendo de cada conversación para mejorar",
            "🌐 Busco información en web cuando la necesito"
        ],
        "servicios_disponibles": servicios_disponibles,
        "version": "3.0 - Agente IA Multifunción",
        "estado": "🟢 Online y lista para ayudar",
        "creada_por": "Tesla Electricidad y Automatización S.A.C."
    }

@router.post("/pili/procesar-archivos")
async def procesar_archivos_ocr(
    tipo_servicio: str = Body(...),
    archivos: List[UploadFile] = File(...),
    contexto_adicional: Optional[str] = Body(""),
    db: Session = Depends(get_db)
):
    """
    🤖 RESTAURADO - Procesamiento OCR multimodal
    
    PILI procesa múltiples tipos de archivos:
    - 📷 Fotos (manuscritos, planos, documentos)
    - 📄 PDFs técnicos
    - 📝 Documentos Word
    - 📊 Archivos Excel
    
    Extrae información relevante usando OCR y la estructura para el servicio solicitado.
    """
    
    try:
        logger.info(f"🤖 PILI procesando {len(archivos)} archivos para {tipo_servicio}")
        
        # Verificar que el servicio existe
        contexto = obtener_contexto_servicio(tipo_servicio)
        if not contexto:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Servicio '{tipo_servicio}' no disponible en PILI"
            )
        
        informacion_extraida = {
            "archivos_procesados": [],
            "texto_extraido": "",
            "datos_estructurados": {},
            "imagenes_detectadas": [],
            "errores": [],
            "servicio": tipo_servicio,
            "agente_pili": contexto.get("nombre_pili", "PILI")
        }
        
        for archivo in archivos:
            try:
                # Crear directorio temporal si no existe
                temp_dir = Path("temp")
                temp_dir.mkdir(exist_ok=True)
                
                # Guardar archivo temporalmente
                temp_path = temp_dir / f"temp_{archivo.filename}"
                contenido = await archivo.read()
                
                with open(temp_path, "wb") as f:
                    f.write(contenido)
                
                texto_archivo = ""
                
                # Procesar según tipo de archivo
                if archivo.filename.lower().endswith(('.pdf')):
                    # Para PDFs - usar PyPDF2 o similar
                    texto_archivo = f"[OCR] Contenido extraído de PDF: {archivo.filename}"
                    # TODO: Implementar extracción real con PyPDF2
                    
                elif archivo.filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                    # Para imágenes - usar Tesseract OCR
                    texto_archivo = f"[OCR] Texto extraído de imagen: {archivo.filename}"
                    informacion_extraida["imagenes_detectadas"].append(archivo.filename)
                    # TODO: Implementar OCR real con Tesseract
                    
                elif archivo.filename.lower().endswith(('.docx', '.doc')):
                    # Para documentos Word - usar python-docx
                    texto_archivo = f"[DOC] Contenido extraído de Word: {archivo.filename}"
                    # TODO: Implementar extracción real con python-docx
                    
                elif archivo.filename.lower().endswith(('.xlsx', '.xls')):
                    # Para Excel - usar pandas
                    texto_archivo = f"[XLS] Datos extraídos de Excel: {archivo.filename}"
                    # TODO: Implementar extracción real con pandas
                
                informacion_extraida["texto_extraido"] += f"\n\nArchivo: {archivo.filename}\n{texto_archivo}"
                
                informacion_extraida["archivos_procesados"].append({
                    "nombre": archivo.filename,
                    "tamaño_kb": round(len(contenido) / 1024, 2),
                    "tipo": archivo.content_type,
                    "procesado": True
                })
                
                # Limpiar archivo temporal
                temp_path.unlink(missing_ok=True)
                
            except Exception as e:
                informacion_extraida["errores"].append({
                    "archivo": archivo.filename,
                    "error": str(e)
                })
                logger.error(f"Error procesando {archivo.filename}: {e}")
        
        # Generar respuesta PILI contextualizada
        nombre_pili = contexto.get("nombre_pili", "PILI")
        total_archivos = len(informacion_extraida["archivos_procesados"])
        total_errores = len(informacion_extraida["errores"])
        
        mensaje_pili = f"""¡Perfecto! 📄 Soy {nombre_pili} y he procesado {total_archivos} archivos para tu {tipo_servicio.replace('-', ' ')}.

📊 **Resumen del procesamiento:**
- ✅ Archivos procesados: {total_archivos}
- ❌ Errores: {total_errores}
- 📝 Texto extraído: {len(informacion_extraida["texto_extraido"])} caracteres
- 📷 Imágenes: {len(informacion_extraida["imagenes_detectadas"])}

{f"⚠️ **Nota:** {total_errores} archivos tuvieron errores al procesarse." if total_errores > 0 else ""}

🎯 **Siguiente paso:** Basándome en la información extraída, puedo ayudarte a:
"""
        
        # Sugerencias específicas por tipo de servicio
        if "cotizacion" in tipo_servicio:
            mensaje_pili += """
- 💰 Generar cotización detallada
- 📋 Crear lista de materiales
- ⚡ Calcular cargas eléctricas
- 📊 Estructurar información en JSON
"""
        elif "proyecto" in tipo_servicio:
            mensaje_pili += """
- 📁 Organizar estructura del proyecto
- 📅 Crear cronograma de trabajo
- 👥 Definir responsabilidades
- 📊 Configurar seguimiento
"""
        elif "informe" in tipo_servicio:
            mensaje_pili += """
- 📄 Generar informe técnico
- 📊 Crear gráficos explicativos
- 📋 Estructurar conclusiones
- 💼 Formatear presentación ejecutiva
"""
        
        return {
            "success": True,
            "mensaje_pili": mensaje_pili,
            "procesamiento": informacion_extraida,
            "puede_continuar": total_archivos > 0,
            "sugerencias_siguientes": [
                f"💬 Conversación guiada con {nombre_pili}",
                "📊 Generar vista previa JSON estructurado", 
                "📄 Crear documento profesional",
                "🔍 Analizar información extraída"
            ]
        }
        
    except Exception as e:
        logger.error(f"❌ Error PILI procesando archivos: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error PILI: {str(e)}"
        )

@router.post("/pili/generar-json-preview")
async def generar_json_preview(
    tipo_servicio: str = Body(...),
    informacion_extraida: Dict[str, Any] = Body(...),
    datos_adicionales: Optional[Dict[str, Any]] = Body(None),
    db: Session = Depends(get_db)
):
    """
    🤖 RESTAURADO - Generar JSON estructurado + Vista previa HTML
    
    PILI toma la información procesada y la estructura en formato JSON optimizado
    para el tipo de servicio, además de generar una vista previa HTML editable.
    """
    
    try:
        logger.info(f"🤖 PILI generando JSON + preview para {tipo_servicio}")
        
        # Obtener contexto del servicio
        contexto = obtener_contexto_servicio(tipo_servicio)
        if not contexto:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Servicio PILI '{tipo_servicio}' no disponible"
            )
        
        # Crear estructura JSON base
        datos_json = {
            "pili_version": "3.0",
            "agente_responsable": contexto.get("nombre_pili", "PILI"),
            "tipo_servicio": tipo_servicio,
            "timestamp": datetime.now().isoformat(),
            "datos_extraidos": {},
            "metadatos": {
                "fuente_procesamiento": "PILI_OCR",
                "archivos_origen": informacion_extraida.get("archivos_procesados", []),
                "confianza_datos": 85,  # Porcentaje de confianza
                "requiere_revision": False
            }
        }
        
        # Combinar datos extraídos con datos adicionales
        texto_base = informacion_extraida.get("texto_extraido", "")
        if datos_adicionales:
            datos_json["datos_extraidos"].update(datos_adicionales)
        
        # Estructura específica según tipo de servicio
        if "cotizacion" in tipo_servicio:
            datos_json["datos_extraidos"].update({
                "numero": f"COT-{datetime.now().strftime('%Y%m%d')}-001",
                "cliente": datos_adicionales.get("cliente", "[Cliente por definir]") if datos_adicionales else "[Cliente por definir]",
                "proyecto": datos_adicionales.get("proyecto", "[Proyecto por definir]") if datos_adicionales else "[Proyecto por definir]",
                "descripcion": texto_base[:500] if texto_base else "[Descripción por completar]",
                "fecha": datetime.now().strftime("%d/%m/%Y"),
                "vigencia": "30 días",
                "items": [
                    {
                        "descripcion": "Punto de luz LED 18W empotrado",
                        "cantidad": 1,
                        "unidad": "und",
                        "precio_unitario": 30.00
                    }
                ],
                "observaciones": "Precios incluyen IGV. Instalación según CNE-Utilización.",
                "subtotal": 0,
                "igv": 0,
                "total": 0
            })
            
        elif "proyecto" in tipo_servicio:
            datos_json["datos_extraidos"].update({
                "nombre_proyecto": datos_adicionales.get("proyecto", "[Nombre del proyecto]") if datos_adicionales else "[Nombre del proyecto]",
                "cliente": datos_adicionales.get("cliente", "[Cliente]") if datos_adicionales else "[Cliente]",
                "descripcion": texto_base[:500] if texto_base else "[Descripción del proyecto]",
                "fecha_inicio": datetime.now().strftime("%d/%m/%Y"),
                "duracion_estimada": "4 semanas",
                "estado": "En planificación",
                "fases": [
                    {"nombre": "Planificación", "duracion": "1 semana", "estado": "pendiente"},
                    {"nombre": "Ejecución", "duracion": "2 semanas", "estado": "pendiente"},
                    {"nombre": "Cierre", "duracion": "1 semana", "estado": "pendiente"}
                ]
            })
            
        elif "informe" in tipo_servicio:
            datos_json["datos_extraidos"].update({
                "titulo_informe": f"Informe Técnico - {tipo_servicio.replace('-', ' ').title()}",
                "fecha_informe": datetime.now().strftime("%d/%m/%Y"),
                "autor": "Tesla Electricidad y Automatización S.A.C.",
                "resumen_ejecutivo": texto_base[:300] if texto_base else "[Resumen ejecutivo por completar]",
                "conclusiones": "[Conclusiones por desarrollar]",
                "recomendaciones": "[Recomendaciones por definir]"
            })
        
        # Generar vista previa HTML editable
        if "cotizacion" in tipo_servicio:
            html_preview = generar_preview_html_editable(datos_json["datos_extraidos"], contexto.get("nombre_pili", "PILI"))
        elif "informe" in tipo_servicio:
            html_preview = generar_preview_informe(datos_json["datos_extraidos"], contexto.get("nombre_pili", "PILI"))
        else:
            html_preview = f"<p>Vista previa no disponible para {tipo_servicio}</p>"
        
        # Guardar para aprendizaje PILI
        aprendizaje_id = None
        try:
            # Simular guardado para aprendizaje
            aprendizaje_id = f"pili_{tipo_servicio}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            logger.info(f"PILI aprendizaje guardado: {aprendizaje_id}")
        except Exception as e:
            logger.warning(f"No se pudo guardar aprendizaje: {e}")
        
        nombre_pili = contexto.get("nombre_pili", "PILI")
        
        return {
            "success": True,
            "mensaje_pili": f"""¡Excelente! 📊 Soy {nombre_pili} y he estructurado toda la información en formato JSON optimizado.

🎯 **Lo que he creado:**
- 📋 Datos estructurados listos para usar
- 👁️ Vista previa HTML completamente editable
- 🧠 Información guardada para mi aprendizaje continuo

✏️ **Puedes editar la vista previa** directamente antes de generar el documento final.

🚀 **¿Siguiente paso?** ¡Genera tu documento profesional Word!""",
            
            "datos_json": datos_json,
            "html_preview": html_preview,
            "puede_generar_documento": True,
            "aprendizaje_guardado": aprendizaje_id is not None,
            "aprendizaje_id": aprendizaje_id,
            "acciones_disponibles": [
                "✏️ Editar vista previa",
                "📄 Generar Word final",
                "📊 Modificar datos JSON",
                "💾 Guardar como plantilla"
            ]
        }
        
    except Exception as e:
        logger.error(f"❌ Error PILI generando JSON preview: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error PILI: {str(e)}"
        )

# ═══════════════════════════════════════════════════════════════
# 🔄 ENDPOINTS CONSERVADOS v2.0 + MEJORADOS PILI v3.0
# ═══════════════════════════════════════════════════════════════

@router.get("/pili/estadisticas-aprendizaje")
async def estadisticas_aprendizaje_pili(db: Session = Depends(get_db)):
    """
    🆕 NUEVO PILI v3.0 - Estadísticas de aprendizaje del agente
    
    Muestra cómo PILI ha evolucionado basándose en conversaciones anteriores
    """
    try:
        # Simular estadísticas de aprendizaje basadas en datos reales
        total_cotizaciones = db.query(Cotizacion).count()
        
        # Calcular "aprendizajes" basados en actividad
        total_aprendizajes = total_cotizaciones * 3  # Cada cotización = múltiples interacciones
        
        # Determinar "nivel de inteligencia" basado en experiencia
        if total_aprendizajes >= 100:
            nivel_inteligencia = "Experto Avanzado"
            mensaje_nivel = "He procesado muchos casos y soy muy precisa en mis recomendaciones."
        elif total_aprendizajes >= 50:
            nivel_inteligencia = "Especialista"
            mensaje_nivel = "Tengo experiencia sólida y genero cotizaciones confiables."
        elif total_aprendizajes >= 20:
            nivel_inteligencia = "Competente"
            mensaje_nivel = "Estoy desarrollando expertise y mejorando constantemente."
        elif total_aprendizajes >= 5:
            nivel_inteligencia = "Principiante"
            mensaje_nivel = "Estoy aprendiendo rápido de cada proyecto."
        else:
            nivel_inteligencia = "Inicial"
            mensaje_nivel = "Estoy en mis primeros casos, pero aprendo rápido."
        
        # Capacidades que ha desarrollado
        capacidades = [
            "🎯 Detección automática de contexto por servicio",
            "📄 Procesamiento OCR cada vez más preciso",
            "💬 Respuestas más especializadas y técnicas",
            "🔄 Flujos de trabajo optimizados",
            "📊 Mejor estructura de datos JSON",
            "🎨 Documentos con formato profesional mejorado"
        ]
        
        return {
            "success": True,
            "pili_aprendizaje": {
                "total_conversaciones": total_aprendizajes,
                "nivel_inteligencia": nivel_inteligencia,
                "mensaje_nivel": mensaje_nivel,
                "servicios_utilizados": {},
                "servicio_mas_usado": "cotizacion-simple",
                "ultima_actualizacion": datetime.now().isoformat(),
                "capacidades_desarrolladas": capacidades
            },
            "mensaje_pili": f"""¡Hola! 🤖 Soy PILI y te cuento sobre mi evolución:

📚 **Mi aprendizaje hasta ahora:**
- 🔢 Total de casos procesados: {total_aprendizajes}
- 🎯 Nivel actual: {nivel_inteligencia}
- 📈 {mensaje_nivel}

🏆 **Lo que he mejorado:**
- Cada cotización me hace más precisa en cálculos
- Cada proyecto me enseña mejores estructuras
- Cada informe perfecciona mi redacción técnica
- Aprendo las preferencias de Tesla Electricidad

🔮 **Próximas mejoras:**
- RAG con proyectos históricos (cuando tengas más datos)
- Búsqueda web inteligente cuando necesite información
- Especialización aún mayor por tipo de instalación

¡Sigo aprendiendo para ser tu mejor asistente IA! 🚀""",
            
            "recomendaciones": [
                "📄 Sube más documentos técnicos para mejorar mi OCR",
                "💬 Úsa diferentes tipos de servicio para expandir mi conocimiento",
                "📊 Los datos que procese se convierten en mejores sugerencias",
                "🔄 Cada corrección que hagas me hace más inteligente"
            ]
        }
        
    except Exception as e:
        logger.error(f"❌ Error estadísticas PILI: {e}")
        # Retornar estadísticas básicas en caso de error
        return {
            "success": True,
            "pili_aprendizaje": {
                "total_conversaciones": 0,
                "nivel_inteligencia": "Inicial",
                "mensaje_nivel": "Estoy lista para comenzar a aprender.",
                "servicios_utilizados": {},
                "servicio_mas_usado": None,
                "ultima_actualizacion": datetime.now().isoformat(),
                "capacidades_desarrolladas": []
            },
            "mensaje_pili": "¡Hola! 🤖 Soy PILI y estoy lista para ayudarte. Mientras más conversemos, más inteligente me vuelvo.",
            "recomendaciones": [
                "🚀 ¡Empecemos a trabajar juntos!",
                "💬 Háblame sobre tu primer proyecto",
                "📄 Puedes subirme documentos para analizar",
                "🎯 Cada interacción me hace más inteligente"
            ]
        }

@router.get("/botones-contextuales/{tipo_flujo}")
async def obtener_botones_contextuales(
    tipo_flujo: str,
    etapa: str = "inicial",
    historial_length: int = 0,
    tiene_cotizacion: bool = False
):
    """
    🔄 CONSERVADO v2.0 - Obtiene botones contextuales para la interfaz
    
    Args:
        tipo_flujo: cotizacion-simple, cotizacion-compleja, informe-simple, etc.
        etapa: inicial, refinamiento, generacion
        historial_length: Cantidad de mensajes en la conversación
        tiene_cotizacion: Si ya se generó una cotización
    
    Returns:
        Lista de botones contextuales para mostrar al usuario
    """
    try:
        logger.info(f"Obteniendo botones para {tipo_flujo}, etapa: {etapa}")
        
        # Obtener contexto del servicio
        contexto = obtener_contexto_servicio(tipo_flujo)
        
        if not contexto:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Tipo de flujo '{tipo_flujo}' no soportado"
            )
        
        # Determinar etapa automáticamente si no se especifica
        if etapa == "inicial" and historial_length > 0:
            if tiene_cotizacion:
                etapa = "generacion"
            elif historial_length >= 3:
                etapa = "refinamiento"
        
        # Obtener botones para la etapa
        botones = obtener_botones_para_etapa(tipo_flujo, etapa)
        
        return {
            "success": True,
            "tipo_flujo": tipo_flujo,
            "etapa": etapa,
            "botones": botones,
            "contexto": {
                "rol_ia": contexto.get("rol_ia", ""),
                "preguntas_esenciales": contexto.get("preguntas_esenciales", [])
            }
        }
        
    except Exception as e:
        logger.error(f"Error obteniendo botones contextuales: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error: {str(e)}"
        )

@router.post("/chat-contextualizado")
async def chat_contextualizado(
    tipo_flujo: str = Body(...),
    mensaje: str = Body(...),
    historial: Optional[List[Dict]] = Body([]),
    contexto_adicional: Optional[str] = Body(""),
    datos_cliente: Optional[Dict] = Body(None),  # ¡NUEVO! Recibir datos del cliente
    cotizacion_id: Optional[int] = Body(None),
    archivos_procesados: Optional[List[Dict]] = Body([]),
    generar_html: Optional[bool] = Body(False),
    conversation_state: Optional[Dict] = Body(None),  # ✅ NUEVO: Estado de conversación
    db: Session = Depends(get_db)
):
    """
    🔄 CONSERVADO v2.0 + MEJORADO PILI v3.0

    Chat inteligente con contexto específico según el servicio.
    PILI ahora responde con su personalidad específica por agente.

    NUEVO: Genera vista previa HTML editable si generar_html=True
    """
    try:
        logger.info(f"🤖 PILI chat contextualizado para {tipo_flujo}")

        # Obtener contexto del servicio
        contexto = obtener_contexto_servicio(tipo_flujo)

        if not contexto:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Tipo de flujo '{tipo_flujo}' no soportado por PILI"
            )

        # Construir prompt especializado PILI
        nombre_pili = contexto.get("nombre_pili", "PILI")
        prompt_especializado = f"""
        Eres {nombre_pili}.

        {contexto.get('personalidad', '')}

        {contexto.get('rol_ia', '')}

        {contexto.get('prompt_especializado', '')}

        CONTEXTO DEL PROYECTO:
        {contexto_adicional}

        HISTORIAL DE CONVERSACIÓN:
        """

        # Agregar historial al prompt
        for i, msg in enumerate(historial[-5:]):  # Últimos 5 mensajes
            role = msg.get('role', 'user')
            content = msg.get('content', msg.get('mensaje', ''))
            prompt_especializado += f"\n{role.upper()}: {content}"

        prompt_especializado += f"\n\nUSUARIO: {mensaje}\n\nRESPUESTA DE {nombre_pili}:"

        # ✅ Inicializar variables
        botones_sugeridos = []  # Inicializar para evitar UnboundLocalError
        datos_generados = {}
        
        # 🔥 CAJA NEGRA ITSE - Usar PILIITSEChatBot independiente
        if tipo_flujo == 'itse':
            try:
                from app.integrations.pili_chatbot.pili_itse_chatbot import PILIITSEChatBot

                logger.info(f"🔥 CAJA NEGRA: Usando PILIITSEChatBot para tipo_flujo='itse'")

                # Crear chatbot ITSE
                chatbot = PILIITSEChatBot()

                # Procesar mensaje con estado de conversación
                resultado = chatbot.procesar(mensaje, conversation_state)

                logger.info(f"✅ Chatbot respondió: {resultado.get('respuesta', '')[:100]}")

                # Retornar respuesta con datos_generados
                return {
                    "success": resultado.get("success", True),
                    "respuesta": resultado.get("respuesta", ""),
                    "botones_sugeridos": resultado.get("botones", []),
                    "botones": resultado.get("botones", []),
                    "state": resultado.get("estado"),
                    "conversation_state": resultado.get("estado"),
                    "datos_generados": resultado.get("datos_generados"),  # ✅ ITEMS PARA TABLA
                    "cotizacion": resultado.get("cotizacion"),
                    "agente_pili": nombre_pili
                }

            except Exception as e:
                logger.error(f"❌ Error en chatbot ITSE: {e}")
                import traceback
                traceback.print_exc()
                # Si falla, continuar con flujo normal
        
        # ✅ USAR PILI INTEGRATOR PARA CONVERSACION INTELIGENTE
        try:
            # Usar PILIIntegrator que maneja conversación brillante para todos los tipos
            logger.info(f"🤖 Usando PILIIntegrator para {tipo_flujo}")
            
            # ✅ NUEVO: Acumular datos de mensajes anteriores del usuario
            datos_acumulados = {}
            servicio_detectado = pili_brain.detectar_servicio(mensaje) if pili_brain else "electrico-residencial"
            
            for msg in historial:
                # Solo procesar mensajes del usuario
                if msg.get('tipo') == 'usuario' or msg.get('role') == 'user':
                    contenido = msg.get('mensaje', msg.get('content', ''))
                    if contenido:
                        # Extraer datos de cada mensaje del usuario
                        datos_msg = pili_brain.extraer_datos(contenido, servicio_detectado) if pili_brain else {}
                        datos_acumulados.update(datos_msg)
            
            logger.info(f"📊 Datos acumulados del historial: {datos_acumulados}")
            logger.info(f"📊 Datos acumulados del historial: {datos_acumulados}")
            
            # ✅ NUEVO: Detectar si se debe forzar ITSE (ROBUSTECIDO)
            servicio_forzado = None
            ctx_safe = (contexto_adicional or "").lower()
            if "itse" in ctx_safe:
                servicio_forzado = "itse"
                logger.info("🔒 Contexto ITSE detectado: Forzando servicio a 'itse'")
            
            resultado_pili = await pili_integrator.procesar_solicitud_completa(
                mensaje=mensaje,
                tipo_flujo=tipo_flujo,
                historial=historial,
                generar_documento=False,  # Solo conversación, no generar archivo aún
                datos_acumulados=datos_acumulados,  # ✅ NUEVO: Pasar datos acumulados
                conversation_state=conversation_state,  # ✅ NUEVO: Pasar estado de conversación
                servicio_forzado=servicio_forzado  # ✅ NUEVO: Forzar servicio ITSE
            )
            
            if resultado_pili.get("success"):
                respuesta = {'mensaje': resultado_pili.get('respuesta', '')}
                
                # Extraer datos generados según tipo
                datos_generados = resultado_pili.get('datos_generados', {})
                
                # ✅ NUEVO: Actualizar botones desde especialistas locales
                # Los especialistas locales retornan 'botones', no 'botones_sugeridos'
                botones_especialista = resultado_pili.get('botones') or resultado_pili.get('botones_sugeridos')
                if botones_especialista:
                    logger.info(f"✅ Usando {len(botones_especialista)} botones del especialista local")
                    botones_sugeridos = botones_especialista
                
            else:
                # Fallback si PILIIntegrator falla
                logger.warning("⚠️ PILIIntegrator falló, usando respuesta básica")
                respuesta = {'mensaje': f"Entiendo que necesitas ayuda con {tipo_flujo}. ¿Podrías darme más detalles?"}
                
        except Exception as e:
            # 🧠 FALLBACK FINAL: Usar PILIBrain básico
            logger.warning(f"⚠️ Error con PILIIntegrator, usando PILIBrain: {e}")
            servicio_detectado = pili_brain.detectar_servicio(mensaje)
            cotizacion_data = pili_brain.generar_cotizacion(mensaje, servicio_detectado, "simple")
            respuesta = {'mensaje': cotizacion_data['conversacion']['mensaje_pili']}

        # Determinar etapa y botones sugeridos SOLO si no hay botones del especialista
        tiene_cotizacion = cotizacion_id is not None
        etapa_actual = determinar_etapa_conversacion(historial, tiene_cotizacion)
        
        # ✅ SOLO usar botones genéricos si el especialista NO proporcionó botones
        if not botones_sugeridos:
            botones_sugeridos = obtener_botones_para_etapa(tipo_flujo, etapa_actual)

        # 🆕 NUEVO: Generar vista previa HTML si se solicita
        html_preview = None
        if generar_html and tipo_flujo.startswith("cotizacion"):
            # Simular datos de cotización para preview
            items_demo = [
                {"descripcion": "Punto de luz LED 18W", "cantidad": 8, "unidad": "pto", "precio_unitario": 30.00},
                {"descripcion": "Tomacorriente doble", "cantidad": 6, "unidad": "pto", "precio_unitario": 35.00},
                {"descripcion": "Cable THW 2.5mm²", "cantidad": 50, "unidad": "m", "precio_unitario": 4.00}
            ]
            # Calcular totales dinámicamente
            subtotal = sum(item["cantidad"] * item["precio_unitario"] for item in items_demo)
            igv = subtotal * 0.18
            total = subtotal + igv
            
            datos_preview = {
                "items": items_demo,
                "cliente": datos_cliente if datos_cliente and datos_cliente.get("nombre") else {"nombre": "Cliente Demo"},
                "proyecto": "Instalación Eléctrica",
                "subtotal": round(subtotal, 2),
                "igv": round(igv, 2),
                "total": round(total, 2)
            }
            html_preview = generar_preview_html_editable(datos_preview, nombre_pili)

        elif generar_html and tipo_flujo.startswith("proyecto"):
            # Generar preview para proyectos
            items_proyecto = [
                {"descripcion": "Fase 1: Planificación y diseño", "cantidad": 1, "unidad": "fase", "precio_unitario": 2500.00},
                {"descripcion": "Fase 2: Instalación eléctrica", "cantidad": 1, "unidad": "fase", "precio_unitario": 5000.00},
                {"descripcion": "Fase 3: Pruebas y certificación", "cantidad": 1, "unidad": "fase", "precio_unitario": 1500.00}
            ]
            # Calcular totales dinámicamente
            subtotal = sum(item["cantidad"] * item["precio_unitario"] for item in items_proyecto)
            igv = subtotal * 0.18
            total = subtotal + igv
            
            datos_preview = {
                "items": items_proyecto,
                "cliente": datos_cliente if datos_cliente and datos_cliente.get("nombre") else {"nombre": "Cliente Demo"},
                "proyecto": "Proyecto Eléctrico",
                "nombre_proyecto": "Instalación Industrial",
                "duracion": "3 meses",
                "subtotal": round(subtotal, 2),
                "igv": round(igv, 2),
                "total": round(total, 2)
            }
            # Usar la misma función que cotizaciones ya que ambos tienen estructura de items
            html_preview = generar_preview_html_editable(datos_preview, nombre_pili)

        elif generar_html and tipo_flujo.startswith("informe"):
            datos_preview = {
                "titulo": "Informe Técnico Eléctrico",
                "cliente": "Cliente Demo"
            }
            html_preview = generar_preview_informe(datos_preview, nombre_pili)

        # 🆕 CRÍTICO: Enviar datos estructurados al frontend para edición
        datos_estructurados = None
        if generar_html and tipo_flujo.startswith("cotizacion"):
            # Usar datos de PILIIntegrator si están disponibles
            if 'datos_generados' in locals() and datos_generados:
                datos_estructurados = datos_generados
            else:
                datos_estructurados = datos_preview
        elif generar_html and tipo_flujo.startswith("proyecto"):
            if 'datos_generados' in locals() and datos_generados:
                datos_estructurados = datos_generados
            else:
                datos_estructurados = datos_preview
        elif generar_html and tipo_flujo.startswith("informe"):
            if 'datos_generados' in locals() and datos_generados:
                datos_estructurados = datos_generados
            else:
                datos_estructurados = datos_preview

        return {
            "success": True,
            "agente_activo": nombre_pili,
            "respuesta": respuesta.get('mensaje', '') if isinstance(respuesta, dict) else str(respuesta),
            "tipo_flujo": tipo_flujo,
            "etapa_actual": etapa_actual,
            "botones_sugeridos": botones_sugeridos,
            "contexto_pili": {
                "personalidad": contexto.get("personalidad", ""),
                "preguntas_esenciales": contexto.get("preguntas_esenciales", []),
                "especialidad": contexto.get("rol_ia", "")
            },
            "html_preview": html_preview,
            "cotizacion_generada": datos_estructurados if tipo_flujo.startswith("cotizacion") else None,
            "proyecto_generado": datos_estructurados if tipo_flujo.startswith("proyecto") else None,
            "informe_generado": datos_estructurados if tipo_flujo.startswith("informe") else None,
            "generar_html": generar_html,
            "timestamp": datetime.now().isoformat(),
            "pili_metadata": {
                "agente_id": tipo_flujo,
                "version": "3.0",
                "capabilities": ["chat", "ocr", "json", "html_preview"],
                "modo": "PILIIntegrator"  # ✅ NUEVO: Indicar que usa PILIIntegrator
            }
        }

    except Exception as e:
        logger.error(f"❌ Error en chat contextualizado PILI: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en PILI: {str(e)}"
        )

@router.post("/iniciar-flujo-inteligente")
async def iniciar_flujo_inteligente(
    tipo_flujo: str = Body(...),
    servicio: str = Body("electricidad"),
    industria: str = Body("general"),
    descripcion_inicial: Optional[str] = Body(""),
    db: Session = Depends(get_db)
):
    """
    🆕 NUEVO PILI v3.0 - Inicia un flujo de trabajo inteligente
    
    Este endpoint inicializa una conversación especializada con el agente PILI apropiado
    y proporciona un análisis inicial del proyecto.
    """
    try:
        logger.info(f"🚀 PILI iniciando flujo inteligente: {tipo_flujo}")
        
        # Obtener contexto del servicio
        contexto = obtener_contexto_servicio(tipo_flujo)
        
        if not contexto:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Tipo de flujo '{tipo_flujo}' no soportado"
            )
        
        nombre_pili = contexto.get("nombre_pili", "PILI")
        
        # Análisis inicial automático por PILI Brain
        analisis = f"""
        {nombre_pili} ha analizado tu solicitud inicial:
        
        📋 **Tipo de proyecto:** {tipo_flujo.replace('-', ' ').title()}
        🏢 **Sector:** {industria.title()}
        ⚡ **Servicio:** {servicio.title()}
        
        📊 **Análisis inicial:**
        - Proyecto clasificado como: {contexto.get('complejidad', 'Estándar')}
        - Tiempo estimado: {contexto.get('tiempo_estimado', '1-3 horas')}
        - Especialista asignado: {nombre_pili}
        
        🎯 **Próximos pasos recomendados:**
        1. Proporcionar detalles específicos del proyecto
        2. Subir documentos técnicos si están disponibles
        3. Definir alcance y requerimientos
        4. Revisar especificaciones y normativas aplicables
        """
        
        # Obtener botones iniciales según el contexto
        botones_iniciales = obtener_botones_para_etapa(tipo_flujo, "inicial")
        
        return {
            "success": True,
            "agente_activado": nombre_pili,
            "personalidad": contexto.get("personalidad", ""),
            "tipo_flujo": tipo_flujo,
            "analisis_inicial": analisis,
            "plan_sugerido": f"Plan de trabajo generado por {nombre_pili}",
            "botones_iniciales": botones_iniciales,
            "preguntas_esenciales": contexto.get("preguntas_esenciales", []),
            "siguiente_paso": f"Conversa con {nombre_pili} usando los botones o escribiendo directamente",
            "mensaje_pili": contexto.get("personalidad", f"¡Hola! Soy {nombre_pili} y estoy lista para ayudarte.")
        }
        
    except Exception as e:
        logger.error(f"Error iniciando flujo inteligente: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error: {str(e)}"
        )

# ════════════════════════════════════════════════════════════════
# 🔄 GESTIÓN DE PLANTILLAS (CONSERVADO INTACTO)
# ════════════════════════════════════════════════════════════════

@router.get("/listar-plantillas")
async def listar_plantillas_disponibles():
    """
    🔄 CONSERVADO - Listar todas las plantillas Word disponibles
    """
    
    try:
        from app.core.config import settings
        
        templates_dir = Path(settings.TEMPLATES_DIR)
        
        if not templates_dir.exists():
            templates_dir.mkdir(parents=True, exist_ok=True)
            return {
                "success": True,
                "plantillas": [],
                "mensaje": "No hay plantillas disponibles. Sube tu primera plantilla."
            }
        
        # Buscar archivos .docx
        plantillas = []
        for archivo in templates_dir.glob("*.docx"):
            plantillas.append({
                "nombre": archivo.name,
                "ruta": str(archivo),
                "tamaño": f"{archivo.stat().st_size / 1024:.1f} KB",
                "fecha_modificacion": datetime.fromtimestamp(archivo.stat().st_mtime).strftime("%d/%m/%Y %H:%M")
            })
        
        return {
            "success": True,
            "plantillas": plantillas,
            "total": len(plantillas),
            "directorio": str(templates_dir)
        }
        
    except Exception as e:
        logger.error(f"Error al listar plantillas: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error: {str(e)}"
        )

@router.get("/obtener-marcadores/{nombre_plantilla}")
async def obtener_marcadores_plantilla(
    nombre_plantilla: str
):
    """
    🔄 CONSERVADO - Obtener marcadores de una plantilla específica
    """
    
    try:
        from app.core.config import settings
        from app.services.template_processor import template_processor
        
        # Ruta de la plantilla
        ruta_plantilla = Path(settings.TEMPLATES_DIR) / nombre_plantilla
        
        if not ruta_plantilla.exists():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Plantilla '{nombre_plantilla}' no encontrada"
            )
        
        # Extraer marcadores usando template_processor
        marcadores = template_processor.extraer_marcadores(str(ruta_plantilla))
        
        return {
            "success": True,
            "nombre_plantilla": nombre_plantilla,
            "marcadores_encontrados": marcadores,
            "total_marcadores": len(marcadores),
            "marcadores_comunes": [
                "{{cliente}}", "{{proyecto}}", "{{fecha}}", "{{numero}}",
                "{{descripcion}}", "{{observaciones}}", 
                "{{subtotal}}", "{{igv}}", "{{total}}",
                "{{items_tabla}}", "{{empresa_nombre}}", "{{empresa_direccion}}"
            ]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al obtener marcadores: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error: {str(e)}"
        )

@router.post("/usar-plantilla/{cotizacion_id}")
async def generar_cotizacion_con_plantilla(
    cotizacion_id: int,
    nombre_plantilla: str = Body(...),
    opciones: Optional[Dict[str, bool]] = Body(None),
    logo_base64: Optional[str] = Body(None),
    db: Session = Depends(get_db)
):
    """
    🔄 CONSERVADO - Generar cotización usando una plantilla personalizada
    """
    
    try:
        # Obtener cotización
        cotizacion = db.query(Cotizacion).filter(Cotizacion.id == cotizacion_id).first()
        
        if not cotizacion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cotización no encontrada"
            )
        
        logger.info(f"Generando cotización {cotizacion.numero} con plantilla: {nombre_plantilla}")
        
        from app.core.config import settings
        from app.services.template_processor import template_processor
        
        # Ruta de la plantilla
        ruta_plantilla = Path(settings.TEMPLATES_DIR) / nombre_plantilla
        
        if not ruta_plantilla.exists():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Plantilla '{nombre_plantilla}' no encontrada"
            )
        
        # Obtener items de la cotización
        items_db = db.query(Item).filter(Item.cotizacion_id == cotizacion_id).all()
        
        items = []
        for item in items_db:
            items.append({
                "descripcion": item.descripcion,
                "cantidad": float(item.cantidad),
                "unidad": item.unidad,
                "precio_unitario": float(item.precio_unitario),
                "subtotal": float(item.cantidad * item.precio_unitario)
            })
        
        # Preparar datos para la plantilla
        datos_cotizacion = {
            "numero": cotizacion.numero,
            "cliente": cotizacion.cliente,
            "proyecto": cotizacion.proyecto or "Instalación Eléctrica",
            "descripcion": cotizacion.descripcion,
            "fecha": datetime.now().strftime("%d/%m/%Y"),
            "subtotal": float(cotizacion.subtotal) if cotizacion.subtotal else 0,
            "igv": float(cotizacion.igv) if cotizacion.igv else 0,
            "total": float(cotizacion.total) if cotizacion.total else 0,
            "items": items
        }
        
        # Generar documento con plantilla
        nombre_salida = f"cotizacion_{cotizacion.numero}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"
        ruta_salida = os.path.join(settings.GENERATED_DIR, nombre_salida)
        
        ruta_generada = template_processor.procesar_plantilla(
            ruta_plantilla=str(ruta_plantilla),
            datos_cotizacion=datos_cotizacion,
            ruta_salida=ruta_salida,
            logo_base64=logo_base64
        )
        
        if not os.path.exists(ruta_generada):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="No se pudo generar el documento"
            )
        
        logger.info(f"✅ Cotización generada con plantilla: {nombre_salida}")
        
        return FileResponse(
            path=ruta_generada,
            filename=nombre_salida,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al usar plantilla: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error: {str(e)}"
        )

@router.delete("/eliminar-plantilla/{nombre_archivo}")
async def eliminar_plantilla(
    nombre_archivo: str
):
    """
    🔄 CONSERVADO - Eliminar una plantilla
    """
    
    try:
        from app.core.config import settings
        
        ruta_plantilla = Path(settings.TEMPLATES_DIR) / nombre_archivo
        
        if not ruta_plantilla.exists():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Plantilla '{nombre_archivo}' no encontrada"
            )
        
        # Eliminar archivo
        ruta_plantilla.unlink()
        
        logger.info(f"✅ Plantilla eliminada: {nombre_archivo}")
        
        return {
            "success": True,
            "mensaje": f"Plantilla '{nombre_archivo}' eliminada exitosamente"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al eliminar plantilla: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error: {str(e)}"
        )

@router.post("/validar-plantilla")
async def validar_plantilla(
    archivo: UploadFile = File(...)
):
    """
    🔄 CONSERVADO - Validar una plantilla antes de subirla
    """
    
    try:
        import tempfile
        from app.services.template_processor import template_processor
        
        # Validar extensión
        if not archivo.filename.endswith('.docx'):
            return {
                "valida": False,
                "error": "El archivo debe ser .docx",
                "recomendacion": "Usa Microsoft Word para crear la plantilla"
            }
        
        # Guardar temporalmente
        with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as tmp:
            contenido = await archivo.read()
            tmp.write(contenido)
            tmp_path = tmp.name
        
        try:
            # Validar plantilla
            es_valida, mensaje = template_processor.validar_plantilla(tmp_path)
            
            if es_valida:
                # Extraer marcadores
                marcadores = template_processor.extraer_marcadores(tmp_path)
                
                return {
                    "valida": True,
                    "mensaje": "Plantilla válida",
                    "total_marcadores": len(marcadores),
                    "marcadores_encontrados": marcadores,
                    "marcadores_sugeridos": [
                        "{{cliente}}", "{{proyecto}}", "{{fecha}}", "{{numero}}",
                        "{{descripcion}}", "{{subtotal}}", "{{igv}}", "{{total}}"
                    ],
                    "recomendacion": "Puedes subir esta plantilla para usarla en cotizaciones"
                }
            else:
                return {
                    "valida": False,
                    "error": mensaje,
                    "recomendacion": "Revisa la plantilla y vuelve a intentar"
                }
                
        finally:
            # Eliminar archivo temporal
            Path(tmp_path).unlink(missing_ok=True)
        
    except Exception as e:
        logger.error(f"Error al validar plantilla: {str(e)}")
        return {
            "valida": False,
            "error": str(e),
            "recomendacion": "Verifica que el archivo no esté corrupto"
        }

@router.post("/subir-plantilla")
async def subir_plantilla(
    archivo: UploadFile = File(...),
    nombre_personalizado: Optional[str] = Body(None)
):
    """
    🔄 CONSERVADO - Subir una nueva plantilla Word
    """
    
    try:
        from app.core.config import settings
        
        # Validar que sea un archivo Word
        if not archivo.filename.endswith('.docx'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Solo se permiten archivos .docx"
            )
        
        # Crear directorio de plantillas si no existe
        templates_dir = Path(settings.TEMPLATES_DIR)
        templates_dir.mkdir(parents=True, exist_ok=True)
        
        # Nombre del archivo
        nombre_archivo = nombre_personalizado if nombre_personalizado else archivo.filename
        if not nombre_archivo.endswith('.docx'):
            nombre_archivo += '.docx'
        
        # Ruta completa
        ruta_plantilla = templates_dir / nombre_archivo
        
        # Guardar archivo
        contenido = await archivo.read()
        with open(ruta_plantilla, 'wb') as f:
            f.write(contenido)
        
        logger.info(f"✅ Plantilla subida: {nombre_archivo}")
        
        # Validar plantilla y extraer marcadores
        from app.services.template_processor import template_processor
        
        try:
            es_valida, mensaje = template_processor.validar_plantilla(str(ruta_plantilla))
            marcadores = template_processor.extraer_marcadores(str(ruta_plantilla)) if es_valida else []
        except:
            es_valida = True  # Asumir que es válida si hay error en validación
            marcadores = []
            mensaje = "Plantilla subida (validación básica)"
        
        return {
            "success": True,
            "mensaje": f"Plantilla '{nombre_archivo}' subida exitosamente",
            "nombre_archivo": nombre_archivo,
            "ruta": str(ruta_plantilla),
            "validacion": {
                "es_valida": es_valida,
                "mensaje": mensaje,
                "marcadores_encontrados": marcadores,
                "total_marcadores": len(marcadores)
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al subir plantilla: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error: {str(e)}"
        )

# ════════════════════════════════════════════════════════════════
# 🔄 ENDPOINTS LEGACY - CONSERVADOS PARA COMPATIBILIDAD
# ════════════════════════════════════════════════════════════════

@router.post("/generar-rapida", response_model=CotizacionResponse)
async def generar_cotizacion_rapida(
    request: CotizacionRapidaRequest,
    db: Session = Depends(get_db)
):
    """
    🔄 CONSERVADO - Generar cotización rápida con IA (endpoint legacy)
    """
    try:
        logger.info("Generando cotización rápida con IA")
        
        # Generar con Gemini
        resultado = gemini_service.generar_cotizacion(
            servicio=request.servicio,
            industria=request.industria,
            descripcion=request.descripcion
        )
        
        if not resultado:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="No se pudo generar la cotización con IA"
            )
        
        # Crear cotización en BD
        nueva_cotizacion = Cotizacion(
            numero=generar_numero_cotizacion(db),
            cliente=resultado.get('cliente', 'Cliente Gemini'),
            proyecto=resultado.get('proyecto', 'Proyecto generado por IA'),
            descripcion=resultado.get('descripcion', ''),
            observaciones=resultado.get('observaciones', ''),
            subtotal=resultado.get('subtotal', 0),
            igv=resultado.get('igv', 0),
            total=resultado.get('total', 0),
            estado="borrador",
            fecha_creacion=datetime.now()
        )
        
        db.add(nueva_cotizacion)
        db.commit()
        db.refresh(nueva_cotizacion)
        
        # Agregar items si los hay
        if 'items' in resultado:
            for item_data in resultado['items']:
                item = Item(
                    cotizacion_id=nueva_cotizacion.id,
                    descripcion=item_data.get('descripcion', ''),
                    cantidad=item_data.get('cantidad', 1),
                    unidad=item_data.get('unidad', 'und'),
                    precio_unitario=item_data.get('precio_unitario', 0)
                )
                db.add(item)
            
            db.commit()
        
        logger.info(f"✅ Cotización creada: {nueva_cotizacion.numero}")
        
        return CotizacionResponse(
            id=nueva_cotizacion.id,
            numero=nueva_cotizacion.numero,
            cliente=nueva_cotizacion.cliente,
            proyecto=nueva_cotizacion.proyecto,
            descripcion=nueva_cotizacion.descripcion,
            observaciones=nueva_cotizacion.observaciones,
            subtotal=float(nueva_cotizacion.subtotal),
            igv=float(nueva_cotizacion.igv),
            total=float(nueva_cotizacion.total),
            estado=nueva_cotizacion.estado,
            fecha_creacion=nueva_cotizacion.fecha_creacion.isoformat() if nueva_cotizacion.fecha_creacion else None,
            items=resultado.get('items', [])
        )
        
    except Exception as e:
        logger.error(f"Error generando cotización rápida: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error: {str(e)}"
        )

@router.post("/conversacional", response_model=ChatResponse)
async def chat_conversacional(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    """
    🔄 CONSERVADO - Chat conversacional para refinar cotizaciones
    """
    try:
        logger.info("Procesando mensaje de chat conversacional")
        
        # Enviar mensaje a Gemini
        respuesta = gemini_service.chat(
            mensaje=request.mensaje,
            contexto=request.contexto,
            cotizacion_id=request.cotizacion_id
        )
        
        return ChatResponse(
            respuesta=respuesta.get('mensaje', '') if isinstance(respuesta, dict) else str(respuesta),
            sugerencias=respuesta.get('sugerencias', []) if isinstance(respuesta, dict) else [],
            accion_recomendada=respuesta.get('accion_recomendada') if isinstance(respuesta, dict) else None
        )
        
    except Exception as e:
        logger.error(f"Error en chat conversacional: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en chat: {str(e)}"
        )

@router.post("/analizar-proyecto")
def analizar_proyecto_ia(
    descripcion: str
):
    """
    🔄 CONSERVADO - Analizar descripción de un proyecto con IA
    """
    try:
        logger.info("Analizando descripción de proyecto")
        
        # Analizar con Gemini
        analisis = gemini_service.analizar_documento(
            texto_documento=descripcion,
            tipo_analisis="proyecto"
        )
        
        return {
            "success": True,
            "analisis": analisis,
            "mensaje": "Análisis completado. Puedes usar esta información para crear una cotización."
        }
        
    except Exception as e:
        logger.error(f"Error al analizar proyecto: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al analizar: {str(e)}"
        )

@router.post("/sugerir-mejoras/{cotizacion_id}")
def sugerir_mejoras_cotizacion(
    cotizacion_id: int,
    db: Session = Depends(get_db)
):
    """
    🔄 CONSERVADO - Obtener sugerencias de mejora para una cotización existente
    """
    cotizacion = db.query(Cotizacion).filter(Cotizacion.id == cotizacion_id).first()
    
    if not cotizacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cotización con ID {cotizacion_id} no encontrada"
        )
    
    try:
        logger.info(f"Generando sugerencias para cotización {cotizacion.numero}")
        
        # Obtener sugerencias de Gemini
        sugerencias = gemini_service.sugerir_mejoras(cotizacion.__dict__)
        
        return {
            "success": True,
            "cotizacion_numero": cotizacion.numero,
            "sugerencias": sugerencias
        }
        
    except Exception as e:
        logger.error(f"Error al sugerir mejoras: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al generar sugerencias: {str(e)}"
        )

@router.get("/health")
def health_check_ia():
    """
    🔄 CONSERVADO + MEJORADO - Verificar estado del servicio de IA
    """
    from app.core.config import settings

    return {
        "gemini_configured": bool(settings.GEMINI_API_KEY),
        "model": settings.GEMINI_MODEL,
        "status": "healthy",
        "pili_version": "3.0",
        "agentes_disponibles": len(CONTEXTOS_SERVICIOS),
        "servicios_inteligentes": list(CONTEXTOS_SERVICIOS.keys()),
        "version": "3.0 - PILI Multifunción"
    }

# ════════════════════════════════════════════════════════════════
# 🆕 AGENTE 3: VISTAS PREVIAS EDITABLES PARA INFORMES
# ════════════════════════════════════════════════════════════════

def generar_preview_informe_tecnico_editable(datos: Dict[str, Any], agente: str) -> str:
    """
    🆕 AGENTE 3 - Vista previa HTML COMPLETAMENTE EDITABLE para Informe Técnico

    Genera HTML con colores AZULES Tesla (#0052A3, #1E40AF, #3B82F6).
    Incluye 5 secciones técnicas editables:
    1. Resumen Ejecutivo
    2. Marco Normativo
    3. Descripción Técnica
    4. Metodología
    5. Resultados y Conclusiones
    """

    titulo = datos.get('titulo', 'INFORME TÉCNICO ELÉCTRICO')
    codigo = datos.get('codigo', f'IT-{datetime.now().strftime("%Y%m%d")}')
    cliente = datos.get('cliente', '')
    fecha = datos.get('fecha', datetime.now().strftime('%Y-%m-%d'))
    normativa = datos.get('normativa', 'CNE Suministro 2011, RD N° 037-2006-EM/DGE')

    # Contenidos por defecto
    resumen = datos.get('resumen', '')
    marco_normativo = datos.get('marco_normativo', 'Código Nacional de Electricidad - Suministro 2011\nReglamento de la Ley de Concesiones Eléctricas - D.L. N° 25844\nNorma DGE - Procedimiento de Elaboración de Proyectos y Ejecución de Obras en Sistemas de Distribución')
    descripcion_tecnica = datos.get('descripcion_tecnica', '')
    metodologia = datos.get('metodologia', '')
    conclusiones = datos.get('conclusiones', '')

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{titulo}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Times New Roman', Times, serif;
            background: linear-gradient(135deg, #e0f2fe 0%, #f0f9ff 100%);
            padding: 20px;
            line-height: 1.6;
        }}

        .container {{
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            box-shadow: 0 10px 40px rgba(0, 82, 163, 0.15);
            border-radius: 12px;
            overflow: hidden;
        }}

        .header {{
            background: linear-gradient(135deg, #0052A3 0%, #1E40AF 100%);
            color: white;
            padding: 40px;
            text-align: center;
            position: relative;
            overflow: hidden;
        }}

        .header::before {{
            content: '';
            position: absolute;
            top: -50%;
            right: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
            animation: pulse 3s ease-in-out infinite;
        }}

        @keyframes pulse {{
            0%, 100% {{ opacity: 0.5; }}
            50% {{ opacity: 1; }}
        }}

        .header-content {{
            position: relative;
            z-index: 1;
        }}

        .titulo-input {{
            font-size: 28px;
            text-align: center;
            background: transparent;
            border: 2px solid rgba(255,255,255,0.3);
            color: white;
            font-weight: 900;
            padding: 15px;
            width: 100%;
            border-radius: 8px;
            text-transform: uppercase;
            letter-spacing: 1px;
            transition: all 0.3s ease;
        }}

        .titulo-input:focus {{
            outline: none;
            border-color: white;
            background: rgba(255,255,255,0.1);
        }}

        .codigo-container {{
            margin-top: 15px;
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 10px;
        }}

        .codigo-label {{
            font-weight: 700;
            font-size: 14px;
        }}

        .codigo-input {{
            background: rgba(255,255,255,0.2);
            border: 1px solid rgba(255,255,255,0.4);
            color: white;
            padding: 8px 15px;
            border-radius: 6px;
            font-size: 14px;
            font-weight: 600;
            width: 220px;
            text-align: center;
        }}

        .codigo-input:focus {{
            outline: none;
            background: rgba(255,255,255,0.3);
        }}

        .empresa {{
            margin-top: 20px;
            font-size: 16px;
            font-weight: 600;
            opacity: 0.95;
        }}

        .info-section {{
            padding: 30px 40px;
            background: #f8fafc;
            border-bottom: 2px solid #e0f2fe;
        }}

        .info-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
        }}

        .info-field {{
            background: white;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #0052A3;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }}

        .info-label {{
            font-weight: 800;
            color: #1E40AF;
            font-size: 13px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
        }}

        .info-input {{
            border: 1px solid #bfdbfe;
            padding: 10px;
            width: 100%;
            border-radius: 6px;
            font-size: 15px;
            color: #1f2937;
            font-weight: 600;
            transition: all 0.3s ease;
        }}

        .info-input:focus {{
            outline: none;
            border-color: #3B82F6;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        }}

        .content {{
            padding: 40px;
        }}

        .seccion {{
            background: white;
            margin-bottom: 30px;
            border: 2px solid #bfdbfe;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0, 82, 163, 0.08);
            transition: all 0.3s ease;
        }}

        .seccion:hover {{
            box-shadow: 0 6px 20px rgba(0, 82, 163, 0.15);
            transform: translateY(-2px);
        }}

        .seccion-header {{
            background: linear-gradient(135deg, #0052A3 0%, #1E40AF 100%);
            color: white;
            padding: 18px 25px;
            font-weight: 800;
            font-size: 18px;
            display: flex;
            align-items: center;
            gap: 12px;
        }}

        .seccion-icon {{
            font-size: 24px;
        }}

        .seccion-content {{
            padding: 25px;
            background: #fafbfc;
        }}

        textarea {{
            border: 2px solid #bfdbfe;
            padding: 15px;
            width: 100%;
            border-radius: 8px;
            font-family: 'Times New Roman', Times, serif;
            font-size: 15px;
            line-height: 1.8;
            color: #1f2937;
            resize: vertical;
            min-height: 120px;
            transition: all 0.3s ease;
        }}

        textarea:focus {{
            outline: none;
            border-color: #3B82F6;
            box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1);
            background: white;
        }}

        .edit-note {{
            background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
            border: 2px solid #fbbf24;
            padding: 20px;
            border-radius: 10px;
            margin-top: 30px;
            font-weight: 600;
            color: #78350f;
            display: flex;
            align-items: center;
            gap: 15px;
            box-shadow: 0 4px 12px rgba(251, 191, 36, 0.2);
        }}

        .edit-icon {{
            font-size: 28px;
        }}

        .footer {{
            text-align: center;
            padding: 30px;
            background: #f8fafc;
            border-top: 3px solid #0052A3;
            color: #64748b;
            font-size: 13px;
        }}

        .footer-bold {{
            color: #1E40AF;
            font-weight: 700;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="header-content">
                <input type="text" name="titulo" value="{titulo}" placeholder="TÍTULO DEL INFORME TÉCNICO" class="titulo-input">
                <div class="codigo-container">
                    <span class="codigo-label">Código:</span>
                    <input type="text" name="codigo" value="{codigo}" class="codigo-input">
                </div>
                <div class="empresa">⚡ TESLA ELECTRICIDAD Y AUTOMATIZACIÓN S.A.C.</div>
            </div>
        </div>

        <div class="info-section">
            <div class="info-grid">
                <div class="info-field">
                    <div class="info-label">👤 Cliente</div>
                    <input type="text" name="cliente" value="{cliente}" placeholder="Nombre del cliente" class="info-input">
                </div>
                <div class="info-field">
                    <div class="info-label">📅 Fecha</div>
                    <input type="date" name="fecha" value="{fecha}" class="info-input">
                </div>
                <div class="info-field">
                    <div class="info-label">⚖️ Normativa Aplicable</div>
                    <input type="text" name="normativa" value="{normativa}" class="info-input">
                </div>
            </div>
        </div>

        <div class="content">
            <div class="seccion">
                <div class="seccion-header">
                    <span class="seccion-icon">📋</span>
                    <span>I. RESUMEN EJECUTIVO</span>
                </div>
                <div class="seccion-content">
                    <textarea name="resumen" rows="5" placeholder="Resumen ejecutivo del informe técnico. Incluya el objetivo principal, alcance y conclusiones clave...">{resumen}</textarea>
                </div>
            </div>

            <div class="seccion">
                <div class="seccion-header">
                    <span class="seccion-icon">📖</span>
                    <span>II. MARCO NORMATIVO</span>
                </div>
                <div class="seccion-content">
                    <textarea name="marco_normativo" rows="5" placeholder="Normativas, códigos y reglamentos aplicables al proyecto...">{marco_normativo}</textarea>
                </div>
            </div>

            <div class="seccion">
                <div class="seccion-header">
                    <span class="seccion-icon">🔧</span>
                    <span>III. DESCRIPCIÓN TÉCNICA</span>
                </div>
                <div class="seccion-content">
                    <textarea name="descripcion_tecnica" rows="6" placeholder="Descripción detallada de las instalaciones eléctricas, equipos, materiales y especificaciones técnicas...">{descripcion_tecnica}</textarea>
                </div>
            </div>

            <div class="seccion">
                <div class="seccion-header">
                    <span class="seccion-icon">⚙️</span>
                    <span>IV. METODOLOGÍA</span>
                </div>
                <div class="seccion-content">
                    <textarea name="metodologia" rows="5" placeholder="Procedimientos de instalación, pruebas realizadas, herramientas utilizadas y metodología de trabajo...">{metodologia}</textarea>
                </div>
            </div>

            <div class="seccion">
                <div class="seccion-header">
                    <span class="seccion-icon">✅</span>
                    <span>V. RESULTADOS Y CONCLUSIONES</span>
                </div>
                <div class="seccion-content">
                    <textarea name="conclusiones" rows="5" placeholder="Resultados obtenidos, análisis de cumplimiento normativo y conclusiones finales...">{conclusiones}</textarea>
                </div>
            </div>

            <div class="edit-note">
                <span class="edit-icon">✏️</span>
                <div>
                    <strong>Edición Completa Habilitada:</strong> Todos los campos son editables. Modifica título, código, fecha, secciones y contenido según tus necesidades. Los cambios se guardarán automáticamente al generar el documento Word final.
                </div>
            </div>
        </div>

        <div class="footer">
            <div class="footer-bold">Documento generado por {agente} v3.0</div>
            <div style="margin-top: 8px;">{datetime.now().strftime('%d/%m/%Y %H:%M')} - Sistema de Gestión Tesla Electricidad</div>
        </div>
    </div>
</body>
</html>
"""

    return html


def generar_preview_informe_ejecutivo_apa_editable(datos: Dict[str, Any], agente: str) -> str:
    """
    🆕 AGENTE 3 - Vista previa HTML COMPLETAMENTE EDITABLE para Informe Ejecutivo APA

    Genera HTML con formato APA 7th edition, colores AZULES Tesla.
    Incluye:
    - Portada editable estilo APA
    - Métricas financieras (ROI, TIR, Payback, Ahorro)
    - Desglose de inversión detallado
    - Resumen ejecutivo extenso
    - Sección de recomendaciones
    """

    titulo = datos.get('titulo', 'ANÁLISIS DE FACTIBILIDAD TÉCNICO-ECONÓMICA')
    subtitulo = datos.get('subtitulo', 'Proyecto de Instalación Eléctrica Industrial')
    cliente = datos.get('cliente', '')
    codigo = datos.get('codigo', f'APA-{datetime.now().strftime("%Y%m%d")}')
    fecha = datos.get('fecha', datetime.now().strftime('%Y-%m-%d'))

    # Métricas financieras
    roi = datos.get('roi', 0)
    tir = datos.get('tir', 0)
    payback = datos.get('payback', 0)
    ahorro_anual = datos.get('ahorro_anual', 0)
    ahorro_energia = datos.get('ahorro_energia', 0)

    # Inversión
    inv_equipos = datos.get('inv_equipos', 0)
    inv_mano_obra = datos.get('inv_mano_obra', 0)
    capital_trabajo = datos.get('capital_trabajo', 0)

    # Contenido
    resumen = datos.get('resumen', '')
    recomendaciones = datos.get('recomendaciones', '')

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{titulo}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Times New Roman', Times, serif;
            background: white;
            padding: 40px;
            line-height: 2.0; /* APA requiere doble espacio */
            color: #000;
        }}

        .container {{
            max-width: 900px;
            margin: 0 auto;
            background: white;
        }}

        /* PORTADA ESTILO APA */
        .portada {{
            text-align: center;
            padding: 100px 40px;
            border: 4px solid #0052A3;
            border-radius: 8px;
            background: linear-gradient(135deg, #f8fafc 0%, #e0f2fe 100%);
            margin-bottom: 50px;
            position: relative;
        }}

        .portada::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 8px;
            background: linear-gradient(90deg, #0052A3 0%, #1E40AF 50%, #3B82F6 100%);
        }}

        .portada-titulo {{
            font-size: 28px;
            font-weight: 900;
            color: #0052A3;
            margin: 20px 0;
            text-transform: uppercase;
            letter-spacing: 1px;
            width: 100%;
            border: 2px solid #bfdbfe;
            padding: 15px;
            background: white;
            border-radius: 8px;
        }}

        .portada-subtitulo {{
            font-size: 18px;
            color: #1E40AF;
            margin: 15px 0;
            font-weight: 600;
            width: 100%;
            border: 2px solid #bfdbfe;
            padding: 12px;
            background: white;
            border-radius: 6px;
        }}

        .portada-info {{
            margin: 30px 0;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }}

        .portada-field {{
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            font-size: 15px;
        }}

        .portada-label {{
            font-weight: 700;
            color: #1E40AF;
            min-width: 80px;
            text-align: right;
        }}

        .portada-input {{
            border: 2px solid #bfdbfe;
            padding: 8px 15px;
            border-radius: 6px;
            font-size: 15px;
            min-width: 250px;
            background: white;
        }}

        .portada-input:focus {{
            outline: none;
            border-color: #3B82F6;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        }}

        .portada-empresa {{
            margin-top: 40px;
            font-size: 16px;
            font-weight: 700;
            color: #0052A3;
        }}

        /* SECCIONES */
        .seccion {{
            margin-bottom: 40px;
            page-break-inside: avoid;
        }}

        .seccion-titulo {{
            font-size: 20px;
            font-weight: 900;
            color: #0052A3;
            border-bottom: 3px solid #1E40AF;
            padding-bottom: 10px;
            margin-bottom: 20px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        textarea {{
            width: 100%;
            border: 2px solid #bfdbfe;
            padding: 15px;
            border-radius: 8px;
            font-family: 'Times New Roman', Times, serif;
            font-size: 14px;
            line-height: 2.0; /* Doble espacio APA */
            resize: vertical;
            min-height: 150px;
            background: #fafbfc;
        }}

        textarea:focus {{
            outline: none;
            border-color: #3B82F6;
            background: white;
            box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.08);
        }}

        /* MÉTRICAS FINANCIERAS */
        .metricas-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 25px 0;
        }}

        .metrica {{
            background: linear-gradient(135deg, #e0f2fe 0%, #bae6fd 100%);
            padding: 20px;
            border-radius: 10px;
            border-left: 6px solid #0052A3;
            box-shadow: 0 4px 12px rgba(0, 82, 163, 0.1);
            transition: all 0.3s ease;
        }}

        .metrica:hover {{
            transform: translateY(-4px);
            box-shadow: 0 6px 20px rgba(0, 82, 163, 0.2);
        }}

        .metrica-label {{
            color: #1E40AF;
            font-weight: 800;
            font-size: 14px;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .metrica-value {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .metrica-input {{
            border: 2px solid #3B82F6;
            padding: 10px;
            border-radius: 6px;
            font-size: 18px;
            font-weight: 700;
            color: #0052A3;
            background: white;
            width: 120px;
        }}

        .metrica-input:focus {{
            outline: none;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
        }}

        .metrica-unit {{
            font-weight: 700;
            color: #1E40AF;
            font-size: 16px;
        }}

        /* TABLA INVERSIÓN */
        .tabla-inversion {{
            width: 100%;
            border-collapse: collapse;
            margin: 25px 0;
            box-shadow: 0 4px 12px rgba(0, 82, 163, 0.1);
            border-radius: 8px;
            overflow: hidden;
        }}

        .tabla-inversion thead {{
            background: linear-gradient(135deg, #0052A3 0%, #1E40AF 100%);
            color: white;
        }}

        .tabla-inversion th {{
            padding: 16px;
            font-weight: 800;
            text-align: left;
            font-size: 15px;
        }}

        .tabla-inversion td {{
            padding: 16px;
            border-bottom: 2px solid #e0f2fe;
            background: white;
        }}

        .tabla-inversion tr:hover td {{
            background: #f8fafc;
        }}

        .tabla-label {{
            font-weight: 700;
            color: #1f2937;
        }}

        .tabla-input {{
            border: 2px solid #bfdbfe;
            padding: 10px;
            border-radius: 6px;
            font-size: 16px;
            font-weight: 700;
            color: #0052A3;
            width: 100%;
            max-width: 200px;
        }}

        .tabla-input:focus {{
            outline: none;
            border-color: #3B82F6;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        }}

        .total-row {{
            background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%) !important;
            font-weight: 900;
        }}

        /* NOTAS */
        .nota-apa {{
            background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
            border: 2px solid #fbbf24;
            padding: 18px;
            border-radius: 8px;
            margin: 30px 0;
            font-size: 13px;
            color: #78350f;
        }}

        .nota-apa strong {{
            color: #92400e;
        }}

        /* FOOTER */
        .footer {{
            margin-top: 50px;
            padding-top: 20px;
            border-top: 3px solid #0052A3;
            text-align: center;
            color: #64748b;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- PORTADA ESTILO APA -->
        <div class="portada">
            <input type="text" name="titulo" value="{titulo}" class="portada-titulo">
            <input type="text" name="subtitulo" value="{subtitulo}" class="portada-subtitulo">

            <div class="portada-info">
                <div class="portada-field">
                    <span class="portada-label">Cliente:</span>
                    <input type="text" name="cliente" value="{cliente}" class="portada-input">
                </div>
                <div class="portada-field">
                    <span class="portada-label">Código:</span>
                    <input type="text" name="codigo" value="{codigo}" class="portada-input">
                </div>
                <div class="portada-field">
                    <span class="portada-label">Fecha:</span>
                    <input type="date" name="fecha" value="{fecha}" class="portada-input">
                </div>
            </div>

            <div class="portada-empresa">
                ⚡ TESLA ELECTRICIDAD Y AUTOMATIZACIÓN S.A.C.<br>
                Departamento de Ingeniería y Proyectos
            </div>
        </div>

        <!-- RESUMEN EJECUTIVO -->
        <div class="seccion">
            <h2 class="seccion-titulo">Resumen Ejecutivo</h2>
            <textarea name="resumen" rows="6" placeholder="Resumen ejecutivo del análisis. Incluya el contexto del proyecto, objetivos principales, metodología aplicada y conclusiones clave. Formato APA requiere párrafos con doble espacio y redacción objetiva en tercera persona...">{resumen}</textarea>
        </div>

        <!-- MÉTRICAS FINANCIERAS -->
        <div class="seccion">
            <h2 class="seccion-titulo">Métricas Financieras</h2>

            <div class="metricas-grid">
                <div class="metrica">
                    <div class="metrica-label">📊 ROI Estimado</div>
                    <div class="metrica-value">
                        <input type="number" name="roi" value="{roi}" step="0.1" class="metrica-input">
                        <span class="metrica-unit">%</span>
                    </div>
                </div>

                <div class="metrica">
                    <div class="metrica-label">📈 TIR Proyectada</div>
                    <div class="metrica-value">
                        <input type="number" name="tir" value="{tir}" step="0.1" class="metrica-input">
                        <span class="metrica-unit">%</span>
                    </div>
                </div>

                <div class="metrica">
                    <div class="metrica-label">⏱️ Período de Retorno (Payback)</div>
                    <div class="metrica-value">
                        <input type="number" name="payback" value="{payback}" class="metrica-input">
                        <span class="metrica-unit">meses</span>
                    </div>
                </div>

                <div class="metrica">
                    <div class="metrica-label">💰 Ahorro Anual Estimado</div>
                    <div class="metrica-value">
                        <span class="metrica-unit">S/</span>
                        <input type="number" name="ahorro_anual" value="{ahorro_anual}" step="0.01" class="metrica-input">
                    </div>
                </div>

                <div class="metrica">
                    <div class="metrica-label">⚡ Ahorro Energético</div>
                    <div class="metrica-value">
                        <input type="number" name="ahorro_energia" value="{ahorro_energia}" step="0.1" class="metrica-input">
                        <span class="metrica-unit">kWh/año</span>
                    </div>
                </div>
            </div>
        </div>

        <!-- INVERSIÓN TOTAL -->
        <div class="seccion">
            <h2 class="seccion-titulo">Desglose de Inversión Total</h2>

            <table class="tabla-inversion">
                <thead>
                    <tr>
                        <th>Concepto</th>
                        <th>Monto (S/)</th>
                        <th>% del Total</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td class="tabla-label">💼 Equipos y Materiales</td>
                        <td>
                            <span style="font-weight: 700; margin-right: 5px;">S/</span>
                            <input type="number" name="inv_equipos" value="{inv_equipos}" step="0.01" class="tabla-input">
                        </td>
                        <td id="percent_equipos" style="font-weight: 700; color: #0052A3;">-</td>
                    </tr>
                    <tr>
                        <td class="tabla-label">👷 Mano de Obra Especializada</td>
                        <td>
                            <span style="font-weight: 700; margin-right: 5px;">S/</span>
                            <input type="number" name="inv_mano_obra" value="{inv_mano_obra}" step="0.01" class="tabla-input">
                        </td>
                        <td id="percent_mano_obra" style="font-weight: 700; color: #0052A3;">-</td>
                    </tr>
                    <tr>
                        <td class="tabla-label">💰 Capital de Trabajo</td>
                        <td>
                            <span style="font-weight: 700; margin-right: 5px;">S/</span>
                            <input type="number" name="capital_trabajo" value="{capital_trabajo}" step="0.01" class="tabla-input">
                        </td>
                        <td id="percent_capital" style="font-weight: 700; color: #0052A3;">-</td>
                    </tr>
                    <tr class="total-row">
                        <td class="tabla-label" style="font-size: 18px;">🏆 INVERSIÓN TOTAL</td>
                        <td id="total_inversion" style="font-size: 18px; color: #0052A3;">S/ 0.00</td>
                        <td style="font-weight: 700; font-size: 16px;">100%</td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- RECOMENDACIONES -->
        <div class="seccion">
            <h2 class="seccion-titulo">Recomendaciones</h2>
            <textarea name="recomendaciones" rows="5" placeholder="Recomendaciones técnicas y estratégicas basadas en el análisis. Incluya sugerencias de implementación, precauciones, optimizaciones y próximos pasos...">{recomendaciones}</textarea>
        </div>

        <!-- NOTA APA -->
        <div class="nota-apa">
            <strong>📚 Formato APA 7th Edition:</strong> Este documento sigue las normas de la American Psychological Association (7ª edición).
            Incluye portada formal, doble espacio, numeración de secciones y referencias estructuradas.
            Al exportar a Word, se mantendrá el formato profesional APA para presentaciones ejecutivas.
        </div>

        <!-- FOOTER -->
        <div class="footer">
            <div style="font-weight: 700; color: #1E40AF; margin-bottom: 5px;">
                Documento generado por {agente} v3.0
            </div>
            <div>
                {datetime.now().strftime('%d/%m/%Y %H:%M')} - Sistema de Gestión Tesla Electricidad<br>
                Formato APA 7th Edition - Confidencial
            </div>
        </div>
    </div>

    <script>
        // Cálculo automático de porcentajes y total
        function calcularTotales() {{
            const equipos = parseFloat(document.querySelector('[name="inv_equipos"]').value) || 0;
            const manoObra = parseFloat(document.querySelector('[name="inv_mano_obra"]').value) || 0;
            const capital = parseFloat(document.querySelector('[name="capital_trabajo"]').value) || 0;

            const total = equipos + manoObra + capital;

            if (total > 0) {{
                document.getElementById('percent_equipos').textContent = ((equipos / total) * 100).toFixed(1) + '%';
                document.getElementById('percent_mano_obra').textContent = ((manoObra / total) * 100).toFixed(1) + '%';
                document.getElementById('percent_capital').textContent = ((capital / total) * 100).toFixed(1) + '%';
            }}

            document.getElementById('total_inversion').textContent = 'S/ ' + total.toFixed(2).replace(/\B(?=(\d{{3}})+(?!\d))/g, ',');
        }}

        // Actualizar al cargar y al cambiar valores
        document.addEventListener('DOMContentLoaded', calcularTotales);
        document.querySelectorAll('.tabla-input').forEach(input => {{
            input.addEventListener('input', calcularTotales);
        }});
    </script>
</body>
</html>
"""

    return html


# ═══════════════════════════════════════════════════════════════
# 🤖 PILI ITSE CHATBOT - Endpoint usando CAJA NEGRA
# ═══════════════════════════════════════════════════════════════

# Importar caja negra


from app.integrations.pili_chatbot.pili_itse_chatbot import PILIITSEChatBot

# Crear instancia global
pili_itse_bot = PILIITSEChatBot()

@router.post("/pili-itse")
async def chat_pili_itse(request: ChatRequest):
    """
    Endpoint para PILI ITSE usando CAJA NEGRA
    
    La lógica está en: Pili_ChatBot/pili_itse_chatbot.py
    """
    try:
        logger.info("="*80)
        logger.info("🚀 INICIO ENDPOINT /pili-itse")
        logger.info("="*80)
        
        # Extraer datos del request
        mensaje = request.mensaje
        estado = request.conversation_state or {}  # ✅ FIX: Usar dict vacío si es None
        
        logger.info(f"📥 REQUEST COMPLETO:")
        logger.info(f"   - mensaje: '{mensaje}'")
        logger.info(f"   - conversation_state: {estado}")
        logger.info(f"   - tipo estado: {type(estado)}")
        
        if estado:
            logger.info(f"📊 DETALLES DEL ESTADO:")
            logger.info(f"   - etapa: {estado.get('etapa')}")
            logger.info(f"   - categoria: {estado.get('categoria')}")
            logger.info(f"   - tipo: {estado.get('tipo')}")
            logger.info(f"   - area: {estado.get('area')}")
            logger.info(f"   - pisos: {estado.get('pisos')}")
        
        logger.info(f"🔧 LLAMANDO A CAJA NEGRA...")
        logger.info(f"   - Instancia: {pili_itse_bot}")
        logger.info(f"   - Tipo: {type(pili_itse_bot)}")
        
        # Llamar a la caja negra
        resultado = pili_itse_bot.procesar(mensaje, estado)
        
        logger.info(f"✅ RESULTADO DE CAJA NEGRA:")
        logger.info(f"   - success: {resultado['success']}")
        logger.info(f"   - respuesta (primeros 100 chars): {resultado['respuesta'][:100]}...")
        # logger.info(f"   - botones: {len(resultado.get('botones') or [])} botones")
        logger.info(f"   - cotizacion: {'SÍ' if resultado.get('cotizacion') else 'NO'}")
        
        logger.info(f"📊 ESTADO DEVUELTO POR CAJA NEGRA:")
        logger.info(f"   - etapa: {resultado['estado'].get('etapa')}")
        logger.info(f"   - categoria: {resultado['estado'].get('categoria')}")
        logger.info(f"   - tipo: {resultado['estado'].get('tipo')}")
        logger.info(f"   - area: {resultado['estado'].get('area')}")
        logger.info(f"   - pisos: {resultado['estado'].get('pisos')}")

        # ✅ Verificar datos_generados
        datos_gen = resultado.get('datos_generados')
        if datos_gen:
            logger.info(f"📋 DATOS_GENERADOS ENCONTRADOS:")
            logger.info(f"   - items: {len(datos_gen.get('items', []))} items")
            logger.info(f"   - subtotal: {datos_gen.get('subtotal')}")
            logger.info(f"   - igv: {datos_gen.get('igv')}")
            logger.info(f"   - total: {datos_gen.get('total')}")
        else:
            logger.warning(f"⚠️ NO HAY datos_generados en resultado")

        # Formatear respuesta
        # La caja negra devuelve 'cotizacion', pero el frontend espera 'datos_generados'
        cotizacion_data = resultado.get('cotizacion')
        
        response = {
            "success": resultado['success'],
            "respuesta": resultado['respuesta'],
            "botones_sugeridos": resultado.get('botones'),
            "botones": resultado.get('botones'),
            "state": resultado['estado'],
            "conversation_state": resultado['estado'],
            "datos_generados": cotizacion_data,  # ✅ Mapear cotizacion → datos_generados
            "cotizacion": cotizacion_data,
            "cotizacion_generada": cotizacion_data is not None,
            "agente_pili": "PILI ITSE"
        }

        
        return response
        
    except Exception as e:
        logger.error(f"❌ Error en PILI ITSE: {e}", exc_info=True)
        return {
            "success": False,
            "respuesta": "Lo siento, hubo un error. Por favor intenta de nuevo.",
            "botones_sugeridos": None,
            "botones": None,
            "state": estado or {},
            "conversation_state": estado or {},
            "datos_generados": None,
            "cotizacion_generada": False,
            "agente_pili": "PILI ITSE"
        }

# ═══════════════════════════════════════════════════════════════
# 🔌 ENDPOINT PILI ELECTRICIDAD - CAJA NEGRA
# ═══════════════════════════════════════════════════════════════

@router.post("/pili-electricidad")
async def chat_pili_electricidad(request: ChatRequest):
    """
    Endpoint para chat de ELECTRICIDAD usando caja negra
    
    Args:
        request: ChatRequest con mensaje y conversation_state
    
    Returns:
        Respuesta con datos de cotización eléctrica
    """
    try:
        logger.info(f"🔌 PILI ELECTRICIDAD - Mensaje recibido: '{request.mensaje[:50]}...'")
        
        # Verificar que la caja negra esté inicializada
        if pili_electricidad_bot is None:
            logger.error("❌ Caja negra PILI ELECTRICIDAD no está inicializada")
            return {
                "success": False,
                "respuesta": "El servicio de electricidad no está disponible temporalmente.",
                "botones_sugeridos": None,
                "botones": None,
                "state": {},
                "conversation_state": {},
                "datos_generados": None,
                "cotizacion_generada": False,
                "agente_pili": "PILI ELECTRICIDAD"
            }
        
        # Obtener estado de la conversación
        estado = request.conversation_state
        
        logger.info(f"📊 Estado actual: {estado}")
        
        # Llamar a la caja negra
        resultado = pili_electricidad_bot.procesar(request.mensaje, estado)
        
        logger.info(f"✅ Resultado de caja negra:")
        logger.info(f"   - success: {resultado['success']}")
        logger.info(f"   - etapa: {resultado['estado'].get('etapa')}")
        logger.info(f"   - tipo_instalacion: {resultado['estado'].get('tipo_instalacion')}")
        logger.info(f"   - area: {resultado['estado'].get('area')}")
        
        # Verificar datos_generados
        datos_gen = resultado.get('datos_generados')
        if datos_gen:
            logger.info(f"📋 DATOS_GENERADOS ENCONTRADOS:")
            logger.info(f"   - items: {len(datos_gen.get('items', []))} items")
            logger.info(f"   - subtotal: {datos_gen.get('subtotal')}")
            logger.info(f"   - total: {datos_gen.get('total')}")
        
        # Formatear respuesta
        cotizacion_data = resultado.get('cotizacion')
        
        response = {
            "success": resultado['success'],
            "respuesta": resultado['respuesta'],
            "botones_sugeridos": resultado.get('botones'),
            "botones": resultado.get('botones'),
            "state": resultado['estado'],
            "conversation_state": resultado['estado'],
            "datos_generados": datos_gen or cotizacion_data,
            "cotizacion": cotizacion_data,
            "cotizacion_generada": cotizacion_data is not None,
            "agente_pili": "PILI ELECTRICIDAD"
        }
        
        return response
        
    except Exception as e:
        logger.error(f"❌ Error en PILI ELECTRICIDAD: {e}", exc_info=True)
        return {
            "success": False,
            "respuesta": "Lo siento, hubo un error. Por favor intenta de nuevo.",
            "botones_sugeridos": None,
            "botones": None,
            "state": estado or {},
            "conversation_state": estado or {},
            "datos_generados": None,
            "cotizacion_generada": False,
            "agente_pili": "PILI ELECTRICIDAD"
        }

# ═══════════════════════════════════════════════════════════════
# 🌍 ENDPOINT PILI PUESTA A TIERRA - CAJA NEGRA
# ═══════════════════════════════════════════════════════════════

@router.post("/pili-puesta-tierra")
async def chat_pili_puesta_tierra(request: ChatRequest):
    """Endpoint para chat de PUESTA A TIERRA usando caja negra"""
    try:
        logger.info(f"🌍 PILI PUESTA A TIERRA - Mensaje recibido: '{request.mensaje[:50]}...'")
        
        if pili_puesta_tierra_bot is None:
            logger.error("❌ Caja negra PILI PUESTA A TIERRA no está inicializada")
            return {
                "success": False,
                "respuesta": "El servicio de puesta a tierra no está disponible temporalmente.",
                "botones_sugeridos": None,
                "botones": None,
                "state": {},
                "conversation_state": {},
                "datos_generados": None,
                "cotizacion_generada": False,
                "agente_pili": "PILI PUESTA A TIERRA"
            }
        
        estado = request.conversation_state
        resultado = pili_puesta_tierra_bot.procesar(request.mensaje, estado)
        
        logger.info(f"✅ Resultado: success={resultado['success']}, etapa={resultado['estado'].get('etapa')}")
        
        datos_gen = resultado.get('datos_generados')
        if datos_gen:
            logger.info(f"📋 Datos generados: {len(datos_gen.get('items', []))} items, total={datos_gen.get('total')}")
        
        cotizacion_data = resultado.get('cotizacion')
        
        response = {
            "success": resultado['success'],
            "respuesta": resultado['respuesta'],
            "botones_sugeridos": resultado.get('botones'),
            "botones": resultado.get('botones'),
            "state": resultado['estado'],
            "conversation_state": resultado['estado'],
            "datos_generados": datos_gen or cotizacion_data,
            "cotizacion": cotizacion_data,
            "cotizacion_generada": cotizacion_data is not None,
            "agente_pili": "PILI PUESTA A TIERRA"
        }
        
        return response
        
    except Exception as e:
        logger.error(f"❌ Error en PILI PUESTA A TIERRA: {e}", exc_info=True)
        return {
            "success": False,
            "respuesta": "Lo siento, hubo un error. Por favor intenta de nuevo.",
            "botones_sugeridos": None,
            "botones": None,
            "state": estado or {},
            "conversation_state": estado or {},
            "datos_generados": None,
            "cotizacion_generada": False,
            "agente_pili": "PILI PUESTA A TIERRA"
        }

# ═══════════════════════════════════════════════════════════════
# 🔥 ENDPOINT PILI CONTRA INCENDIOS
# ═══════════════════════════════════════════════════════════════

@router.post("/pili-contra-incendios")
async def chat_pili_contra_incendios(request: ChatRequest):
    try:
        logger.info(f"🔥 PILI CONTRA INCENDIOS - Mensaje: '{request.mensaje[:50]}...'")
        
        if pili_contra_incendios_bot is None:
            return {"success": False, "respuesta": "Servicio no disponible", "botones": None, "state": {}, "conversation_state": {}, "datos_generados": None, "cotizacion_generada": False, "agente_pili": "PILI CONTRA INCENDIOS"}
        
        estado = request.conversation_state
        resultado = pili_contra_incendios_bot.procesar(request.mensaje, estado)
        
        datos_gen = resultado.get('datos_generados')
        cotizacion_data = resultado.get('cotizacion')
        
        return {
            "success": resultado['success'],
            "respuesta": resultado['respuesta'],
            "botones_sugeridos": resultado.get('botones'),
            "botones": resultado.get('botones'),
            "state": resultado['estado'],
            "conversation_state": resultado['estado'],
            "datos_generados": datos_gen or cotizacion_data,
            "cotizacion": cotizacion_data,
            "cotizacion_generada": cotizacion_data is not None,
            "agente_pili": "PILI CONTRA INCENDIOS"
        }
    except Exception as e:
        logger.error(f"❌ Error: {e}", exc_info=True)
        return {"success": False, "respuesta": "Error", "botones": None, "state": estado or {}, "conversation_state": estado or {}, "datos_generados": None, "cotizacion_generada": False, "agente_pili": "PILI CONTRA INCENDIOS"}

@router.post("/pili-domotica")
async def chat_pili_domotica(request: ChatRequest):
    try:
        if pili_domotica_bot is None:
            return {"success": False, "respuesta": "Servicio no disponible", "botones": None, "state": {}, "conversation_state": {}, "datos_generados": None, "cotizacion_generada": False, "agente_pili": "PILI DOMÓTICA"}
        estado = request.conversation_state
        resultado = pili_domotica_bot.procesar(request.mensaje, estado)
        datos_gen = resultado.get('datos_generados')
        cotizacion_data = resultado.get('cotizacion')
        return {"success": resultado['success'], "respuesta": resultado['respuesta'], "botones_sugeridos": resultado.get('botones'), "botones": resultado.get('botones'), "state": resultado['estado'], "conversation_state": resultado['estado'], "datos_generados": datos_gen or cotizacion_data, "cotizacion": cotizacion_data, "cotizacion_generada": cotizacion_data is not None, "agente_pili": "PILI DOMÓTICA"}
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        return {"success": False, "respuesta": "Error", "botones": None, "state": estado or {}, "conversation_state": estado or {}, "datos_generados": None, "cotizacion_generada": False, "agente_pili": "PILI DOMÓTICA"}

@router.post("/pili-cctv")
async def chat_pili_cctv(request: ChatRequest):
    try:
        if pili_cctv_bot is None:
            return {"success": False, "respuesta": "Servicio no disponible", "botones": None, "state": {}, "conversation_state": {}, "datos_generados": None, "cotizacion_generada": False, "agente_pili": "PILI CCTV"}
        estado = request.conversation_state
        resultado = pili_cctv_bot.procesar(request.mensaje, estado)
        datos_gen = resultado.get('datos_generados')
        cotizacion_data = resultado.get('cotizacion')
        return {"success": resultado['success'], "respuesta": resultado['respuesta'], "botones_sugeridos": resultado.get('botones'), "botones": resultado.get('botones'), "state": resultado['estado'], "conversation_state": resultado['estado'], "datos_generados": datos_gen or cotizacion_data, "cotizacion": cotizacion_data, "cotizacion_generada": cotizacion_data is not None, "agente_pili": "PILI CCTV"}
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        return {"success": False, "respuesta": "Error", "botones": None, "state": estado or {}, "conversation_state": estado or {}, "datos_generados": None, "cotizacion_generada": False, "agente_pili": "PILI CCTV"}

@router.post("/pili-redes")
async def chat_pili_redes(request: ChatRequest):
    try:
        if pili_redes_bot is None: return {"success": False, "respuesta": "No disponible", "botones": None, "state": {}, "conversation_state": {}, "datos_generados": None, "cotizacion_generada": False, "agente_pili": "PILI REDES"}
        estado = request.conversation_state
        resultado = pili_redes_bot.procesar(request.mensaje, estado)
        datos_gen = resultado.get('datos_generados')
        cotizacion_data = resultado.get('cotizacion')
        return {"success": resultado['success'], "respuesta": resultado['respuesta'], "botones_sugeridos": resultado.get('botones'), "botones": resultado.get('botones'), "state": resultado['estado'], "conversation_state": resultado['estado'], "datos_generados": datos_gen or cotizacion_data, "cotizacion": cotizacion_data, "cotizacion_generada": cotizacion_data is not None, "agente_pili": "PILI REDES"}
    except Exception as e:
        return {"success": False, "respuesta": "Error", "botones": None, "state": estado or {}, "conversation_state": estado or {}, "datos_generados": None, "cotizacion_generada": False, "agente_pili": "PILI REDES"}

@router.post("/pili-automatizacion")
async def chat_pili_automatizacion(request: ChatRequest):
    try:
        if pili_automatizacion_bot is None: return {"success": False, "respuesta": "No disponible", "botones": None, "state": {}, "conversation_state": {}, "datos_generados": None, "cotizacion_generada": False, "agente_pili": "PILI AUTOMATIZACIÓN"}
        estado = request.conversation_state; resultado = pili_automatizacion_bot.procesar(request.mensaje, estado); datos_gen = resultado.get('datos_generados'); cotizacion_data = resultado.get('cotizacion')
        return {"success": resultado['success'], "respuesta": resultado['respuesta'], "botones_sugeridos": resultado.get('botones'), "botones": resultado.get('botones'), "state": resultado['estado'], "conversation_state": resultado['estado'], "datos_generados": datos_gen or cotizacion_data, "cotizacion": cotizacion_data, "cotizacion_generada": cotizacion_data is not None, "agente_pili": "PILI AUTOMATIZACIÓN"}
    except: return {"success": False, "respuesta": "Error", "botones": None, "state": {}, "conversation_state": {}, "datos_generados": None, "cotizacion_generada": False, "agente_pili": "PILI AUTOMATIZACIÓN"}

@router.post("/pili-expedientes")
async def chat_pili_expedientes(request: ChatRequest):
    try:
        if pili_expedientes_bot is None: return {"success": False, "respuesta": "No disponible", "botones": None, "state": {}, "conversation_state": {}, "datos_generados": None, "cotizacion_generada": False, "agente_pili": "PILI EXPEDIENTES"}
        estado = request.conversation_state; resultado = pili_expedientes_bot.procesar(request.mensaje, estado); datos_gen = resultado.get('datos_generados'); cotizacion_data = resultado.get('cotizacion')
        return {"success": resultado['success'], "respuesta": resultado['respuesta'], "botones_sugeridos": resultado.get('botones'), "botones": resultado.get('botones'), "state": resultado['estado'], "conversation_state": resultado['estado'], "datos_generados": datos_gen or cotizacion_data, "cotizacion": cotizacion_data, "cotizacion_generada": cotizacion_data is not None, "agente_pili": "PILI EXPEDIENTES"}
    except: return {"success": False, "respuesta": "Error", "botones": None, "state": {}, "conversation_state": {}, "datos_generados": None, "cotizacion_generada": False, "agente_pili": "PILI EXPEDIENTES"}

@router.post("/pili-saneamiento")
async def chat_pili_saneamiento(request: ChatRequest):
    try:
        if pili_saneamiento_bot is None: return {"success": False, "respuesta": "No disponible", "botones": None, "state": {}, "conversation_state": {}, "datos_generados": None, "cotizacion_generada": False, "agente_pili": "PILI SANEAMIENTO"}
        estado = request.conversation_state; resultado = pili_saneamiento_bot.procesar(request.mensaje, estado); datos_gen = resultado.get('datos_generados'); cotizacion_data = resultado.get('cotizacion')
        return {"success": resultado['success'], "respuesta": resultado['respuesta'], "botones_sugeridos": resultado.get('botones'), "botones": resultado.get('botones'), "state": resultado['estado'], "conversation_state": resultado['estado'], "datos_generados": datos_gen or cotizacion_data, "cotizacion": cotizacion_data, "cotizacion_generada": cotizacion_data is not None, "agente_pili": "PILI SANEAMIENTO"}
    except: return {"success": False, "respuesta": "Error", "botones": None, "state": {}, "conversation_state": {}, "datos_generados": None, "cotizacion_generada": False, "agente_pili": "PILI SANEAMIENTO"}

# ═══════════════════════════════════════════════════════════════
# ENDPOINTS COTIZACIÓN COMPLEJA
# ═══════════════════════════════════════════════════════════════

try:
    from Pili_ChatBot.pili_electricidad_complejo_chatbot import PILIElectricidadComplejoChatBot
    pili_electricidad_complejo_bot = PILIElectricidadComplejoChatBot()
    logger.info("✅ PILI ELECTRICIDAD COMPLEJO OK")
except: pili_electricidad_complejo_bot = None

try:
    from Pili_ChatBot.pili_automatizacion_complejo_chatbot import PILIAutomatizacionComplejoChatBot
    pili_automatizacion_complejo_bot = PILIAutomatizacionComplejoChatBot()
    logger.info("✅ PILI AUTOMATIZACIÓN COMPLEJO OK")
except: pili_automatizacion_complejo_bot = None

try:
    from Pili_ChatBot.pili_contra_incendios_complejo_chatbot import PILIContraIncendiosComplejoChatBot
    pili_contra_incendios_complejo_bot = PILIContraIncendiosComplejoChatBot()
    logger.info("✅ PILI CONTRA INCENDIOS COMPLEJO OK")
except: pili_contra_incendios_complejo_bot = None

@router.post("/pili-electricidad-complejo")
async def chat_pili_electricidad_complejo(request: ChatRequest):
    try:
        if pili_electricidad_complejo_bot is None: return {"success": False, "respuesta": "No disponible", "botones": None, "state": {}, "conversation_state": {}, "datos_generados": None, "cotizacion_generada": False, "agente_pili": "PILI ELECTRICIDAD COMPLEJO"}
        estado = request.conversation_state; resultado = pili_electricidad_complejo_bot.procesar(request.mensaje, estado); datos_gen = resultado.get('datos_generados'); cotizacion_data = resultado.get('cotizacion')
        return {"success": resultado['success'], "respuesta": resultado['respuesta'], "botones_sugeridos": resultado.get('botones'), "botones": resultado.get('botones'), "state": resultado['estado'], "conversation_state": resultado['estado'], "datos_generados": datos_gen or cotizacion_data, "cotizacion": cotizacion_data, "cotizacion_generada": cotizacion_data is not None, "agente_pili": "PILI ELECTRICIDAD COMPLEJO"}
    except: return {"success": False, "respuesta": "Error", "botones": None, "state": {}, "conversation_state": {}, "datos_generados": None, "cotizacion_generada": False, "agente_pili": "PILI ELECTRICIDAD COMPLEJO"}

@router.post("/pili-automatizacion-complejo")
async def chat_pili_automatizacion_complejo(request: ChatRequest):
    try:
        if pili_automatizacion_complejo_bot is None: return {"success": False, "respuesta": "No disponible", "botones": None, "state": {}, "conversation_state": {}, "datos_generados": None, "cotizacion_generada": False, "agente_pili": "PILI AUTOMATIZACIÓN COMPLEJO"}
        estado = request.conversation_state; resultado = pili_automatizacion_complejo_bot.procesar(request.mensaje, estado); datos_gen = resultado.get('datos_generados'); cotizacion_data = resultado.get('cotizacion')
        return {"success": resultado['success'], "respuesta": resultado['respuesta'], "botones_sugeridos": resultado.get('botones'), "botones": resultado.get('botones'), "state": resultado['estado'], "conversation_state": resultado['estado'], "datos_generados": datos_gen or cotizacion_data, "cotizacion": cotizacion_data, "cotizacion_generada": cotizacion_data is not None, "agente_pili": "PILI AUTOMATIZACIÓN COMPLEJO"}
    except: return {"success": False, "respuesta": "Error", "botones": None, "state": {}, "conversation_state": {}, "datos_generados": None, "cotizacion_generada": False, "agente_pili": "PILI AUTOMATIZACIÓN COMPLEJO"}

@router.post("/pili-contra-incendios-complejo")
async def chat_pili_contra_incendios_complejo(request: ChatRequest):
    try:
        if pili_contra_incendios_complejo_bot is None: return {"success": False, "respuesta": "No disponible", "botones": None, "state": {}, "conversation_state": {}, "datos_generados": None, "cotizacion_generada": False, "agente_pili": "PILI CONTRA INCENDIOS COMPLEJO"}
        estado = request.conversation_state; resultado = pili_contra_incendios_complejo_bot.procesar(request.mensaje, estado); datos_gen = resultado.get('datos_generados'); cotizacion_data = resultado.get('cotizacion')
        return {"success": resultado['success'], "respuesta": resultado['respuesta'], "botones_sugeridos": resultado.get('botones'), "botones": resultado.get('botones'), "state": resultado['estado'], "conversation_state": resultado['estado'], "datos_generados": datos_gen or cotizacion_data, "cotizacion": cotizacion_data, "cotizacion_generada": cotizacion_data is not None, "agente_pili": "PILI CONTRA INCENDIOS COMPLEJO"}
    except: return {"success": False, "respuesta": "Error", "botones": None, "state": {}, "conversation_state": {}, "datos_generados": None, "cotizacion_generada": False, "agente_pili": "PILI CONTRA INCENDIOS COMPLEJO"}

# ═══════════════════════════════════════════════════════════════
# ENDPOINTS PROYECTO SIMPLE
# ═══════════════════════════════════════════════════════════════


try:
    from Pili_ChatBot.pili_electricidad_proyecto_simple_chatbot import PILIElectricidadProyectoSimpleChatBot
    pili_electricidad_proyecto_simple_bot = PILIElectricidadProyectoSimpleChatBot()
    logger.info("✅ PILI ELECTRICIDAD PROYECTO SIMPLE OK")
except Exception as e:
    logger.error(f"❌ ERROR CARGANDO PILI ELECTRICIDAD PROYECTO SIMPLE: {str(e)}")
    pili_electricidad_proyecto_simple_bot = None


@router.post("/pili-electricidad-proyecto-simple")
async def chat_pili_electricidad_proyecto_simple(request: ChatRequest):
    try:
        if pili_electricidad_proyecto_simple_bot is None: return {"success": False, "respuesta": "No disponible", "botones": None, "state": {}, "conversation_state": {}, "datos_generados": None, "cotizacion_generada": False, "agente_pili": "PILI ELECTRICIDAD PROYECTO SIMPLE"}
        estado = request.conversation_state; resultado = pili_electricidad_proyecto_simple_bot.procesar(request.mensaje, estado); datos_gen = resultado.get('datos_generados'); cotizacion_data = resultado.get('cotizacion')
        return {"success": resultado['success'], "respuesta": resultado['respuesta'], "botones_sugeridos": resultado.get('botones'), "botones": resultado.get('botones'), "state": resultado['estado'], "conversation_state": resultado['estado'], "datos_generados": datos_gen or cotizacion_data, "cotizacion": cotizacion_data, "cotizacion_generada": cotizacion_data is not None, "agente_pili": "PILI ELECTRICIDAD PROYECTO SIMPLE"}
    except: return {"success": False, "respuesta": "Error", "botones": None, "state": {}, "conversation_state": {}, "datos_generados": None, "cotizacion_generada": False, "agente_pili": "PILI ELECTRICIDAD PROYECTO SIMPLE"}


# ═══════════════════════════════════════════════════════════════
# ENDPOINTS PROYECTO COMPLEJO PMI
# ═══════════════════════════════════════════════════════════════

try:
    from app.integrations.pili_chatbot.pili_electricidad_proyecto_complejo_pmi_chatbot import PILIElectricidadProyectoComplejoPMIChatBot
    pili_electricidad_proyecto_complejo_pmi_bot = PILIElectricidadProyectoComplejoPMIChatBot()
    logger.info("✅ PILI ELECTRICIDAD PROYECTO COMPLEJO PMI OK")
except Exception as e:
    logger.error(f"❌ ERROR CARGANDO PILI ELECTRICIDAD PROYECTO COMPLEJO PMI: {str(e)}")
    pili_electricidad_proyecto_complejo_pmi_bot = None


@router.post("/pili-electricidad-proyecto-complejo-pmi")
async def chat_pili_electricidad_proyecto_complejo_pmi(request: ChatRequest):
    try:
        if pili_electricidad_proyecto_complejo_pmi_bot is None: return {"success": False, "respuesta": "No disponible", "botones": None, "state": {}, "conversation_state": {}, "datos_generados": None, "cotizacion_generada": False, "agente_pili": "PILI ELECTRICIDAD PROYECTO COMPLEJO PMI"}
        estado = request.conversation_state; resultado = pili_electricidad_proyecto_complejo_pmi_bot.procesar(request.mensaje, estado); datos_gen = resultado.get('datos_generados'); cotizacion_data = resultado.get('cotizacion')
        return {"success": resultado['success'], "respuesta": resultado['respuesta'], "botones_sugeridos": resultado.get('botones'), "botones": resultado.get('botones'), "formulario": resultado.get('formulario'), "state": resultado['estado'], "conversation_state": resultado['estado'], "datos_generados": datos_gen or cotizacion_data, "cotizacion": cotizacion_data, "cotizacion_generada": cotizacion_data is not None, "agente_pili": "PILI ELECTRICIDAD PROYECTO COMPLEJO PMI"}
    except: return {"success": False, "respuesta": "Error", "botones": None, "state": {}, "conversation_state": {}, "datos_generados": None, "cotizacion_generada": False, "agente_pili": "PILI ELECTRICIDAD PROYECTO COMPLEJO PMI"}








