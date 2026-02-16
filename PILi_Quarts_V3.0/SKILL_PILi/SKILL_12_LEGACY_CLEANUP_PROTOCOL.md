# Skill 12: Protocolo de Desmantelamiento de Deuda Técnica

> **Objetivo:** Eliminar código muerto, duplicado o hardcodeado tras una migración exitosa a Nodos Especializados.
> **Principio:** "Delete code, keep value."

## 1. Procedimiento de Borrado Seguro (Quarantine First)

Nunca borrar directamente. Siempre mover a cuarentena.

1.  **Identificación:** Localizar el bloque de código a eliminar (ej. Diccionarios gigantes).
2.  **Backup:** Copiar el archivo completo a `backend/quarantine/`.
3.  **Incisión:** Eliminar el código en el archivo original.
4.  **Prótesis:** Inyectar la llamada al nuevo Nodo (N02/N04) que reemplaza la funcionalidad.
5.  **Validación:** Ejecutar test de integración. Si falla, rollback inmediato.

## 2. Redirección de Flujo

El código legacy debe convertirse en un "Cascarón Vacío" (Shell) que solo enruta peticiones.

**Antes:**
```python
def get_price(item):
    return HARDCODED_DICT[item]
```

**Después:**
```python
from modules.N02_Pili_Logic import logic_node

def get_price(item):
    response = logic_node.process_intention({"item": item})
    if "error" in response:
        raise NodeConnectionError("N02 Unreachable")
    return response["price"]
```

## 3. Métricas de Éxito

*   Reducción de Líneas de Código (LOC).
*   Reducción de tamaño de archivo (KB).
*   Desacoplamiento (Menos imports).
