# 🏗️ PLAN INTEGRAL DE REFACTORIZACIÓN ARQUITECTÓNICA
## Senior Architect - Soluciones Permanentes

---

## 📋 ÍNDICE

1. [Análisis de Problemas Estructurales](#1-análisis-de-problemas-estructurales)
2. [Arquitectura Objetivo](#2-arquitectura-objetivo)
3. [Plan de Migración en Fases](#3-plan-de-migración-en-fases)
4. [Estrategia de Testing](#4-estrategia-de-testing)
5. [Roadmap de Implementación](#5-roadmap-de-implementación)

---

## 1. ANÁLISIS DE PROBLEMAS ESTRUCTURALES

### 1.1 Problemas Críticos Identificados

#### A. **Duplicidad de Responsabilidades (Frontend ↔ Backend)**

**Problema:**
```
Frontend (PiliITSEChat.jsx)
├── Mensaje inicial hardcoded ❌
├── Botones hardcoded ❌
├── Lógica de presentación ⚠️
└── Estado de conversación ⚠️

Backend (pili_local_specialists.py)
├── Mismo mensaje inicial ❌
├── Mismos botones ❌
├── Lógica de negocio ✅
└── Estado de conversación ✅
```

**Causa Raíz:** Violación del principio de Single Source of Truth (SSOT)

**Impacto:**
- Cambios requieren modificar 2 archivos
- Desincronización entre frontend y backend
- Bugs difíciles de rastrear

---

#### B. **Múltiples Flujos para Mismo Objetivo**

**Problema:**
```
chat.py tiene 2 flujos para ITSE:

Flujo 1: Bypass Directo (línea 2891)
├── LocalSpecialistFactory.create('itse')
└── ITSESpecialist.process_message()

Flujo 2: PILIIntegrator (línea 2954)
├── pili_integrator.procesar_solicitud_completa()
├── LocalSpecialistFactory.create('itse')
└── ITSESpecialist.process_message()
```

**Causa Raíz:** Código legacy + parches incrementales

**Impacto:**
- Confusión sobre cuál usar
- Mantenimiento duplicado
- Bugs en uno no se arreglan en el otro

---

#### C. **Arquitectura de 12,000 Líneas**

**Problema:**
```
chat.py: 4,636 líneas
pili_local_specialists.py: 3,880 líneas
pili_integrator.py: 1,248 líneas
pili_brain.py: 1,614 líneas
─────────────────────────────
TOTAL: 11,378 líneas para chat
```

**Causa Raíz:** Crecimiento orgánico sin refactorización

**Impacto:**
- Imposible de mantener
- Onboarding de nuevos devs: 2+ semanas
- Bugs ocultos en código muerto

---

#### D. **Estado Distribuido**

**Problema:**
```
Estado de conversación existe en:
├── Frontend: conversationState
├── Backend: conversation_state (parámetro)
├── Backend: self.conversation_state (clase)
└── Backend: state (retorno)
```

**Causa Raíz:** Sin arquitectura clara de manejo de estado

**Impacto:**
- Desincronización
- Pérdida de contexto
- Chat se rompe aleatoriamente

---

### 1.2 Análisis de Causa Raíz (5 Whys)

**¿Por qué el chat ITSE no funciona?**
→ Porque el estado no se actualiza correctamente

**¿Por qué el estado no se actualiza?**
→ Porque hay múltiples flujos y no todos actualizan el estado

**¿Por qué hay múltiples flujos?**
→ Porque se agregaron bypasses para "arreglar rápido"

**¿Por qué se agregaron bypasses?**
→ Porque la arquitectura original no soportaba ITSE fácilmente

**¿Por qué la arquitectura no lo soportaba?**
→ **CAUSA RAÍZ:** Arquitectura monolítica sin separación de responsabilidades

---

## 2. ARQUITECTURA OBJETIVO

### 2.1 Principios de Diseño

1. **Single Source of Truth (SSOT)**
   - Frontend: Solo presentación
   - Backend: Única fuente de verdad

2. **Separation of Concerns (SoC)**
   - Cada capa tiene una responsabilidad clara
   - Sin lógica de negocio en frontend

3. **Single Responsibility Principle (SRP)**
   - Cada clase/función hace UNA cosa
   - Archivos < 500 líneas

4. **Don't Repeat Yourself (DRY)**
   - Cero duplicación de código
   - Reutilización mediante composición

5. **Open/Closed Principle (OCP)**
   - Fácil agregar nuevos servicios
   - Sin modificar código existente

---

### 2.2 Arquitectura en Capas

```
┌─────────────────────────────────────────────────┐
│           FRONTEND (React)                      │
│  ┌──────────────────────────────────────────┐  │
│  │  UniversalChat.jsx (300 líneas)          │  │
│  │  - Renderiza mensajes                    │  │
│  │  - Envía clicks al backend               │  │
│  │  - NO tiene lógica de negocio            │  │
│  └──────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
                      ↓ HTTP POST
┌─────────────────────────────────────────────────┐
│           API LAYER (FastAPI)                   │
│  ┌──────────────────────────────────────────┐  │
│  │  chat.py (300 líneas)                    │  │
│  │  - Valida request                        │  │
│  │  - Llama a ChatService                   │  │
│  │  - Retorna response                      │  │
│  └──────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│        SERVICE LAYER (Business Logic)           │
│  ┌──────────────────────────────────────────┐  │
│  │  ChatService (400 líneas)                │  │
│  │  - Detecta servicio                      │  │
│  │  - Crea especialista correcto            │  │
│  │  - Orquesta conversación                 │  │
│  │  - Maneja estado                         │  │
│  └──────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│        SPECIALIST LAYER (Domain Logic)          │
│  ┌──────────────────────────────────────────┐  │
│  │  BaseSpecialist (150 líneas)             │  │
│  │  - Clase abstracta                       │  │
│  │  - Métodos comunes                       │  │
│  └──────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────┐  │
│  │  ITSESpecialist (250 líneas)             │  │
│  │  - Lógica específica ITSE                │  │
│  │  - Maneja conversación ITSE              │  │
│  └──────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────┐  │
│  │  ElectricidadSpecialist (250 líneas)     │  │
│  │  - Lógica específica electricidad        │  │
│  └──────────────────────────────────────────┘  │
│  ... (8 especialistas más)                     │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│         DATA LAYER (Knowledge Base)             │
│  ┌──────────────────────────────────────────┐  │
│  │  knowledge_base.py (600 líneas)          │  │
│  │  - KNOWLEDGE_BASE único                  │  │
│  │  - Configuración de servicios            │  │
│  └──────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
```

**Total:** ~2,500 líneas (vs 12,000 actuales)

---

### 2.3 Flujo de Datos Unidireccional

```
Usuario hace click
    ↓
UniversalChat.jsx
    ↓ fetch('/api/chat', {mensaje, serviceType})
chat.py (API)
    ↓ ChatService.process_message()
ChatService
    ↓ create_specialist(serviceType)
ITSESpecialist
    ↓ process_message(mensaje, state)
Lógica de negocio
    ↓ return {texto, botones, state}
ChatService
    ↓ return response
chat.py
    ↓ JSON response
UniversalChat.jsx
    ↓ setState(response)
Renderiza UI
```

**Características:**
- ✅ Flujo lineal (fácil de seguir)
- ✅ Sin bypasses
- ✅ Sin duplicación
- ✅ Estado manejado solo en backend

---

## 3. PLAN DE MIGRACIÓN EN FASES

### FASE 1: Preparación (2 horas)

#### 1.1 Crear Rama de Refactorización
```bash
git checkout -b refactor/clean-architecture
git commit -m "CHECKPOINT: Antes de refactorización integral"
```

#### 1.2 Crear Estructura de Carpetas
```bash
mkdir -p backend/app/services/chat
mkdir -p backend/app/services/specialists
mkdir -p backend/app/data
```

#### 1.3 Crear task.md
```markdown
# Refactorización Integral - Chat PILI

## Fase 1: Preparación
- [x] Crear rama
- [x] Crear estructura
- [ ] Crear task.md

## Fase 2: Data Layer
- [ ] Consolidar KNOWLEDGE_BASE
- [ ] Crear knowledge_base.py
- [ ] Migrar datos

## Fase 3: Specialist Layer
- [ ] Crear BaseSpecialist
- [ ] Extraer ITSESpecialist
- [ ] Crear Factory

## Fase 4: Service Layer
- [ ] Crear ChatService
- [ ] Migrar lógica de orquestación
- [ ] Eliminar bypasses

## Fase 5: API Layer
- [ ] Simplificar chat.py
- [ ] Un solo endpoint
- [ ] Eliminar código legacy

## Fase 6: Frontend
- [ ] Crear UniversalChat.jsx
- [ ] Eliminar lógica hardcoded
- [ ] Migrar PiliITSEChat

## Fase 7: Testing
- [ ] Tests unitarios
- [ ] Tests de integración
- [ ] Tests E2E

## Fase 8: Deployment
- [ ] Merge a main
- [ ] Deploy
- [ ] Monitoreo
```

---

### FASE 2: Data Layer (1 hora)

#### 2.1 Consolidar KNOWLEDGE_BASE

**Crear:** `backend/app/data/knowledge_base.py`

```python
"""
Única fuente de verdad para configuración de servicios
"""

KNOWLEDGE_BASE = {
    "itse": {
        "nombre": "Certificados ITSE",
        "categorias": {
            "SALUD": {
                "nombre": "Establecimientos de Salud",
                "tipos": [
                    "Centro de Salud",
                    "Clínica",
                    "Hospital",
                    # ...
                ]
            },
            # ... resto de categorías
        },
        "precios_base": {
            "hasta_100m2": 450.00,
            "hasta_500m2": 850.00,
            # ...
        }
    },
    "electricidad": {
        # ...
    },
    # ... resto de servicios
}

def get_service_config(service_type: str) -> dict:
    """Obtiene configuración de un servicio"""
    return KNOWLEDGE_BASE.get(service_type, {})
```

#### 2.2 Migrar Datos

**Acción:**
1. Copiar KNOWLEDGE_BASE de `pili_local_specialists.py` líneas 50-686
2. Pegar en `knowledge_base.py`
3. Eliminar de `pili_local_specialists.py`
4. Eliminar de `pili_brain.py`

**Verificación:**
```python
from app.data.knowledge_base import KNOWLEDGE_BASE
assert "itse" in KNOWLEDGE_BASE
assert "SALUD" in KNOWLEDGE_BASE["itse"]["categorias"]
```

---

### FASE 3: Specialist Layer (3 horas)

#### 3.1 Crear BaseSpecialist

**Crear:** `backend/app/services/specialists/base.py`

```python
from abc import ABC, abstractmethod
from typing import Dict, Any
from app.data.knowledge_base import get_service_config

class BaseSpecialist(ABC):
    """Clase base para todos los especialistas"""
    
    def __init__(self, service_type: str):
        self.service_type = service_type
        self.kb = get_service_config(service_type)
        self.conversation_state = {
            'stage': 'initial',
            'data': {},
            'history': []
        }
    
    @abstractmethod
    def process_message(self, message: str, state: Dict = None) -> Dict[str, Any]:
        """
        Procesa un mensaje del usuario
        
        Args:
            message: Mensaje del usuario
            state: Estado de conversación (opcional)
        
        Returns:
            {
                'texto': str,
                'botones': list,
                'state': dict,
                'datos_generados': dict (opcional)
            }
        """
        pass
    
    def reset_conversation(self):
        """Reinicia la conversación"""
        self.conversation_state = {
            'stage': 'initial',
            'data': {},
            'history': []
        }
```

#### 3.2 Extraer ITSESpecialist

**Crear:** `backend/app/services/specialists/itse.py`

```python
from .base import BaseSpecialist
from typing import Dict, Any

class ITSESpecialist(BaseSpecialist):
    """Especialista en certificaciones ITSE"""
    
    def process_message(self, message: str, state: Dict = None) -> Dict[str, Any]:
        # Usar estado proporcionado o el interno
        if state:
            self.conversation_state = state
        
        stage = self.conversation_state["stage"]
        data = self.conversation_state["data"]
        
        # Detectar selección de categoría
        message_upper = message.upper().strip()
        if message_upper in self.kb["categorias"].keys():
            return self._handle_categoria_selection(message_upper)
        
        # Procesar según stage
        if stage == "initial":
            return self._handle_initial()
        elif stage == "tipo_especifico":
            return self._handle_tipo_especifico(message)
        elif stage == "area":
            return self._handle_area(message)
        elif stage == "datos_cliente":
            return self._handle_datos_cliente(message)
        elif stage == "confirmacion":
            return self._handle_confirmacion(message)
        else:
            return self._handle_error()
    
    def _handle_initial(self) -> Dict[str, Any]:
        """Maneja el mensaje inicial"""
        return {
            "texto": """¡Hola! 👋 Soy **PILI**, especialista en certificados ITSE.
            
🎯 Te ayudo a obtener tu certificado ITSE con:
✅ Visita técnica GRATUITA
✅ Precios oficiales TUPA Huancayo
✅ Trámite 100% gestionado
✅ Entrega en 7 días hábiles

**Selecciona tu tipo de establecimiento:**""",
            "botones": [
                {"text": "🏥 Salud", "value": "SALUD"},
                {"text": "🎓 Educación", "value": "EDUCACION"},
                {"text": "🏨 Hospedaje", "value": "HOSPEDAJE"},
                {"text": "🏪 Comercio", "value": "COMERCIO"},
                {"text": "🍽️ Restaurante", "value": "RESTAURANTE"},
                {"text": "🏢 Oficina", "value": "OFICINA"},
                {"text": "🏭 Industrial", "value": "INDUSTRIAL"},
                {"text": "🎭 Encuentro", "value": "ENCUENTRO"}
            ],
            "state": self.conversation_state,
            "progreso": "1/5"
        }
    
    def _handle_categoria_selection(self, categoria: str) -> Dict[str, Any]:
        """Maneja la selección de categoría"""
        self.conversation_state["data"]["categoria"] = categoria
        self.conversation_state["stage"] = "tipo_especifico"
        
        tipos = self.kb["categorias"][categoria]["tipos"]
        
        return {
            "texto": f"""Perfecto, sector **{self.kb["categorias"][categoria]["nombre"]}**.

¿Qué tipo específico es tu establecimiento?""",
            "botones": [{"text": t, "value": t} for t in tipos],
            "state": self.conversation_state,
            "progreso": "2/5"
        }
    
    # ... resto de métodos _handle_*
```

#### 3.3 Crear Factory

**Crear:** `backend/app/services/specialists/__init__.py`

```python
from .base import BaseSpecialist
from .itse import ITSESpecialist
from .electricidad import ElectricidadSpecialist
# ... resto de imports

SPECIALISTS = {
    'itse': ITSESpecialist,
    'electricidad': ElectricidadSpecialist,
    # ... resto
}

def create_specialist(service_type: str) -> BaseSpecialist:
    """
    Factory para crear especialistas
    
    Args:
        service_type: Tipo de servicio ('itse', 'electricidad', etc.)
    
    Returns:
        Instancia del especialista correspondiente
    
    Raises:
        ValueError: Si el servicio no existe
    """
    specialist_class = SPECIALISTS.get(service_type)
    if not specialist_class:
        raise ValueError(f"Servicio '{service_type}' no soportado")
    return specialist_class(service_type)
```

---

### FASE 4: Service Layer (2 horas)

#### 4.1 Crear ChatService

**Crear:** `backend/app/services/chat/chat_service.py`

```python
from typing import Dict, Any, Optional
from app.services.specialists import create_specialist
import logging

logger = logging.getLogger(__name__)

class ChatService:
    """
    Servicio de chat que orquesta la conversación
    
    Responsabilidades:
    - Detectar tipo de servicio
    - Crear especialista correcto
    - Manejar estado de conversación
    - Retornar respuesta estructurada
    """
    
    def process_message(
        self,
        mensaje: str,
        tipo_flujo: str,
        conversation_state: Optional[Dict] = None,
        historial: Optional[list] = None
    ) -> Dict[str, Any]:
        """
        Procesa un mensaje de chat
        
        Args:
            mensaje: Mensaje del usuario
            tipo_flujo: Tipo de flujo ('itse', 'cotizacion-simple', etc.)
            conversation_state: Estado de conversación (opcional)
            historial: Historial de mensajes (opcional)
        
        Returns:
            {
                'success': bool,
                'respuesta': str,
                'botones': list,
                'state': dict,
                'datos_generados': dict (opcional)
            }
        """
        try:
            # 1. Mapear tipo_flujo a service_type
            service_type = self._map_tipo_flujo(tipo_flujo)
            logger.info(f"📨 Procesando mensaje para servicio: {service_type}")
            
            # 2. Crear especialista
            specialist = create_specialist(service_type)
            
            # 3. Procesar mensaje
            response = specialist.process_message(mensaje, conversation_state)
            
            # 4. Retornar respuesta estructurada
            return {
                'success': True,
                'respuesta': response.get('texto', ''),
                'botones': response.get('botones', []),
                'state': response.get('state'),
                'datos_generados': response.get('datos_generados'),
                'progreso': response.get('progreso', '0/0')
            }
            
        except ValueError as e:
            logger.error(f"❌ Error de validación: {e}")
            return {
                'success': False,
                'error': str(e),
                'respuesta': 'Lo siento, hubo un error. Por favor intenta de nuevo.'
            }
        except Exception as e:
            logger.error(f"❌ Error inesperado: {e}")
            return {
                'success': False,
                'error': str(e),
                'respuesta': 'Error interno. Por favor contacta a soporte.'
            }
    
    def _map_tipo_flujo(self, tipo_flujo: str) -> str:
        """Mapea tipo_flujo del frontend a service_type del backend"""
        mapping = {
            'itse': 'itse',
            'cotizacion-simple': 'electricidad',
            'cotizacion-compleja': 'electricidad',
            'proyecto-simple': 'electricidad',
            'proyecto-complejo': 'electricidad',
            # ... resto
        }
        return mapping.get(tipo_flujo, 'electricidad')
```

---

### FASE 5: API Layer (1 hora)

#### 5.1 Simplificar chat.py

**Reducir de 4,636 líneas a 300 líneas:**

```python
from fastapi import APIRouter, HTTPException, Body
from typing import Optional, Dict, List
from app.services.chat.chat_service import ChatService
import logging

router = APIRouter()
logger = logging.getLogger(__name__)
chat_service = ChatService()

@router.post("/chat-contextualizado")
async def chat_contextualizado(
    tipo_flujo: str = Body(...),
    mensaje: str = Body(...),
    historial: Optional[List[Dict]] = Body(None),
    conversation_state: Optional[Dict] = Body(None),
    contexto_adicional: Optional[str] = Body(None),
    generar_html: bool = Body(False),
    datos_cliente: Optional[Dict] = Body(None)
):
    """
    Endpoint único para chat contextualizado con PILI
    
    Maneja TODOS los tipos de flujo (ITSE, electricidad, etc.)
    """
    try:
        logger.info(f"🤖 Chat contextualizado: {tipo_flujo}")
        
        # Procesar con ChatService
        response = chat_service.process_message(
            mensaje=mensaje,
            tipo_flujo=tipo_flujo,
            conversation_state=conversation_state,
            historial=historial or []
        )
        
        return response
        
    except Exception as e:
        logger.error(f"❌ Error en chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))
```

**Eliminar:**
- ❌ Bypass directo ITSE (líneas 2891-2924)
- ❌ Flujo PILIIntegrator duplicado
- ❌ Código legacy (3,000+ líneas)

---

### FASE 6: Frontend (2 horas)

#### 6.1 Crear UniversalChat.jsx

**Crear:** `frontend/src/components/UniversalChat.jsx`

```javascript
import React, { useState, useRef, useEffect } from 'react';
import { Send } from 'lucide-react';

/**
 * Componente universal de chat para TODOS los servicios
 * 
 * Props:
 * - serviceType: 'itse' | 'electricidad' | ...
 * - onDatosGenerados: callback cuando se generan datos
 */
const UniversalChat = ({ serviceType, onDatosGenerados, onBack }) => {
    const [conversacion, setConversacion] = useState([]);
    const [inputValue, setInputValue] = useState('');
    const [isTyping, setIsTyping] = useState(false);
    const [conversationState, setConversationState] = useState(null);
    const messagesEndRef = useRef(null);
    const initialized = useRef(false);

    // Mapeo de serviceType a tipo_flujo del backend
    const tipoFlujoMap = {
        'itse': 'itse',
        'electricidad': 'cotizacion-simple',
        // ...
    };

    useEffect(() => {
        if (initialized.current) return;
        initialized.current = true;

        // Obtener mensaje inicial del backend
        enviarMensajeBackend('INIT');
    }, []);

    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [conversacion]);

    const enviarMensajeBackend = async (mensaje) => {
        setIsTyping(true);

        try {
            const response = await fetch('http://localhost:8000/api/chat/chat-contextualizado', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    tipo_flujo: tipoFlujoMap[serviceType],
                    mensaje: mensaje,
                    historial: conversacion.map(msg => ({
                        tipo: msg.sender === 'bot' ? 'asistente' : 'usuario',
                        mensaje: msg.text
                    })),
                    conversation_state: conversationState
                })
            });

            const data = await response.json();

            if (data.success) {
                // Actualizar estado
                if (data.state) {
                    setConversationState(data.state);
                }

                // Agregar respuesta
                addBotMessage(data.respuesta, data.botones);

                // Notificar datos generados
                if (data.datos_generados && onDatosGenerados) {
                    onDatosGenerados(data.datos_generados);
                }
            } else {
                addBotMessage('Lo siento, hubo un error. Por favor intenta de nuevo.');
            }
        } catch (error) {
            console.error('Error:', error);
            addBotMessage('Error de conexión. Verifica que el backend esté activo.');
        } finally {
            setIsTyping(false);
        }
    };

    const addBotMessage = (text, buttons = null) => {
        const mensaje = {
            sender: 'bot',
            text,
            buttons,
            timestamp: new Date().toLocaleTimeString('es-PE', { hour: '2-digit', minute: '2-digit' })
        };
        setConversacion(prev => [...prev, mensaje]);
    };

    const addUserMessage = (text) => {
        const mensaje = {
            sender: 'user',
            text,
            timestamp: new Date().toLocaleTimeString('es-PE', { hour: '2-digit', minute: '2-digit' })
        };
        setConversacion(prev => [...prev, mensaje]);
    };

    const handleButtonClick = async (value, label) => {
        addUserMessage(label);
        await enviarMensajeBackend(value);
    };

    const handleSendMessage = async () => {
        if (!inputValue.trim()) return;
        
        addUserMessage(inputValue);
        await enviarMensajeBackend(inputValue);
        setInputValue('');
    };

    // ... resto del componente (renderizado)
};

export default UniversalChat;
```

#### 6.2 Migrar PiliITSEChat

**En `App.jsx`:**

```javascript
// Antes:
<PiliITSEChat 
    onDatosGenerados={...}
    onBack={...}
/>

// Después:
<UniversalChat 
    serviceType="itse"
    onDatosGenerados={...}
    onBack={...}
/>
```

**Eliminar:**
- ❌ `PiliITSEChat.jsx` (mover a `_deprecated/`)
- ❌ `ChatIA.jsx` (mover a `_deprecated/`)

---

### FASE 7: Testing (3 horas)

#### 7.1 Tests Unitarios

**Crear:** `backend/tests/test_specialists.py`

```python
import pytest
from app.services.specialists import create_specialist

def test_itse_specialist_initial():
    """Test mensaje inicial de ITSESpecialist"""
    specialist = create_specialist('itse')
    response = specialist.process_message('INIT', None)
    
    assert response['texto'].startswith('¡Hola!')
    assert len(response['botones']) == 8
    assert response['state']['stage'] == 'initial'

def test_itse_specialist_categoria():
    """Test selección de categoría"""
    specialist = create_specialist('itse')
    response = specialist.process_message('SALUD', {'stage': 'initial', 'data': {}})
    
    assert 'Salud' in response['texto']
    assert response['state']['stage'] == 'tipo_especifico'
    assert response['state']['data']['categoria'] == 'SALUD'
```

#### 7.2 Tests de Integración

**Crear:** `backend/tests/test_chat_service.py`

```python
import pytest
from app.services.chat.chat_service import ChatService

def test_chat_service_itse_flow():
    """Test flujo completo de ITSE"""
    service = ChatService()
    
    # Mensaje inicial
    r1 = service.process_message('INIT', 'itse', None)
    assert r1['success']
    assert len(r1['botones']) == 8
    
    # Selección de categoría
    r2 = service.process_message('SALUD', 'itse', r1['state'])
    assert r2['success']
    assert r2['state']['data']['categoria'] == 'SALUD'
```

#### 7.3 Tests E2E

**Crear:** `frontend/src/__tests__/UniversalChat.test.jsx`

```javascript
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import UniversalChat from '../components/UniversalChat';

test('UniversalChat muestra mensaje inicial', async () => {
    render(<UniversalChat serviceType="itse" />);
    
    await waitFor(() => {
        expect(screen.getByText(/Hola/i)).toBeInTheDocument();
    });
});

test('UniversalChat maneja click en botón', async () => {
    render(<UniversalChat serviceType="itse" />);
    
    await waitFor(() => {
        const botonSalud = screen.getByText(/Salud/i);
        fireEvent.click(botonSalud);
    });
    
    await waitFor(() => {
        expect(screen.getByText(/tipo específico/i)).toBeInTheDocument();
    });
});
```

---

## 4. ESTRATEGIA DE TESTING

### 4.1 Pirámide de Testing

```
        E2E Tests (10%)
       /              \
      /                \
     /  Integration (30%)\
    /                    \
   /   Unit Tests (60%)   \
  /________________________\
```

### 4.2 Coverage Mínimo

- Unit Tests: 80%
- Integration Tests: 60%
- E2E Tests: Flujos críticos (ITSE, Electricidad)

### 4.3 CI/CD

```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run backend tests
        run: pytest backend/tests
      - name: Run frontend tests
        run: npm test
```

---

## 5. ROADMAP DE IMPLEMENTACIÓN

### Semana 1: Foundation

| Día | Fase | Horas | Entregable |
|-----|------|-------|------------|
| 1 | Fase 1: Preparación | 2h | Estructura + task.md |
| 1 | Fase 2: Data Layer | 1h | knowledge_base.py |
| 2-3 | Fase 3: Specialist Layer | 6h | BaseSpecialist + ITSESpecialist |
| 4 | Fase 4: Service Layer | 2h | ChatService |
| 5 | Fase 5: API Layer | 1h | chat.py simplificado |

**Total Semana 1:** 12 horas

---

### Semana 2: Frontend + Testing

| Día | Fase | Horas | Entregable |
|-----|------|-------|------------|
| 1-2 | Fase 6: Frontend | 4h | UniversalChat.jsx |
| 3-5 | Fase 7: Testing | 6h | Tests completos |

**Total Semana 2:** 10 horas

---

### Semana 3: Deployment + Monitoring

| Día | Fase | Horas | Entregable |
|-----|------|-------|------------|
| 1 | Fase 8: Deployment | 2h | Deploy a producción |
| 2-5 | Monitoreo | 4h | Logs + Métricas |

**Total Semana 3:** 6 horas

---

## 6. MÉTRICAS DE ÉXITO

### 6.1 Métricas Técnicas

| Métrica | Antes | Objetivo | Medición |
|---------|-------|----------|----------|
| Líneas de código | 12,000 | 2,500 | -79% |
| Archivos | 25 | 12 | -52% |
| Duplicación | 40% | 0% | SonarQube |
| Complejidad ciclomática | 150 | 10 | Radon |
| Coverage | 0% | 80% | pytest-cov |

### 6.2 Métricas de Negocio

| Métrica | Antes | Objetivo |
|---------|-------|----------|
| Tiempo de onboarding | 2 semanas | 2 días |
| Tiempo de agregar servicio | 1 semana | 2 horas |
| Bugs en producción | 5/mes | 0/mes |
| Tiempo de respuesta | 500ms | 100ms |

---

## 7. RIESGOS Y MITIGACIÓN

### Riesgo 1: Romper Funcionalidad Existente

**Probabilidad:** Alta  
**Impacto:** Crítico

**Mitigación:**
- Trabajar en rama separada
- Tests exhaustivos
- Deployment gradual (feature flags)
- Rollback plan

---

### Riesgo 2: Tiempo Mayor al Estimado

**Probabilidad:** Media  
**Impacto:** Alto

**Mitigación:**
- Plan dividido en fases pequeñas
- Cada fase es independiente
- Puede pausarse en cualquier momento

---

### Riesgo 3: Resistencia al Cambio

**Probabilidad:** Baja  
**Impacto:** Medio

**Mitigación:**
- Documentación clara
- Capacitación del equipo
- Beneficios medibles

---

## 8. CONCLUSIÓN

### 8.1 Beneficios de la Refactorización

**Técnicos:**
- ✅ Código 79% más pequeño
- ✅ Cero duplicación
- ✅ Fácil de mantener
- ✅ Fácil de testear
- ✅ Escalable

**Negocio:**
- ✅ Menos bugs
- ✅ Desarrollo más rápido
- ✅ Onboarding más fácil
- ✅ Mejor experiencia de usuario

### 8.2 Próximos Pasos

1. **Aprobar plan** (tú decides)
2. **Crear rama** (5 min)
3. **Fase 1: Preparación** (2 horas)
4. **Continuar según roadmap**

---

## 9. DECISIÓN REQUERIDA

¿Apruebas este plan integral de refactorización?

**Opción A:** SÍ, proceder con Fase 1  
**Opción B:** Modificar el plan primero  
**Opción C:** Solo hacer parches (NO recomendado)

**Mi recomendación como Senior Architect:** Opción A

**Tiempo total:** 28 horas (3.5 días de trabajo)  
**Beneficio:** Sistema limpio, mantenible, escalable para los próximos 5 años
