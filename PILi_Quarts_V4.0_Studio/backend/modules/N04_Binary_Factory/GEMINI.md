---
trigger: always_on
---

# GEMINI.md — N04 Binary Factory

> Este archivo define cómo el AI se comporta DENTRO de este módulo.
> Prioridad: Este archivo > Los skills en `.agent/skills/`

---

## 🎯 IDENTIDAD DEL MÓDULO

**N04 Binary Factory** es un **microservicio autónomo** de generación de documentos profesionales.
- **Backend**: FastAPI en puerto **8005**
- **Frontend (Studio)**: React/Vite en puerto **5173**
- **Independiente**: No depende de ningún otro servicio de PILi_Quarts

---

## 🤖 AGENTE ACTIVO

Para cualquier tarea en este módulo, aplicar el skill **`binary-factory`** como base.

```
🤖 Aplicando conocimiento de @[binary-factory]...
```

### Routing por tarea:

| Tipo de tarea | Skill a aplicar |
|---|---|
| Modificar generadores Python | `python-patterns` |
| Modificar UI del Studio | `frontend-design` |
| Crear/modificar templates HTML | `binary-factory` |
| Debug de generación | `python-patterns` |
| Nuevo endpoint API | `python-patterns` |

---

## 📋 REGLAS DE ESTE MÓDULO

### 🔴 CRÍTICO — NO HACER:

1. **NO mover archivos** fuera de esta carpeta
2. **NO crear dependencias** hacia otros módulos del proyecto PILi
3. **NO modificar lógica** de los generadores sin auditoría
4. **NO usar** `AnimatePresence mode="wait"` en el frontend (causa crash)
5. **NO silenciar** excepciones en los generadores

### ✅ SIEMPRE HACER:

1. Usar paths con `Path(__file__).parent` (no strings hardcodeados)
2. Retornar `{"success": True/False, "error": "..."}` desde todos los generadores
3. Validar con `BinaryFactoryInput` antes de procesar
4. Mantener puertos **8005** (backend) y **5173** (frontend) sin cambiarlos
5. Loggear con `logger.info/error()` (no `print()`)

---

## 🏗️ ARQUITECTURA RÁPIDA

```
studio_api.py (FastAPI 8005)
    └── index.py (BinaryFactory)
            ├── generators/cotizacion_simple_generator.py   → DOCX
            ├── generators/cotizacion_compleja_generator.py → DOCX
            ├── generators/proyecto_simple_generator.py     → DOCX
            ├── generators/proyecto_complejo_pmi_generator.py → DOCX
            ├── generators/informe_tecnico_generator.py     → DOCX
            ├── generators/informe_ejecutivo_apa_generator.py → DOCX
            ├── generators/excel_generator.py               → XLSX
            └── generators/html_to_pdf_generator.py         → PDF (Playwright)

studio/ (React/Vite 5173)
    └── src/App.tsx → PersonalizerPanel + Monaco Editor + Preview
```

---

## 🚀 ARRANQUE DEL MÓDULO

```powershell
# Windows (desde la raíz del módulo):
.\start.bat

# Manual:
# Terminal 1 - Backend:
cd <raiz_N04>
venv\Scripts\python -m uvicorn studio_api:app --port 8005 --reload

# Terminal 2 - Frontend:
cd studio
npm run dev  # → http://localhost:5173
```

---

## 📦 DESPLIEGUE EN SERVIDOR

```bash
# Con Docker Compose:
docker-compose up --build

# Backend solo:
docker build -t n04-factory .
docker run -p 8005:8005 n04-factory
```
