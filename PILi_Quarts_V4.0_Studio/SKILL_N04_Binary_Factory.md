# SKILL: N04_Binary_Factory - Generador Soberano de Documentos

## 1. VISIÓN GENERAL

**N04_Binary_Factory** es el módulo **Soberano e Independiente** de generación de documentos del ecosistema PILi. Funciona como una "caja negra" autónoma que transforma datos técnicos en documentos profesionales de alta fidelidad en formatos **DOCX**, **XLSX** y **PDF**.

### Propósito Principal
- Generar documentos técnicos/comerciales sin dependencias externas del Core
- Proveer vista previa en tiempo real vía Studio web
- Permitir personalización visual (ADN Visual: colores, fuentes, logo)
- Exportar a tres formatos estándar de oficina

### Filosofía "Soberana"
- **Independencia Total**: No importa archivos fuera de su directorio
- **Motores Locales**: Todos los generadores están contenidos internamente
- **Zero External Dependencies**: Solo requiere librerías Python/Node estándar
- **Protocolo RALFTH**: Blindaje contra errores de índice y validación estricta

---

## 2. ARQUITECTURA ACTUAL

### 2.1 Estructura de Archivos

```
N04_Binary_Factory/
├── index.py                    # Orquestador principal (BinaryFactory class)
├── studio_api.py              # API FastAPI (Puerto 8005)
├── models.py                  # Contratos Pydantic
├── contract.json              # Esquema de entrada JSON
├── requirements_N04.txt     # Dependencias Python
│
├── generators/                # 12 Motores de generación
│   ├── base_generator.py     # Clase base con utilidades comunes
│   ├── excel_generator.py    # Generador profesional de Excel
│   ├── cotizacion_simple_generator.py
│   ├── cotizacion_compleja_generator.py
│   ├── proyecto_simple_generator.py
│   ├── proyecto_complejo_pmi_generator.py
│   ├── informe_tecnico_generator.py
│   ├── informe_ejecutivo_apa_generator.py
│   ├── html_to_word_generator.py
│   ├── html_to_pdf_generator.py
│   ├── html_parser.py
│   └── pdf_converter.py
│
├── templates/
│   ├── html/                  # 6 Plantillas HTML Jinja2
│   │   ├── PLANTILLA_HTML_COTIZACION_SIMPLE.html
│   │   ├── PLANTILLA_HTML_COTIZACION_COMPLEJA.html
│   │   ├── PLANTILLA_HTML_PROYECTO_SIMPLE.html
│   │   ├── PLANTILLA_HTML_PROYECTO_COMPLEJO_PMI.html
│   │   ├── PLANTILLA_HTML_INFORME_TECNICO.html
│   │   └── PLANTILLA_HTML_INFORME_EJECUTIVO_APA.html
│   └── word_masters/         # Plantillas maestras DOCX (opcional)
│
├── studio/                    # Frontend React + TypeScript
│   ├── src/
│   │   ├── App.tsx           # Componente principal
│   │   └── components/
│   │       ├── studio/
│   │       │   ├── Sidebar.tsx      # Lista de templates
│   │       │   ├── EditorPanel.tsx  # Editor HTML
│   │       │   ├── MirrorPanel.tsx  # Vista previa
│   │       │   └── PersonalizerPanel.tsx  # ADN Visual
│   │       └── ...
│   └── package.json
│
└── output_sandbox/           # Directorio de salida temporal
```

### 2.2 Flujo de Datos

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   FRONTEND      │     │   API BACKEND    │     │   GENERADORES │
│   (Studio)      │────▶│   (FastAPI)      │────▶│   (Nativos)     │
│   Puerto 3010   │     │   Puerto 8005    │     │                 │
└─────────────────┘     └──────────────────┘     └─────────────────┘
        │                       │                       │
        ▼                       ▼                       ▼
  - Selección de         - Validación          - DOCX/Excel
    Template               Pydantic              Nativos
  - Edición HTML          - Render Jinja2      - PDF vía Playwright
  - Personalización       - Dispatch Engine    - Base64 Output
    (ADN Visual)
