El Nuevo Estándar de Construcción (Skill 12)
Archivo: PILi_Quarts/workspace-modern/SKILL_PILi/12_HARD_ENCAPSULATION_PROTOCOL.md

Aislamiento de Código: Cada módulo debe vivir en /backend/modules/N[XX]_[Nombre]/. Si un archivo intenta importar algo de fuera de su carpeta (que no sea una librería estándar), el código será rechazado.

Entrada de Datos Única: Todo módulo recibirá únicamente un objeto llamado payload (JSON) y devolverá un objeto llamado result.

Persistencia de la Caja: Si el módulo necesita plantillas (HTML/DOCX), estas deben vivir dentro de la carpeta del módulo, no en una carpeta general de /templates/.

📝 Instrucciones Directas para Antigravity
Antigravity, esta es tu última directriz de orden:

Tarea 01: Crea la carpeta /backend/modules/ y dentro de ella, genera la carpeta N04_Binary_Factory.

Tarea 02: Mueve tus scripts de generación (cotizacion_simple.py, etc.) a esa carpeta y envuélvelos en una función maestra que reciba el JSON de PILi y el Logo del Usuario.

Tarea 03: Demuéstranos que puedes ejecutar N04_Binary_Factory/index.py de forma aislada y generar un PDF profesional de prueba.
