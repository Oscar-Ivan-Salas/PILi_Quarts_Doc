# 📋 ARCHIVOS MÍNIMOS PARA CHAT INTELIGENTE

## 🎯 RESUMEN EJECUTIVO

**Total de archivos necesarios:** 8 archivos

- **Frontend:** 2 archivos
- **Backend:** 6 archivos

---

## 🖥️ FRONTEND (2 archivos)

### 1. `App.jsx`
**Ruta:** `frontend/src/App.jsx`  
**Líneas:** ~2,300 (pero solo usa 50 líneas para chat)  
**Responsabilidad:**
- Renderizar el componente de chat cuando usuario selecciona ITSE
- Pasar props al componente de chat
- Manejar navegación

**Código relevante:**
```javascript
// Línea 6
import PiliITSEChat from './components/PiliITSEChat';

// Línea 1798
<PiliITSEChat
    onDatosGenerados={handleDatosGenerados}
    onBack={() => setPantallaActual('inicio')}
/>
```

---

### 2. `PiliITSEChat.jsx`
**Ruta:** `frontend/src/components/PiliITSEChat.jsx`  
**Líneas:** 483  
**Responsabilidad:**
- Renderizar interfaz de chat
- Enviar mensajes al backend
- Mostrar respuestas y botones
- Mantener estado de conversación (temporal)

**Funciones clave:**
- `enviarMensajeBackend()` - Hace fetch a `/api/chat/chat-contextualizado`
- `addBotMessage()` - Agrega mensaje del bot
- `addUserMessage()` - Agrega mensaje del usuario
- `handleButtonClick()` - Maneja clicks en botones

---

## ⚙️ BACKEND (6 archivos)

### 1. `main.py`
**Ruta:** `backend/app/main.py`  
**Líneas:** ~1,000 (pero solo usa 20 líneas para chat)  
**Responsabilidad:**
- Inicializar FastAPI
- Registrar routers
- Configurar CORS

**Código relevante:**
```python
from app.routers import chat

app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
```

---

### 2. `chat.py`
**Ruta:** `backend/app/routers/chat.py`  
**Líneas:** 4,636 (pero solo usa 200 líneas para ITSE)  
**Responsabilidad:**
- Endpoint `/api/chat/chat-contextualizado`
- Recibir request del frontend
- Llamar a `ITSESpecialist`
- Retornar response

**Código relevante (líneas 2891-2918):**
```python
@router.post("/chat-contextualizado")
async def chat_contextualizado(...):
    # Bypass directo para ITSE
    if tipo_flujo == 'itse':
        specialist = LocalSpecialistFactory.create('itse')
        response = specialist.process_message(mensaje, conversation_state)
        return response
```

---

### 3. `pili_local_specialists.py`
**Ruta:** `backend/app/services/pili_local_specialists.py`  
**Líneas:** 3,880 (pero solo usa 500 líneas para ITSE)  
**Responsabilidad:**
- Clase `ITSESpecialist`
- Lógica de conversación ITSE
- KNOWLEDGE_BASE de ITSE
- Manejo de estado de conversación

**Clases clave:**
- `LocalSpecialist` (clase base)
- `ITSESpecialist` (especialista ITSE)
- `LocalSpecialistFactory` (factory para crear especialistas)

**Métodos clave:**
- `process_message()` - Procesa mensaje del usuario
- `_process_itse()` - Lógica específica de ITSE

---

### 4. `database.py`
**Ruta:** `backend/app/core/database.py`  
**Líneas:** 83  
**Responsabilidad:**
- Conexión a base de datos
- Sesión de SQLAlchemy
- Dependency injection

**Código relevante:**
```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

---

### 5. `config.py`
**Ruta:** `backend/app/core/config.py`  
**Líneas:** 304  
**Responsabilidad:**
- Configuración global
- Variables de entorno
- Rutas de archivos

**Variables clave:**
```python
class Settings:
    DATABASE_URL: str
    GEMINI_API_KEY: str
    TEMPLATES_DIR: Path
    GENERATED_DIR: Path
