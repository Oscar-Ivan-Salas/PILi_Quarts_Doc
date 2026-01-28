# 🏗️ Arquitectura Profesional: PILI Especialistas Escalable

## 🎯 Pregunta Crítica del Usuario

> "¿Agregar 5000+ líneas a `pili_brain.py` o modularizar en 10 archivos pequeños?"
> "Esto será una App Web de clase mundial con miles de usuarios concurrentes"

---

## 📊 Análisis de Opciones

### **Opción 1: Monolítico (Todo en pili_brain.py)**

```
pili_brain.py (7000+ líneas)
├── SERVICIOS_PILI (líneas 38-118)
├── KNOWLEDGE_BASE_ELECTRICIDAD (500 líneas)
├── KNOWLEDGE_BASE_ITSE (500 líneas)
├── KNOWLEDGE_BASE_POZO_TIERRA (500 líneas)
├── ... (8 servicios más × 500 líneas = 4000 líneas)
└── PILIBrain class (1615 líneas existentes)
```

**Ventajas:**
- ✅ Un solo archivo
- ✅ Fácil de encontrar

**Desventajas:**
- ❌ **7000+ líneas** (imposible de mantener)
- ❌ **Lento** para cargar en memoria
- ❌ **Difícil de debuggear**
- ❌ **Conflictos** en Git con múltiples desarrolladores
- ❌ **No escalable** para miles de usuarios
- ❌ **Viola principios SOLID**

**Veredicto:** ❌ **NO RECOMENDADO** para app profesional

---

### **Opción 2: Modular Completo (10 archivos separados)**

```
backend/app/services/pili/
├── __init__.py
├── base.py                          # Clase base abstracta
├── specialists/
│   ├── __init__.py
│   ├── electricidad_specialist.py   # 300 líneas
│   ├── itse_specialist.py           # 300 líneas
│   ├── pozo_tierra_specialist.py    # 300 líneas
│   ├── contraincendios_specialist.py
│   ├── domotica_specialist.py
│   ├── cctv_specialist.py
│   ├── redes_specialist.py
│   ├── automatizacion_specialist.py
│   ├── expedientes_specialist.py
│   └── saneamiento_specialist.py
├── knowledge_bases/
│   ├── __init__.py
│   ├── electricidad_kb.py           # 200 líneas
│   ├── itse_kb.py                   # 200 líneas
│   └── ... (8 más)
└── calculators/
    ├── __init__.py
    ├── electricidad_calculator.py
    ├── itse_calculator.py
    └── ... (8 más)
```

**Ventajas:**
- ✅ **Modular** y organizado
- ✅ **Fácil de mantener**
- ✅ **Fácil de testear**
- ✅ **Múltiples devs** pueden trabajar sin conflictos
- ✅ **Escalable**
- ✅ **Sigue principios SOLID**

**Desventajas:**
- ⚠️ Más archivos (pero organizados)
- ⚠️ Requiere imports

**Veredicto:** ✅ **RECOMENDADO** para app profesional

---

### **Opción 3: Híbrido (Recomendación del Especialista)**

```
backend/app/services/pili/
├── __init__.py                      # Exports públicos
├── pili_brain.py                    # Core (mantener, 1615 líneas)
├── pili_integrator.py               # Orchestrator (mantener, 980 líneas)
├── base_specialist.py               # Clase base abstracta (150 líneas)
│
├── specialists/                     # ✅ NUEVO
│   ├── __init__.py
│   ├── electricidad.py              # 250 líneas
│   ├── itse.py                      # 250 líneas
│   ├── pozo_tierra.py
│   ├── contraincendios.py
│   ├── domotica.py
│   ├── cctv.py
│   ├── redes.py
│   ├── automatizacion.py
│   ├── expedientes.py
│   └── saneamiento.py
│
└── knowledge/                       # ✅ NUEVO
    ├── __init__.py
    ├── precios.py                   # Precios centralizados
    ├── reglas.py                    # Reglas de negocio
    └── normativas.py                # Normativas técnicas
```

**Ventajas:**
- ✅ **Mantiene** archivos existentes
- ✅ **Modular** para nuevos servicios
- ✅ **Escalable** y profesional
- ✅ **Fácil migración** gradual
- ✅ **Mejor de ambos mundos**

