# 🎯 CONCLUSIONES DEFINITIVAS: PILI Especialista Profesional

## 📊 Investigación Completada

### **Artefacto ITSE Analizado (632 líneas):**
✅ Conversación por etapas (initial → businessType → area → floors → quotation)
✅ Knowledge base con reglas de negocio inteligentes
✅ Botones dinámicos que cambian según contexto
✅ Validación en tiempo real (isNaN, <= 0)
✅ Cálculo automático basado en reglas
✅ Cotización formateada profesionalmente
✅ Captura progresiva de datos del cliente

### **Mejores Prácticas 2024 (Investigación Web):**
✅ Progressive disclosure (una pregunta a la vez)
✅ Conditional logic (mostrar/ocultar según respuestas)
✅ Real-time validation (feedback inmediato)
✅ Dynamic field population (pre-rellenar datos)
✅ Conversational tone (lenguaje natural)
✅ Clear bot persona (personalidad consistente)
✅ Mobile-friendly (responsive design)

---

## 🏆 DECISIÓN FINAL DEL ESPECIALISTA

### **Arquitectura: UN SOLO ARCHIVO**

**Archivo:** `backend/app/services/pili_local_specialists.py`
**Tamaño:** ~3000 líneas
**Razón:** Simplicidad + Mantenibilidad + Suficiente para fallback

---

## 📋 ESPECIFICACIONES EXACTAS (Basadas en ITSE)

### **1. Estructura del Archivo**

