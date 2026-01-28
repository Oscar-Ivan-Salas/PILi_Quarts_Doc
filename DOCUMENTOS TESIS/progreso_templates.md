# 📊 Progreso: Integración de Plantillas HTML

**Fecha**: 21 de Diciembre, 2025 - 00:35 AM  
**Estado**: ✅ Fase 1 Completada - Listo para Fase 2

---

## ✅ COMPLETADO (Fase 1)

### 1. Plantillas HTML Copiadas
**Ubicación**: `backend/app/templates/documentos/`

✅ Archivos verificados:
- `PLANTILLA_HTML_COTIZACION_SIMPLE.html` (15 KB)
- `PLANTILLA_HTML_COTIZACION_COMPLEJA.html` (22 KB)
- `PLANTILLA_HTML_PROYECTO_SIMPLE.html` (21 KB)
- `PLANTILLA_HTML_PROYECTO_COMPLEJO_PMI.html` (26 KB)
- `PLANTILLA_HTML_INFORME_TECNICO.html` (20 KB)
- `PLANTILLA_HTML_INFORME_EJECUTIVO_APA.html` (26 KB)

**Total**: 6 plantillas profesionales listas

### 2. Endpoint API Creado
**Archivo**: `backend/app/main.py` (líneas 872-910)

✅ Endpoint: `GET /api/templates/{tipo}`

**Funcionalidad**:
- Sirve plantillas HTML al frontend
- Mapea 6 tipos de documentos
- Retorna JSON con contenido HTML
- Manejo de errores completo

**Tipos soportados**:
- `cotizacion-simple`
- `cotizacion-compleja`
- `proyecto-simple`
- `proyecto-pmi`
- `informe-tecnico`
- `informe-ejecutivo`

**Ejemplo de uso**:
```javascript
const response = await fetch('/api/templates/cotizacion-simple');
const data = await response.json();
const html = data.html; // Contenido HTML completo
```

---

## 🔄 PENDIENTE (Fase 2)

### 1. Modificar App.jsx

**Archivo**: `frontend/src/App.jsx`

**Funciones a modificar** (3):

#### A) `generarHTMLCotizacion` (líneas 604-664)
**Cambio**: De generar HTML con template strings → Cargar plantilla

**Código actual**:
```javascript
const generarHTMLCotizacion = (datos) => {
  return `<div style="...">...</div>`; // HTML hardcodeado
};
```

**Código nuevo**:
```javascript
const generarHTMLCotizacion = async (datos) => {
  // 1. Cargar plantilla
  const response = await fetch('/api/templates/cotizacion-simple');
  const { html } = await response.json();
  
  // 2. Calcular totales
  const totales = calcularTotales(datos?.items || []);
  
  // 3. Reemplazar variables
  let htmlFinal = html
    .replace(/\{\{CLIENTE_NOMBRE\}\}/g, datos.cliente || 'Cliente')
    .replace(/\{\{NUMERO_COTIZACION\}\}/g, datos.numero || 'COT-001')
    .replace(/\{\{FECHA_COTIZACION\}\}/g, new Date().toLocaleDateString())
    .replace(/\{\{SUBTOTAL\}\}/g, totales.subtotal)
    .replace(/\{\{IGV\}\}/g, totales.igv)
    .replace(/\{\{TOTAL\}\}/g, totales.total);
  
  // 4. Aplicar colores personalizados
  htmlFinal = aplicarColores(htmlFinal, esquemaColorActual);
  
  return htmlFinal;
};
```

#### B) `generarHTMLProyecto` (líneas 666-691)
**Cambio**: Similar a cotización

```javascript
const generarHTMLProyecto = async (datos) => {
  const response = await fetch('/api/templates/proyecto-simple');
  const { html } = await response.json();
  
  let htmlFinal = html
    .replace(/\{\{NOMBRE_PROYECTO\}\}/g, nombreProyecto)
    .replace(/\{\{CLIENTE\}\}/g, clienteProyecto)
    .replace(/\{\{PRESUPUESTO\}\}/g, presupuestoEstimado);
  
  htmlFinal = aplicarColores(htmlFinal, esquemaColorActual);
  return htmlFinal;
};
```

#### C) `generarHTMLInforme` (líneas 693-717)
**Cambio**: Similar a cotización