```

---

### 6. `models/` (opcional pero recomendado)
**Ruta:** `backend/app/models/`  
**Archivos:** `cliente.py`, `cotizacion.py`, etc.  
**Responsabilidad:**
- Modelos de base de datos
- Solo si quieres guardar cotizaciones

---

## 📊 DIAGRAMA DE DEPENDENCIAS

```
Frontend
├── App.jsx
│   └── PiliITSEChat.jsx
│       └── fetch('/api/chat/chat-contextualizado')
│
Backend
├── main.py
│   └── include_router(chat.router)
│       └── chat.py
│           └── LocalSpecialistFactory.create('itse')
│               └── pili_local_specialists.py
│                   ├── ITSESpecialist
│                   └── KNOWLEDGE_BASE
│
Config
├── config.py
└── database.py
```

---

## ✅ ARCHIVOS MÍNIMOS (Sin Extras)

Si quieres el **mínimo absoluto** para que funcione:

### Frontend (2 archivos)
1. `App.jsx`
2. `PiliITSEChat.jsx`

### Backend (4 archivos)
1. `main.py`
2. `chat.py`
3. `pili_local_specialists.py`
4. `config.py`

**Total:** 6 archivos

---

## ❌ ARCHIVOS QUE NO SON NECESARIOS

### Frontend
- ❌ `ChatIA.jsx` (componente viejo)
- ❌ Otros componentes de chat

### Backend
- ❌ `pili_integrator.py` (si usas bypass directo)
- ❌ `pili_brain.py` (si usas bypass directo)
- ❌ `pili_orchestrator.py` (ya movido a deprecated)
- ❌ `gemini_service.py` (si no usas Gemini)
- ❌ `multi_ia_*` (ya movidos a deprecated)
- ❌ Carpeta `pili/` (ya movida a backup)
- ❌ Carpeta `professional/` (ya movida a backup)

---

## 🎯 CONFIGURACIÓN MÍNIMA

### 1. Variables de Entorno

**`.env`:**
```env
DATABASE_URL=sqlite:///./tesla.db
GEMINI_API_KEY=tu_key_aqui  # Opcional si no usas IA
```

### 2. Dependencias Python

**`requirements.txt`:**
```
fastapi
uvicorn
sqlalchemy
pydantic
python-dotenv
```

### 3. Dependencias Frontend

**`package.json`:**
```json
{
  "dependencies": {
    "react": "^18.0.0",
    "react-dom": "^18.0.0",
    "lucide-react": "^0.263.1"
  }
}
```

---

## 🚀 CÓMO EJECUTAR (Mínimo)

### Backend
```bash
cd backend
python -m uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm start
```

---

## 📋 CHECKLIST DE ARCHIVOS

### ✅ Archivos Necesarios

**Frontend:**
- [x] `App.jsx`
- [x] `PiliITSEChat.jsx`

**Backend:**
- [x] `main.py`
- [x] `chat.py`
- [x] `pili_local_specialists.py`
- [x] `config.py`
- [x] `database.py` (opcional)

**Total:** 6-7 archivos

---

## 🎯 CONCLUSIÓN

**Para que el chat inteligente funcione necesitas:**

### Mínimo Absoluto
- **6 archivos** (2 frontend + 4 backend)
- **~9,000 líneas** de código (pero solo ~1,000 se usan activamente)

### Recomendado
- **7 archivos** (incluir database.py)
- Permite guardar cotizaciones en BD

### Arquitectura Limpia (Plan Integral)
- **12 archivos** (bien organizados)
- **~2,500 líneas** de código
- Fácil de mantener y escalar

---

## 💡 RECOMENDACIÓN

**Opción 1: Mínimo (6 archivos)**
- ✅ Funciona ahora
- ❌ Difícil de mantener
- ❌ Código duplicado

**Opción 2: Arquitectura Limpia (12 archivos)**
- ✅ Fácil de mantener
- ✅ Sin duplicación
- ✅ Escalable
- ⏰ 28 horas de trabajo

**Mi recomendación:** Opción 2 (vale la pena la inversión)
