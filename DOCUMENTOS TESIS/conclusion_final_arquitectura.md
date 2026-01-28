# 🎯 Conclusión del Especialista: Arquitectura PILI Local

## 📊 Análisis Final

### **Contexto Clave:**
- ✅ PILI busca IA (Gemini) primero
- ✅ Si no encuentra IA → usa lógica local (fallback)
- ✅ En producción → 90% usará Gemini
- ✅ Lógica local → solo desarrollo y emergencias

---

## 🏆 RECOMENDACIÓN FINAL: UN SOLO ARCHIVO

### **Opción Ganadora: `pili_local_specialists.py`**

```python
# backend/app/services/pili_local_specialists.py
# ~2500 líneas total
# Fallback inteligente cuando Gemini no está disponible

"""
🧠 PILI LOCAL SPECIALISTS
Lógica de conversación inteligente para 10 servicios eléctricos
Se usa como FALLBACK cuando Gemini API no está disponible
"""

# ══════════════════════════════════════════════════════════
# 📦 IMPORTS
# ══════════════════════════════════════════════════════════
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


# ══════════════════════════════════════════════════════════
# 💰 KNOWLEDGE BASES (Líneas 1-500)
# ══════════════════════════════════════════════════════════

KNOWLEDGE_BASE = {
    "electricidad": {
        "tipos": {
            "RESIDENCIAL": {
                "precios": {"punto_luz": 80, "tomacorriente": 60, ...},
                "reglas": "Hasta 200m²"
            },
            "COMERCIAL": {...},
            "INDUSTRIAL": {...}
        }
    },
    
    "itse": {
        "categorias": {
            "SALUD": {
                "tipos": ["Hospital", "Clínica"],
                "riesgo_default": "ALTO"
            },
            ...
        },
        "precios_municipales": {...},
        "precios_tesla": {...}
    },
    
    # ... 8 servicios más (cada uno ~50 líneas)
}


# ══════════════════════════════════════════════════════════
# 🎯 CLASE BASE (Líneas 500-700)
# ══════════════════════════════════════════════════════════

class LocalSpecialist:
    """Clase base para especialistas locales"""
    
    def __init__(self, service_type: str):
        self.service_type = service_type
        self.kb = KNOWLEDGE_BASE.get(service_type, {})
        self.conversation_state = {"stage": "initial", "data": {}}
    
    def process_message(self, message: str, state: Dict) -> Dict:
        """Procesa mensaje según servicio"""
        method_name = f"_process_{self.service_type}"
        method = getattr(self, method_name, self._process_generic)
        return method(message, state)
    
    def _process_generic(self, message: str, state: Dict) -> Dict:
        """Procesamiento genérico"""
        return {"texto": "Servicio no implementado", "stage": "error"}


# ══════════════════════════════════════════════════════════
# ⚡ ELECTRICIDAD (Líneas 700-950)
# ══════════════════════════════════════════════════════════

class ElectricidadSpecialist(LocalSpecialist):
    """Especialista en instalaciones eléctricas"""
    
    def _process_electricidad(self, message: str, state: Dict) -> Dict:
        stage = state.get("stage", "initial")
        
        if stage == "initial":
            return {
                "texto": "¿Qué tipo de instalación necesitas?",
                "botones": [
                    {"text": "🏠 Residencial", "value": "RESIDENCIAL"},
                    {"text": "🏢 Comercial", "value": "COMERCIAL"},
                    {"text": "🏭 Industrial", "value": "INDUSTRIAL"}
                ],
                "stage": "tipo"
            }
        
        elif stage == "tipo":
            state["data"]["tipo"] = message
            return {
                "texto": f"Perfecto, instalación {message}.\n\n📏 ¿Área en m²?",
                "stage": "area"
            }
        
        elif stage == "area":
            try:
                area = float(message)
                state["data"]["area"] = area
                return {
                    "texto": f"📐 Área: {area} m²\n\n🏢 ¿Cuántos pisos?",
                    "stage": "pisos"
                }
            except:
                return {
                    "texto": "Por favor ingresa un número válido",
                    "stage": "area"
                }
        
        # ... más etapas (pisos, puntos, tomas, tableros, quotation)
        
        elif stage == "quotation":
            return self._generar_cotizacion_electricidad(state["data"])
    
    def _generar_cotizacion_electricidad(self, data: Dict) -> Dict:
        """Genera cotización eléctrica"""
        tipo = data["tipo"]
        area = data["area"]
        puntos = data.get("puntos_luz", 0)
        tomas = data.get("tomacorrientes", 0)
        
        precios = self.kb["tipos"][tipo]["precios"]
        
        items = [
            {
                "descripcion": f"Puntos de luz ({puntos})",
                "total": puntos * precios["punto_luz"]
            },
            # ... más items
        ]
        
        total = sum(item["total"] for item in items)
        
        return {
            "texto": f"📊 COTIZACIÓN\n\nTotal: S/ {total:.2f}",
            "items": items,
            "total": total,
            "stage": "complete"
        }


# ══════════════════════════════════════════════════════════
# 📋 ITSE (Líneas 950-1200)
# ══════════════════════════════════════════════════════════

class ITSESpecialist(LocalSpecialist):
    """Especialista en certificaciones ITSE"""
    
    def _process_itse(self, message: str, state: Dict) -> Dict:
        stage = state.get("stage", "initial")
        
        if stage == "initial":
            return {
                "texto": "Selecciona tu tipo de establecimiento:",
                "botones": [
                    {"text": "🏥 Salud", "value": "SALUD"},
                    {"text": "🎓 Educación", "value": "EDUCACION"},
                    # ... 6 más
                ],
                "stage": "categoria"
            }
        
        elif stage == "categoria":
            state["data"]["categoria"] = message
            tipos = self.kb["categorias"][message]["tipos"]
            return {
                "texto": f"¿Qué tipo específico de {message}?",
                "botones": [{"text": t, "value": t} for t in tipos],
                "stage": "tipo"
            }
        
        # ... más etapas (tipo, area, pisos, quotation)
        
        elif stage == "quotation":
            return self._generar_cotizacion_itse(state["data"])
    
    def _calcular_riesgo(self, categoria: str, area: float, pisos: int) -> str:
        """Calcula nivel de riesgo ITSE"""
        if categoria == "SALUD":
            if area > 500 or pisos >= 2:
                return "MUY_ALTO"
            return "ALTO"
        
        # ... más reglas
        
        return self.kb["categorias"][categoria]["riesgo_default"]
    
    def _generar_cotizacion_itse(self, data: Dict) -> Dict:
        """Genera cotización ITSE"""
        riesgo = self._calcular_riesgo(
            data["categoria"],
            data["area"],
            data["pisos"]
        )
        
        municipal = self.kb["precios_municipales"][riesgo]
        tesla = self.kb["precios_tesla"][riesgo]
        
        total_min = municipal["precio"] + tesla["min"]
        total_max = municipal["precio"] + tesla["max"]
        
        return {
            "texto": f"📊 COTIZACIÓN ITSE\n\nNivel: {riesgo}\nTotal: S/ {total_min} - {total_max}",
            "total_min": total_min,
            "total_max": total_max,
            "stage": "complete"
        }


# ══════════════════════════════════════════════════════════
# 🔌 POZO A TIERRA (Líneas 1200-1400)
# ══════════════════════════════════════════════════════════

class PozoTierraSpecialist(LocalSpecialist):
    """Especialista en sistemas de puesta a tierra"""
    # ... (similar estructura, ~200 líneas)


# ══════════════════════════════════════════════════════════
# 🔥 CONTRAINCENDIOS (Líneas 1400-1600)
# ══════════════════════════════════════════════════════════

class ContraincendiosSpecialist(LocalSpecialist):
    """Especialista en sistemas contraincendios"""
    # ... (~200 líneas)


# ══════════════════════════════════════════════════════════
# 🏠 DOMÓTICA (Líneas 1600-1800)
# ══════════════════════════════════════════════════════════

class DomoticaSpecialist(LocalSpecialist):
    """Especialista en domótica"""
    # ... (~200 líneas)


# ══════════════════════════════════════════════════════════
# 📹 CCTV (Líneas 1800-2000)
# ══════════════════════════════════════════════════════════

class CCTVSpecialist(LocalSpecialist):
    """Especialista en CCTV"""
    # ... (~200 líneas)


# ══════════════════════════════════════════════════════════
# 🌐 REDES (Líneas 2000-2200)
# ══════════════════════════════════════════════════════════

class RedesSpecialist(LocalSpecialist):
    """Especialista en redes"""
    # ... (~200 líneas)


# ══════════════════════════════════════════════════════════
# ⚙️ AUTOMATIZACIÓN INDUSTRIAL (Líneas 2200-2400)
# ══════════════════════════════════════════════════════════

class AutomatizacionSpecialist(LocalSpecialist):
    """Especialista en automatización industrial"""
    # ... (~200 líneas)


# ══════════════════════════════════════════════════════════
# 📄 EXPEDIENTES (Líneas 2400-2600)
# ══════════════════════════════════════════════════════════

class ExpedientesSpecialist(LocalSpecialist):
    """Especialista en expedientes técnicos"""
    # ... (~200 líneas)


# ══════════════════════════════════════════════════════════
# 💧 SANEAMIENTO (Líneas 2600-2800)
# ══════════════════════════════════════════════════════════

class SaneamientoSpecialist(LocalSpecialist):
    """Especialista en saneamiento"""
    # ... (~200 líneas)


# ══════════════════════════════════════════════════════════
# 🏭 FACTORY (Líneas 2800-2900)
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
        """Crea especialista local"""
        specialist_class = cls._specialists.get(service_type)
        if not specialist_class:
            return LocalSpecialist(service_type)
        return specialist_class(service_type)


# ══════════════════════════════════════════════════════════
# 🎯 FUNCIÓN PRINCIPAL (Líneas 2900-3000)
# ══════════════════════════════════════════════════════════

def process_with_local_specialist(
    service_type: str,
    message: str,
    conversation_state: Dict
) -> Dict:
    """
    Procesa mensaje con especialista local
    Se usa como FALLBACK cuando Gemini no está disponible
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
            "stage": "error"
        }
```

