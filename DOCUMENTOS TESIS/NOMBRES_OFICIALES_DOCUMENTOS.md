# 📋 NOMBRES REALES DE DOCUMENTOS - PROYECTO TESLA COTIZADOR V3.0

**Fecha:** 2026-01-01  
**Fuente:** Código existente en `App.jsx` líneas 1377-1382

---

## ✅ 6 TIPOS DE DOCUMENTOS (NOMBRES OFICIALES)

### Según el código existente:

```javascript
const configuracion = {
  'cotizacion-simple': { 
    titulo: '⚡ Cotización Simple', 
    desc: 'Vista previa en tiempo real - 5 a 15 minutos', 
    icon: Zap 
  },
  'cotizacion-compleja': { 
    titulo: '📄 Cotización Compleja', 
    desc: 'Análisis detallado con edición avanzada', 
    icon: Layers 
  },
  'proyecto-simple': { 
    titulo: '📁 Proyecto Simple', 
    desc: 'Gestión básica con vista previa', 
    icon: Folder 
  },
  'proyecto-complejo': { 
    titulo: '🏗️ Proyecto Complejo', 
    desc: 'Gantt, hitos y seguimiento avanzado', 
    icon: Layout 
  },
  'informe-simple': { 
    titulo: '📄 Informe Simple', 
    desc: 'PDF básico con vista previa editable', 
    icon: FileText 
  },
  'informe-ejecutivo': { 
    titulo: '📊 Informe Ejecutivo', 
    desc: 'Word APA, tablas y gráficos automáticos', 
    icon: BarChart3 
  }
};
```

---

## 📊 NOMBRES CORRECTOS PARA ARQUITECTURA

### IDs de Documentos (para código):

1. `cotizacion-simple`
2. `cotizacion-compleja`  
3. `proyecto-simple`
4. `proyecto-complejo`
5. `informe-simple`
6. `informe-ejecutivo` ⚠️ **NO "informe-complejo"**

---

## 🏗️ ARQUITECTURA CORREGIDA

```
Pili_ChatBot/
├── core/
│   ├── base_service.py
│   ├── base_document.py
│   ├── service_registry.py
│   └── document_registry.py
│
├── services/                    ← 10 SERVICIOS
│   ├── itse.py
│   ├── puesta_tierra.py
│   ├── instalaciones.py
│   ├── mantenimiento.py
│   ├── proyectos.py
│   ├── consultoria.py
│   ├── capacitacion.py
│   ├── auditoria.py
│   ├── emergencias.py
│   └── soporte.py
│
└── documents/                   ← 6 DOCUMENTOS (NOMBRES REALES)
    ├── cotizacion_simple.py     
    ├── cotizacion_compleja.py
    ├── proyecto_simple.py
    ├── proyecto_complejo.py
    ├── informe_simple.py
    └── informe_ejecutivo.py     ⚠️ EJECUTIVO, no "complejo"
```

---

## 📋 MATRIZ REAL CORREGIDA

```
                           SERVICIOS (10)
                           ↓
DOCUMENTOS (6)         │ ITSE │ Tierra │ Inst │ Mant │ Proy │ Cons │ Cap │ Aud │ Emer │ Sop │
───────────────────────┼──────┼────────┼──────┼──────┼──────┼──────┼─────┼─────┼──────┼─────┤
1. cotizacion-simple   │  ✅  │   ❌   │  ❌  │  ❌  │  ❌  │  ❌  │ ❌  │ ❌  │  ❌  │ ❌  │
2. cotizacion-compleja │  ❌  │   ❌   │  ❌  │  ❌  │  ❌  │  ❌  │ ❌  │ ❌  │  ❌  │ ❌  │
3. proyecto-simple     │  ❌  │   ❌   │  ❌  │  ❌  │  ❌  │  ❌  │ ❌  │ ❌  │  ❌  │ ❌  │
4. proyecto-complejo   │  ❌  │   ❌   │  ❌  │  ❌  │  ❌  │  ❌  │ ❌  │ ❌  │  ❌  │ ❌  │
5. informe-simple      │  ❌  │   ❌   │  ❌  │  ❌  │  ❌  │  ❌  │ ❌  │ ❌  │  ❌  │ ❌  │
6. informe-ejecutivo   │  ❌  │   ❌   │  ❌  │  ❌  │  ❌  │  ❌  │ ❌  │ ❌  │  ❌  │ ❌  │
```

---

## ⚠️ CORRECCIONES IMPORTANTES

### Lo que dije antes (INCORRECTO):
- ❌ "Informe Complejo"

### Lo que es REALMENTE (CORRECTO):
- ✅ "Informe Ejecutivo"

---

## 🎯 ESTADO ACTUAL DEL PROYECTO

### Implementado:
- ✅ `cotizacion-simple` + ITSE (parcial)

### Pendiente:
- ❌ 59 combinaciones restantes

### Servicios en código:
```javascript
const servicios = [
  { id: 'electricidad', nombre: '⚡ Electricidad' },
  { id: 'itse', nombre: '📋 Certificado ITSE' },
  { id: 'puesta-tierra', nombre: '🔌 Puesta a Tierra' },
  { id: 'contra-incendios', nombre: '🔥 Contra Incendios' },
  { id: 'domotica', nombre: '🏠 Domótica' },
  { id: 'cctv', nombre: '📹 CCTV' },
  { id: 'redes', nombre: '🌐 Redes' },
  { id: 'automatizacion-industrial', nombre: '⚙️ Automatización Industrial' },
  { id: 'expedientes', nombre: '📄 Expedientes Técnicos' },
  { id: 'saneamiento', nombre: '💧 Saneamiento' }
];
```

---

## ✅ CONFIRMACIÓN FINAL

**Nombres oficiales para implementación:**

1. `cotizacion-simple`
2. `cotizacion-compleja`
3. `proyecto-simple`
4. `proyecto-complejo`
5. `informe-simple`
6. `informe-ejecutivo` ← **EJECUTIVO**

**NO crear archivos con otros nombres.**

---

**Archivo:** `NOMBRES_OFICIALES_DOCUMENTOS.md`  
**Estado:** Verificado contra código existente  
**Fuente:** `App.jsx` líneas 1377-1382