**Veredicto:** ✅✅ **ALTAMENTE RECOMENDADO**

---

## 🏗️ Arquitectura Profesional Recomendada

### **Estructura de Carpetas:**

```
backend/app/
├── services/
│   ├── pili/
│   │   ├── __init__.py
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── brain.py              # PILIBrain (mantener)
│   │   │   ├── integrator.py         # PILIIntegrator (mantener)
│   │   │   └── orchestrator.py       # PILIOrchestrator (mantener)
│   │   │
│   │   ├── base/
│   │   │   ├── __init__.py
│   │   │   ├── specialist.py         # Clase base abstracta
│   │   │   ├── knowledge_base.py     # Base para KB
│   │   │   └── calculator.py         # Base para cálculos
│   │   │
│   │   ├── specialists/              # ✅ 10 especialistas
│   │   │   ├── __init__.py
│   │   │   ├── electricidad.py
│   │   │   ├── itse.py
│   │   │   ├── pozo_tierra.py
│   │   │   ├── contraincendios.py
│   │   │   ├── domotica.py
│   │   │   ├── cctv.py
│   │   │   ├── redes.py
│   │   │   ├── automatizacion.py
│   │   │   ├── expedientes.py
│   │   │   └── saneamiento.py
│   │   │
│   │   ├── knowledge/                # ✅ Knowledge bases
│   │   │   ├── __init__.py
│   │   │   ├── precios.py
│   │   │   ├── reglas.py
│   │   │   └── normativas.py
│   │   │
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── validators.py
│   │       └── formatters.py
│   │
│   ├── generators/                   # Mantener
│   ├── gemini_service.py             # Mantener
│   └── ...
│
├── routers/
│   ├── chat.py                       # Mantener
│   └── ...
│
└── models/
    ├── cliente.py                    # Mantener
    └── ...
```

---

## 🎨 Patrón de Diseño: Strategy + Factory

### **1. Clase Base Abstracta:**

```python
# backend/app/services/pili/base/specialist.py

from abc import ABC, abstractmethod
from typing import Dict, List, Optional

class BaseSpecialist(ABC):
    """
    Clase base abstracta para todos los especialistas PILI
    Patrón: Strategy Pattern
    """
    
    def __init__(self):
        self.knowledge_base = self.load_knowledge_base()
        self.conversation_stages = self.define_stages()
    
    @abstractmethod
    def load_knowledge_base(self) -> Dict:
        """Carga knowledge base específico del servicio"""
        pass
    
    @abstractmethod
    def define_stages(self) -> List[str]:
        """Define etapas de conversación"""
        pass
    
    @abstractmethod
    def process_stage(self, stage: str, user_input: str, state: Dict) -> Dict:
        """Procesa una etapa de conversación"""
        pass
    
    @abstractmethod
    def calculate_quotation(self, data: Dict) -> Dict:
        """Calcula cotización"""
        pass
    
    def get_initial_message(self) -> Dict:
        """Mensaje inicial (puede ser sobrescrito)"""
        return {
            "texto": f"¡Hola! Soy PILI, especialista en {self.get_service_name()}.",
            "botones": self.get_initial_buttons()
        }
    
    @abstractmethod
    def get_service_name(self) -> str:
        """Nombre del servicio"""
        pass
    
    @abstractmethod
    def get_initial_buttons(self) -> List[Dict]:
        """Botones iniciales"""
        pass
```

### **2. Especialista Concreto (Ejemplo: Electricidad):**