---

## ✅ VENTAJAS de UN SOLO ARCHIVO

### **1. Simplicidad**
- ✅ Un solo archivo para revisar
- ✅ Búsqueda rápida (Ctrl+F)
- ✅ No necesitas navegar entre carpetas

### **2. Mantenibilidad**
- ✅ Fácil de encontrar código
- ✅ Fácil de copiar/pegar entre servicios
- ✅ Cambios globales más rápidos

### **3. Performance**
- ✅ Un solo import
- ✅ Carga más rápida en memoria
- ✅ Menos overhead de archivos

### **4. Desarrollo**
- ✅ Fácil de debuggear
- ✅ Stack traces más claros
- ✅ No te pierdes entre archivos

### **5. Git**
- ✅ Un solo archivo en commits
- ✅ Diff más claro
- ✅ Menos conflictos

---

## ❌ DESVENTAJAS (Mínimas)

- ⚠️ Archivo grande (~2500 líneas)
  - **Solución:** Buena organización con comentarios
  
- ⚠️ Scroll largo
  - **Solución:** Usar outline del IDE (Ctrl+Shift+O)

---

## 🔄 Integración con Sistema Existente

### **En `pili_integrator.py`:**

```python
# backend/app/services/pili_integrator.py

from .pili_local_specialists import process_with_local_specialist

async def _generar_respuesta_chat(self, mensaje, tipo_flujo, historial, servicio, datos_acumulados):
    """Genera respuesta conversacional"""
    
    # 1. Intentar con Gemini (IA de clase mundial)
    if self.estado_servicios["gemini"] and self.gemini_service:
        try:
            respuesta_gemini = await self.gemini_service.chat_conversacional(...)
            if respuesta_gemini.get("success"):
                return respuesta_gemini
        except Exception as e:
            logger.warning(f"Gemini no disponible: {e}")
    
    # 2. FALLBACK: Usar especialista local
    logger.info("🔄 Usando especialista local como fallback")
    return process_with_local_specialist(
        service_type=servicio,
        message=mensaje,
        conversation_state=datos_acumulados or {}
    )
```

---

## 🎯 CONCLUSIÓN FINAL

### **Recomendación: UN SOLO ARCHIVO**

**Archivo:** `backend/app/services/pili_local_specialists.py`
**Tamaño:** ~2500-3000 líneas
**Estructura:**
- Knowledge bases (500 líneas)
- Clase base (200 líneas)
- 10 especialistas (200 líneas cada uno = 2000 líneas)
- Factory (100 líneas)
- Función principal (100 líneas)

**Por qué:**
1. ✅ **Simple** - Un solo archivo
2. ✅ **Práctico** - Fácil de mantener
3. ✅ **Suficiente** - Solo es fallback
4. ✅ **Organizado** - Con buenos comentarios
5. ✅ **Escalable** - Funciona para 10 servicios

**NO necesitas:**
- ❌ Carpeta `specialists/`
- ❌ Carpeta `knowledge/`
- ❌ Carpeta `base/`
- ❌ 10+ archivos separados

---

## 🚀 Próximo Paso

¿Procedo a crear `pili_local_specialists.py` con los 10 servicios?
