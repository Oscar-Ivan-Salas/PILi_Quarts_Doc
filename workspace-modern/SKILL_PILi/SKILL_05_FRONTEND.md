📄 Skill 05: Frontend & Active Canvas (The Interface)
Archivo: PILi_Quarts/workspace-modern/SKILL_PILi/SKILL_05_FRONTEND.md

Versión: 3.0.1

Rol: Experiencia de Usuario, Animaciones y Sincronización Real-Time.

1. 🎨 UI/UX Estándar 2026
Framework: React 18+ con Vite.

Estilos: Tailwind CSS (Dark Mode nativo).

Componentes: Uso de AnimatedAIChat (21st.dev) para la interacción y un Canvas personalizado para la vista previa A4.

2. 🔄 Sincronización del "Active Canvas"
Este Skill debe implementar un WebSocket o Server-Sent Events (SSE):

Cuando PILi Brain procesa un cambio, el Frontend recibe el fragmento de HTML actualizado y lo inyecta en el lienzo sin recargar la página.

Interactividad: Cada input en la vista previa tiene un onChange que actualiza el JSON local para que la descarga final sea exacta a lo editado por el humano.

Entendido, colega. Como Arquitecto Senior, cerraremos este Blueprint de Ingeniería con los 3 Skills finales. Estos documentos no son solo descriptivos; establecen los contratos de sincronización y la infraestructura de comunicación que evitarán que el código se rompa cuando escales a miles de usuarios.

Aquí tienes la entrega final para la ruta: PILi_Quarts/workspace-modern/SKILL_PILi/.

📄 Skill 05: Frontend & Active Canvas (The UI Engine)
Archivo: 05_FRONTEND_ENGINE.md

5.1 Misión Técnica
Este Skill no es solo una interfaz; es un Motor de Renderizado Reactivo. Su responsabilidad es la gestión del estado visual y la persistencia de la sesión en el lado del cliente, garantizando que el "Active Canvas" sea una representación exacta del documento final.

5.2 Contrato de Sincronización (Real-Time)
State Management: Uso obligatorio de Zustand para el estado global (useWorkspaceStore).

Active Canvas Hook: Debe implementar un observador que inyecte el HTML dinámico proveniente del Skill 02 directamente en el DOM, permitiendo edición bidireccional (Chat -> Canvas / Canvas -> Chat).

5.3 Stack de Componentes
Canvas: Contenedor con escala A4 (210mm x 297mm) con soporte para impresión CSS (@media print).

Interaction: Framer Motion para las transiciones de carga de los 6 tipos de documentos.