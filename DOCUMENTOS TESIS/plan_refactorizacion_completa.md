# 🔧 PLAN DE REFACTORIZACIÓN - Reducir 12,000 → 3,000 Líneas

## 🎯 Objetivo
Eliminar duplicidad, consolidar lógica de servicios, y crear arquitectura clara donde cada archivo tiene UNA responsabilidad.

---

## 📊 ESTADO ACTUAL (12,000 líneas)

### Backend
| Archivo | Líneas | ¿Necesario? | Acción |
|---------|--------|-------------|--------|
| `chat.py` | 4,601 | ✅ Parcial | **REDUCIR a 300 líneas** (solo endpoints) |
| `pili_integrator.py` | 1,249 | ❌ NO | **ELIMINAR** (funcionalidad a chat_service.py) |
| `pili_local_specialists.py` | 3,879 | ✅ SÍ | **MANTENER** (es el cerebro correcto) |
| `pili_brain.py` | 1,615 | ❌ NO | **ELIMINAR** (duplica KNOWLEDGE_BASE) |

### Frontend
| Archivo | Líneas | ¿Necesario? | Acción |
|---------|--------|-------------|--------|
| `ChatIA.jsx` | 466 | ❌ NO | **ELIMINAR** (unificar en UniversalChat.jsx) |
| `PiliITSEChat.jsx` | 482 | ✅ Parcial | **REFACTORIZAR** → UniversalChat.jsx |

---

## ✅ ARQUITECTURA OBJETIVO (3,000 líneas)

### Backend Simplificado

```
backend/
├── routers/
│   └── chat.py (300 líneas) ← REDUCIDO
│       └── POST /api/chat
│           ├── Valida entrada
│           ├── Llama a ChatService
│           └── Retorna respuesta
│
├── services/
│   ├── chat_service.py (400 líneas) ← NUEVO
│   │   └── Orquestador único
│   │       ├── Detecta servicio
│   │       ├── Crea especialista correcto
│   │       ├── Maneja conversación
│   │       └── Genera documentos
│   │
│   └── specialists/
│       ├── base.py (150 líneas) ← NUEVO
│       │   └── BaseSpecialist (clase abstracta)
│       │
│       ├── itse.py (250 líneas) ← EXTRAÍDO de pili_local_specialists.py
│       ├── electricidad.py (250 líneas) ← EXTRAÍDO
│       ├── pozo_tierra.py (200 líneas) ← EXTRAÍDO
│       └── ... (7 archivos más)
│
└── data/
    └── knowledge_base.py (600 líneas) ← CONSOLIDADO
        └── KNOWLEDGE_BASE completo (10 servicios)
```

**Total Backend:** ~2,700 líneas

### Frontend Simplificado

```
frontend/src/components/
└── UniversalChat.jsx (300 líneas) ← NUEVO
    └── Props: { serviceType: 'itse' | 'electricidad' | ... }
```

**Total Frontend:** 300 líneas

---

## 🔍 ANÁLISIS DE DUPLICIDAD

### 1. Detección de Servicio (TRIPLICADA)

**Actual:**
- `chat.py` línea 2850: `detectar_servicio()`
- `pili_integrator.py` línea 180: `detectar_servicio()`
- `pili_brain.py` línea 200: `detectar_servicio()`

**Objetivo:**
- `chat_service.py` línea 50: `detectar_servicio()` ← **ÚNICA**

### 2. KNOWLEDGE_BASE (DUPLICADO)

**Actual:**
- `pili_local_specialists.py` línea 50-686: KNOWLEDGE_BASE completo
- `pili_brain.py` línea 38-150: KNOWLEDGE_BASE parcial

**Objetivo:**
- `knowledge_base.py`: KNOWLEDGE_BASE completo ← **ÚNICO**

### 3. Lógica de Conversación (DUPLICADA)

**Actual:**
- `chat.py` línea 2800-3000: Maneja conversación
- `pili_local_specialists.py` línea 1206-1400: Maneja conversación

**Objetivo:**
- `specialists/itse.py`: Maneja conversación ← **ÚNICO**

---

## 📋 PLAN DE EJECUCIÓN (Paso a Paso)

### FASE 1: Preparación (30 min)

#### 1.1 Crear Rama de Refactorización
```bash
git checkout -b refactor/clean-architecture
git commit -m "CHECKPOINT: Antes de refactorización"
```