```

---

## 3. FUNCIONALIDADES EXISTENTES (✅ LO QUE TIENE)

### 3.1 Generadores de Documentos (6 Tipos)

| Tipo | DOCX | XLSX | PDF | Descripción |
|------|------|------|-----|-------------|
| **Cotización Simple** | ✅ Native | ✅ Native | ✅ Playwright | Cotización básica con items |
| **Cotización Compleja** | ✅ Native | ✅ Native | ✅ Playwright | Con capítulos, cronograma, garantías |
| **Proyecto Simple** | ✅ Native | ✅ Native | ✅ Playwright | Gestión de proyectos básica |
| **Proyecto Complejo PMI** | ✅ Native | ✅ Native | ✅ Playwright | Con fases PMI, riesgos, KPIs |
| **Informe Técnico** | ✅ Native | ✅ Native | ✅ Playwright | Formato técnico estándar |
| **Informe Ejecutivo APA** | ✅ Native | ✅ Native | ✅ Playwright | Formato APA para ejecutivos |

### 3.2 API Endpoints (FastAPI)

```
GET  /api/studio/ping              → Health check
GET  /api/studio/templates         → Lista templates disponibles
GET  /api/studio/template/{name}   → Obtener template + mock data
POST /api/studio/render            → Renderizar HTML con Jinja2
POST /api/studio/generate          → Generar documento (word/excel/pdf)
```

### 3.3 Motor de Plantillas (Jinja2)

**Filtros disponibles:**
- `format_currency` → Formato de moneda (S/ 1,234.56)
- `format_number` → Formato numérico (1,234.56)

**Variables de contexto inyectadas:**
```python
{
  "TITULO_DOCUMENTO", "SUBTITULO_DOCUMENTO", "CODIGO_DOC", "FECHA_DOC",
  "NOMBRE_EMISOR", "RUC_EMISOR", "DIRECCION_EMISOR",
  "CLIENTE_NOMBRE", "CLIENTE_RUC", "CLIENTE_DIRECCION", "CLIENTE_EMAIL",
  "PROYECTO_NOMBRE", "PROYECTO_RESUMEN", "VIGENCIA",
  "MONEDA_SIMBOLO", "MONEDA_NOMBRE", "SUBTOTAL", "IGV", "TOTAL", "DURACION",
  "KPI_SPI", "KPI_CPI", "AVANCE_FISICO", "AVANCE_FINANCIERO",
  "suministros", "entregables", "fases_pmi", "fases", "riesgos",
  "RESUMEN_EJECUTIVO", "METRICA_ROI", "METRICA_PAYBACK", "METRICA_TIR",
  "conclusiones", "recomendaciones"
}
```

### 3.4 ADN Visual (Personalización)

**Parámetros soportados:**
- `primaryColor` → Color primario (#0052A3)
- `secondaryColor` → Color secundario (#1E40AF)
- `fontFamily` → Fuente (Calibri, Arial, etc.)
- `fontSize` → Tamaño base (11pt)
- `currency` → Moneda (PEN, USD, EUR)
- `logo` → Logo en Base64

**Inyección CSS en PDF:**
El sistema inyecta variables CSS personalizadas en el HTML antes de la conversión a PDF:
```css
:root {
  --pili-primary: #0052A3;
  --pili-secondary: #1E40AF;
  --pili-font: "Calibri";
  --pili-font-size: 11pt;
}
```

### 3.5 Sistema de Branding Dinámico

- Extracción de logo desde Base64 → archivo PNG temporal
- Aplicación de colores personalizados a:
  - Encabezados y títulos
  - Tablas y celdas
  - Totales y resaltados
  - Bordes y separadores

---

## 4. GAPS Y MEJORAS NECESARIAS (❌ LO QUE LE FALTA)

### 4.1 Frontend (Studio)

| # | Problema | Severidad | Solución |
|---|----------|-----------|----------|
| 1 | URLs hardcodeadas al puerto 8006 | 🔴 Alta | Configurar VITE_API_URL en .env |
| 2 | Editor HTML básico (textarea) | 🟡 Media | Integrar Monaco Editor o CodeMirror |
| 3 | Sin autocompletado de variables | 🟡 Media | Implementar intellisense Jinja2 |
| 4 | No hay undo/redo | 🟡 Media | Implementar historial de cambios |
| 5 | Preview solo muestra resultado, no diff | 🟢 Baja | Agregar modo split-view |
| 6 | Sin validación de sintaxis Jinja2 | 🟡 Media | Validar templates antes de enviar |
| 7 | No persiste cambios entre sesiones | 🟡 Media | LocalStorage o backend storage |

### 4.2 Backend (API)

| # | Problema | Severidad | Solución |
|---|----------|-----------|----------|
| 1 | Sin sistema de caché | 🟡 Media | Redis/caché en memoria para templates |
| 2 | No hay rate limiting | 🟡 Media | Implementar throttling |
| 3 | Sin autenticación | 🔴 Alta | JWT o API Keys |
| 4 | Logs básicos (solo consola) | 🟡 Media | Sistema de logging estructurado |
| 5 | Sin métricas/observabilidad | 🟢 Baja | Prometheus/OpenTelemetry |
| 6 | Playwright puede bloquearse | 🔴 Alta | Timeout agresivo + watchdog |
| 7 | Sin cola de generación | 🟡 Media | Implementar async jobs (Celery/RQ) |

### 4.3 Generadores

| # | Problema | Severidad | Solución |
|---|----------|-----------|----------|
| 1 | Excel usa fórmulas hardcodeadas | 🟡 Media | Sistema de fórmulas dinámicas en mapping.json |
| 2 | PDF depende de Playwright externo | 🔴 Alta | Fallback a fpdf si Playwright falla |
| 3 | Sin soporte para imágenes en celdas Excel | 🟡 Media | Implementar insert_image en openpyxl |
| 4 | No hay sistema de "campos calculados" | 🟡 Media | Motor de expresiones (subtotal*cantidad) |
| 5 | Sin paginación automática en Word | 🟢 Baja | Control de saltos de página |
| 6 | No hay headers/footers dinámicos | 🟡 Media | Implementar en base_generator |
| 7 | Sin soporte para múltiples hojas Excel | 🟢 Baja | Extender excel_generator |

### 4.4 Templates

| # | Problema | Severidad | Solución |
|---|----------|-----------|----------|
| 1 | No hay sistema de versionado | 🟡 Media | Git-based o versioning interno |
| 2 | Sin validación de contrato | 🔴 Alta | Validar que todas las variables existan |
| 3 | No hay templates condicionales | 🟡 Media | Soporte para if/else basado en datos |
| 4 | Sin componentes reutilizables | 🟡 Media | Sistema de includes/macros Jinja2 |
| 5 | No hay preview de datos reales | 🟡 Media | Conectar a BD para datos de ejemplo |
| 6 | Sin sistema de themes | 🟢 Baja | Múltiples esquemas visuales predefinidos |

### 4.5 Arquitectura

| # | Problema | Severidad | Solución |
|---|----------|-----------|----------|
| 1 | Puerto del backend hardcodeado (8006) | 🔴 Alta | Usar variable de entorno PORT |
| 2 | Sin Docker/containerización | 🟡 Media | Dockerfile + docker-compose |
| 3 | No hay tests automatizados | 🔴 Alta | Pytest + Jest para cobertura |
| 4 | Sin CI/CD pipeline | 🟡 Media | GitHub Actions para testing/deploy |
| 5 | CORS muy permisivo (allow_origins=["*"]) | 🔴 Alta | Configurar orígenes específicos |
| 6 | Sin manejo de errores granular | 🟡 Media | Códigos de error específicos |
| 7 | No hay sistema de plugins/extensions | 🟢 Baja | Arquitectura de plugins |

---

## 5. ESPECIFICACIONES TÉCNICAS DETALLADAS

### 5.1 Contrato de Entrada (JSON)

```json
{
  "header": {
    "user_id": "UUID_STRING",
    "service_id": 1,
    "document_type": "COTIZACION_SIMPLE"
  },
  "branding": {
    "logo_b64": "data:image/png;base64,...",
    "color_hex": "#0052A3",
    "secondary_color": "#1E40AF",
    "font_family": "Calibri"
  },
  "payload": {
    "items": [
      {
        "descripcion": "Item 1",
        "cantidad": 2,
        "unidad": "und",
        "precio_unitario": 100.00,
        "total": 200.00
      }
    ],
    "totals": {
      "subtotal": 200.00,
      "igv": 36.00,
      "total": 236.00
    },
    "client_info": {
      "nombre": "Cliente S.A.",
      "ruc": "20123456789",
      "direccion": "Av. Principal 123",
      "fecha": "25/02/2026"
    },
    "technical_notes": "Notas técnicas adicionales",
    "settings": {
      "capitulos": [],
      "cronograma": {},
      "garantias": []
    }
  },
  "output_format": "DOCX|XLSX|PDF"
}
```

### 5.2 Respuesta de Éxito

```json
{
  "success": true,
  "filename": "COTIZACION_SIMPLE_0001_TESLA.docx",
  "file_b64": "UEsDBBQABgAIAAAAIQDfpNJs...",
  "engine": "Native Word Generator (Alta Fidelidad - V10)"
}
```

### 5.3 Respuesta de Error

```json
{
  "success": false,
  "error": "Template COTIZACION_INVALIDA not found",
  "detail": "Error en Factoría SOBERANA al generar docx",
  "code": "TEMPLATE_NOT_FOUND"
}
```

---

## 6. RECOMENDACIONES PARA SKILL

### 6.1 Arquitectura Recomendada

```
┌─────────────────────────────────────────────────────────────────┐
│                         SKILL N04                                │
│                   (Arquitectura Objetivo)                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐       │
│  │   NGINX      │    │   Redis      │    │  PostgreSQL  │       │
│  │   (Proxy)    │    │   (Cache)    │    │  (Metadata)  │       │
│  └──────┬───────┘    └──────────────┘    └──────────────┘       │
│         │                                                        │
│         ▼                                                        │
│  ┌──────────────────────────────────────────────────────┐      │
│  │              N04 Binary Factory Cluster                │      │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐       │      │
│  │  │  API #1    │  │  API #2    │  │  API #3    │       │      │
│  │  │  (FastAPI) │  │  (FastAPI) │  │  (FastAPI) │       │      │
│  │  └─────┬──────┘  └─────┬──────┘  └─────┬──────┘       │      │
│  │        └─────────────────┼─────────────────┘            │      │
│  │                          ▼                             │      │
│  │              ┌─────────────────────────┐                │      │
│  │              │    Celery Workers       │                │      │
│  │              │  (Generación Async)     │                │      │
│  │              └─────────────────────────┘                │      │
│  └──────────────────────────────────────────────────────┘      │
│                          │                                      │
│                          ▼                                      │
│  ┌──────────────────────────────────────────────────────┐      │
│  │                   Storage Layer                      │      │
│  │    (Templates, Output Files, Assets)               │      │
│  └──────────────────────────────────────────────────────┘      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 6.2 Stack Tecnológico Recomendado

