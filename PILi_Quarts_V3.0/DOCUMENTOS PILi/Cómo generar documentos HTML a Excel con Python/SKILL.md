# Skill: Tesla HTML-to-Excel Converter

Esta skill permite transformar plantillas HTML profesionales de Tesla Electricidad en "gemelos digitales" en formato Excel, manteniendo la fidelidad visual, la jerarquía de datos y la funcionalidad numérica.

## Directivas de Diseño de Software

Como experto en diseño de software, para que un Excel sea un "gemelo exacto" de un HTML, se deben seguir estas reglas:

1.  **Mapeo de Estilos Visuales:**
    *   **Paleta de Colores:** Usar estrictamente los colores corporativos: Azul Primario (`#0052A3`), Azul Secundario (`#1E40AF`) y Gris Claro (`#F9FAFB`).
    *   **Tipografía:** Simular 'Calibri' o 'Arial'. Usar negritas para títulos y etiquetas de datos (`info-label`).
    *   **Bordes:** Replicar los acentos visuales (como el `border-left` grueso en títulos) usando bordes izquierdos de estilo `thick`.

2.  **Integridad de Datos:**
    *   **Conversión Numérica:** Nunca dejar valores como texto si son monetarios o cantidades. Limpiar símbolos (`$`, `,`) y placeholders (`{{TOTAL}}`) antes de la inserción.
    *   **Formatos de Celda:** Aplicar `number_format = '"$"#,##0.00'` a todas las celdas de precios y totales.

3.  **Arquitectura de Documentos:**
    *   **Cotizaciones:** Estructura de tabla rígida con anchos de columna fijos (A:10, B:50, C:12, D:12, E:15, F:15).
    *   **Informes:** Estructura narrativa con columnas anchas y `wrap_text = True` para párrafos largos.
    *   **Detección Automática:** El sistema debe identificar el tipo de documento buscando clases clave como `portada-apa` o `tabla-section`.

## Instrucciones de Uso

1.  Asegurarse de tener instaladas las dependencias: `pip install openpyxl beautifulsoup4`.
2.  Utilizar el script `convertidor_tesla.py` proporcionado en este paquete.
3.  Ejecutar el método `convert(html_path, output_path)` para procesar cualquier plantilla nueva.

## Estándares de Calidad
*   Las celdas de totales deben estar resaltadas en azul primario con texto blanco.
*   Las tablas deben usar estilo cebra (filas alternas en gris claro) para mejorar la legibilidad.
*   El pie de página debe estar centrado y con fuente pequeña (tamaño 8).
