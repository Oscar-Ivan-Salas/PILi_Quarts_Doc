# 🔧 Solución: Problemas de Codificación UTF-8 en Vista Previa

## 🐛 Problema Detectado

Los caracteres especiales del español (á, é, í, ó, ú, ñ) aparecen como símbolos ilegibles en la vista previa HTML:
- "CÓDIGO" aparece como "CÓDIGO"
- "Duración" aparece con caracteres extraños
- "Instalación Eléctrica" se muestra mal codificado

![Problema de Encoding](file:///C:/Users/USUARIO/.gemini/antigravity/brain/e49dd4cc-507e-428d-8803-bba3270b39d6/uploaded_image_1766519987902.png)

---

## 🔍 Causa Raíz

El problema es un **doble encoding UTF-8**:
1. ✅ El HTML generado en Python tiene `<meta charset="UTF-8">` correcto
2. ✅ FastAPI envía el JSON con UTF-8 correcto
3. ❌ **El frontend está interpretando el HTML con encoding incorrecto**

---

## ✅ Soluciones

### **Solución 1: Verificar cómo se renderiza el HTML en React**

El frontend debe usar uno de estos métodos para renderizar el HTML:

#### **Opción A: Usando iframe con srcdoc**
```javascript
<iframe
  srcDoc={htmlContent}
  style={{ width: '100%', height: '800px', border: 'none' }}
  title="Vista Previa"
/>
```

#### **Opción B: Usando dangerouslySetInnerHTML**
```javascript
<div 
  dangerouslySetInnerHTML={{ __html: htmlContent }}
  style={{ width: '100%' }}
/>
```

#### **Opción C: Usando Blob URL (RECOMENDADO)**
```javascript
const blob = new Blob([htmlContent], { type: 'text/html; charset=utf-8' });
const url = URL.createObjectURL(blob);

<iframe
  src={url}
  style={{ width: '100%', height: '800px', border: 'none' }}
  title="Vista Previa"
/>
```

---

### **Solución 2: Asegurar que el backend envíe el Content-Type correcto**

En `chat.py`, cuando se retorna el HTML, asegurarse de que FastAPI use UTF-8:

```python
from fastapi.responses import JSONResponse

# En lugar de retornar directamente el dict:
return {
    "html_preview": html_preview,
    ...
}

# Usar JSONResponse explícito:
return JSONResponse(
    content={
        "html_preview": html_preview,
        ...
    },
    media_type="application/json; charset=utf-8"
)
```

---

### **Solución 3: Agregar BOM UTF-8 al HTML generado**

Modificar las funciones de preview en `chat.py` para agregar el BOM UTF-8:

```python
def generar_preview_proyecto_complejo_pmi_editable(datos: Dict[str, Any], agente: str) -> str:
    # Agregar BOM UTF-8 al inicio
    html = "\ufeff"  # BOM UTF-8
    
    html += f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <title>Proyecto Complejo PMI - {agente}</title>
    ...
```

---

### **Solución 4: Verificar que el archivo Python use UTF-8**

Agregar al inicio de `chat.py`:

```python
# -*- coding: utf-8 -*-
```

---

## 🎯 Solución Recomendada (Paso a Paso)

### **Paso 1: Modificar el Backend**

Editar `e:\TESLA_COTIZADOR-V3.0\backend\app\routers\chat.py`:

1. Agregar al inicio del archivo:
```python
# -*- coding: utf-8 -*-
```

2. En las funciones de preview (líneas 1774, 1477, 3573, 3957), agregar BOM y meta http-equiv:

```python
html = "\ufeff"  # BOM UTF-8
html += f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    ...
```

### **Paso 2: Modificar el Frontend**

Buscar el componente que renderiza la vista previa (probablemente en `VistaPreviaProfesional.jsx` o similar) y usar el método Blob URL:

```javascript
import React, { useEffect, useState } from 'react';

function VistaPrevia({ htmlContent }) {
    const [iframeUrl, setIframeUrl] = useState('');

    useEffect(() => {
        if (htmlContent) {
            // Crear Blob con encoding UTF-8 explícito
            const blob = new Blob([htmlContent], { 
                type: 'text/html; charset=utf-8' 
            });
            const url = URL.createObjectURL(blob);
            setIframeUrl(url);

            // Cleanup
            return () => URL.revokeObjectURL(url);
        }
    }, [htmlContent]);

    return (
        <iframe
            src={iframeUrl}
            style={{ width: '100%', height: '800px', border: 'none' }}
            title="Vista Previa Documento"
        />
    );
}
```

---

## 🧪 Verificación

Después de aplicar las soluciones:

1. ✅ Verificar que "CÓDIGO" se muestre correctamente
2. ✅ Verificar que "Duración" se muestre correctamente
3. ✅ Verificar que "Instalación Eléctrica" se muestre correctamente
4. ✅ Probar con todos los 6 tipos de documentos

---

## 📝 Archivos a Modificar

1. **Backend:**
   - `e:\TESLA_COTIZADOR-V3.0\backend\app\routers\chat.py`
     - Línea 1774: `generar_preview_proyecto_complejo_pmi_editable`
     - Línea 1477: `generar_preview_proyecto_simple_editable`
     - Línea 3573: `generar_preview_informe_tecnico_editable`
     - Línea 3957: `generar_preview_informe_ejecutivo_apa_editable`

2. **Frontend:**
   - Buscar el componente que renderiza `htmlContent` o `html_preview`
   - Probablemente en `src/components/` o `src/pages/`

---

## 🔍 Debugging

Si el problema persiste, verificar:

1. **En el navegador:**
   - Abrir DevTools → Network → Ver el response del endpoint
   - Verificar que el Content-Type sea `application/json; charset=utf-8`
   - Copiar el HTML del response y pegarlo en un archivo .html
   - Abrir el archivo .html directamente en el navegador

2. **En Python:**
   ```python
   # Agregar logging para debug
   logger.info(f"HTML encoding: {html.encode('utf-8')[:100]}")
   ```

3. **En React:**
   ```javascript
   console.log('HTML recibido:', htmlContent.substring(0, 200));
   console.log('Encoding detectado:', new TextEncoder().encode(htmlContent).slice(0, 50));
   ```

---

## 🎯 Conclusión

El problema es que el HTML está siendo interpretado con el encoding incorrecto en el frontend. La solución más robusta es usar **Blob URL con charset UTF-8 explícito** en el componente React que renderiza la vista previa.
