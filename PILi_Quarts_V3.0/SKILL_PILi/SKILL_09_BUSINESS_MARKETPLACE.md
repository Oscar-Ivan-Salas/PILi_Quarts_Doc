📄 Skill 09: Business Logic & Marketplace (The Uber Engine)
Archivo: PILi_Quarts/workspace-modern/SKILL_PILi/09_BUSINESS_MARKETPLACE.md Propósito: Definir el flujo de intermediación y la personalización de marca blanca (White Label) para los ejecutores.

1. 👥 Gestión de Identidad Dual
El sistema debe diferenciar y almacenar dos tipos de perfiles en la BD (Skill 03):


Perfil Cliente: Datos capturados en el formulario inicial (Nombre/Razón Social, RUC, Dirección) para ser receptores de la cotización.

Perfil Usuario (Ejecutor): Datos de la empresa que presta el servicio (Logo, Firma, RUC propio, Certificaciones). Estos datos sobreescriben los encabezados de las plantillas para que el documento final salga con su propia marca profesional.

2. 🔄 Flujo de Caso de Uso: Licitación "Uber Style"

Solicitud: Un cliente llena el formulario inicial detallando su necesidad (Ej: Instalación de Tableros).


Estandarización: PILi procesa el requerimiento y genera un Documento de Referencia técnico.

Licitación Abierta: El "Skill 07 (Marketplace)" notifica a las empresas prestadoras calificadas.


Postulación Personalizada: El ejecutor acepta el reto, PILi inyecta sus datos de usuario en la plantilla y genera la propuesta oficial en segundos para enviar al cliente.

🛑 Instrucciones de Actualización para Antigravity
Antigravity, incorpora estos cambios inmediatamente para evitar alucinaciones en el modelo de negocio:


Actualización del Formulario Inicial: Debes asegurar que el Skill 05 (Frontend) permita al usuario logueado configurar sus propios "Datos de Empresa" una sola vez.

Inyección Dinámica de Cabeceras: El Skill 02 (Executor) debe dejar de usar una cabecera estática de Tesla S.A.C. por defecto. Ahora debe realizar un merge entre los datos del Cliente y los datos del Usuario Prestador guardados en la BD.


Validación de Caso de Uso: Si el usuario no ha configurado su perfil de prestador, PILi Brain (Skill 01) debe pedirle esos datos antes de generar cualquier documento, explicando que son necesarios para la personalización.

📊 Impacto en la Tesis de Maestría
Este enfoque añade un valor científico y técnico inmenso a tu tesis en Ciencia de Datos:


Análisis Predictivo: Podrás incluir un capítulo sobre cómo PILi predice el costo de un servicio basado en históricos de licitaciones anteriores.


Optimización de Marketplaces: Documentarás la eficiencia de usar agentes IA para reducir la asimetría de información entre clientes y contratistas.

¿Procedemos a que Antigravity genere el código para la "Tabla de Usuarios Ejecutores" en la base de datos para habilitar esta personalización?