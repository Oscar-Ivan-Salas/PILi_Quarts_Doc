---
name: n04-binary-factory
description: Reglas operativas, estructura interna y contratos de API del nodo N04-Studio — generador independiente de documentos técnicos profesionales (Word, PDF, Excel) desde HTML. No usa IA. Es un nodo autónomo.
---

# N04-Studio — Nodo Independiente de Generación de Documentos

> **MANDATORY:** Todo agente que modifique, repare o extienda este nodo debe leer ESTE archivo completo antes de tocar una sola línea de código.

---

## 1. Identidad del Nodo
| Campo | Valor |
|---|---|
| **Nombre Canónico** | N04-Studio |
| **Alias** | La Caja Negra |
| **Puerto frontend** | 3012 |
| **Puerto backend** | 8005 (o autónomo vía `run_backend.py`) |
| **Carpeta raíz** | `PILi_Quarts_V4.0_Studio/backend/modules/N04_Binary_Factory/` |
| **Estado** | Nodo independiente — NO depende de PILi-App ni de PILi-Agent |

---

## 2. Principio de la Caja Negra (Regla de Hierro)

✅ **PRINCIPIO DEL DOCUMENTO ESPEJO**
Este nodo recibe HTML editado (la Vista Previa que el usuario ve en pantalla) y lo devuelve como binario físico exacto. Los documentos generados deben ser **espejos precisos** del HTML enviado.

✅ **CEGUERA TOTAL A LA IA**
N04-Studio NO importa, NO llama y NO depende de ningún LLM (Gemini, OpenAI, etc.). Es un obrero de fuerza bruta pura. Si se intenta inyectar lógica de IA en este nodo → **VIOLACIÓN CRÍTICA**.

---

## 3. Estructura Interna del Nodo (Mapa Completo)

```text
N04_Binary_Factory/
│
├── studio/                        ← 🖥️  FRONTEND (React TSX, Vite, Puerto 3012)
│   └── src/
│       ├── App.tsx                # Controlador principal (23 KB) — estado, tabs, descarga
│       └── components/studio/
│           ├── Sidebar.tsx        # Selector de plantillas (11 KB)
│           ├── MirrorPanel.tsx    # Vista previa HTML en vivo + scanline animado (14 KB)
│           ├── EditorPanel.tsx    # Editor Monaco de código HTML (2.6 KB)
│           ├── PersonalizerPanel.tsx  # Configuración: logo, color, moneda (21 KB ⭐)
│           └── UIActionCard.tsx   # Botones Word/PDF/Excel con estado (3 KB)
│
├── studio_api.py                  ← 🐍 API FastAPI del nodo (22 KB)  
│   # Expone: GET /template/{name}, POST /generate
│
├── generators/                    ← ⚙️  MOTORES DE CONVERSIÓN (núcleo de la Caja Negra)
│   ├── base_generator.py          # Clase base para todos los generadores (13 KB)
│   ├── cotizacion_simple_generator.py   (11 KB)
│   ├── cotizacion_compleja_generator.py (21 KB)
│   ├── informe_tecnico_generator.py     (8.5 KB)
│   ├── informe_ejecutivo_apa_generator.py (11 KB)
│   ├── proyecto_simple_generator.py     (18 KB)
│   ├── proyecto_complejo_pmi_generator.py (32 KB ⭐ más complejo)
│   ├── excel_generator.py               (45 KB ⭐ más pesado)
│   ├── html_to_pdf_generator.py         (6.7 KB)
│   └── pdf_converter.py                 (3.7 KB)
│
├── templates/                     ← 📄 PLANTILLAS DORADAS HTML (Jinja2)
│   ├── ELECTRICIDAD_COTIZACION_SIMPLE/
│   ├── ELECTRICIDAD_COTIZACION_COMPLEJA/
│   ├── ELECTRICIDAD_INFORME_TECNICO/
│   ├── ELECTRICIDAD_INFORME_EJECUTIVO/
│   ├── ELECTRICIDAD_PROYECTO_SIMPLE/
│   ├── ELECTRICIDAD_PROYECTO_COMPLEJO/
│   ├── ELECTRICIDAD_MEMORIA_DESCRIPTIVA/
│   ├── ELECTRICIDAD_ESPECIFICACIONES_TECNICAS/
│   ├── ELECTRICIDAD_PRESUPUESTO_BASE/
│   ├── ELECTRICIDAD_CRONOGRAMA_EJECUCION/
│   ├── ELECTRICIDAD_PROTOCOLO_PRUEBAS/
│   ├── ELECTRICIDAD_PLAN_SEGURIDAD/
│   ├── ELECTRICIDAD_INFORME_LEVANTAMIENTO/
│   ├── ELECTRICIDAD_CUADRO_CARGAS/
│   └── MODELO_USUARIO_TEST/
│
├── excel_converter.py             # Conversor Excel independiente (30 KB)
├── html_to_word_generator.py      # Conversor Word independiente (20 KB)
├── html_parser.py                 # Parser HTML/CSS -> estructura de datos (9 KB)
├── index.py                       # Orquestador principal FastAPI (49 KB ⭐ más grande)
├── models.py                      # Modelos Pydantic de la API
├── requirements_N04.txt           # Dependencias exclusivas del nodo
├── run_backend.py                 # Script para levantar el backend de forma autónoma
├── docker-compose.yml             # Docker independiente del nodo
└── supabase_setup.sql             # Setup de BD Supabase (opcional)
```

