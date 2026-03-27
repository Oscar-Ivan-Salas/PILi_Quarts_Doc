---
name: pili-architecture
description: Arquitectura oficial, filosofía de "Vibe Coding" y reglas de desarrollo del sistema PILi_Quarts (Procesadora Inteligente de Licitaciones Industriales). Contiene el motor N04 (Caja Negra) y el agente PILI.
---

# PILi_Quarts - Core Architecture & Master Guide

## 0. Registro de Módulos (Nombres Canónicos)
> **OBLIGATORIO:** Siempre usar estos nombres en lugar de números de puerto, que cambian.

| Nombre Oficial | Puerto Ref. | Carpeta Raíz | Rol |
|---|---|---|---|
| **PILi-App** | 3011 | `PILi_Quarts_V3.0/frontend` | 🏠 Nido final — integra TODOS los módulos maduros |
| **N04-Studio** | 3012 | `V4.0_Studio/backend/modules/N04_Binary_Factory/studio` | ⚙️ Módulo generador de documentos (desarrollo activo) |
| **PILi-Agent** | TBD | Pendiente | 🤖 Módulo agente IA (desarrollo futuro) |
| **N04-Backend** | 8005 | `PILi_Quarts_V3.0/backend` | 🐍 Motor Python FastAPI que sirve la generación binaria |

**Regla:** Solo cuando un módulo esté al 100% funcional e independiente, se nida dentro de **PILi-App**.

> **MANDATORY:** Todo agente que edite, repare o expanda PILi_Quarts DEBE leer y seguir esta arquitectura detalladamente para no romper la modularidad ni la separación de responsabilidades que costó meses perfeccionar.

## 1. Identidad del Sistema
**Nombre:** PILi_Quarts
**Propósito:** Generador de documentos técnicos profesionales (Cotizaciones, Informes, Proyectos) de calidad mundial.
**Filosofía:** 
- Modularidad absoluta ("Caja Negra" independiente por cada servicio).
- Frontend de ultimísima generación y estética premium.
- Motor Python robusto asistido por IA, conectado a Bases de Datos.

## 2. Stack Tecnológico Oficial
*   **Frontend (UI/UX Calidad Mundial):** React + TypeScript (Vite). TailwindCSS, Framer Motion (para animaciones premium, pantallas divididas y "Efecto Escaneado"), Zustand (manejo global del estado).
*   **Backend (Motor y API):** Python 3.14 + FastAPI.
*   **Base de Datos:** PostgreSQL. Administrada mediante SQLAlchemy y Alembic.
*   **Corazón de la Generación (IA):** Agente Inteligente PILI (Modelos de lenguaje, Google Gemini).
*   **Motor de Conversión Binaria (N04):** BeautifulSoup4, Jinja2, python-docx, openpyxl, reportlab/PyPDF2.

## 3. Principio de "Vibe Coding" y Reparación Escalonada por Nodos
Para garantizar una mantenibilidad perpetua y evitar los bloqueos de las versiones monolíticas (V1.0), PILi_Quarts adopta la arquitectura de nodos independientes. Esto significa que **ninguna IA ni desarrollador necesita leer o comprender todo el archivo del proyecto** para crear o reparar una funcionalidad.

*   **Reparación Quirúrgica:** Si el sistema falla al renderizar una tabla de Excel, la IA ("vibe code") **solo debe leer y reparar el nodo específico** responsable de eso (ej. el nodo de conversión de Jinja2 a openpyxl). Toda la UI, los modelos de base de datos y la orquestación del servidor quedan blindados e irrelevantes para dicha tarea.
*   **Escalabilidad de Vibe Coding:** Al estructurarse en nodos aislados, la IA puede "creer" o estructurar un nuevo nodo conceptual desde cero (ej. un nodo "Generador de Contratos Legales") sin alterar los módulos de "Cotizaciones" o "Informes Técnicos".
*   **Beneficio Cognitivo Operativo:** El agente no desperdiciará ventanas de contexto leyendo el árbol de directorios inmenso ni código muerto. Simplemente pide el archivo del nodo afectado, aplica el fix y el macro-sistema seguirá operando.

## 4. Módulos Críticos y Separación Estricta de Responsabilidades

### Módulo 1: N04_Binary_Factory ("La Caja Negra")
*   **Rol:** Convertir Plantillas HTML renderizadas a binarios físicos de calidad mundial (Word `.docx`, PDF `.pdf`, Excel `.xlsx`).
*   **Regla de Oro Constitucional:** Este módulo ES CIEGO respecto a la Inteligencia Artificial. No razona, no redacta, solo procesa código HTML estricto mediante inyección `Jinja2` (Plantillas Doradas) y librerías de conversión. **Nunca** inyectar lógica de LLM (Gemini) dentro de los generadores binarios.

### Módulo 2: Agente PILI ("El Corazón Inteligente")
*   **Rol:** Asistente cognitivo que interactúa con el usuario, procesa carga cognitiva (ej. lee PDFs masivos, extrae datos técnicos de licitaciones) y estructura la información cruda en un JSON (Payload).
*   **Regla de Oro Constitucional:** PILI solo genera y formatea datos (Texto/JSON). PILI **NUNCA** genera ni manipula el archivo Word/PDF físicamente. Su trabajo termina al entregar los datos correctos al Frontend.

### Flujo Exacto de Vida de una Generación (El "Efecto Escáner")
1.  **UI (Frontend):** El usuario interactúa con PILI (Chat en panel lateral izquierdo).
2.  **Preparación (PILI):** PILI procesa y estructura los datos técnicos del proyecto.
3.  **Renderizado en Vivo:** El frontend (`WorkArea.tsx`) toma estos datos y actualiza la Vista Previa HTML en tiempo real a la vista del usuario.
4.  **Disparo (Click en Botón UI):** El usuario pide el archivo. El frontend extrae el DOM HTML *crudo y final* de la vista previa mostrada en pantalla.
5.  **Animación ("El Escáner"):** Se lanza una barra animada "Generando PDF/Word/Excel...". El frontend hace un `POST` enviando exclusivamente el Payload HTML al backend.
6.  **Caja Negra (N04):** El backend recibe el HTML, invoca los conversores puros de Python, ensambla el binario inyectando variables (ej. `{{MONEDA_SIMBOLO}}`, logo local) y lo retorna.
7.  **Descarga:** El frontend intercepta el blob y dispara la descarga silenciosa al cliente.

## 5. Protocolos de Desarrollo Obligatorios
*   **Restricción Frontend:** Mantener intacto el factor "Wow" visual. Bajo ninguna circunstancia se debe simplificar o degradar el "Efecto Escaneado", las paletas oscuras o los loaders. Todo cambio debe respetar el alto nivel de UX/UI (`frontend-design`, `clean-code`).
*   **Restricción Backend:** Si en el futuro se incorpora un nuevo formato, el script de conversión debe encapsularse OBLIGATORIAMENTE dentro de una subcarpeta aislada o un archivo especializado. Todo servicio nuevo DEBE ser un nodo aislado.
*   **Compatibilidad de Entorno:** Si el servidor de Python arroja inconsistencias de importación ligadas a Inteligencia Artificial debido a cambios de versión en Windows, se debe aplicar 'try-catch' o generar un mock. El motor N04 (Caja Negra) y el Frontend DEBEN seguir funcionando aunque el Agente PILI falle, garantizando acceso al sistema base a toda costa.