```python
# backend/app/services/pili/specialists/electricidad.py

from ..base.specialist import BaseSpecialist
from ..knowledge.precios import PRECIOS_ELECTRICIDAD
from ..knowledge.reglas import REGLAS_ELECTRICIDAD

class ElectricidadSpecialist(BaseSpecialist):
    """
    Especialista en Instalaciones Eléctricas
    Maneja: Residencial, Comercial, Industrial
    """
    
    def load_knowledge_base(self) -> Dict:
        return {
            "tipos": {
                "RESIDENCIAL": {
                    "nombre": "Instalación Eléctrica Residencial",
                    "precios": PRECIOS_ELECTRICIDAD["residencial"],
                    "reglas": REGLAS_ELECTRICIDAD["residencial"]
                },
                "COMERCIAL": {
                    "nombre": "Instalación Eléctrica Comercial",
                    "precios": PRECIOS_ELECTRICIDAD["comercial"],
                    "reglas": REGLAS_ELECTRICIDAD["comercial"]
                },
                "INDUSTRIAL": {
                    "nombre": "Instalación Eléctrica Industrial",
                    "precios": PRECIOS_ELECTRICIDAD["industrial"],
                    "reglas": REGLAS_ELECTRICIDAD["industrial"]
                }
            }
        }
    
    def define_stages(self) -> List[str]:
        return [
            "initial",
            "tipo_instalacion",
            "area",
            "pisos",
            "puntos_luz",
            "tomacorrientes",
            "tableros",
            "quotation"
        ]
    
    def get_service_name(self) -> str:
        return "Instalaciones Eléctricas"
    
    def get_initial_buttons(self) -> List[Dict]:
        return [
            {"text": "🏠 Residencial", "value": "RESIDENCIAL"},
            {"text": "🏢 Comercial", "value": "COMERCIAL"},
            {"text": "🏭 Industrial", "value": "INDUSTRIAL"}
        ]
    
    def process_stage(self, stage: str, user_input: str, state: Dict) -> Dict:
        if stage == "initial":
            return self._process_initial(user_input, state)
        elif stage == "tipo_instalacion":
            return self._process_tipo(user_input, state)
        elif stage == "area":
            return self._process_area(user_input, state)
        # ... más etapas
    
    def _process_initial(self, user_input: str, state: Dict) -> Dict:
        """Procesa selección inicial"""
        state["tipo"] = user_input
        return {
            "texto": f"Perfecto, instalación {user_input}.\n\n📏 ¿Cuál es el área total en m²?",
            "stage": "area",
            "state": state
        }
    
    def _process_area(self, user_input: str, state: Dict) -> Dict:
        """Procesa área"""
        try:
            area = float(user_input)
            if area <= 0:
                raise ValueError()
            
            state["area"] = area
            return {
                "texto": f"📐 Área: {area} m²\n\n🏢 ¿Cuántos pisos tiene?",
                "stage": "pisos",
                "state": state
            }
        except:
            return {
                "texto": "Por favor ingresa un número válido de área en m²",
                "stage": "area",  # Mantener en misma etapa
                "state": state
            }
    
    def calculate_quotation(self, data: Dict) -> Dict:
        """Calcula cotización eléctrica"""
        tipo = data["tipo"]
        area = data["area"]
        puntos = data["puntos_luz"]
        tomas = data["tomacorrientes"]
        tableros = data["tableros"]
        
        precios = self.knowledge_base["tipos"][tipo]["precios"]
        
        items = [
            {
                "descripcion": f"Puntos de luz empotrados ({puntos})",
                "cantidad": puntos,
                "precio_unitario": precios["punto_luz"],
                "total": puntos * precios["punto_luz"]
            },
            {
                "descripcion": f"Tomacorrientes dobles ({tomas})",
                "cantidad": tomas,
                "precio_unitario": precios["tomacorriente"],
                "total": tomas * precios["tomacorriente"]
            },
            {
                "descripcion": f"Tableros eléctricos ({tableros})",
                "cantidad": tableros,
                "precio_unitario": precios["tablero"],
                "total": tableros * precios["tablero"]
            },
            {
                "descripcion": f"Cable THW 2.5mm² ({area * 1.5}m)",
                "cantidad": area * 1.5,
                "precio_unitario": precios["cable_m2"],
                "total": area * 1.5 * precios["cable_m2"]
            }
        ]
        
        subtotal = sum(item["total"] for item in items)
        
        return {
            "items": items,
            "subtotal": subtotal,
            "igv": subtotal * 0.18,
            "total": subtotal * 1.18
        }
```

### **3. Factory Pattern:**

