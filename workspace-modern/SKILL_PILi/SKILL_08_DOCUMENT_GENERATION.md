# N04 Binary Factory: Generación de Documentos Aislada

> **Estado:** ✅ IMPLEMENTADO (Fase de Extirpación)
> **Tipo:** Caja Negra (Black Box)
> **Contrato:** Estricto (JSON Schema / Pydantic)

## 1. Arquitectura del Nodo
El Nodo N04 opera como una fábrica aislada que recibe datos crudos y devuelve archivos binarios. No contiene lógica de negocio, cálculos de precios ni reglas de validación complejas. Su única responsabilidad es "dibujar" el documento.

### Estructura de Archivos
```text
backend/modules/N04_Binary_Factory/
├── index.py                <-- Punto de Entrada Único (Factory Proxy)
├── contract.json           <-- Definición del Contrato de Datos
├── models.py               <-- Modelos de Validación Pydantic
├── excel_generator.py      <-- Motor de Excel (openpyxl)
├── word_generator.py       <-- Motor de Word (python-docx)
├── pdf_generator.py        <-- Motor de PDF (ReportLab)
└── templates/              <-- Plantillas HTML/DOCX encapsuladas
```

## 2. Contrato de Datos (Input)
El nodo rechaza cualquier petición que no cumpla con este esquema:

```json
{
  "user_context": {
    "empresa_nombre": "Tesla S.A.C.",
    "empresa_ruc": "20601138787",
    ...
  },
  "document_metadata": {
    "tipo": "COTIZACION",
    "subtipo": "SIMPLE",
    "formato": "XLSX"
  },
  "payload": {
    "items": [...],
    "totales": {...}
  }
}
```

## 3. Evidencia de Aislamiento
Se ha verificado mediante el script `test_n04_isolation.py` que el nodo puede generar documentos completos sin importar ninguna librería del `legacy` o `app.main`.

## 4. Patrón de Diseño
Se utiliza un **Abstract Factory Pattern** en `index.py`:
1.  **Validación:** Pydantic asegura integridad de datos.
2.  **Despacho:** `process_request` enruta al generador específico según `metadata.formato`.
3.  **Adaptador:** Los generadores antiguos (`excel_generator_complete.py`) son adaptados para cumplir con la interfaz del nodo.
