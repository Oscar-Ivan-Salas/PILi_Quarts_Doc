# 🎯 Plan de Integración PILI - Frontend

## ✅ Endpoints Existentes (NO crear nuevos)

### 1. `/api/chat/chat-contextualizado` (Principal)
**Ubicación:** `backend/app/routers/chat.py` línea 2762

**Funcionalidad:**
- ✅ Chat inteligente con PILI
- ✅ Fallback automático a PILIBrain si Gemini no disponible
- ✅ Genera datos estructurados
- ✅ Retorna vista previa HTML

**Request:**
```json
{
  "tipo_flujo": "informe-simple",
  "mensaje": "Necesito informe para casa 120m²",
  "historial": [],
  "generar_html": true,
  "datos_cliente": {
    "nombre": "Juan Pérez"
  }
}
```

**Response:**
```json
{
  "success": true,
  "agente_activo": "PILI Reportera",
  "respuesta": "He analizado tu solicitud...",
  "cotizacion_generada": {...},  // Si es cotización
  "proyecto_generado": {...},    // Si es proyecto
  "informe_generado": {...},     // Si es informe
  "html_preview": "<div>...</div>",
  "botones_sugeridos": [...]
}
```

### 2. `/api/chat/pili/generar-json-preview`
**Ubicación:** `backend/app/routers/chat.py` línea 2451

**Funcionalidad:**
- ✅ Genera JSON estructurado
- ✅ Vista previa HTML editable

### 3. `/api/chat/pili/procesar-archivos`
**Ubicación:** `backend/app/routers/chat.py` línea 2294

**Funcionalidad:**
- ✅ Procesar archivos con OCR
- ✅ Extraer datos de planos/fotos

---

## 🔧 Integración Frontend

### **Paso 1: Actualizar ChatIA.jsx**

**Archivo:** `frontend/src/ChatIA.jsx`

**Cambios:**
```javascript
// Llamar a PILI cuando usuario envía mensaje
const handleEnviarMensaje = async (mensaje) => {
  try {
    const response = await fetch('/api/chat/chat-contextualizado', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        tipo_flujo: tipoFlujo,  // 'informe-simple', 'cotizacion-simple', etc.
        mensaje: mensaje,
        historial: historialChat,
        generar_html: true,  // Siempre generar datos
        datos_cliente: datosCliente
      })
    });

    const data = await response.json();

    // Agregar respuesta al chat
    setHistorialChat([...historialChat, {
      role: 'assistant',
      content: data.respuesta,
      agente: data.agente_activo
    }]);

    // ✅ AUTO-RELLENAR DATOS
    if (data.informe_generado) {
      onDatosGenerados(data.informe_generado);
    } else if (data.cotizacion_generada) {
      onDatosGenerados(data.cotizacion_generada);
    } else if (data.proyecto_generado) {
      onDatosGenerados(data.proyecto_generado);
    }

    // Actualizar botones sugeridos
    setBotonesSugeridos(data.botones_sugeridos);

  } catch (error) {
    console.error('Error llamando a PILI:', error);
  }
};
```

### **Paso 2: Actualizar App.jsx**

**Archivo:** `frontend/src/App.jsx`

**Cambios:**
```javascript
// Agregar callback para recibir datos de PILI
const handleDatosGeneradosPILI = (datos) => {
  console.log('📦 Datos recibidos de PILI:', datos);
  
  // Auto-rellenar HTML Editable
  setDatosEditables(datos);
  
  // Mostrar vista previa
  setMostrarVistaPrevia(true);
};

// Pasar callback a ChatIA
<ChatIA
  tipoFlujo={tipoFlujo}
  datosCliente={datosCliente}
  onDatosGenerados={handleDatosGeneradosPILI}
/>
```

### **Paso 3: Mapeo de Datos**

**Problema:** PILI genera datos en un formato, HTML Editables esperan otro

**Solución:** Función de mapeo

