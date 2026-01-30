# PILi_Quarts Workspace Modern

Workspace moderno con tecnologías de última generación.

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
- PostgreSQL
- WebSockets
- Gemini AI

## 📁 Estructura

```
workspace-modern/
├── frontend/          # React + Vite
├── backend/           # Python FastAPI
├── docker-compose.yml
└── README.md
```

## 🐳 Docker

```bash
docker-compose up -d
```

## 🔧 Desarrollo Local

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## 🌐 URLs

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 📝 Notas

Este es un proyecto completamente nuevo y separado del PILi_Quarts existente.
El código original permanece intacto en la carpeta raíz.
