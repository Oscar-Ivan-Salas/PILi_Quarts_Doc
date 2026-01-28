# 🔄 Instrucciones para Reiniciar Todo

**Fecha**: 21 de Diciembre, 2025 - 01:02 AM  
**Objetivo**: Limpiar caché y reiniciar servidores para aplicar cambios

---

## 📋 PASOS A SEGUIR

### 1. Detener Todos los Servidores

**En la terminal de backend**:
```powershell
# Presiona Ctrl+C para detener uvicorn
```

**En la terminal de frontend**:
```powershell
# Presiona Ctrl+C para detener npm
```

### 2. Limpiar Caché del Navegador

**Opción A - Chrome/Edge** (Recomendado):
1. Presiona `Ctrl + Shift + Delete`
2. Selecciona "Imágenes y archivos en caché"
3. Rango: "Última hora"
4. Clic "Borrar datos"

**Opción B - Modo Incógnito**:
1. Presiona `Ctrl + Shift + N`
2. Abre `http://localhost:3000`

**Opción C - Hard Refresh**:
1. En la página, presiona `Ctrl + Shift + R`

### 3. Limpiar Caché de npm (Opcional)

```powershell
cd frontend
npm cache clean --force
```

### 4. Reiniciar Backend

```powershell
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Verificar**: Deberías ver:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

### 5. Reiniciar Frontend

**En otra terminal**:
```powershell
cd frontend
npm start
```

**Verificar**: Deberías ver:
```
Compiled successfully!
```

### 6. Probar Endpoint de Templates

**En otra terminal**:
```powershell
curl http://localhost:8000/api/templates/cotizacion-simple
```

**Resultado esperado**: JSON con HTML largo (15KB+)

### 7. Abrir Navegador Limpio

1. Abre navegador en modo incógnito (`Ctrl + Shift + N`)
2. Ve a `http://localhost:3000`
3. Abre consola del navegador (`F12`)
4. Ve a la pestaña "Network"

### 8. Generar Cotización

1. Inicia chat con PILI
2. Escribe: "Necesito una cotización para instalación eléctrica"
3. **Observa en Network**: Debería aparecer request a `/api/templates/cotizacion-simple`
4. **Observa en Console**: No debería haber errores rojos

---

## 🔍 VERIFICACIÓN

### En la Consola del Navegador (F12):

**Busca**:
- ✅ Request a `/api/templates/cotizacion-simple` (status 200)
- ✅ Response con HTML largo
- ❌ NO debe haber errores "Failed to fetch"
- ❌ NO debe haber errores "404 Not Found"

### En la Vista Previa:

**Deberías ver**:
- ✅ Diseño profesional con colores Tesla
- ✅ Tabla con bordes y estilos
- ✅ Header con logo/título
- ❌ NO el HTML básico simple

---

## 🐛 SI AÚN NO FUNCIONA

### Debug Paso a Paso:

1. **Verificar que el endpoint responde**:
```powershell
curl http://localhost:8000/api/templates/cotizacion-simple
```

Si da error 404:
- El backend no tiene el endpoint
- Revisar que `main.py` tenga el código del endpoint

2. **Verificar en consola del navegador**:
```javascript
fetch('/api/templates/cotizacion-simple')
  .then(r => r.json())
  .then(d => console.log(d.html.length))
```

Debería mostrar un número grande (15000+)

3. **Verificar que las funciones son async**:
En consola del navegador:
```javascript
// Debería mostrar "AsyncFunction"
console.log(generarHTMLCotizacion.constructor.name)
```

---

## 📸 CAPTURA DE PANTALLA

**Antes de reiniciar**: Toma screenshot del HTML actual  
**Después de reiniciar**: Toma screenshot del nuevo HTML  
**Compara**: Deberían verse diferentes

---

**Preparado por**: Senior Coordinator  
**Estado**: Listo para reiniciar  
**Tiempo estimado**: 5 minutos
