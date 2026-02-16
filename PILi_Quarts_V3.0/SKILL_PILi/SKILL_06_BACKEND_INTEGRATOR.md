📄 Skill 06: Integrador & Backend (The Heart)
Archivo: PILi_Quarts/workspace-modern/SKILL_PILi/SKILL_06_BACKEND_INTEGRATOR.md

Versión: 3.0.1

Rol: Orquestación de Micro-Agentes y Lógica de Negocio.

1. ⚙️ El Motor Central
Este es el "pegamento" (FastAPI) que une a todos los demás:

Recibe el mensaje del Frontend.

Verifica la identidad con el Skill de Auth.

Pasa la petición al Skill PILi Brain.

Persiste los datos en el Skill de BD.

Si el usuario pide descarga, activa el Skill Generador.

📄 Skill 06: Backend Integrator (The Event Bus)
Archivo: 06_BACKEND_INTEGRATOR.md

6.1 Misión Técnica
Actuar como el Orquestador Central y punto de unión (Middleware) entre todos los Skills. Es el corazón que hace que la AppWeb funcione como un organismo único y sincronizado.

6.2 Arquitectura de Comunicación
Protocolo: FastAPI (Asíncrono) para el manejo de múltiples hilos de procesamiento de documentos.

Event Orchestration:

Recibe input del Skill 05 (Frontend).

Valida seguridad con Skill 04 (Security).

Consulta memoria histórica en Skill 03 (DB).

Procesa lógica con Skill 01 (Brain).

Renderiza archivo con Skill 02 (Executor).