# Arquitectura Técnica Integral: PILi Quarts v3.0
**Documentación Técnica para Ingeniería de Software**

> **Autor:** Sistema Antigravity  
> **Versión del Sistema:** v3.0.1  
> **Fecha:** Febrero 2026  
> **Estado:** Producción

---

## 1. Visión General del Sistema (System Overview)

PILi Quarts v3.0 es una plataforma de ingeniería avanzada para la generación automatizada de documentos técnicos (Cotizaciones, Proyectos, Informes).  
Su arquitectura se basa en un modelo **Híbrido Distribuido**:

*   **Frontend (React/Vite):** Cliente SPA reactivo y moderno.
*   **Backend (FastAPI/Python):** API REST asíncrona y modular.
*   **Core (PILI Brain):** Motor de inteligencia artificial híbrido (IA Generativa + Reglas Determinísticas).

El sistema opera bajo el principio de **"Inteligencia Local Primero"**, garantizando funcionalidad incluso sin conexión a servicios externos de IA.

---

## 2. Arquitectura Frontend (Cliente)

El cliente está construido sobre **React 18** utilizando **Vite** como bundler para máximo rendimiento.

### 2.1 Stack Tecnológico
*   **Lenguaje:** TypeScript (Estrictamente tipado).
*   **UI Framework:** Tailwind CSS v3 (Utilitypyfirst).
*   **Animaciones:** Framer Motion (Transiciones fluidas y micro-interacciones).
*   **Estado Global:** Zustand (`useWorkspaceStore` para gestión de proyectos/cotizaciones).
*   **Estado Local Complex:** React Context (`PiliContext`) y Hooks personalizados (`useTransition`).

### 2.2 Componente Crítico: `AnimatedAIChat`
Este componente no es solo una "ventana de chat", es el **Controlador de Flujo** de la aplicación:
1.  **Gestión de Estado de Conversación (`conversationData`):** Mantiene un objeto persistente que acumula las respuestas del usuario (área, potencias, etc.) y lo reenvía al backend en cada petición. Esto soluciona el problema de "falta de memoria" de las APIs REST tradicionales (Stateless).
2.  **Renderizado Adaptativo:**
    *   **Modo "Greeting":** Muestra título y sugerencias.
    *   **Modo "Active":** Oculta elementos decorativos para maximizar el área de lectura.
    *   **Extracción de Pensamientos:** Visualiza el `thought_trace` (traza de pensamiento) del backend.
3.  **Manejo de Errores Robusto:** Implementa captura de excepciones detallada (código 422/500) para feedback inmediato al usuario.

---

## 3. Arquitectura Backend (Servidor)

El servidor es una aplicación **Python / FastAPI** diseñada bajo principios de **Clean Architecture**.

### 3.1 Estructura Modular (`/modules/pili/`)
El backend no es monolítico; está dividido en módulos funcionales:
*   `api/`: Routers y Schemas (Pydantic) para validación de entrada/salida.
*   `core/`: Lógica de negocio central (`Brain`).
*   `legacy/`: Integradores de sistemas heredados (`PILIIntegrator`).
*   `config/`: Variables de entorno y configuraciones globales.

### 3.2 Entry Point (`main.py`)
Configura el servidor **Uvicorn** en el puerto **3030**.
*   **Middleware CORS:** Configurado explícitamente para permitir orígenes `http://localhost:3010` (Frontend).
*   **Manejo de Excepciones Globales:** Estandariza las respuestas de error JSON.

---

## 4. El Núcleo: PILi Brain & Integrator (Logic Layer)

Esta es la "joya de la corona". PILi no es un simple chatbot; es un **Sistema Multi-Agente Orquestado**.

### 4.1 Patrón de Diseño: Orquestador (The Integrator)
La clase `PILIIntegrator` actua como el director de orquesta.
Cuando llega un mensaje, el flujo es:
1.  **Recepción:** Recibe mensaje + `contexto` (incluyendo `datos_acumulados`).
2.  **Detección de Intención:** Analiza si el usuario quiere "Cotizar", "Proyectar" o "Informar".
3.  **Enrutamiento de Agente (Routing):**
    *   Si el servicio es complejo (ej. "ITSE"), enruta al **Especialista Técnico**.
    *   Si es simple, lo maneja el **Asistente General**.
4.  **Selección de Estrategia de Respuesta (Tiered Logic):**
    *   **Nivel 1 (IA Generativa - Gemini):** Si está disponible y configurada, genera una respuesta natural y creativa.
    *   **Nivel 2 (Lógica Determinística - Local Specialist):** Si no hay IA, usa reglas lógicas (`if/else` avanzados) para guiar al usuario paso a paso (Etapa 1: Saludo -> Etapa 2: Recopilación -> Etapa 3: Confirmación).
    *   **Nivel 3 (Plantillas Fallback):** Respuestas predefinidas para errores críticos.

### 4.2 Lógica Independiente (Modo Offline)
Cuando la IA externa no está disponible, PILi opera de manera autónoma utilizando `pili_local_specialists.py` (o lógica embebida en `integrator`):
*   **Máquina de Estados Finitos (FSM):** El integrador rastrea en qué "Etapa" está la conversación.
    *   *Ejemplo:* Si faltan datos (`area_m2` es nulo), la FSM pasa al estado `recopilando_datos` y genera la pregunta específica.
*   **Memoria Contextual:** Al recibir el objeto `conversationData` del frontend, el integrador "recuerda" inmediatamente el estado anterior sin necesidad de base de datos persistente para la sesión volátil.

### 4.3 Generador de Documentos
Una vez recopilados los datos necesarios (via Chat), el sistema invoca al `WordGenerator` o `PDFGenerator`:
1.  **Mapping:** Convierte el JSON de la conversación en un diccionario de contexto plano.
2.  **Templating:** Usa `python-docx-template` para inyectar variables en plantillas `.docx` pre-diseñadas (evitando problemas de formato).
3.  **Renderizado:** Genera el binario final y devuelve la URL de descarga local.

---

## 5. Base de Datos (Persistencia)

Aunque el Chat es mayormente "in-memory" durante la sesión, los proyectos finales se persisten:
*   **SQLite (Dev/Local):** Ligera, rápida, sin configuración.
*   **SQLAlchemy ORM:** Abstracción de base de datos. Permite cambiar a PostgreSQL en producción sin tocar el código de negocio.
*   **Modelos:**
    *   `Project`: Metadatos del proyecto.
    *   `Quote`: Detalle de cotizaciones y versiones.
    *   `Client`: Información reutilizable de clientes.

---

## Conclusión

La arquitectura v3.0 de PILi destaca por su **Resiliencia**. No depende de una conexión a internet para funciones críticas de ingeniería. Su diseño desacoplado (Frontend React <-> Backend Python) permite escalar cada parte independientemente, mientras que el `PILIIntegrator` asegura que la lógica de negocio compleja se mantenga centralizada y testeable.
