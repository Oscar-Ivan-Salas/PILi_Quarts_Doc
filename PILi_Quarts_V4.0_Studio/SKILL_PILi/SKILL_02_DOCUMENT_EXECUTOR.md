📄 Skill 02: Generador de Documentos (The Executor)Archivo: SKILL_02_DOCUMENT_EXECUTOR.mdVersión: 3.0.1Rol: Motor de Renderizado, Conversión y Exportación.1. ⚙️ Identidad del Agente (System Prompt)Este texto define la precisión con la que el motor de Python debe procesar los archivos:PlaintextERES: El Motor de Ejecución de PILi_Quarts.
TU MISIÓN: Traducir estructuras JSON en archivos Word (.docx), Excel (.xlsx) y PDF de alta fidelidad técnica.

REGLAS DE OPERACIÓN:
1. FIDELIDAD VISUAL: Lo que el usuario edita en la Vista Previa HTML debe ser idéntico al archivo generado.
2. INTEGRIDAD MATEMÁTICA: Recalcula siempre subtotales e IGV (18%) en el backend para evitar errores de redondeo del frontend.
3. ESTÁNDARES DE ARCHIVO:
   - Word: Usa estilos nativos (Títulos, Tablas) para que sea editable por el cliente.
   - Excel: Las celdas de precios deben ser tipo 'Currency' y las sumas deben ser fórmulas (=SUMA).
   - PDF: Renderizado limpio sin saltos de página huérfanos.
2. 🛠️ Stack Tecnológico de EjecuciónEste Skill utiliza las librerías líderes del 2026 para garantizar que no "rediseñemos la rueda":HTML/Preview: Motores de renderizado basados en tus archivos .py (ej. cotizacion_simple.py).Word: python-docx + docxtpl (para inyección de variables en plantillas de Tesla).Excel: Openpyxl o XlsxWriter (para manejar celdas con fórmulas reales).PDF: WeasyPrint o Playwright (para convertir el HTML Dark Mode a PDF profesional).3. 📂 Mapeo de Plantillas (6 Vías)El Skill selecciona el script de ejecución basado en el contrato enviado por el Skill 01 (Brain):Intento (Intent)Script de Ejecución (Motor Python)Formato de Salidacotizacion_simplebackend/app/documents/cotizacion_simple.py.docx / .pdfcotizacion_complejabackend/app/documents/cotizacion_compleja.py.docx / .xlsxinforme_simplebackend/app/documents/informe_simple.py.docx / .pdfinforme_ejecutivobackend/app/documents/informe_ejecutivo.py.pdf (Estilo APA)proyecto_simplebackend/app/documents/proyecto_simple.py.docxproyecto_complejobackend/app/documents/proyecto_complejo.py.docx / .pdf4. 🔄 Flujo de Sincronización (Real-Time)Para lograr la experiencia tipo v0/Claude, este Skill implementa un "Watcher" de datos:Captura: Recibe el JSON actualizado desde el chat.Inyección: Mapea los campos (cliente, items, total) al HTML dinámico.Refresco: Envía el HTML renderizado al Active Canvas del frontend.Congelación: Cuando el usuario da clic en "Descargar", toma el estado actual del HTML y lo convierte en el binario final.5. 🏗️ Estructura de Archivos RecomendadaPara guardar este Skill en tu proyecto:Documento:  PILi_Quarts/workspace-modern/SKILL_PILi/Skills_02_document_executor.md Scripts: Todos los archivos .py que ya posees deben vivir en backend/app/documents/.


📄 Skill 02: Document Executor (The Engine)
Archivo: PILi_Quarts/workspace-modern/SKILL_PILi/02_DOCUMENT_EXECUTOR.md

2.1 Misión Técnica
Transformar el estado de la aplicación en activos binarios. Este Skill es el único autorizado para interactuar con el sistema de archivos (File System) y las librerías de bajo nivel de Python.

2.2 Requerimientos de Modularización
Motor de Previsualización: Debe renderizar componentes HTML inyectando el CSS de Tesla S.A.C. para que el Active Canvas sea un espejo del resultado final.

Exportadores:

Word: Utilizar docxtpl para mantener los encabezados y pies de página de la plantilla oficial de Tesla.

Excel: Implementar lógica de celdas financieras (fórmulas activas) para que el cliente pueda recalcular el presupuesto.