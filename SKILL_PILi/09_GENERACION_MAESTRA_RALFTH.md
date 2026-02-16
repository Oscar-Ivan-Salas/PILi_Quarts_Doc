# 📜 Skill de Generación Maestra: El Sello de Piedra (R.A.L.F.T.H.)

> **Directiva Suprema**: "Fidelidad Absoluta. El bit que sale del servidor debe ser indistinguible del papel firmado por un ingeniero colegiado."
> **Calidad**: Solo se permite la liberación de código que pase la Matriz 6x3 sin errores.

## 1. El Protocolo R.A.L.F.H.

### **R - Refine (Refinamiento)**
*   **Logos**: Alta resolución, posicionamiento absoluto (X,Y) en PDF. No pixelación.
*   **Firmas**: Integración vectorial o imagen de alta calidad.

### **A - Analyze (Análisis)**
*   **Estructura**: Validación estricta contra esquemas PMI/Electricidad.
*   **Datos**: Tipos de datos fuertes (Float para moneda). Unidades (m², S/, $) obligatorias.

### **L - Learn (Aprendizaje)**
*   **Estilo**: Respeto absoluto a la identidad visual del usuario (Colores Tesla, Fuentes Corporativas).

### **F - Faithfulness (Fidelidad "Espejo Total")**
*   **Visual**: HTML Preview == Output Binario.
*   **Técnica**: Tablas `openpyxl` con bordes y estilos reales. PDF `ReportLab` con layouts de tablas anidadas.

### **H - Hybrid (Motor Híbrido)**
*   **Word/Excel**: Motores Nativos (`python-docx`, `openpyxl`) para editabilidad.
*   **PDF**: Renderizado Directo (`ReportLab`) para precisión milimétrica.

---

## 2. La Matriz de Validación 6x3

Para certificar cualquier versión, el sistema debe generar **18 Archivos Perfectos**:

| MODELO (6)      | WORD | EXCEL | PDF | REQUISITO CRÍTICO |
| :---            | :---:| :---: | :---:| :--- |
| Cot. Simple     | ✅   | ✅    | ✅   | Logo + IGV 18% |
| Cot. Compleja   | ✅   | ✅    | ✅   | APU Desglosado |
| Proy. Simple    | ✅   | ✅    | ✅   | Cronograma Básico |
| Proy. Complejo  | ✅   | ✅    | ✅   | Dashboard KPI + Riesgos |
| Inf. Técnico    | ✅   | ✅    | ✅   | Formato Ingeniería Tesla |
| Inf. Ejecutivo  | ✅   | ✅    | ✅   | Normas APA |

### **Reglas de Zonificación (Excel R.A.L.F.T.H.)**
*   **Zona 1 (Filas 1-9):** Branding Obligatorio. Logo flotante (B2) + Datos Empresa (E2). **PROHIBIDO** escribir datos técnicos aquí.
*   **Zona 2 (Filas 10-16):** Datos del Cliente. Inyección dinámica de metadatos.
*   **Zona 3 (Fila 17+):** Cuerpo Técnico. Alcance, Tablas y Cronogramas.
*   **Zona 3 (Fila 17+):** Cuerpo Técnico. Alcance, Tablas y Cronogramas.
*   **Regla de Oro:** "Todo contenido técnico debe tener un row_offset mínimo de 8 filas respecto al encabezado".

### **Protocolo V10: "The Mirror" (Maquetación)**
*   **Grid System**: Uso de 12 Columnas (A-L) para distribución proporcional.
*   **Wrap Text**: Texto enriquecido activado por defecto en descripciones.
*   **Freeze Panes**: Encabezado inmovilizado (A10) para mantener identidad visible.
*   **Universal Renderer**: Soporte nativo para `.portada`, `.seccion`, `.kpis-grid`, `.gantt` y `.raci`.
*   **Full Scope**: Los 6 modelos deben tener contenido, no solo las cotizaciones.
*   **Tri-Brid Output**: Node N04 debe ser capaz de generar XLSX (Universal), DOCX (Mirror), y PDF (ReportLab) bajo demanda.

### Procedimiento de Certificación

1.  **Ejecutar Validator**: `python modules/N04_Binary_Factory/validate_mirror.py`
2.  **Verificar 18 Archivos**: Asegurar que existen 3 archivos (XLSX, DOCX, PDF) por cada uno de los 6 modelos.
3.  **Inspección Visual**: Abrir al menos un Proyeco y un Informe para verificar el "Llenado".
4.  **Resultado**: 18/18 Éxito = **RELEASE CANDIDATE**.

---

**Estado del Skill**: PROTEGIDO POR LEY DE INGENIERÍA.
**Versión**: 1.0 (Sello de Piedra)
