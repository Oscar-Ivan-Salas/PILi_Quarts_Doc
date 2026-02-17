# Skill 03: Esquema de Base de Datos para Ingeniería de Conocimiento PILi

> **Objetivo:** Normalizar el conocimiento técnico de PILi en una base de datos relacional (SQLite), eliminando diccionarios hardcodeados.
> **Principio:** RAG (Retrieval-Augmented Generation) para reglas de negocio.

## Diagrama ER

```mermaid
erDiagram
    PILI_SERVICES ||--o{ PILI_KNOWLEDGE_BASE : "define items of"
    PILI_SERVICES ||--o{ PILI_RULES : "governed by"
    
    PILI_SERVICES {
        int id PK
        string service_key UK "slug único (e.g. 'electricidad_residencial')"
        string display_name "Nombre legible"
        string normativa_referencia "Ref. técnica"
        string descripcion "Descripción del servicio"
    }

    PILI_KNOWLEDGE_BASE {
        int id PK
        int service_id FK
        string category "Categoría del item (e.g. 'MATERIAL', 'MANO_OBRA')"
        string item_description "Descripción del item"
        string unit_measure "Unidad (m2, und, glba)"
        decimal unit_price "Precio unitario"
        string currency "PEN / USD"
    }

    PILI_RULES {
        int id PK
        int service_id FK
        string rule_slug "Identificador de regla"
        string condition_logic "Lógica (JSON o string)"
        string outcome_action "Acción o sugerencia"
        int criticality "1-5 nivel de importancia"
    }
```

## Definición de Tablas (DDL - SQLAlchemy)

La implementación física se realizará e `backend/modules/N02_Pili_Logic/knowledge_db.py`.

### 1. `pili_services`
Catálogo maestro de los 10 servicios especializados.

### 2. `pili_knowledge_base`
Lista de precios unitarios, materiales y costos asociados por servicio. Replaza a los diccionarios de precios actuales.

### 3. `pili_rules`
Reglas de inferencia técnica. Ejemplo: "Si es residencial y > 200m2, sugerir trifásico".