#### 1.2 Crear Estructura de Carpetas
```bash
mkdir backend/app/services/specialists
mkdir backend/app/data
```

---

### FASE 2: Consolidar KNOWLEDGE_BASE (1 hora)

#### 2.1 Crear `knowledge_base.py`
```python
# backend/app/data/knowledge_base.py

KNOWLEDGE_BASE = {
    "itse": { ... },      # Copiar de pili_local_specialists.py línea 686-827
    "electricidad": { ... },  # Copiar de pili_local_specialists.py línea 54-300
    # ... resto de servicios
}
```

#### 2.2 Actualizar Imports
- `pili_local_specialists.py`: `from app.data.knowledge_base import KNOWLEDGE_BASE`
- Verificar que funciona: `python -c "from app.data.knowledge_base import KNOWLEDGE_BASE; print(list(KNOWLEDGE_BASE.keys()))"`

#### 2.3 Eliminar KNOWLEDGE_BASE de `pili_brain.py`
- Comentar líneas 38-150
- Actualizar imports

---

### FASE 3: Extraer Especialistas (2 horas)

#### 3.1 Crear `base.py`
```python
# backend/app/services/specialists/base.py

class BaseSpecialist:
    def __init__(self, service_type: str):
        self.service_type = service_type
        self.kb = KNOWLEDGE_BASE.get(service_type, {})
        self.conversation_state = {
            'stage': 'initial',
            'data': {},
            'history': []
        }
    
    def process_message(self, message: str, state: dict) -> dict:
        raise NotImplementedError
```

#### 3.2 Crear `itse.py`
```python
# backend/app/services/specialists/itse.py

from .base import BaseSpecialist

class ITSESpecialist(BaseSpecialist):
    def process_message(self, message: str, state: dict) -> dict:
        # Copiar de pili_local_specialists.py línea 1206-1400
        ...
```

#### 3.3 Crear Factory
```python
# backend/app/services/specialists/__init__.py

from .itse import ITSESpecialist
from .electricidad import ElectricidadSpecialist
# ... resto

SPECIALISTS = {
    'itse': ITSESpecialist,
    'electricidad': ElectricidadSpecialist,
    # ...
}

def create_specialist(service_type: str):
    specialist_class = SPECIALISTS.get(service_type)
    if not specialist_class:
        raise ValueError(f"Servicio no soportado: {service_type}")
    return specialist_class(service_type)
```

---

### FASE 4: Crear ChatService (1 hora)

#### 4.1 Crear `chat_service.py`
```python
# backend/app/services/chat_service.py

from app.services.specialists import create_specialist
from app.data.knowledge_base import KNOWLEDGE_BASE

class ChatService:
    def process_message(self, mensaje: str, tipo_flujo: str, 
                       conversation_state: dict = None) -> dict:
        """
        Procesa un mensaje de chat.
        
        Returns:
            {
                'success': bool,
                'respuesta': str,
                'botones': list,
                'state': dict,
                'datos_generados': dict (opcional)
            }
        """
        # 1. Detectar servicio
        service_type = self._detect_service(mensaje, tipo_flujo)
        
        # 2. Crear especialista
        specialist = create_specialist(service_type)
        
        # 3. Procesar mensaje
        if conversation_state:
            specialist.conversation_state = conversation_state
        
        response = specialist.process_message(mensaje, conversation_state or {})
        
        # 4. Retornar respuesta
        return {
            'success': True,
            'respuesta': response.get('texto', ''),
            'botones': response.get('botones', []),
            'state': response.get('state', {}),
            'datos_generados': response.get('datos_generados')
        }
    
    def _detect_service(self, mensaje: str, tipo_flujo: str) -> str:
        # Mapeo directo de tipo_flujo
        mapping = {
            'itse': 'itse',
            'cotizacion-simple': 'electricidad',
            # ...
        }
        return mapping.get(tipo_flujo, 'electricidad')
```

---

### FASE 5: Simplificar `chat.py` (30 min)

#### 5.1 Reducir a Solo Endpoint
```python
# backend/app/routers/chat.py (REDUCIDO a 300 líneas)

from app.services.chat_service import ChatService

chat_service = ChatService()

@router.post("/chat-contextualizado")
async def chat_contextualizado(request: ChatRequest):
    try:
        response = chat_service.process_message(
            mensaje=request.mensaje,
            tipo_flujo=request.tipo_flujo,
            conversation_state=request.conversation_state
        )
        return response
    except Exception as e:
        logger.error(f"Error: {e}")
        return {"success": False, "error": str(e)}
```

