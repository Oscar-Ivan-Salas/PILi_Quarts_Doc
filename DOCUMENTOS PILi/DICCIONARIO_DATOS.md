# 💾 DICCIONARIO DE DATOS - PILi V3.0

Referencia técnica de la estructura de información manejada por el sistema.

---

## 1. 🗄️ MODELO DE BASE DE DATOS (Relacional)

El sistema utiliza **SQLAlchemy** (ORM). Las tablas principales son:

### 1.1 `proyectos`
Almacena la cabecera de cada operación (sea cotización, proyecto o informe).

| Campo | Tipo | Descripción |
| :--- | :--- | :--- |
| `id` | Integer (PK) | Identificador único autoincremental. |
| `nombre` | String(200) | Título descriptivo (ej. "Instalación Oficinas Tesla"). |
| `cliente` | String(100) | Nombre del cliente final. |
| `tipo` | Enum | Tipo de servicio: `electrico`, `automatizacion`, `proyecto_pmi`. |
| `estado` | Enum | `borrador`, `generado`, `enviado`, `aprobado`. |
| `fecha_creacion` | DateTime | Timestamp de creación. |
| `datos_json` | JSON | **(CRÍTICO)** Contiene toda la estructura flexible (ítems, precios, cronograma). |

---

## 2. 🧬 ESTRUCTURA JSON (Campo `datos_json`)

Debido a la naturaleza flexible de las cotizaciones, la mayoría de la data vive en un campo JSON.

### 2.1 Estructura para COTIZACIONES (`cotizacion_simple`, `cotizacion_compleja`)

```json
{
  "items": [
    {
      "descripcion": "Interruptor Termomagnético 3x63A",
      "cantidad": 2,
      "unidad": "und",
      "precio_unitario": 145.50,
      "subtotal": 291.00
    }
  ],
  "totales": {
    "subtotal": 291.00,
    "igv": 52.38,
    "total": 343.38
  },
  "condiciones": {
    "validez": "15 días",
    "tiempo_entrega": "Inmediata"
  }
}
```

### 2.2 Estructura para PROYECTOS PMI (`proyecto_complejo`)

```json
{
  "fases": [
    {
      "nombre": "Fase 1: Ingeniería",
      "duracion_dias": 10,
      "responsable": "Ing. Residente"
    }
  ],
  "riesgos": [
    {
      "riesgo": "Demora en aduanas",
      "impacto": "Alto",
      "mitigacion": "Comprar localmente si demora > 5 días"
    }
  ],
  "raci": {
    "Gerente": ["A", "I"],
    "Técnico": ["R", "C"]
  }
}
```

---
*Arquitectura de Datos - GatoMichuy*
