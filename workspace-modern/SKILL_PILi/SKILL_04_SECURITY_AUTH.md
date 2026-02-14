📄 Skill 04: Seguridad y Autenticación (The Guardian)
Archivo: PILi_Quarts/workspace-modern/SKILL_PILi/SKILL_04_SECURITY_AUTH.md

Versión: 3.0.1

Rol: Blindaje de Accesos y Protección de Propiedad Intelectual.

1. 🔑 Autenticación de Primer Nivel
Para competir con las grandes Apps del 2026, eliminamos las contraseñas inseguras:

Método: Passwordless / Magic Links.

Flujo: El usuario ingresa su correo -> Recibe un token firmado (JWT) -> Acceso instantáneo.

Seguridad: Tokens con expiración de 15 minutos y un solo uso.

2. 🛡️ Blindaje contra Ataques
Sanitización de Entradas: Validación estricta para evitar Inyección SQL y XSS en los campos editables del HTML.

CORS Policy: Solo el dominio de PILi_Quarts puede realizar peticiones al backend.

Rate Limiting: Evita que bots saturen el Skill de PILi realizando miles de preguntas por segundo.

📄 Skill 04: Security & Authentication (The Shield)
Archivo: PILi_Quarts/workspace-modern/SKILL_PILi/04_SECURITY_SHIELD.md

4.1 Misión Técnica
Blindar la propiedad intelectual de Tesla S.A.C. y la privacidad de los clientes. Este Skill debe ser agnóstico al frontend para evitar ataques de inyección de scripts.

4.2 Protocolos de Seguridad
Autenticación: OAuth2 con JWT (JSON Web Tokens). No se almacenan contraseñas en texto plano.

Sanitización: Todo dato proveniente de la IA o del usuario debe pasar por un filtro de limpieza antes de ser procesado por el motor de Python (previene ejecución de código arbitrario).