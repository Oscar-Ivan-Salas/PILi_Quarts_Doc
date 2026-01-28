# 📋 Punto 2: Chat Amigable con Opciones

## 🎯 Objetivo

Hacer que PILI sea más conversacional y amigable:
- ✅ Preguntas **una por una** (no todas juntas)
- ✅ Opción de **formulario rápido** inline
- ✅ **Botones de respuesta rápida**
- ✅ **Indicador de progreso** visual

---

## 📊 Problema Actual

**PILI lanza todas las preguntas juntas:**
```
PILI: "Para completar la cotización, necesito:

📏 ¿Cuál es el área del proyecto en m²?
💡 ¿Cuántos puntos de luz necesitas?
🔌 ¿Cuántos tomacorrientes?

💬 Cuéntame estos detalles y prepararé todo para ti."
```

**Problema:**
- Usuario se abruma con muchas preguntas
- No hay flujo conversacional natural
- No hay feedback de progreso

---

## ✅ Solución: 3 Estrategias

### **Estrategia 1: Preguntas Una por Una (Más Amigable)**

```
PILI: "¡Hola! 👋 Veo que necesitas Instalaciones Eléctricas Residenciales.

📏 Para comenzar, ¿cuál es el área del proyecto en m²?"

Usuario: "120"

PILI: "Perfecto, 120 m². ✅

💡 ¿Cuántos puntos de luz necesitas?"

Usuario: "15"

PILI: "Excelente, 15 puntos de luz. ✅

🔌 ¿Cuántos tomacorrientes?"
```

**Ventajas:**
- Conversación natural
- Usuario no se abruma
- Feedback inmediato

**Desventajas:**
- Más mensajes
- Puede ser lento para usuarios expertos

### **Estrategia 2: Formulario Rápido Inline (Más Rápido)**

```
PILI: "¡Hola! 👋 Para tu cotización de Instalaciones Eléctricas Residenciales.

¿Prefieres responder por chat o usar un formulario rápido?

[💬 Chat Conversacional] [📝 Formulario Rápido]"

Si elige Formulario:
┌─────────────────────────────┐
│ 📝 Datos del Proyecto       │
├─────────────────────────────┤
│ Área m²: [____]             │
│ Puntos luz: [____]          │
│ Tomacorrientes: [____]      │
│ Pisos: [____]               │
│                             │
│ [Enviar]                    │
└─────────────────────────────┘
```

**Ventajas:**
- Muy rápido
- Usuario experto puede llenar todo de una vez
- Menos mensajes

**Desventajas:**
- Menos conversacional
- Requiere componente React adicional

### **Estrategia 3: Híbrida (Recomendada) ⭐**

```
PILI: "¡Hola! 👋 Veo que necesitas Instalaciones Eléctricas Residenciales.

Puedo ayudarte de dos formas:

[💬 Conversación Guiada] - Te pregunto paso a paso
[📝 Formulario Rápido] - Llenas todo de una vez

¿Cuál prefieres?"

Si elige Conversación:
  → Preguntas una por una
  
Si elige Formulario:
  → Muestra formulario inline
```

**Ventajas:**
- Usuario elige su preferencia
- Flexibilidad
- Mejor UX

---

## 🔧 Implementación

### **Paso 1: Agregar Estado Conversacional en Backend**

**Archivo:** `backend/app/services/pili_integrator.py`

```python
def _generar_respuesta_pili_local(self, mensaje, servicio, agente):
    """Genera respuesta guiada una pregunta a la vez"""
    
    # Extraer datos del mensaje
    datos = self.pili_brain.extraer_datos(mensaje, servicio)
    
    # Determinar qué datos faltan
    datos_requeridos = {
        'area_m2': '📏 ¿Cuál es el área del proyecto en m²?',
        'cantidad_puntos': '💡 ¿Cuántos puntos de luz necesitas?',
        'cantidad_tomacorrientes': '🔌 ¿Cuántos tomacorrientes?',
        'num_pisos': '🏢 ¿Cuántos pisos tiene?'
    }
    
    # Encontrar el primer dato que falta
    for campo, pregunta in datos_requeridos.items():
        if not datos.get(campo):
            # Mostrar datos ya recopilados
            respuesta = ""
            datos_recopilados = []
            for c, p in datos_requeridos.items():
                if datos.get(c):
                    emoji = p.split()[0]
                    datos_recopilados.append(f"{emoji} {c.replace('_', ' ').title()}: {datos[c]}")
            
            if datos_recopilados:
                respuesta = "Perfecto, tengo:\n"
                for d in datos_recopilados:
                    respuesta += f"✅ {d}\n"
                respuesta += "\n"
            
            # Hacer la siguiente pregunta
            respuesta += pregunta
            
            return {
                "texto": respuesta,
                "agente": agente,
                "datos_recopilados": list(datos.keys()),
                "datos_faltantes": [k for k in datos_requeridos.keys() if not datos.get(k)],
                "progreso": f"{len(datos)}/{len(datos_requeridos)}"
            }
    
    # Si tenemos todos los datos, generar cotización
    cot_data = self.pili_brain.generar_cotizacion(mensaje, servicio, "simple")
    return {
        "texto": f"✅ ¡Perfecto! Tengo todos los datos.\n\n📊 Cotización generada: S/ {cot_data['datos']['total']:,.2f}",
        "agente": agente,
        "datos_generados": cot_data.get("datos"),
        "progreso": "4/4"
    }
```