```javascript
const mapearDatosPILI = (datosPILI, tipoFlujo) => {
  if (tipoFlujo.includes('informe')) {
    return {
      titulo: datosPILI.titulo || 'Informe Técnico',
      codigo: datosPILI.codigo || `INF-${Date.now()}`,
      cliente: datosPILI.cliente || { nombre: 'Cliente' },
      fecha: datosPILI.fecha || new Date().toLocaleDateString('es-PE'),
      resumen: datosPILI.resumen || '',
      introduccion: datosPILI.introduccion || '',
      analisis_tecnico: datosPILI.analisis_tecnico || '',
      resultados: datosPILI.resultados || '',
      conclusiones: datosPILI.conclusiones || '',
      recomendaciones: datosPILI.recomendaciones || []
    };
  } else if (tipoFlujo.includes('cotizacion')) {
    return {
      numero: datosPILI.numero || `COT-${Date.now()}`,
      cliente: datosPILI.cliente || { nombre: 'Cliente' },
      proyecto: datosPILI.proyecto || '',
      items: datosPILI.items || [],
      subtotal: datosPILI.subtotal || 0,
      igv: datosPILI.igv || 0,
      total: datosPILI.total || 0
    };
  } else if (tipoFlujo.includes('proyecto')) {
    return {
      nombre: datosPILI.nombre_proyecto || 'Proyecto',
      codigo: datosPILI.codigo || `PROY-${Date.now()}`,
      cliente: datosPILI.cliente || { nombre: 'Cliente' },
      presupuesto: datosPILI.total || 0,
      duracion: datosPILI.duracion || '30 días',
      fases: datosPILI.items || []  // Items como fases
    };
  }
};

// Usar en handleDatosGeneradosPILI
const handleDatosGeneradosPILI = (datos) => {
  const datosMapeados = mapearDatosPILI(datos, tipoFlujo);
  setDatosEditables(datosMapeados);
};
```

---

## 🎯 Flujo Completo

```
1. Usuario selecciona "Informe Simple"
   ↓
2. ChatIA muestra interfaz de chat
   ↓
3. Usuario escribe: "Necesito informe para casa 120m²"
   ↓
4. ChatIA llama a /chat-contextualizado
   ↓
5. PILI (backend) procesa:
   - Detecta servicio: electrico-residencial
   - Extrae datos: area=120m²
   - Genera JSON estructurado
   ↓
6. Backend retorna:
   {
     respuesta: "He analizado...",
     informe_generado: {
       titulo: "Informe Técnico Eléctrico",
       codigo: "INF-...",
       ...
     }
   }
   ↓
7. ChatIA recibe respuesta:
   - Muestra mensaje en chat
   - Llama onDatosGenerados(informe_generado)
   ↓
8. App.jsx recibe datos:
   - Mapea datos al formato correcto
   - setDatosEditables(datosMapeados)
   ↓
9. HTML Editable se auto-rellena
   ↓
10. Usuario puede editar
   ↓
11. Usuario genera documento con sistema actual (V2)
```

---

## ✅ Ventajas de Este Enfoque

1. **NO modifica generadores Python** ✅
2. **NO modifica HTML editables** ✅
3. **NO modifica endpoints de generación** ✅
4. **Usa endpoints existentes** ✅
5. **Separación de responsabilidades:**
   - PILI: Conversar + Extraer
   - HTML Editables: Mostrar + Editar
   - Python Generators: Generar documentos

---

## 🚀 Implementación Inmediata

### **Archivos a modificar:**

1. ✅ `frontend/src/ChatIA.jsx` - Agregar llamada a endpoint
2. ✅ `frontend/src/App.jsx` - Agregar callback y mapeo

### **Archivos a NO tocar:**

1. ❌ `backend/app/services/generators/*.py`
2. ❌ `frontend/src/components/EDITABLE_*.jsx`
3. ❌ `backend/app/routers/generar_directo.py`

---

## 📝 Próximos Pasos

1. Actualizar `ChatIA.jsx` con llamada a endpoint
2. Actualizar `App.jsx` con callback
3. Crear función de mapeo de datos
4. Probar flujo completo
5. Ajustar mapeo según necesidad

**¿Procedo con la implementación?**