```javascript
const generarHTMLInforme = async (datos) => {
  const tipo = tipoFlujo.includes('ejecutivo') ? 'informe-ejecutivo' : 'informe-tecnico';
  const response = await fetch(`/api/templates/${tipo}`);
  const { html } = await response.json();
  
  let htmlFinal = html
    .replace(/\{\{TITULO_INFORME\}\}/g, proyectosMock.find(p => p.id === proyectoSeleccionado)?.nombre || 'General')
    .replace(/\{\{FECHA\}\}/g, new Date().toLocaleDateString());
  
  htmlFinal = aplicarColores(htmlFinal, esquemaColorActual);
  return htmlFinal;
};
```

### 2. Crear Función Auxiliar

**Agregar en App.jsx**:

```javascript
const aplicarColores = (html, esquema) => {
  const ESQUEMAS = {
    'azul': { p: '#0052A3', s: '#1E40AF', a: '#3B82F6' },
    'rojo': { p: '#8B0000', s: '#991B1B', a: '#DC2626' },
    'verde': { p: '#065F46', s: '#047857', a: '#10B981' },
    'dorado': { p: '#D4AF37', s: '#B8860B', a: '#FFD700' },
  };
  
  const c = ESQUEMAS[esquema] || ESQUEMAS.azul;
  
  return html
    .replace(/#0052A3/g, c.p)
    .replace(/#1E40AF/g, c.s)
    .replace(/#3B82F6/g, c.a);
};
```

### 3. Actualizar Llamadas

**Cambiar de**:
```javascript
const html = generarHTMLCotizacion(datos);
```

**A**:
```javascript
const html = await generarHTMLCotizacion(datos);
```

**Ubicaciones a actualizar**:
- Donde se llama `generarHTMLCotizacion`
- Donde se llama `generarHTMLProyecto`
- Donde se llama `generarHTMLInforme`

---

## 🧪 TESTING

### Checklist de Pruebas

#### Frontend
- [ ] Cargar cotización simple → Ver plantilla profesional
- [ ] Cambiar colores → Colores se aplican
- [ ] Editar tabla → Funciona correctamente
- [ ] Vista final → Se ve correcta
- [ ] Generar Word → Funciona

#### Backend
- [ ] Endpoint `/api/templates/cotizacion-simple` → Retorna HTML
- [ ] Endpoint `/api/templates/proyecto-pmi` → Retorna HTML
- [ ] Endpoint `/api/templates/informe-tecnico` → Retorna HTML
- [ ] Error 404 para tipo inválido

#### Integración
- [ ] PILI → Vista previa con plantilla
- [ ] Edición → Mantiene plantilla
- [ ] Finalizar → Vista final correcta
- [ ] Generar Word → Documento correcto
- [ ] Los 6 tipos funcionan

---

## ⏱️ TIEMPO ESTIMADO RESTANTE

- **Modificar App.jsx**: 1-2 horas
- **Testing**: 1 hora
- **Ajustes**: 30 min

**Total**: 2.5-3.5 horas

---

## 📝 NOTAS IMPORTANTES

### Cambios Críticos
1. **Funciones ahora son async**: Usar `await` al llamarlas
2. **Colores dinámicos**: Aplicar después de cargar plantilla
3. **Variables**: Reemplazar `{{VARIABLE}}` con datos reales

### Mantener Funcionalidad
✅ Personalización de colores (4 esquemas)  
✅ Tabla editable  
✅ Cálculo de totales  
✅ Opciones (ocultar IGV, precios unitarios)  
✅ Generación Word/PDF  

### Rollback
Si algo falla:
```bash
git checkout HEAD -- backend/app/main.py
git checkout HEAD -- frontend/src/App.jsx
```

---

## 🚀 PRÓXIMOS PASOS (Mañana)

1. **Modificar las 3 funciones** en App.jsx
2. **Crear función `aplicarColores`**
3. **Actualizar llamadas** a funciones (agregar `await`)
4. **Probar** con cotización simple
5. **Probar** los 6 tipos
6. **Commit** final

---

## 📊 PROGRESO GENERAL

```
Fase 1: Preparación          ✅ 100% COMPLETADO
├─ Copiar plantillas HTML     ✅
├─ Crear endpoint API         ✅
└─ Verificar archivos         ✅

Fase 2: Integración Frontend  ⏳ 0% PENDIENTE
├─ Modificar App.jsx          ⏳
├─ Función aplicarColores     ⏳
└─ Actualizar llamadas        ⏳

Fase 3: Testing               ⏳ 0% PENDIENTE
├─ Probar 6 tipos             ⏳
├─ Verificar colores          ⏳
└─ Generar Word/PDF           ⏳
```

**Progreso Total**: 33% (1/3 fases)

---

**Preparado por**: Senior Coordinator  
**Estado**: ✅ Listo para continuar mañana  
**Próxima sesión**: Modificar App.jsx y testing