### **Paso 2: Agregar Componente de Progreso en Frontend**

**Archivo:** `frontend/src/App.jsx`

```javascript
// Nuevo estado para tracking de progreso
const [datosRecopilados, setDatosRecopilados] = useState([]);
const [datosFaltantes, setDatosFaltantes] = useState([]);
const [progresoChat, setProgresoChat] = useState('0/0');

// Componente de progreso
const ProgresoDatos = () => {
  if (datosRecopilados.length === 0 && datosFaltantes.length === 0) return null;
  
  const total = datosRecopilados.length + datosFaltantes.length;
  const progreso = (datosRecopilados.length / total) * 100;
  
  return (
    <div className="bg-white p-4 rounded-lg shadow mb-4">
      <div className="flex justify-between mb-2">
        <span className="text-sm font-semibold text-gray-700">
          Progreso de Datos
        </span>
        <span className="text-sm text-gray-600">{progresoChat}</span>
      </div>
      
      <div className="w-full bg-gray-200 rounded-full h-2 mb-3">
        <div 
          className="bg-yellow-600 h-2 rounded-full transition-all duration-500"
          style={{ width: `${progreso}%` }}
        />
      </div>
      
      <div className="flex flex-wrap gap-2">
        {datosRecopilados.map(campo => (
          <span 
            key={campo} 
            className="bg-green-100 text-green-800 px-2 py-1 rounded text-xs font-medium"
          >
            ✅ {campo}
          </span>
        ))}
        {datosFaltantes.map(campo => (
          <span 
            key={campo} 
            className="bg-gray-100 text-gray-600 px-2 py-1 rounded text-xs"
          >
            ⏳ {campo}
          </span>
        ))}
      </div>
    </div>
  );
};
```

### **Paso 3: Actualizar handleEnviarMensajeChat**

```javascript
const handleEnviarMensajeChat = async () => {
  // ... código existente ...
  
  const data = await response.json();
  
  if (data.success) {
    // Actualizar progreso
    if (data.datos_recopilados) {
      setDatosRecopilados(data.datos_recopilados);
    }
    if (data.datos_faltantes) {
      setDatosFaltantes(data.datos_faltantes);
    }
    if (data.progreso) {
      setProgresoChat(data.progreso);
    }
    
    // Actualizar datosEditables si hay datos generados
    if (data.datos_generados) {
      setDatosEditables(prev => ({
        ...prev,
        ...data.datos_generados
      }));
    }
  }
};
```

---

## 📋 Tareas de Implementación

### Backend
- [ ] Modificar `_generar_respuesta_pili_local()` para preguntas una por una
- [ ] Agregar tracking de datos recopilados vs faltantes
- [ ] Retornar `datos_recopilados`, `datos_faltantes`, `progreso`
- [ ] Implementar lógica de "siguiente pregunta"

### Frontend
- [ ] Crear componente `ProgresoDatos`
- [ ] Agregar estados `datosRecopilados`, `datosFaltantes`, `progresoChat`
- [ ] Actualizar `handleEnviarMensajeChat` para procesar progreso
- [ ] Mostrar `ProgresoDatos` en el chat

### Opcional (Formulario Rápido)
- [ ] Crear componente `FormularioRapido`
- [ ] Agregar botones de selección (Chat vs Formulario)
- [ ] Implementar envío de formulario completo

---

## ✅ Resultado Esperado

**Antes:**
```
PILI: "Necesito: área, puntos, tomacorrientes, pisos"
Usuario: "120m², 15, 10, 2"
PILI: "Cotización: S/ 4,850"
```

**Después:**
```
PILI: "📏 ¿Área en m²?"
Usuario: "120"

PILI: "✅ Área: 120 m²
      💡 ¿Puntos de luz?"
Usuario: "15"

PILI: "✅ Área: 120 m²
      ✅ Puntos: 15
      🔌 ¿Tomacorrientes?"
Usuario: "10"

PILI: "✅ Área: 120 m²
      ✅ Puntos: 15
      ✅ Tomacorrientes: 10
      🏢 ¿Pisos?"
Usuario: "2"

PILI: "✅ ¡Perfecto! Tengo todos los datos.
      📊 Cotización: S/ 4,850.00"
```

**Con indicador de progreso:**
```
┌─────────────────────────────┐
│ Progreso de Datos    3/4    │
├─────────────────────────────┤
│ ████████████░░░░░░░░  75%   │
├─────────────────────────────┤
│ ✅ área  ✅ puntos  ✅ tomas │
│ ⏳ pisos                     │
└─────────────────────────────┘
```

---

## 🎯 Orden de Implementación

1. **Primero:** Backend - Preguntas una por una (1-2h)
2. **Segundo:** Frontend - Componente de progreso (1h)
3. **Tercero:** Integración y pruebas (1h)
4. **Opcional:** Formulario rápido (2h)

**Total estimado:** 3-6 horas