```python
# backend/app/services/pili_local_specialists.py

"""
🧠 PILI LOCAL SPECIALISTS - Fallback Inteligente
Conversación profesional para 10 servicios eléctricos
Se usa cuando Gemini API no está disponible
"""

# ══════════════════════════════════════════════════════════
# 📦 LÍNEAS 1-50: IMPORTS Y CONFIGURACIÓN
# ══════════════════════════════════════════════════════════

from typing import Dict, List, Optional, Tuple
from datetime import datetime
import logging
import re

logger = logging.getLogger(__name__)


# ══════════════════════════════════════════════════════════
# 💰 LÍNEAS 50-600: KNOWLEDGE BASES (10 servicios × 50 líneas)
# ══════════════════════════════════════════════════════════

KNOWLEDGE_BASE = {
    # ─────────────────────────────────────────────────────
    # ⚡ ELECTRICIDAD (Líneas 50-150)
    # ─────────────────────────────────────────────────────
    "electricidad": {
        "tipos": {
            "RESIDENCIAL": {
                "nombre": "Instalación Eléctrica Residencial",
                "precios": {
                    "punto_luz_empotrado": 80,
                    "punto_luz_adosado": 65,
                    "tomacorriente_doble": 60,
                    "tomacorriente_simple": 45,
                    "interruptor_simple": 35,
                    "interruptor_doble": 50,
                    "interruptor_triple": 65,
                    "tablero_monofasico": 800,
                    "tablero_trifasico": 1200,
                    "cable_thw_2_5mm": 2.5,  # por metro
                    "cable_thw_4mm": 3.8,
                    "cable_thw_6mm": 5.5,
                    "tuberia_pvc_3_4": 1.2,
                    "caja_octogonal": 3.5,
                    "caja_rectangular": 4.0
                },
                "reglas": {
                    "area_max": 200,
                    "pisos_max": 2,
                    "puntos_por_m2": 0.15,  # Promedio
                    "tomas_por_m2": 0.10
                },
                "normativa": "CNE Suministro 2011 - Sección 050",
                "tiempo_estimado": "5-7 días hábiles"
            },
            "COMERCIAL": {
                "nombre": "Instalación Eléctrica Comercial",
                "precios": {
                    "punto_luz_empotrado": 95,
                    "tomacorriente_doble": 75,
                    "tablero_trifasico": 1500,
                    "cable_thw_2_5mm": 3.2,
                    # ... más items
                },
                "reglas": {
                    "area_min": 50,
                    "area_max": 1000,
                    "puntos_por_m2": 0.12,
                    "tomas_por_m2": 0.15
                },
                "normativa": "CNE Suministro 2011 - Sección 050 + 060",
                "tiempo_estimado": "7-10 días hábiles"
            },
            "INDUSTRIAL": {
                "nombre": "Instalación Eléctrica Industrial",
                "precios": {
                    "punto_luz_industrial": 120,
                    "tomacorriente_industrial": 95,
                    "tablero_industrial": 2800,
                    "cable_thw_6mm": 6.5,
                    # ... más items
                },
                "reglas": {
                    "area_min": 200,
                    "potencia_min_kw": 50,
                    "puntos_por_m2": 0.08,
                    "tomas_por_m2": 0.12
                },
                "normativa": "CNE Suministro + CNE Utilización",
                "tiempo_estimado": "15-20 días hábiles"
            }
        },
        "etapas": [
            "initial",          # Selección tipo (Residencial/Comercial/Industrial)
            "area",             # Área en m²
            "pisos",            # Número de pisos
            "puntos_luz",       # Cantidad de puntos de luz
            "tomacorrientes",   # Cantidad de tomacorrientes
            "tableros",         # Cantidad de tableros
            "potencia",         # Potencia estimada (opcional)
            "quotation"         # Mostrar cotización
        ]
    },
    
    # ─────────────────────────────────────────────────────
    # 📋 ITSE (Líneas 150-250)
    # ─────────────────────────────────────────────────────
    "itse": {
        "categorias": {
            "SALUD": {
                "tipos": ["Hospital", "Clínica", "Centro Médico", "Consultorio", "Laboratorio"],
                "riesgo_default": "ALTO",
                "reglas": "Más de 500m² o 2+ pisos = MUY ALTO"
            },
            "EDUCACION": {
                "tipos": ["Colegio", "Universidad", "Instituto", "Academia", "Guardería"],
                "riesgo_default": "MEDIO",
                "reglas": "Más de 1000m² o 3+ pisos = ALTO"
            },
            # ... 6 categorías más (HOSPEDAJE, COMERCIO, RESTAURANTE, OFICINA, INDUSTRIAL, ENCUENTRO)
        },
        "precios_municipales": {
            "BAJO": {"precio": 168.30, "renovacion": 90.30, "dias": 7},
            "MEDIO": {"precio": 208.60, "renovacion": 109.40, "dias": 7},
            "ALTO": {"precio": 703.00, "renovacion": 417.40, "dias": 7},
            "MUY_ALTO": {"precio": 1084.60, "renovacion": 629.20, "dias": 7}
        },
        "precios_tesla": {
            "BAJO": {"min": 300, "max": 500},
            "MEDIO": {"min": 450, "max": 650},
            "ALTO": {"min": 800, "max": 1200},
            "MUY_ALTO": {"min": 1200, "max": 1800}
        },
        "etapas": [
            "initial",          # Selección categoría (8 opciones)
            "tipo_especifico",  # Tipo específico según categoría
            "area",             # Área en m²
            "pisos",            # Número de pisos
            "quotation"         # Calcular riesgo y mostrar cotización
        ]
    },
    
    # ... 8 servicios más (cada uno ~50-100 líneas)
}


# ══════════════════════════════════════════════════════════
# 🎯 LÍNEAS 600-800: CLASE BASE
# ══════════════════════════════════════════════════════════

class LocalSpecialist:
    """
    Clase base para especialistas locales
    Implementa patrón de conversación por etapas
    """
    
    def __init__(self, service_type: str):
        self.service_type = service_type
        self.kb = KNOWLEDGE_BASE.get(service_type, {})
        self.conversation_state = {
            "stage": "initial",
            "data": {},
            "history": []
        }
    
    def process_message(
        self, 
        message: str, 
        state: Optional[Dict] = None
    ) -> Dict:
        """
        Procesa mensaje del usuario
        Retorna: {
            "texto": str,
            "botones": List[Dict],  # Opcional
            "stage": str,
            "state": Dict,
            "datos_generados": Dict,  # Para plantilla HTML
            "progreso": str  # "3/7"
        }
        """
        if state:
            self.conversation_state = state
        
        # Delegar a método específico del servicio
        method_name = f"_process_{self.service_type}"
        method = getattr(self, method_name, self._process_generic)
        
        return method(message)
    
    def _process_generic(self, message: str) -> Dict:
        """Procesamiento genérico para servicios no implementados"""
        return {
            "texto": f"Servicio {self.service_type} en desarrollo",
            "stage": "error",
            "state": self.conversation_state
        }
    
    def _validar_numero(
        self, 
        valor: str, 
        tipo: str = "entero",
        min_val: float = 0,
        max_val: float = None
    ) -> Tuple[bool, Optional[float], str]:
        """
        Valida entrada numérica
        Retorna: (es_valido, valor_convertido, mensaje_error)
        """
        try:
            if tipo == "entero":
                num = int(valor)
            else:
                num = float(valor)
            
            if num <= min_val:
                return False, None, f"El valor debe ser mayor a {min_val}"
            
            if max_val and num > max_val:
                return False, None, f"El valor debe ser menor a {max_val}"
            
            return True, num, ""
            
        except ValueError:
            return False, None, "Por favor ingresa un número válido"
    
    def _calcular_progreso(self) -> str:
        """Calcula progreso de la conversación"""
        etapas = self.kb.get("etapas", [])
        stage_actual = self.conversation_state["stage"]
        
        try:
            indice = etapas.index(stage_actual)
            return f"{indice + 1}/{len(etapas)}"
        except:
            return "0/0"


# ══════════════════════════════════════════════════════════
# ⚡ LÍNEAS 800-1100: ELECTRICIDAD SPECIALIST
# ══════════════════════════════════════════════════════════

class ElectricidadSpecialist(LocalSpecialist):
    """Especialista en instalaciones eléctricas"""
    
    def _process_electricidad(self, message: str) -> Dict:
        stage = self.conversation_state["stage"]
        data = self.conversation_state["data"]
        
        # ─────────────────────────────────────────────────
        # ETAPA 1: Selección de tipo
        # ─────────────────────────────────────────────────
        if stage == "initial":
            return {
                "texto": """¡Hola! 👋 Soy **PILI**, especialista en Instalaciones Eléctricas de **Tesla Electricidad**.

🎯 Te ayudo a cotizar tu proyecto eléctrico con:
✅ Precios según CNE 2011
✅ Cálculo automático de materiales
✅ Cotización profesional en minutos

**¿Qué tipo de instalación necesitas?**""",
                "botones": [
                    {"text": "🏠 Residencial", "value": "RESIDENCIAL"},
                    {"text": "🏢 Comercial", "value": "COMERCIAL"},
                    {"text": "🏭 Industrial", "value": "INDUSTRIAL"}
                ],
                "stage": "initial",
                "state": self.conversation_state,
                "progreso": "1/7"
            }
        
        # ─────────────────────────────────────────────────
        # ETAPA 2: Área
        # ─────────────────────────────────────────────────
        elif stage == "tipo":
            data["tipo"] = message
            tipo_info = self.kb["tipos"][message]
            
            return {
                "texto": f"""Perfecto, instalación **{tipo_info["nombre"]}**. 

📋 **Normativa:** {tipo_info["normativa"]}
⏱️ **Tiempo:** {tipo_info["tiempo_estimado"]}

📏 **¿Cuál es el área total del proyecto en m²?**

_Escribe el número (ejemplo: 120)_""",
                "stage": "area",
                "state": self.conversation_state,
                "progreso": "2/7"
            }
        
        # ─────────────────────────────────────────────────
        # ETAPA 3: Validar área
        # ─────────────────────────────────────────────────
        elif stage == "area":
            es_valido, area, error = self._validar_numero(message, "decimal", 0, 10000)
            
            if not es_valido:
                return {
                    "texto": f"❌ {error}\n\nPor favor ingresa el área en m² (ejemplo: 120)",
                    "stage": "area",
                    "state": self.conversation_state,
                    "progreso": "2/7"
                }
            
            data["area"] = area
            
            return {
                "texto": f"""✅ Área: **{area} m²**

🏢 **¿Cuántos pisos tiene el proyecto?**

_Escribe el número (ejemplo: 2)_""",
                "stage": "pisos",
                "state": self.conversation_state,
                "datos_generados": {"area_m2": area},  # ✅ Para plantilla HTML
                "progreso": "3/7"
            }
        
        # ... más etapas (pisos, puntos_luz, tomacorrientes, tableros, quotation)
        
        # ─────────────────────────────────────────────────
        # ETAPA FINAL: Cotización
        # ─────────────────────────────────────────────────
        elif stage == "quotation":
            return self._generar_cotizacion_electricidad()
    
    def _generar_cotizacion_electricidad(self) -> Dict:
        """Genera cotización eléctrica con cálculo automático"""
        data = self.conversation_state["data"]
        tipo = data["tipo"]
        area = data["area"]
        pisos = data["pisos"]
        puntos = data["puntos_luz"]
        tomas = data["tomacorrientes"]
        tableros = data["tableros"]
        
        precios = self.kb["tipos"][tipo]["precios"]
        
        # ✅ CÁLCULO AUTOMÁTICO DE ITEMS
        items = []
        
        # 1. Puntos de luz
        items.append({
            "descripcion": f"Puntos de luz empotrados ({puntos} und)",
            "cantidad": puntos,
            "precio_unitario": precios["punto_luz_empotrado"],
            "total": puntos * precios["punto_luz_empotrado"]
        })
        
        # 2. Tomacorrientes
        items.append({
            "descripcion": f"Tomacorrientes dobles ({tomas} und)",
            "cantidad": tomas,
            "precio_unitario": precios["tomacorriente_doble"],
            "total": tomas * precios["tomacorriente_doble"]
        })
        
        # 3. Tableros
        items.append({
            "descripcion": f"Tableros eléctricos ({tableros} und)",
            "cantidad": tableros,
            "precio_unitario": precios["tablero_trifasico"],
            "total": tableros * precios["tablero_trifasico"]
        })
        
        # 4. Cable (estimado por área)
        cable_metros = area * 1.5 * pisos
        items.append({
            "descripcion": f"Cable THW 2.5mm² ({cable_metros:.0f}m)",
            "cantidad": cable_metros,
            "precio_unitario": precios["cable_thw_2_5mm"],
            "total": cable_metros * precios["cable_thw_2_5mm"]
        })
        
        # 5. Tubería PVC
        tuberia_metros = area * 1.2 * pisos
        items.append({
            "descripcion": f"Tubería PVC 3/4\" ({tuberia_metros:.0f}m)",
            "cantidad": tuberia_metros,
            "precio_unitario": precios["tuberia_pvc_3_4"],
            "total": tuberia_metros * precios["tuberia_pvc_3_4"]
        })
        
        # TOTALES
        subtotal = sum(item["total"] for item in items)
        igv = subtotal * 0.18
        total = subtotal + igv
        
        # ✅ COTIZACIÓN FORMATEADA
        texto_cotizacion = f"""📊 **COTIZACIÓN INSTALACIÓN ELÉCTRICA {tipo}**

━━━━━━━━━━━━━━━━━━━━━━━
**📋 DATOS DEL PROYECTO:**

📏 Área: {area} m²
🏢 Pisos: {pisos}
💡 Puntos de luz: {puntos}
🔌 Tomacorrientes: {tomas}
⚡ Tableros: {tableros}

━━━━━━━━━━━━━━━━━━━━━━━
**💰 ITEMS CALCULADOS:**

"""
        for i, item in enumerate(items, 1):
            texto_cotizacion += f"{i}. {item['descripcion']}\n   └ S/ {item['total']:.2f}\n\n"
        
        texto_cotizacion += f"""━━━━━━━━━━━━━━━━━━━━━━━
**📈 TOTALES:**

Subtotal: S/ {subtotal:.2f}
IGV (18%): S/ {igv:.2f}
**TOTAL: S/ {total:.2f}**
━━━━━━━━━━━━━━━━━━━━━━━

✅ Incluye: Materiales + Mano de obra
⏱️ Tiempo: {self.kb["tipos"][tipo]["tiempo_estimado"]}
📋 Normativa: {self.kb["tipos"][tipo]["normativa"]}
🎁 Garantía: 1 año

¿Deseas generar el documento?"""
        
        return {
            "texto": texto_cotizacion,
            "botones": [
                {"text": "📄 Generar Cotización", "value": "GENERAR"},
                {"text": "🔄 Nueva consulta", "value": "RESTART"}
            ],
            "stage": "complete",
            "state": self.conversation_state,
            "datos_generados": {  # ✅ PARA PLANTILLA HTML
                "proyecto": {
                    "nombre": f"Instalación Eléctrica {tipo}",
                    "area_m2": area
                },
                "items": items,
                "subtotal": subtotal,
                "igv": igv,
                "total": total
            },
            "progreso": "7/7"
        }


# ══════════════════════════════════════════════════════════
# 📋 LÍNEAS 1100-1350: ITSE SPECIALIST
# ══════════════════════════════════════════════════════════

class ITSESpecialist(LocalSpecialist):
    """Especialista en certificaciones ITSE"""
    # ... (similar estructura, 250 líneas)


# ══════════════════════════════════════════════════════════
# 🔌 LÍNEAS 1350-1550: POZO TIERRA SPECIALIST
# ══════════════════════════════════════════════════════════

class PozoTierraSpecialist(LocalSpecialist):
    """Especialista en sistemas de puesta a tierra"""
    # ... (200 líneas)


# ... 7 especialistas más (cada uno 150-250 líneas)


# ══════════════════════════════════════════════════════════
# 🏭 LÍNEAS 2800-2900: FACTORY
# ══════════════════════════════════════════════════════════

class LocalSpecialistFactory:
    """Factory para crear especialistas locales"""
    
    _specialists = {
        "electricidad": ElectricidadSpecialist,
        "itse": ITSESpecialist,
        "pozo-tierra": PozoTierraSpecialist,
        "contraincendios": ContraincendiosSpecialist,
        "domotica": DomoticaSpecialist,
        "cctv": CCTVSpecialist,
        "redes": RedesSpecialist,
        "automatizacion-industrial": AutomatizacionSpecialist,
        "expedientes": ExpedientesSpecialist,
        "saneamiento": SaneamientoSpecialist
    }
    
    @classmethod
    def create(cls, service_type: str) -> LocalSpecialist:
        specialist_class = cls._specialists.get(service_type)
        if not specialist_class:
            return LocalSpecialist(service_type)
        return specialist_class(service_type)


# ══════════════════════════════════════════════════════════
# 🎯 LÍNEAS 2900-3000: FUNCIÓN PRINCIPAL
# ══════════════════════════════════════════════════════════

def process_with_local_specialist(
    service_type: str,
    message: str,
    conversation_state: Optional[Dict] = None
) -> Dict:
    """
    Procesa mensaje con especialista local (FALLBACK)
    
    Returns:
        {
            "texto": str,
            "botones": List[Dict],
            "stage": str,
            "state": Dict,
            "datos_generados": Dict,  # ✅ Para plantilla HTML
            "progreso": str
        }
    """
    try:
        specialist = LocalSpecialistFactory.create(service_type)
        response = specialist.process_message(message, conversation_state)
        
        logger.info(f"✅ Procesado con especialista local: {service_type}")
        return response
        
    except Exception as e:
        logger.error(f"❌ Error en especialista local: {e}")
        return {
            "texto": "Lo siento, ocurrió un error. Por favor intenta de nuevo.",
            "stage": "error",
            "state": conversation_state or {}
        }
```