---

## 4. Stack Tecnológico del Nodo

### Frontend (N04-Studio UI)
- **React 19 + TypeScript + Vite 7**
- **Monaco Editor** → Editor de código HTML en vivo
- **Framer Motion** → Animaciones premium (scanline cinemático en MirrorPanel)
- **Tailwind CSS v4** → Estilos

### Backend (Motor de Conversión)
- **FastAPI** → API REST
- **python-docx + htmldocx** → Conversión a Word
- **openpyxl** → Conversión a Excel
- **pdfkit / Playwright PDF** → Conversión a PDF
- **BeautifulSoup4** → Parseo de HTML
- **Jinja2** → Inyección de variables en plantillas (`{{MONEDA_SIMBOLO}}`, `{{CLIENTE_NOMBRE}}`)

---

## 5. REGLA INMUTABLE DE GENERACIÓN (GRABADO EN PIEDRA)

> 🔴 **PROHIBICIÓN ESTRICTA:** Queda TERMINANTEMENTE PROHIBIDO crear nuevos generadores paralelos, usar librerías externas o invocar archivos fuera del módulo `N04_Binary_Factory`. TODO el flujo debe usar **única y exclusivamente** los scripts existentes en esta carpeta. No asumas soluciones; respeta el prototipo creado minuciosamente en años de trabajo.

El sistema se basa en **6 modelos de documentos alojados en `templates/html/`** que sirven tanto para la visualización en tiempo real en la interfaz (espejo) como moldes inalterables de la generación final.

### Flujo Exacto Exigido (El Principio del Espejo)

1. **WORD (`html_to_word_generator.py`)**
   - **Mecanismo:** El Frontend hace POST a `index.py`. Éste debe enrutar *EXCLUSIVAMENTE* hacia `html_to_word_generator.py`.
   - **Flujo Interno:** El generador extrae los datos del Frontend, carga su plantilla HTML respectiva (`templates/html/*.html`), inyecta la información estructurada con `Jinja2` y `BeautifulSoup4`, y finalmente incrusta este contenido procesado dentro del contenedor corporativo (`templates/master_tesla.docx`) usando el empaquetador de la librería.
   - **Regla:** **Jamás** invocar los generadores locales legados de `python-docx` puro (ej. `cotizacion_simple_generator.py` ubicado en `generators/`). Ese código obsoleto rompe el espejo. El Word debe nacer invariablemente del HTML.

2. **PDF (`html_to_pdf_generator.py` con Motor Playwright)**
   - **Mecanismo:** El Frontend hace POST a `index.py`. Éste intercepta y llama a `_generate_mirror_pdf()`.
   - **Flujo Interno:** Se inyecta el ADN visual dinámico (estilos) directamente en el cuerpo del HTML frontend y se instancia `playwright_pdf_cli.py` en un subproceso para renderizar (fotografiar) e imprimir la vista virtual idéntica como PDF físico inalterable.

3. **EXCEL (`excel_generator.py` / `excel_converter.py`)**
   - **Mecanismo:** Se emplea estrictamente el script interno, respetando cálculos precisos, herencia de colores corporativos del ADN visual del estudio y arquitectura de celdas nativas en cuadros de cargas y metrados. 

✅ **LEY ABSOLUTA:** Si a futuro hay un reporte sobre que "El Word/PDF no sale idéntico a la vista previa", el error **NUNCA** se repara re-escribiendo los generadores o asumiendo soluciones mágicas. Se diagnostica verificando el conducto en `index.py` y asegurando que consuma los scripts principales obligatorios (`html_to_word_generator.py`, Playwright, etc.) que consumen los 6 modelos HTML existentes en `templates/html/`.

---

## 6. Protocolo de Vibe Coding (Reparación Quirúrgica)

| Fallo | Archivo a Revisar | NO tocar |
|---|---|---|
| PDF visualmente roto | `html_to_pdf_generator.py` + template HTML | Excel, Word |
| Excel no abre / celdas mal | `excel_generator.py` | PDF, Word |
| Word sin estilos | `html_to_word_generator.py` | Resto |
| Botón no activa sin plantilla | `App.tsx` línea `disabled={!selectedTemplate}` | Backend |
| Scanline no aparece | `MirrorPanel.tsx` + `index.css @keyframes scan` | Backend |
| Variable `{{MONEDA}}` no reemplaza | `studio_api.py` → lógica de Jinja2 render | Frontend |

---

## 7. Cómo Levantar el Nodo de Forma Autónoma

```powershell
# Backend (desde la carpeta del nodo)
python run_backend.py
# o: uvicorn studio_api:app --port 8005

# Frontend (desde /studio)
npm run dev -- --port 3012
```

El nodo funciona 100% solo sin necesitar PILi-App ni PILi-Agent activos.
