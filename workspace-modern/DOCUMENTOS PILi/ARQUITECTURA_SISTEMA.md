# 🏛️ ARQUITECTURA DEL SISTEMA PILi_Quarts (v3.0)

Este documento detalla la estructura, tecnologías y diseño del sistema **PILi_Quarts** (Tesla Cotizador Inteligente), diseñado para ser la referencia técnica para arquitectos de software y desarrolladores.

---

## 1. 🏗️ ESTRUTURA DEL PROYECTO

El sistema sigue una arquitectura **Monorepo** con separación clara entre Backend (API) y Frontend (Cliente SPA).

### 📂 ESTRUCTURA DE DIRECTORIOS

```
PILi_Quarts/
│
├── 📂 backend/                  # Servidor API y Lógica de Negocio (Python/FastAPI)
│   ├── 📂 app/
│   │   ├── 📂 core/             # Configuraciones globales (DB, Security, Config)
│   │   ├── 📂 documents/        # [NUEVO] Módulos de generación de documentos (HTML/PDF) 
│   │   ├── 📂 integrations/     # Integraciones externas (WhatsApp, Email, etc.)
│   │   ├── 📂 main.py           # Punto de entrada de la aplicación (FastAPI app)
│   │   ├── 📂 models/           # Modelos ORM (SQLAlchemy) - Base de datos
│   │   ├── 📂 routers/          # Endpoints de la API (Controllers)
│   │   ├── 📂 schemas/          # Esquemas Pydantic (Validación de datos)
│   │   └── 📂 services/         # Lógica de negocio compleja (AI, Cálculos, Procesamiento)
│   └── 📄 requirements.txt      # Dependencias de Python
│
├── 📂 frontend/                 # Interfaz de Usuario (React + Vite/CRA)
│   ├── 📂 public/               # Assets estáticos públicos
│   ├── 📂 src/
│   │   ├── 📂 components/       # Componentes React reutilizables y específicos
│   │   │   ├── 📄 Pili*.jsx     # Componentes de Chatbots especializados (Electricidad, ITSE, etc.)
│   │   │   └── 📄 EDITABLE_*.jsx # Vistas previas editables de documentos
│   │   ├── 📂 services/         # Servicios de consumo de API (Axios/Fetch)
│   │   ├── 📂 utils/            # Utilidades y helpers frontend
│   │   ├── 📄 App.jsx           # Componente raíz y Rutas
│   │   └── 📄 main.jsx/index.js # Punto de entrada React
│   └── 📄 package.json          # Dependencias de Node.js
│
└── 📂 DOCUMENTOS PILi/          # Documentación técnica y arquitectónica
```

---

## 2. 🛠️ STACK TECNOLÓGICO

### 🔙 BACKEND (Python) - 50% del Código
El núcleo lógico del sistema.

*   **Lenguaje:** Python 3.12+
*   **Framework Web:** **FastAPI** (Alto rendimiento, asíncrono, validación automática).
*   **Servidor:** Uvicorn (ASGI).
*   **Base de Datos (ORM):** **SQLAlchemy 2.0+** con **Alembic** para migraciones (SQLite/PostgreSQL).
*   **Validación:** Pydantic 2.x.
*   **Inteligencia Artificial:**
    *   **Google Gemini Pro (google-generativeai):** Cerebro principal de PILI.
    *   **ChromaDB:** Base de datos vectorial para RAG (Retrieval Augmented Generation).
    *   **PyPDF2 / Tesseract / Python-docx:** Procesamiento OCR y lectura de documentos.
*   **Generación de Documentos:**
    *   **ReportLab / WeasyPrint:** Generación de PDFs profesionales.
    *   **Python-docx:** Manipulación de archivos Word.

### 🖥️ FRONTEND (JavaScript/React) - 40% del Código
La interfaz interactiva.