---

## ✅ CARACTERÍSTICAS PROFESIONALES GARANTIZADAS

### **1. Conversación Inteligente**
- ✅ Una pregunta a la vez (progressive disclosure)
- ✅ Botones dinámicos según contexto
- ✅ Validación en tiempo real
- ✅ Mensajes de error claros

### **2. Cálculo Automático**
- ✅ Reglas de negocio por servicio
- ✅ Precios actualizados 2025
- ✅ Items calculados automáticamente
- ✅ Totales con IGV

### **3. Actualización en Tiempo Real**
- ✅ `datos_generados` en cada respuesta
- ✅ Frontend actualiza plantilla HTML
- ✅ Usuario ve cambios instantáneos
- ✅ Progreso visible (3/7)

### **4. Experiencia Profesional**
- ✅ Emojis y formato markdown
- ✅ Cotizaciones formateadas
- ✅ Información técnica precisa
- ✅ Lenguaje natural y amigable

---

## 🎯 INTEGRACIÓN CON SISTEMA EXISTENTE

### **En `pili_integrator.py`:**

```python
from .pili_local_specialists import process_with_local_specialist

async def _generar_respuesta_chat(self, mensaje, tipo_flujo, historial, servicio, datos_acumulados):
    # 1. Intentar con Gemini (IA de clase mundial)
    if self.gemini_service:
        try:
            respuesta = await self.gemini_service.chat_conversacional(...)
            if respuesta.get("success"):
                return respuesta
        except:
            pass
    
    # 2. FALLBACK: Especialista local
    return process_with_local_specialist(
        service_type=servicio,
        message=mensaje,
        conversation_state=datos_acumulados
    )
```

### **En `App.jsx` (Frontend):**

```javascript
// Actualizar plantilla HTML en tiempo real
if (data.datos_generados) {
    setDatosEditables(prev => ({
        ...prev,
        ...data.datos_generados
    }));
    
    // Actualizar cotización
    if (data.datos_generados.items) {
        setCotizacion(prev => ({
            ...prev,
            items: data.datos_generados.items,
            subtotal: data.datos_generados.subtotal,
            igv: data.datos_generados.igv,
            total: data.datos_generados.total
        }));
    }
}
```

---

## 🚀 PRÓXIMO PASO

**¿Procedo a crear `pili_local_specialists.py` con:**
- ✅ Knowledge bases completos (10 servicios)
- ✅ Conversación por etapas (estilo ITSE)
- ✅ Validación inteligente
- ✅ Cálculo automático
- ✅ Actualización tiempo real
- ✅ ~3000 líneas profesionales

**SÍ o NO?**
