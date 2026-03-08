---
name: binary-factory
description: Motor de generación de documentos de alta fidelidad (Caja Negra de PILi). Gestiona Word (DOCX), Excel (XLSX) y PDF.
---

# SKILL: Binary Factory (La Caja Negra)

Este Skill encapsula la tecnología pilar de PILi para la generación de documentos profesionales. Opera como un sistema de **micro-agentes** donde los datos se inyectan en modelos HTML editables y se procesan mediante generadores nativos de alta fidelidad.

## 🛡️ Principios del Skill

1. **Conservación de la Tecnología**: Este Skill utiliza los generadores operacionales ubicados en `generators/`. No se debe generar código nuevo de generación; se debe usar y mantener el existente que ya ha sido probado.
2. **Fidelidad Total**: El motor garantiza que lo que se ve en el HTML (Mirror) sea lo que se obtiene en el binario (DOCX/XLSX/PDF).
3. **Contrato Estricto**: Toda comunicación con este motor debe seguir el contrato definido en `models.py`.

## 🏗️ Los 6 Pilares (Modelos HTML)

El Skill gobierna los siguientes modelos editables ubicados en `templates/html/`:

| Modelo | Archivo HTML | Formato Destino |
| :--- | :--- | :--- |
| **Cotización Simple** | `PLANTILLA_HTML_COTIZACION_SIMPLE.html` | DOCX / XLSX / PDF |
| **Cotización Compleja** | `PLANTILLA_HTML_COTIZACION_COMPLEJA.html` | DOCX / XLSX / PDF |
| **Proyecto Simple** | `PLANTILLA_HTML_PROYECTO_SIMPLE.html` | DOCX / XLSX / PDF |
| **Proyecto Complejo** | `PLANTILLA_HTML_PROYECTO_COMPLEJO_PMI.html` | DOCX / XLSX / PDF (PMI) |
| **Informe Técnico** | `PLANTILLA_HTML_INFORME_TECNICO.html` | DOCX / XLSX / PDF |
| **Informe Ejecutivo** | `PLANTILLA_HTML_INFORME_EJECUTIVO_APA.html` | DOCX / XLSX / PDF (APA) |

## 🤖 Protocolo del Micro-agente

Cuando un agente necesite generar un documento, debe:

1. **Validar Datos**: Asegurar que el payload contenga `items`, `totals` y `client_info`.
2. **Invocar Motor**: Usar `binary_factory.process_request(payload)` de `index.py`.
3. **Manejar Branding**: El logo se inserta automáticamente desde `branding.logo_b64` a menos que se especifique `mostrar_logo: false`.

## 🔌 API del Studio (Puerto 8005)

| Endpoint | Método | Función |
|---|---|---|
| `/api/studio/ping` | GET | Health check |
| `/api/studio/templates` | GET | Lista plantillas disponibles |
| `/api/studio/template/{name}` | GET | HTML renderizado con datos mock |
| `/api/studio/render` | POST | Renderiza HTML + inyecta ADN Visual |
| `/api/studio/generate` | POST | Genera DOCX/XLSX/PDF y descarga |

## 📂 Estructura Interna

```
N04_Binary_Factory/
├── index.py          ← BinaryFactory: Motor principal (Factory Pattern)
├── studio_api.py     ← API FastAPI (Puerto 8005)
├── models.py         ← BinaryFactoryInput (Contrato Pydantic)
├── generators/       ← 6 motores especializados + ExcelGenerator
├── templates/        ← 15 tipos de plantilla + 6 HTML + 6 Word Masters
└── studio/           ← Frontend React/Vite (Puerto 5173)
```

> [!IMPORTANT]
> **NO MODIFICAR LA LÓGICA DE LOS GENERADORES BINARIOS** sin una auditoría completa. Los cambios se realizan preferentemente en el **HTML** para mantener la flexibilidad.

> [!WARNING]
> Bug conocido en `index.py`: doble bloque `except` en `_generate_excel()` (líneas ~504-510). El segundo bloque es código muerto y nunca se ejecuta.
