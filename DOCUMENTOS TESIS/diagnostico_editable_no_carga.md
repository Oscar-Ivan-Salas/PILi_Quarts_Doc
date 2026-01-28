# 🔍 DIAGNÓSTICO: EDITABLE Component No Se Carga

## 🚨 PROBLEMA REPORTADO

Usuario ha:
- ✅ Reiniciado backend
- ✅ Reiniciado frontend  
- ✅ Limpiado caché del navegador
- ✅ Recargado la aplicación

**Pero**: Vista previa sigue mostrando HTML inline antiguo, NO `EDITABLE_COTIZACION_COMPLEJA`

![Pantalla Actual](file:///C:/Users/USUARIO/.gemini/antigravity/brain/e49dd4cc-507e-428d-8803-bba3270b39d6/uploaded_image_1766502377444.png)

---

## ✅ VERIFICACIONES REALIZADAS

### 1. Código Está Correcto

```javascript
// VistaPreviaProfesional.jsx línea 5
import EDITABLE_COTIZACION_COMPLEJA from './EDITABLE_COTIZACION_COMPLEJA'; ✅

// VistaPreviaProfesional.jsx líneas 507-519
const renderDocumentoEditable = () => {
  if (tipoDocumento === 'cotizacion-compleja' || tipoDocumento === 'cotizacion') { ✅
    return (
      <EDITABLE_COTIZACION_COMPLEJA
        datos={cotizacionEditable}
        esquemaColores={esquemaColores}
        logoBase64={logoBase64}
        fuenteDocumento={fuenteDocumento}
        onDatosChange={handleDatosChange}
      />
    );
  }
  return null;
};
```

**Conclusión**: El código está bien guardado.

---

## 🔍 POSIBLES CAUSAS

### Causa 1: Import No Funciona

**Síntoma**: Error en consola del navegador
**Verificar**: Abrir DevTools → Console → Buscar errores

**Posibles errores**:
```
Module not found: Can't resolve './EDITABLE_COTIZACION_COMPLEJA'
SyntaxError in EDITABLE_COTIZACION_COMPLEJA.jsx
```

**Solución**: Verificar que archivo existe y no tiene errores de sintaxis

---

### Causa 2: Condicional No Se Cumple

**Síntoma**: No hay errores, pero componente no se renderiza
**Verificar**: Valor de `tipoDocumento`

**Debug en navegador**:
```javascript
// Abrir DevTools → Console → Ejecutar:
console.log('tipoDocumento:', tipoDocumento);
// Debe mostrar: 'cotizacion' o 'cotizacion-compleja'
```

**Si muestra otro valor**: La condición no se cumple

---

### Causa 3: React Build Cache

**Síntoma**: Cambios no se reflejan
**Verificar**: Build de React no detectó cambios

**Solución**:
```bash
# Detener frontend (Ctrl+C)
# Eliminar cache
rm -rf node_modules/.cache
# Reiniciar
npm start
```

---

### Causa 4: Componente Se Renderiza Pero No Es Visible

**Síntoma**: Componente existe en DOM pero no se ve
**Verificar**: Inspeccionar elemento en navegador

**Debug**:
1. Click derecho en vista previa → Inspeccionar
2. Buscar en HTML: `EDITABLE_COTIZACION_COMPLEJA`
3. Si existe pero no se ve → Problema de CSS

---

## 🧪 PASOS DE DEBUGGING

### Paso 1: Verificar Consola del Navegador

```
1. Abrir aplicación
2. F12 (DevTools)
3. Tab "Console"
4. Buscar errores en rojo
5. Copiar errores si existen
```

**Errores comunes**:
- `Module not found` → Archivo no existe o ruta incorrecta
- `SyntaxError` → Error de sintaxis en componente
- `undefined is not an object` → Props incorrectos

---

### Paso 2: Agregar Console.log Temporal

**Modificar VistaPreviaProfesional.jsx**:

```javascript
const renderDocumentoEditable = () => {
  console.log('🔍 DEBUG renderDocumentoEditable');
  console.log('tipoDocumento:', tipoDocumento);
  console.log('cotizacionEditable:', cotizacionEditable);
  
  if (tipoDocumento === 'cotizacion-compleja' || tipoDocumento === 'cotizacion') {
    console.log('✅ CONDICIÓN SE CUMPLE - Renderizando EDITABLE');
    return (
      <EDITABLE_COTIZACION_COMPLEJA
        datos={cotizacionEditable}
        esquemaColores={esquemaColores}
        logoBase64={logoBase64}
        fuenteDocumento={fuenteDocumento}
        onDatosChange={handleDatosChange}
      />
    );
  }
  
  console.log('❌ CONDICIÓN NO SE CUMPLE - Usando HTML inline');
  return null;
};
```

**Verificar en consola**:
- Si NO aparece "🔍 DEBUG" → Función no se ejecuta
- Si aparece "❌ CONDICIÓN NO SE CUMPLE" → `tipoDocumento` tiene valor incorrecto
- Si aparece "✅ CONDICIÓN SE CUMPLE" → Componente se está renderizando

---

### Paso 3: Verificar Renderizado en JSX

**Buscar en VistaPreviaProfesional.jsx** (línea ~590):

```javascript
<div className="cotizacion-profesional" ref={documentoRef}>
  {renderDocumentoEditable() || (
    <>
      {/* HTML inline antiguo */}
    </>
  )}
</div>
```

**Agregar debug**:

```javascript
<div className="cotizacion-profesional" ref={documentoRef}>
  {(() => {
    const editable = renderDocumentoEditable();
    console.log('🎨 Componente EDITABLE:', editable);
    return editable || (
      <>
        {console.log('📄 Usando HTML inline')}
        {/* HTML inline antiguo */}
      </>
    );
  })()}
</div>
```

---

### Paso 4: Verificar Import del Componente

**Agregar al inicio de VistaPreviaProfesional.jsx**:

```javascript
import EDITABLE_COTIZACION_COMPLEJA from './EDITABLE_COTIZACION_COMPLEJA';

console.log('📦 EDITABLE_COTIZACION_COMPLEJA importado:', EDITABLE_COTIZACION_COMPLEJA);
// Debe mostrar: [Function] o similar
// Si muestra undefined → Import falló
```

---

## 🔧 SOLUCIONES SEGÚN CAUSA

### Si: "Module not found"

```bash
# Verificar que archivo existe
ls frontend/src/components/EDITABLE_COTIZACION_COMPLEJA.jsx

# Si no existe, verificar nombre exacto
ls frontend/src/components/ | grep EDITABLE
```

---

### Si: tipoDocumento tiene valor incorrecto

**Opción A**: Forzar valor en App.jsx

```javascript
// App.jsx línea ~1959
<VistaPreviaProfesional
  tipoDocumento="cotizacion"  // ← Forzar valor
  ...
/>
```

**Opción B**: Ampliar condición

```javascript
// VistaPreviaProfesional.jsx
if (
  tipoDocumento === 'cotizacion-compleja' || 
  tipoDocumento === 'cotizacion' ||
  tipoDocumento.includes('cotizacion')  // ← Más permisivo
) {
  return <EDITABLE_COTIZACION_COMPLEJA ... />;
}
```

---

### Si: Build cache no se limpia

```bash
# Opción 1: Limpiar cache manualmente
cd frontend
rm -rf node_modules/.cache
rm -rf build
npm start

# Opción 2: Forzar rebuild
npm run build
npm start

# Opción 3: Reinstalar dependencias
rm -rf node_modules
npm install
npm start
```

---

### Si: Componente se renderiza pero no se ve

**Verificar CSS**:

```javascript
// Agregar estilo inline temporal
<EDITABLE_COTIZACION_COMPLEJA
  datos={cotizacionEditable}
  esquemaColores={esquemaColores}
  logoBase64={logoBase64}
  fuenteDocumento={fuenteDocumento}
  onDatosChange={handleDatosChange}
  style={{ border: '5px solid red', padding: '20px' }}  // ← Debug visual
/>
```

---

## 📋 CHECKLIST DE VERIFICACIÓN

### Antes de Continuar

- [ ] ¿Hay errores en consola del navegador?
- [ ] ¿Qué valor tiene `tipoDocumento`?
- [ ] ¿Se ejecuta `renderDocumentoEditable()`?
- [ ] ¿Se cumple la condición del if?
- [ ] ¿El componente EDITABLE está importado correctamente?
- [ ] ¿El archivo EDITABLE_COTIZACION_COMPLEJA.jsx existe?
- [ ] ¿React detectó los cambios? (verificar timestamp en terminal)

---

## 🚀 ACCIÓN INMEDIATA RECOMENDADA

### Opción 1: Verificar Consola (MÁS RÁPIDO)

```
1. Abrir aplicación en navegador
2. F12 → Console
3. Buscar errores
4. Reportar lo que dice
```

### Opción 2: Agregar Logs de Debug

```javascript
// En VistaPreviaProfesional.jsx, línea 507
const renderDocumentoEditable = () => {
  console.log('DEBUG:', {
    tipoDocumento,
    cumpleCondicion: tipoDocumento === 'cotizacion-compleja' || tipoDocumento === 'cotizacion',
    componenteImportado: !!EDITABLE_COTIZACION_COMPLEJA
  });
  
  // ... resto del código
};
```

### Opción 3: Forzar Renderizado (TEMPORAL)

```javascript
// Comentar condicional temporalmente
const renderDocumentoEditable = () => {
  // SIEMPRE renderizar EDITABLE (solo para debug)
  return (
    <EDITABLE_COTIZACION_COMPLEJA
      datos={cotizacionEditable}
      esquemaColores={esquemaColores}
      logoBase64={logoBase64}
      fuenteDocumento={fuenteDocumento}
      onDatosChange={handleDatosChange}
    />
  );
};
```

Si esto funciona → Problema es la condición
Si esto NO funciona → Problema es el import o el componente

---

## 📊 INFORMACIÓN NECESARIA

Para diagnosticar correctamente, necesito saber:

1. **¿Hay errores en consola del navegador?**
   - Sí/No
   - Si sí, ¿cuál es el error exacto?

2. **¿Qué valor tiene `tipoDocumento`?**
   - Agregar `console.log('tipoDocumento:', tipoDocumento)` y reportar

3. **¿React detectó los cambios?**
   - Verificar en terminal de frontend si dice "Compiled successfully"

4. **¿El archivo EDITABLE_COTIZACION_COMPLEJA.jsx existe?**
   - Verificar ruta: `frontend/src/components/EDITABLE_COTIZACION_COMPLEJA.jsx`

---

**Preparado por**: Antigravity AI  
**Fecha**: 2025-12-23  
**Tipo**: Guía de Diagnóstico  
**Estado**: ⏳ **ESPERANDO INFORMACIÓN DEL USUARIO**
