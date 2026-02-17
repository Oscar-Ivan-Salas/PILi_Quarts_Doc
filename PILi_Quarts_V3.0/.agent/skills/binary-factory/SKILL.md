---
name: binary-factory
description: Motor de generación de documentos de alta fidelidad (Caja Negra de PILi). Gestiona Word (DOCX), Excel (XLSX) y PDF.
---

# SKILL: Binary Factory (La Caja Negra)

Este Skill encapsula la tecnología pilar de PILi para la generación de documentos profesionales. Opera como un sistema de **micro-agentes** donde los datos se inyectan en modelos HTML editables y se procesan mediante generadores nativos de alta fidelidad.

## 🛡️ Principios del Skill

1. **Conservación de la Tecnología**: Este Skill utiliza los generadores operacionales ubicados en `backend/modules/N04_Binary_Factory`. No se debe generar código nuevo de generación; se debe usar y mantener el existente que ya ha sido probado.
2. **Fidelidad Total**: El motor garantiza que lo que se ve en el HTML (Mirror) sea lo que se obtiene en el binario (DOCX/XLSX/PDF).
3. **Contrato Estricto**: Toda comunicación con este motor debe seguir el contrato definido en `backend/modules/N04_Binary_Factory/models.py`.

## 🏗️ Los 6 Pilares (Modelos HTML)

El Skill gobierna los siguientes modelos editables ubicados en `resources/templates/`:

| Modelo | Archivo HTML | Formato Destino |
| :--- | :--- | :--- |
| **Cotización Simple** | `PLANTILLA_HTML_COTIZACION_SIMPLE.html` | DOCX / PDF |
| **Cotización Compleja** | `PLANTILLA_HTML_COTIZACION_COMPLEJA.html` | DOCX / PDF |
| **Proyecto Simple** | `PLANTILLA_HTML_PROYECTO_SIMPLE.html` | DOCX / PDF |
| **Proyecto Complejo** | `PLANTILLA_HTML_PROYECTO_COMPLEJO_PMI.html` | DOCX / PDF (PMI) |
| **Informe Técnico** | `PLANTILLA_HTML_INFORME_TECNICO.html` | DOCX / PDF |
| **Informe Ejecutivo** | `PLANTILLA_HTML_INFORME_EJECUTIVO_APA.html` | DOCX / PDF (APA) |

## 🤖 Protocolo del Micro-agente

Cuando un agente necesite generar un documento, debe:

1. **Validar Datos**: Asegurar que el payload contenga `items`, `totals` y `client_info`.
2. **Invocar Motor**: Usar `binary_factory.process_request(payload)` de `index.py`.
3. **Manejar Branding**: El logo de Tesla se inserta automáticamente desde el Header nativo del Skill a menos que se especifique `mostrar_logo: false`.

## 📂 Estructura de Recursos
- `resources/templates/`: Copias maestras de los HTML para referencia y edición.
- `index.py`: El cerebro que coordina los micro-agentes de generación.
- `generators/`: Los motores binarios (Word, Excel, PDF).

> [!IMPORTANT]
> **NO MODIFICAR LA LÓGICA DE LOS GENERADORES BINARIOS** sin una auditoría completa. Los cambios se realizan preferentemente en el **HTML** para mantener la flexibilidad.
