# PILi_Quarts V3.0 (Versión Estable)

**Anteriormente:** `workspace-modern`

Esta es la versión consolidad y modular del sistema PILi Quarts, diseñada para eliminar conflictos de versiones anteriores.

## 🚀 Stack Tecnológico

### Frontend
- React 18 + Vite
- shadcn/ui + Radix UI
- Tailwind CSS v4
- Tiptap (Document Editor)
- Framer Motion (Animations)
- Zustand (State Management)
- Socket.IO Client (Real-time)

### Backend
- Python FastAPI
- PostgreSQL / SQLite (Development)
- WebSockets
- Gemini AI
- **Nodos Integrados (N04/N06)** con Plantillas "Espejo"

## 📁 Estructura

```
PILi_Quarts_V3.0/
├── frontend/          # React + Vite
├── backend/           # Python FastAPI
├── DOCUMENTOS PILi/   # Documentación Técnica
└── INICIAR.ps1        # Script de Arranque Rápido
```

## 🔧 Desarrollo Local

### Opción A: Script Automático (Recomendado)
Ejecutar desde PowerShell en la carpeta raíz:
```powershell
.\INICIAR.ps1
```

### Opción B: Manual

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

#### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\Activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8005 --reload
```

## 🌐 URLs

- Frontend: http://localhost:3010
- Backend API: http://localhost:8005
- API Docs: http://localhost:8005/docs