| Capa | Tecnología Actual | Recomendación SKILL |
|------|-------------------|---------------------|
| Frontend | React + Vite | Next.js 14 + Tailwind |
| Backend | FastAPI + Uvicorn | FastAPI + Gunicorn + Nginx |
| Cola de Tareas | None (sync) | Celery + Redis |
| Caché | None | Redis |
| Base de Datos | None (JSON) | PostgreSQL (metadata) |
| PDF | Playwright | Playwright + WeasyPrint (fallback) |
| Testing | None | Pytest + Playwright |
| CI/CD | None | GitHub Actions |
| Container | None | Docker + Docker Compose |
| Observabilidad | None | Prometheus + Grafana |

### 6.3 Funcionalidades Críticas a Implementar

**Fase 1 - Estabilización (URGENTE):**
1. Corregir puertos hardcodeados (8005/8006)
2. Implementar manejo de errores robusto
3. Agregar tests básicos
4. Sistema de logging estructurado

**Fase 2 - Mejoras (MEDIA PRIORIDAD):**
1. Editor HTML mejorado (Monaco/CodeMirror)
2. Sistema de caché con Redis
3. Autenticación JWT
4. Cola de generación async

**Fase 3 - Escalabilidad (BAJA PRIORIDAD):**
1. Containerización Docker
2. Clustering de workers
3. Sistema de plugins
4. Analytics y métricas