*   **Lenguaje:** JavaScript (ES6+) / React 18.
*   **Framework CSS:** **Tailwind CSS** (Estilizado utilitario rápido y moderno).
*   **Iconos:** Lucide React.
*   **Gestión de Estado:** React Hooks (useState, useEffect, useContext).
*   **Componentes Clave:**
    *   `Pili*Chat.jsx`: Interfaces de chat específicas por dominio.
    *   `EDITABLE_*.jsx`: Editores WYSIWYG para cotizaciones e informes en tiempo real.

### ⚙️ INFRAESTRUCTURA Y DEVOPS - 10%
*   **Control de Versiones:** Git.
*   **Entorno:** Virtualenv (Python), NPM (Node).

---

## 3. 🧩 COMPONENTES PRINCIPALES Y SU FUNCIÓN

### 🧠 PILIBrain (Backend Service)
El "cerebro" central que orquesta la IA. Decide qué agente activar, gestiona el contexto de la conversación y procesa la intención del usuario.

### 💬 Módulos de Chat (Frontend)
Interfaces especializadas (`PiliElectricidadChat`, `PiliITSEChat`, etc.) que adaptan la UX al tipo de servicio solicitado (ej. solicitando área en m² para planos, o potencia para cargas).

### 📄 Generadores de Documentos (`app/documents`)
Módulos refactorizados que contienen la lógica pura para generar HTMLs editables y documentos finales.
*   `cotizacion_simple.py`: Para servicios rápidos.
*   `cotizacion_compleja.py`: Incluye cronogramas y términos comerciales.
*   `proyecto_complejo.py`: Gestión PMI (RACI, Gantt, Riesgos).
*   `informe_*.py`: Generadores de informes técnicos y ejecutivos (APA).

### 🔌 API Routers (`app/routers`)
*   `chat.py`: Maneja la interacción con la IA y el flujo de mensajes.
*   `templates.py`: Sirve las vistas previas HTML dinámicas.
*   `calculos.py`: Realiza cálculos matemáticos complejos (cargas eléctricas, presupuestos) fuera de la IA para garantizar precisión.

---

## 4. 💎 PROPUESTA DE VALOR (Value Proposition)

**Para el Usuario (Ingenieros/Ventas Tesla):**
> "PILI no es solo un chatbot, es una **Ingeniera Junior IA** que automatiza el 80% del trabajo operativo de preventa."

1.  **Velocidad Extrema:** Reduce el tiempo de cotización de 4 horas a 5 minutos.
2.  **Precisión Técnica:** Combina la creatividad de la IA con la precisión de cálculos programados (Python), evitando "alucinaciones" matemáticas.
3.  **Flexibilidad Total:** Permite editar cada detalle del documento generado antes de exportarlo a PDF/Word, dando control final al experto humano.
4.  **Estandarización:** Asegura que todas las cotizaciones salgan con el formato, branding y calidad profesional de Tesla, independientemente de quién las genere.
5.  **Multi-Modalidad:** Capaz de "leer" planos y fotos para entender el contexto sin que el usuario tenga que escribir todo.

---

## 5. 🚀 PRÓXIMOS PASOS (Roadmap Técnico)

1.  **Refactorización Frontend:**
    *   Modularizar `App.jsx` (actualmente monolítico) en rutas dedicadas.
    *   Crear un contexto global (`PiliContext`) para manejar el estado de la sesión entre componentes.

2.  **Optimización de IA (RAG):**
    *   Alimentar ChromaDB con históricos de cotizaciones reales de Tesla para mejorar la precisión de precios y tiempos.

3.  **Seguridad y Autenticación:**
    *   Implementar Login real (JWT) para proteger el acceso (actualmente simulado o básico).
    *   Roles de usuario (Vendedor vs. Ingeniero Senior).

4.  **Despliegue (Deploy):**
    *   Dockerizar la aplicación (Frontend + Backend).
    *   Configurar pipeline CI/CD.

5.  **Testing:**
    *   Añadir tests unitarios para los nuevos módulos de documentos en `backend/tests`.
    *   Tests E2E para el flujo crítico de "Chat -> Cotización -> PDF".

---
*Documento generado por Arquitecto de Software AI - Proyecto PILi_Quarts*
