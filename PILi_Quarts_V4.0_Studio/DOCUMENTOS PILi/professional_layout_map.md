
# 🖥️ Mapa de Identidad Profesional de la Aplicación (Landing View)

A continuación se detalla la disección profesional de la interfaz actual, asignando una identidad técnica y funcional a cada región crítica del sistema.

Este "Landing Page View" representa el estado del arte de nuestra arquitectura frontend.

---

## 1. 🧭 The Navigation Hub (Izquierda)
*Componente: [NavigationPanel.tsx](file:///e:/PILi_Quarts/workspace-modern/frontend/src/components/NavigationPanel.tsx)*

**Definición Profesional:**
El centro de comando logístico. Es el punto de entrada para todas las rutas de negocio. No es un simple menú; es un **Hub Jerárquico** que orquesta el flujo de trabajo.

**Elementos Clave:**
*   **Proyectos & Flujos**: Acceso rápido a [Cotizaciones](file:///e:/PILi_Quarts/frontend/src/components/workspace/CotizacionesView.jsx#16-140), `Informes`, `Proyectos`.
*   **Contadores de Estado (Badges)**: Indicadores visuales de tareas pendientes (e.g., Simple: `10`, Complejo: `3`).
*   **Acciones Rápidas (Quick Actions)**: Botones de acceso directo a herramientas críticas (`Zap` Nuevo, `Calculator`).

---

## 2. ⚡ The Command Center (Arriba)
*Componente: [WorkspaceHeader.tsx](file:///e:/PILi_Quarts/workspace-modern/frontend/src/components/WorkspaceHeader.tsx)*

**Definición Profesional:**
La barra de control global. Supervisa el estado de la sesión, la identidad de la marca y las configuraciones transversales.

**Elementos Clave:**
*   **Brand Identity**: El logo "P" (PILi) y el título del workspace (`Agentic v3.0`).
*   **Global Actions**: Controles de persistencia ([Guardar](file:///e:/PILi_Quarts/frontend/src/App.jsx#329-372)), Navegación raíz ([Inicio](file:///e:/PILi_Quarts/frontend/src/App.jsx#280-306)).
*   **Theme Switcher**: Control de atmósfera visual (`Dark`, `Light`, `Tesla`, `Magenta`).
*   **User Profile**: Gestión de identidad del usuario activo.

---

## 3. 🎯 The Active Canvas (Centro)
*Componente: [WorkArea.tsx](file:///e:/PILi_Quarts/workspace-modern/frontend/src/components/WorkArea.tsx)*

**Definición Profesional:**
El escenario principal. Es un lienzo dinámico ("Canvas") que muta según la intención del usuario. Aquí es donde **ocurre el trabajo**.

**Estados del Canvas:**
*   **State A: Dashboard**: Vista resumen (cuando no hay flujo activo).
*   **State B: Form Input**: Captura de datos estructurados ([ComplexProjectForm](file:///e:/PILi_Quarts/workspace-modern/frontend/src/components/ComplexProjectForm.tsx#42-334)).
*   **State C: Live Preview**: Renderizado en tiempo real del documento final ([EditableCotizacionSimple](file:///e:/PILi_Quarts/workspace-modern/frontend/src/components/EditableCotizacionSimple.tsx#16-203)).
*   **State D: Personalization**: *[Integrándose ahora]* Panel de ajuste visual (Colores, Logos, Fuentes).

---

## 4. 🧠 PILI Intelligence Panel (Derecha)
*Componente: [ChatPanel.tsx](file:///e:/PILi_Quarts/workspace-modern/frontend/src/components/ChatPanel.tsx)*

**Definición Profesional:**
El cerebro asistente lateral. No es un simple chat; es un **Copiloto Contextual Persistente**.

**Responsabilidades:**
*   **Context Awareness**: "Sabe" lo que estás haciendo en el *Active Canvas*.
*   **Proactive Assistance**: Sugiere acciones basadas en el estado del formulario.
*   **Data Injection**: Inyecta datos extraídos directamente al *Active Canvas*.
*   **Always-On**: Siempre accesible, nunca intrusivo.

---

## 🏗️ Resumen de Arquitectura Visual

```
+---------------------------------------------------------------+
|                      COMMAND CENTER (Header)                  |
+-------------------+-----------------------+-------------------+
|    10% (Nav)      |     60% (Canvas)      |    30% (Chat)     |
|                   |                       |                   |
|  NAVIGATION HUB   |     ACTIVE CANVAS     | PILI INTELLIGENCE |
|  (Minimal Fixed)  |     (Expanded Work)   | (Assistant)       |
|                   |                       |                   |
|                   |                       |                   |
|                   |                       |                   |
+-------------------+-----------------------+-------------------+
```
🖥️ Mapa de Identidad Profesional de la Aplicación (Landing View)
A continuación se detalla la disección profesional de la interfaz actual, asignando una identidad técnica y funcional a cada región crítica del sistema.

Este "Landing Page View" representa el estado del arte de nuestra arquitectura frontend (Layout Cinemático 10-60-30).

1. 🧭 The Navigation Hub (Izquierda - 10%)
Componente: 
NavigationPanel.tsx

Definición Profesional: El centro de comando logístico. Es el punto de entrada para todas las rutas de negocio. No es un simple menú; es un Hub Jerárquico que orquesta el flujo de trabajo.

Elementos Clave:

Proyectos & Flujos: Acceso rápido a 
Cotizaciones
, Informes, Proyectos.
Contadores de Estado (Badges): Indicadores visuales de tareas pendientes (e.g., Simple: 10, Complejo: 3).
Acciones Rápidas (Quick Actions): Botones de acceso directo a herramientas críticas (Zap Nuevo, Calculator).
2. ⚡ The Command Center (Arriba)
Componente: 
WorkspaceHeader.tsx

Definición Profesional: La barra de control global. Supervisa el estado de la sesión, la identidad de la marca y las configuraciones transversales.

Elementos Clave:

Brand Identity: El logo "P" (PILi) y el título del workspace (Agentic v3.0).
Global Actions: Controles de persistencia (
Guardar
), Navegación raíz (
Inicio
).
Theme Switcher: Control de atmósfera visual (Dark, Light, Tesla, Magenta).
User Profile: Gestión de identidad del usuario activo.
3. 🎯 The Active Canvas (Centro - 60%)
Componente: 
WorkArea.tsx

Definición Profesional: El escenario principal. Es un lienzo dinámico ("Canvas") que muta según la intención del usuario. Aquí es donde ocurre el trabajo.

Estados del Canvas:

State A: Dashboard: Vista resumen (cuando no hay flujo activo).
State B: Form Input: Captura de datos estructurados (
ComplexProjectForm
).
State C: Live Preview: Renderizado en tiempo real del documento final (
EditableCotizacionSimple
).
State D: Personalization: [Integrándose ahora] Panel de ajuste visual (Colores, Logos, Fuentes).
4. 🧠 PILI Intelligence Panel (Derecha - 30%)
Componente: 
ChatPanel.tsx

Definición Profesional: El cerebro asistente lateral. No es un simple chat; es un Copiloto Contextual Persistente.

Responsabilidades:

Context Awareness: "Sabe" lo que estás haciendo en el Active Canvas.
Proactive Assistance: Sugiere acciones basadas en el estado del formulario.
Data Injection: Inyecta datos extraídos directamente al Active Canvas.
Always-On: Siempre accesible, nunca intrusivo.
🏗️ Resumen de Arquitectura Visual
+---------------------------------------------------------------+
|                      COMMAND CENTER (Header)                  |
+-------------------+-----------------------+-------------------+
|                   |                       |                   |
|                   |                       |                   |
|  NAVIGATION HUB   |     ACTIVE CANVAS     | PILI INTELLIGENCE |
|  (Sidebar)        |     (Main Work)       | (Assistant)       |
|                   |                       |                   |
|                   |                       |                   |
|                   |                       |                   |
+-------------------+-----------------------+-------------------+

Comment
Ctrl+Alt+M
