---
name: python-patterns
description: Python development principles and decision-making. Framework selection, async patterns, type hints, project structure. Teaches thinking, not copying.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Python Patterns

> Python development principles and decision-making para el módulo N04 Binary Factory.
> **Aprende a PENSAR, no a memorizar patrones.**

---

## Framework en uso: FastAPI

El N04 usa **FastAPI** porque:
- Es un microservicio API-first
- Necesita async para múltiples conexiones concurrentes
- Usa Pydantic para validación de contratos (BinaryFactoryInput)
- Se despliega con uvicorn en puerto 8005

---

## Principios Clave para N04

### async def vs def en FastAPI

```
Use async def cuando:
├── Operaciones de I/O (leer/escribir archivos de documentos)
├── Llamadas externas (Playwright para PDF)
└── Quieres manejar múltiples solicitudes de generación concurrentes

Use def cuando:
├── Operaciones CPU-bound (procesamiento Word/Excel con openpyxl/python-docx)
├── BinaryFactory.process_request() es síncrono por diseño
└── Los generadores binarios son síncronos (bloquean thread)
```

### Pydantic para el Contrato N04

```python
# El contrato es sagrado. Siempre validar con Pydantic:
from models import BinaryFactoryInput

validated = BinaryFactoryInput(**input_data)
# Si falla → Contract Violation (no silenciar errores)
```

### Manejo de Errores en Generadores

```
Estrategia N04:
├── Validar con Pydantic PRIMERO (fail fast)
├── Loggear con detalle: logger.error(f"...", exc_info=True)
├── NO silenciar excepciones con except Exception: pass
├── Retornar {"success": False, "error": str(e)} (nunca None)
└── NUNCA doble bloque except (bug existente a corregir)
```

### Paths con pathlib (obligatorio)

```python
# Siempre usar pathlib para paths (no os.path)
from pathlib import Path

BASE_DIR = Path(__file__).parent
template_path = BASE_DIR / "templates" / "html" / "PLANTILLA_HTML_COTIZACION_SIMPLE.html"
```

---

## Anti-Patrones a Evitar en N04

- ❌ Doble bloque `except` (bug existente en `_generate_excel()`)
- ❌ Retornar `None` en lugar de `{"success": False, "error": "..."}`
- ❌ Rutas hardcodeadas con strings (usar `Path(__file__).parent`)
- ❌ Generar lógica nueva de documentos — usar los generadores existentes
