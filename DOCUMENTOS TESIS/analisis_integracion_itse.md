# Análisis de Integración: Chat ITSE -> Vista Previa

## 🚨 El Problema Reportado
El usuario percibe una "incoherencia" y dificultad para integrar lo necesario. A pesar de que el chat ahora tiene lógica (pregunta cosas de ITSE), el paso a la siguiente etapa (Vista Previa/Edición) parece estar desconectado o ser inconsistente.

## 🔍 Puntos Críticos de Inspección

### 1. El Puente de Datos (`App.jsx`)
¿Qué pasa exactamente cuando el Chat dispara `onCotizacionGenerada`?
- ¿Se transforman los datos?
- ¿Se pierden campos clave?

### 2. El Receptor (`VistaPreviaProfesional.jsx`)
Los logs muestran:
`✅ Renderizando EDITABLE_COTIZACION_SIMPLE`
`📦 Props: Object`

Necesitamos verificar si `EDITABLE_COTIZACION_SIMPLE` está preparado para recibir la estructura específica de ITSE o si solo espera campos de Electricidad.

### 3. La Estructura de Datos (JSON Match)
**Lo que envía `ITSESpecialist`:**
```json
{
    "tipo_flujo": "cotizacion-simple",
    "servicio": "itse",
    "items": [...],
    "total": ...,
    "moneda": "PEN"
}
```

**Lo que espera la Vista Previa:**
¿Espera `cliente`? ¿Espera `fecha`? ¿Espera una estructura específica de `items`?

## 🧪 Plan de Acción
1. Revisar `App.jsx`: Manejador `handleCotizacionGenerada` (o similar dentro del render de `PiliITSEChat`).
2. Revisar `EditableCotizacionSimple.jsx`: Ver qué props consume y cómo renderiza los items.
3. Identificar el "Gap" (Brecha) de datos.