---

## 7. CONCLUSIONES

**Fortalezas del Módulo:**
- ✅ Arquitectura soberana bien diseñada
- ✅ Separación clara de responsabilidades
- ✅ Múltiples generadores especializados
- ✅ Sistema de ADN Visual funcional
- ✅ Templates HTML con Jinja2

**Debilidades Críticas:**
- ❌ Hardcoded ports y URLs
- ❌ Sin sistema de autenticación
- ❌ Dependencia crítica de Playwright
- ❌ Sin tests ni CI/CD
- ❌ Sin persistencia de datos

**Riesgos Técnicos:**
1. **Playwright bloqueado** → Generación PDF falla silenciosamente
2. **Puerto 8005 ocupado** → Backend no inicia
3. **Template malformado** → Error 500 sin contexto
4. **Logo muy grande** → Base64 excede memoria

**Estado General:** **7/10** - Funcional pero necesita estabilización antes de producción.

---

## 8. CORRECCIONES APLICADAS (Post-Análisis)

### ✅ Sincronización ADN Visual Implementada

**Problema Identificado:** La personalización visual (colores, fuentes, logo) no se reflejaba en los documentos generados.

**Soluciones Implementadas:**

| Componente | Cambio | Archivo |
|------------|--------|---------|
| **Vista Previa HTML** | Inyección CSS dinámica con ADN Visual en endpoint `/api/studio/render` | `studio_api.py` |
| **Backend Bridge** | Propagación completa de primaryColor, secondaryColor, fontFamily, fontSize | `index.py` |
| **Base Generator** | Captura y aplicación de fuentes personalizadas | `base_generator.py` |

**Flujo Actual de ADN Visual:**
```
Usuario cambia color → Frontend envía settings → 
Backend inyecta CSS en preview → Backend propaga a generadores → 
PDF/Word/Excel reciben branding completo
```

**Estado Post-Corrección:**
- ✅ Vista previa HTML = Refleja ADN Visual correctamente
- ✅ PDF = Ya funcionaba (Playwright + CSS injection)
- ✅ Word = Recibe colores y fuentes personalizadas
- ⚠️ Excel = Pendiente verificación de aplicación de fuentes

---

**Documento generado:** SKILL_N04_Binary_Factory.md  
**Versión:** 1.1 (Con correcciones aplicadas)  
**Fecha:** 2026-02-25  
**Autor:** Cascade AI Analysis
