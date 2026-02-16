# Skill 02: Nodo N02 - Pili Logic (The Brain)

> **Misión:** Actuar como el cerebro lógico y recuperador de conocimiento de la IA.
> **Responsabilidad:** Consultar la BD de Conocimiento y estructurar la lógica de negocio.
> **Input:** Intención/Contexto del usuario.
> **Output:** JSON estructurado para N04 (Binary Factory) o Frontend.

## Arquitectura del Nodo

Este nodo NO genera documentos. Este nodo PIENSA y RECUPERA datos.

```text
backend/modules/N02_Pili_Logic/
├── index.py                <-- Punto de Entrada (Logic Controller)
├── knowledge_db.py         <-- Modelos ORM y Conexión DB
├── services/               <-- Lógica específica por dominio (opcional)
└── migration/              <-- Scripts de carga de datos (ETL)
```

## Flujo de Trabajo (RAG Técnico)

1.  **Recepción:** Recibe "Necesito cotización para casa de 150m2".
2.  **Inferencia:** Detecta servicio `electricidad_residencial`.
3.  **Recuperación:** Consulta `PILI_KNOWLEDGE_BASE` filtrando por `service_id`.
4.  **Cálculo:** Aplica reglas de `PILI_RULES` (ej. factor de área).
5.  **Estructuración:** Genera el payload JSON que el N04 necesita.

## Contrato de Salida (hacia N04)

El N02 es el responsable de crear el `payload` válido para el N04.

```json
{
  "target_node": "N04_BINARY_FACTORY",
  "action": "GENERATE_DOCUMENT",
  "data": {
     "document_metadata": { ... },
     "payload": {
        "items": [
           { "descripcion": "Punto de Luz", "cantidad": 15, "precio": 45.00 }
        ],
        "totales": { ... }
     }
  }
}
```