#### 5.2 Eliminar Código Duplicado
- Eliminar líneas 2800-3500 (lógica de conversación)
- Mantener solo endpoints y validación

---

### FASE 6: Frontend Unificado (2 horas)

#### 6.1 Crear `UniversalChat.jsx`
```javascript
// frontend/src/components/UniversalChat.jsx

const UniversalChat = ({ serviceType, onDatosGenerados }) => {
    // Lógica genérica que funciona para TODOS los servicios
    // Recibe serviceType como prop: 'itse', 'electricidad', etc.
    
    const tipoFlujoMap = {
        'itse': 'itse',
        'electricidad': 'cotizacion-simple',
        // ...
    };
    
    const enviarMensaje = async (mensaje) => {
        const response = await fetch('/api/chat/chat-contextualizado', {
            method: 'POST',
            body: JSON.stringify({
                tipo_flujo: tipoFlujoMap[serviceType],
                mensaje,
                conversation_state: conversationState
            })
        });
        // ... resto igual
    };
    
    // ... resto del componente
};
```

#### 6.2 Actualizar `App.jsx`
```javascript
// Reemplazar:
<PiliITSEChat ... />

// Por:
<UniversalChat serviceType="itse" ... />
```

---

### FASE 7: Eliminar Archivos Innecesarios (15 min)

```bash
# Mover a backup (NO eliminar aún)
mkdir backend/_deprecated
mv backend/app/services/pili_integrator.py backend/_deprecated/
mv backend/app/services/pili_brain.py backend/_deprecated/
mv frontend/src/components/ChatIA.jsx frontend/_deprecated/
mv frontend/src/components/PiliITSEChat.jsx frontend/_deprecated/
```

---

### FASE 8: Testing (1 hora)

#### 8.1 Test Backend
```bash
python -c "from app.services.chat_service import ChatService; cs = ChatService(); r = cs.process_message('SALUD', 'itse', {'stage':'initial','data':{}}); print('STAGE:', r['state']['stage']); print('SUCCESS:', r['success'])"
```

**Esperado:**
```
STAGE: tipo_especifico
SUCCESS: True
```

#### 8.2 Test Frontend
1. Abrir navegador
2. Ir a chat ITSE
3. Hacer clic en "Salud"
4. Verificar que responde: "Perfecto, sector **Establecimientos de Salud**..."

#### 8.3 Test Completo
- Probar todos los servicios (electricidad, ITSE, pozo tierra)
- Verificar generación de documentos
- Verificar vista previa

---

## 📊 RESULTADO ESPERADO

### Antes
```
Backend:  11,344 líneas (4 archivos)
Frontend:    948 líneas (2 componentes)
Total:    12,292 líneas
```

### Después
```
Backend:   2,700 líneas (chat.py 300 + chat_service.py 400 + specialists 1,400 + knowledge_base 600)
Frontend:    300 líneas (UniversalChat.jsx)
Total:     3,000 líneas
```

**Reducción: 75%** (de 12,000 a 3,000 líneas)

---

## ⚠️ RIESGOS Y MITIGACIÓN

### Riesgo 1: Romper Funcionalidad Existente
**Mitigación:**
- Hacer en rama separada
- Testing exhaustivo en cada fase
- Mantener archivos viejos en `_deprecated/` hasta confirmar que todo funciona

### Riesgo 2: Tiempo Mayor al Estimado
**Mitigación:**
- Plan dividido en fases pequeñas
- Cada fase es independiente
- Puedes parar en cualquier momento y seguir después

### Riesgo 3: Bugs Nuevos
**Mitigación:**
- Testing después de cada fase
- Rollback fácil con git
- Archivos viejos disponibles para referencia

---

## 🎯 DECISIÓN REQUERIDA

¿Quieres proceder con este plan?

**Opción A:** SÍ, empezar con Fase 1 (Preparación)  
**Opción B:** Modificar el plan primero  
**Opción C:** Hacer solo algunas fases (¿cuáles?)

**Tiempo total estimado:** 8 horas de trabajo  
**Beneficio:** Sistema limpio, mantenible, escalable
