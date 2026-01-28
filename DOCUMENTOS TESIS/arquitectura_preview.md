# 🔍 Arquitectura Actual de Vista Previa

**Fecha**: 21 de Diciembre, 2025 - 06:12 AM

---

## 📐 CÓMO FUNCIONA ACTUALMENTE

### Archivo 1: `App.jsx`
**Contiene**: 3 funciones de generación HTML

```javascript
// Líneas 604-649
const generarHTMLCotizacion = async (datos) => {
  // Carga plantilla desde /api/templates/cotizacion-simple
  // Reemplaza variables {{CLIENTE_NOMBRE}}, etc.
  // Retorna: string HTML
}

// Líneas 651-689  
const generarHTMLProyecto = async (datos) => {
  // Similar para proyectos
}

// Líneas 692-737
const generarHTMLInforme = async (datos) => {
  // Similar para informes
}
```

**Problema**: Estas funciones generan HTML pero **NO se usan para la vista previa**

### Archivo 2: `VistaPrevia.jsx`
**Contiene**: Componente React que muestra la vista previa

```jsx
// Líneas 1-397
const VistaPrevia = ({ cotizacion, proyecto, informe, ... }) => {
  // Renderiza tabla editable con React
  // NO usa el HTML generado por App.jsx
  // Usa componentes React directamente
  
  return (
    <div className="bg-gradient-to-br from-gray-900 to-black">
      {/* Tabla editable */}
      {/* Totales */}
      {/* Botones */}
    </div>
  );
}
```

**Problema**: Usa diseño básico con Tailwind, no las plantillas profesionales

---

## 🔄 FLUJO ACTUAL (Lo Que Pasa Ahora)

### 1. Usuario habla con PILI
```
Usuario: "Necesito una cotización"
```

### 2. PILI genera datos
```javascript
datos = {
  cliente: "Minel",
  items: [...]
}
```

### 3. App.jsx intenta generar HTML
```javascript
const html = await generarHTMLCotizacion(datos);
setHtmlPreview(html);
```

### 4. VistaPrevia.jsx recibe datos
```jsx
<VistaPrevia 
  cotizacion={datos}
  htmlPreview={html}  // ⚠️ NO SE USA
/>
```

### 5. VistaPrevia renderiza con React
```jsx
// IGNORA htmlPreview
// Renderiza su propia tabla editable
return <div>...</div>
```

**Resultado**: Se ve el diseño básico de VistaPrevia, NO el HTML profesional

---

## ⚠️ EL PROBLEMA

### Dos Sistemas Separados:

**Sistema 1 - App.jsx** (Generación HTML):
- ✅ Carga plantillas profesionales
- ✅ Reemplaza variables
- ✅ Aplica colores
- ❌ **NO se usa para mostrar**

**Sistema 2 - VistaPrevia.jsx** (Visualización):
- ✅ Muestra tabla editable
- ✅ Permite editar items
- ✅ Recalcula totales
- ❌ **Diseño básico, no profesional**

**Desconexión**: El HTML profesional se genera pero no se muestra

---

## 💡 SOLUCIÓN

### Opción A: Modificar VistaPrevia.jsx (SIMPLE)
**Agregar estilos profesionales directamente al componente React**

```jsx
// VistaPrevia.jsx
const VistaPrevia = ({ ... }) => {
  return (
    <div className="cotizacion-profesional">
      <style>{`
        .cotizacion-profesional {
          max-width: 210mm;
          margin: 0 auto;
          padding: 20mm;
          background: white;
          font-family: Calibri, Arial, sans-serif;
        }
        
        .header-profesional {
          display: flex;
          justify-content: space-between;
          border-bottom: 4px solid #0052A3;
          padding-bottom: 20px;
        }
        
        .tabla-items thead {
          background: linear-gradient(135deg, #0052A3, #1E40AF);
          color: white;
        }
        
        /* ... más estilos de la plantilla HTML */
      `}</style>
      
      {/* Contenido actual editable */}
      <div className="header-profesional">...</div>
      <table className="tabla-items">...</table>
    </div>
  );
}
```

**Ventajas**:
- ✅ Rápido (1 hora)
- ✅ Mantiene funcionalidad editable
- ✅ Diseño profesional
- ✅ Sin problemas de async

### Opción B: Usar HTML generado (COMPLEJO)
**Hacer que VistaPrevia use el HTML de App.jsx**

```jsx
// VistaPrevia.jsx
const VistaPrevia = ({ htmlPreview, ... }) => {
  if (htmlPreview) {
    return (
      <div dangerouslySetInnerHTML={{ __html: htmlPreview }} />
    );
  }
  // ... resto del código
}
```

**Problemas**:
- ❌ Pierde funcionalidad editable
- ❌ Tabla no se puede editar inline
- ❌ Necesita reescribir lógica de edición

---

## 🎯 RECOMENDACIÓN

### Opción A: Modificar VistaPrevia.jsx

**Por qué**:
1. ✅ Mantiene TODO lo que funciona (tabla editable)
2. ✅ Solo agrega estilos profesionales
3. ✅ Rápido de implementar
4. ✅ Sin riesgo de romper funcionalidad

**Resultado**:
- Vista previa con diseño profesional
- Tabla completamente editable
- Totales se recalculan
- **Se ve igual que el Word generado** ✅

---

## 📋 PLAN DE ACCIÓN

### Paso 1: Extraer CSS de Plantilla HTML
```bash
# De: PLANTILLA_HTML_COTIZACION_SIMPLE.html
# Copiar: <style>...</style>
```

### Paso 2: Agregar a VistaPrevia.jsx
```jsx
const estilosProfesionales = `
  /* CSS de la plantilla */
`;

return (
  <div>
    <style>{estilosProfesionales}</style>
    {/* Contenido actual */}
  </div>
);
```

### Paso 3: Ajustar clases CSS
```jsx
// Cambiar:
<div className="bg-gradient-to-br from-gray-900">

// Por:
<div className="cotizacion-profesional">
```

### Paso 4: Probar
- Ver vista previa
- Editar tabla
- Generar Word
- Comparar diseños

**Tiempo total**: 1-2 horas

---

## ✅ CONFIRMACIÓN

**¿Es correcto que?**:
1. ✅ App.jsx tiene las funciones de generación HTML
2. ✅ VistaPrevia.jsx muestra la vista previa
3. ✅ Actualmente NO están conectados
4. ✅ Queremos que VistaPrevia use diseño profesional
5. ✅ Manteniendo funcionalidad editable

**¿Procedemos con Opción A (modificar VistaPrevia.jsx)?**
