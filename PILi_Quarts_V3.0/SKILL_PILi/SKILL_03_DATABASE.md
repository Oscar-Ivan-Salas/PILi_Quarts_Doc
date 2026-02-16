📄 Skill 03: Base de Datos (The Memory)Archivo: PILi_Quarts/workspace-modern/SKILL_PILi/SKILL_03_DATABASE.mdVersión: 3.0.1Rol: Persistencia, Integridad y Escalabilidad de Datos.1. 🧬 Arquitectura de DatosEste Skill define cómo se almacena la información para que sea escalable a miles de usuarios.Motor Recomendado: PostgreSQL (Producción) / SQLite (Pruebas).ORM: SQLAlchemy / Prisma (para asegurar migraciones sin dolor).2. 🗄️ Modelado de Tablas PrincipalesTablaDescripciónCampos CríticosUsersPerfiles de empresas y ejecutores.id, email, password_hash, company_name, logo_url, ruc.DocumentsEl corazón de la app.id, user_id, type (6 tipos), status, data_json (Contenido dinámico).MarketplaceProyectos publicados para licitación.id, doc_id, budget_base, category, expiry_date.Prices_DBReferencial de suministros.id, item_name, unit, market_price, last_update.3. 🛡️ Reglas de IntegridadJSON Schema Validation: Antes de guardar en data_json, el Skill debe validar que el esquema coincida con el tipo de documento (ej. que una cotización tenga items y totales).Versioning: Cada vez que PILi edita el documento mediante el chat, se crea un checkpoint para que el usuario pueda "deshacer" cambios.

📄 Skill 03: Data Architecture & Persistence
Archivo: PILi_Quarts/workspace-modern/SKILL_PILi/03_DATABASE_ARCH.md

3.1 Misión Técnica
Garantizar la persistencia y la trazabilidad de los proyectos. El diseño debe permitir migraciones en caliente (Zero-Downtime) y ser compatible con bases de datos distribuidas.

3.2 Esquema de Datos Relacional (Puntos Críticos)
Tabla Projects: UUID como llave primaria (no IDs incrementales por seguridad).

Tabla Snapshots: Guardar el estado del JSON en cada hito importante para permitir el "Time Travel" (volver a versiones anteriores de la cotización).

Módulo de Precios: Sincronización con el mercado para alertar si un material en la cotización está por debajo del costo real.