```python
# backend/app/services/pili/__init__.py

from .specialists.electricidad import ElectricidadSpecialist
from .specialists.itse import ITSESpecialist
from .specialists.pozo_tierra import PozoTierraSpecialist
# ... imports

class SpecialistFactory:
    """
    Factory para crear especialistas
    Patrón: Factory Pattern
    """
    
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
    def create(cls, service_type: str) -> BaseSpecialist:
        """Crea especialista según tipo de servicio"""
        specialist_class = cls._specialists.get(service_type)
        if not specialist_class:
            raise ValueError(f"Servicio no soportado: {service_type}")
        
        return specialist_class()
    
    @classmethod
    def get_available_services(cls) -> List[str]:
        """Retorna lista de servicios disponibles"""
        return list(cls._specialists.keys())
```

---

## 🚀 Escalabilidad para Miles de Usuarios

### **1. Caching con Redis:**

```python
# backend/app/services/pili/core/cache.py

import redis
import json
from typing import Optional

class ConversationCache:
    """Cache de conversaciones con Redis"""
    
    def __init__(self):
        self.redis = redis.Redis(
            host='localhost',
            port=6379,
            db=0,
            decode_responses=True
        )
    
    def save_state(self, user_id: str, conversation_state: Dict):
        """Guarda estado de conversación"""
        key = f"pili:conversation:{user_id}"
        self.redis.setex(
            key,
            3600,  # 1 hora de expiración
            json.dumps(conversation_state)
        )
    
    def get_state(self, user_id: str) -> Optional[Dict]:
        """Obtiene estado de conversación"""
        key = f"pili:conversation:{user_id}"
        data = self.redis.get(key)
        return json.loads(data) if data else None
```

### **2. Async/Await para Concurrencia:**

```python
# backend/app/routers/chat.py

from fastapi import APIRouter, BackgroundTasks
import asyncio

@router.post("/chat")
async def chat_endpoint(
    request: ChatRequest,
    background_tasks: BackgroundTasks
):
    """Endpoint async para manejar miles de usuarios"""
    
    # Crear especialista
    specialist = SpecialistFactory.create(request.service_type)
    
    # Procesar en paralelo
    response = await asyncio.create_task(
        specialist.process_stage_async(
            request.stage,
            request.user_input,
            request.state
        )
    )
    
    # Guardar en background
    background_tasks.add_task(
        save_conversation_history,
        request.user_id,
        response
    )
    
    return response
```

### **3. Load Balancing:**

```
┌─────────────┐
│   Nginx     │  ← Load Balancer
│   (Port 80) │
└──────┬──────┘
       │
       ├──────────────┬──────────────┬──────────────┐
       │              │              │              │
   ┌───▼───┐      ┌───▼───┐      ┌───▼───┐      ┌───▼───┐
   │FastAPI│      │FastAPI│      │FastAPI│      │FastAPI│
   │ :8001 │      │ :8002 │      │ :8003 │      │ :8004 │
   └───┬───┘      └───┬───┘      └───┬───┘      └───┬───┘
       │              │              │              │
       └──────────────┴──────────────┴──────────────┘
                      │
                  ┌───▼───┐
                  │ Redis │  ← Cache compartido
                  │ Cache │
                  └───┬───┘
                      │
                  ┌───▼───┐
                  │  DB   │  ← PostgreSQL
                  └───────┘
```

---

## ✅ Recomendación Final

### **Arquitectura Híbrida Modular:**

1. ✅ **Mantener** archivos core existentes
2. ✅ **Crear** carpeta `specialists/` con 10 archivos
3. ✅ **Crear** carpeta `knowledge/` centralizada
4. ✅ **Usar** Factory Pattern
5. ✅ **Implementar** caching con Redis
6. ✅ **Usar** async/await
7. ✅ **Preparar** para load balancing

### **Ventajas:**
- ✅ **Escalable** a miles de usuarios
- ✅ **Mantenible** (cada servicio 250 líneas)
- ✅ **Testeable** (tests unitarios por servicio)
- ✅ **Profesional** (patrones de diseño)
- ✅ **Rápido** (caching + async)
- ✅ **Organizado** (estructura clara)

---

## 🎯 Próximos Pasos

1. Crear estructura de carpetas
2. Crear `BaseSpecialist` abstracto
3. Migrar ITSE a `ITSESpecialist`
4. Crear `ElectricidadSpecialist`
5. Implementar Factory
6. Probar con 2-3 servicios
7. Replicar para los 10

¿Procedo con esta arquitectura profesional?
