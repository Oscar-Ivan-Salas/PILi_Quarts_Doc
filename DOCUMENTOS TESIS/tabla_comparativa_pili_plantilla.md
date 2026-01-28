# 📊 Tabla Comparativa: Plantilla vs Preguntas de PILI

## 🎯 Flujo Completo

```
1. Usuario rellena DATOS DEL CLIENTE
   ↓
2. Selecciona SERVICIO + INDUSTRIA
   ↓
3. PILI se activa en MODO ESPECIALISTA
   ↓
4. PILI hace PREGUNTAS PRECISAS
   ↓
5. Datos se SINCRONIZAN con PLANTILLA
   ↓
6. Plantilla se RELLENA AUTOMÁTICAMENTE
```

---

## 📋 Análisis de Imágenes

### **Imagen 1: Datos del Cliente (Ya rellenados)**
![Datos Cliente](file:///C:/Users/USUARIO/.gemini/antigravity/brain/e49dd4cc-507e-428d-8803-bba3270b39d6/uploaded_image_0_1766756234232.png)

**Datos capturados:**
- ✅ Nombre: Rogelio Infantas Contreras
- ✅ RUC: 10204438189
- ✅ Dirección: Concepción
- ✅ Teléfono: 906315971
- ✅ Email: rogelio.infantas@gmail.com

### **Imagen 2: Plantilla - Datos del Cliente**
![Plantilla Cliente](file:///C:/Users/USUARIO/.gemini/antigravity/brain/e49dd4cc-507e-428d-8803-bba3270b39d6/uploaded_image_1_1766756234232.png)

**Campos en plantilla:**
- Cliente: ________ (vacío)
- Proyecto: Instalaciones Eléctricas Resi...
- Área: 0 m²

### **Imagen 3: Plantilla - Datos de Cotización**
![Plantilla Cotización](file:///C:/Users/USUARIO/.gemini/antigravity/brain/e49dd4cc-507e-428d-8803-bba3270b39d6/uploaded_image_2_1766756234232.png)

**Campos en plantilla:**
- Fecha: 26/12/2025
- Vigencia: 30 días calendario
- Servicio: Instalaciones Eléctricas

---

## 📊 TABLA COMPARATIVA POR SERVICIO

### **1. ⚡ ELECTRICIDAD (Residencial/Comercial/Industrial)**

| Campo en Plantilla | Dato Actual | Pregunta de PILI | Tipo Respuesta |
|-------------------|-------------|------------------|----------------|
| **DATOS DEL CLIENTE** (Ya rellenados) |
| Cliente | Rogelio Infantas | ✅ Ya tiene | - |
| RUC | 10204438189 | ✅ Ya tiene | - |
| Dirección | Concepción | ✅ Ya tiene | - |
| **DATOS DEL PROYECTO** |
| Proyecto | Instalaciones Eléctricas | ✅ Auto (del servicio) | - |
| Área (m²) | 0 | "📏 ¿Cuál es el área total del proyecto en m²?" | Número |
| Tipo instalación | - | "🏠 ¿Es Residencial, Comercial o Industrial?" | Botones |
| Número de pisos | - | "🏢 ¿Cuántos pisos tiene?" | Número |
| **DATOS TÉCNICOS** |
| Puntos de luz | - | "💡 ¿Cuántos puntos de luz necesitas?" | Número |
| Tomacorrientes | - | "🔌 ¿Cuántos tomacorrientes?" | Número |
| Tableros | - | "⚡ ¿Cuántos tableros eléctricos?" | Número |
| Potencia (kW) | - | "⚡ ¿Cuál es la potencia requerida en kW?" | Número |
| **DATOS DE COTIZACIÓN** |
| Fecha | 26/12/2025 | ✅ Auto (hoy) | - |
| Vigencia | 30 días | ✅ Auto (estándar) | - |
| Servicio | Instalaciones Eléctricas | ✅ Auto (seleccionado) | - |

**Flujo de PILI:**
```
PILI: "¡Hola! Soy PILI, especialista en Instalaciones Eléctricas. 👋

Veo que el cliente es Rogelio Infantas Contreras. ✅

¿Qué tipo de instalación necesitas?"

[🏠 Residencial] [🏢 Comercial] [🏭 Industrial]

Usuario: [Residencial]

PILI: "Perfecto, instalación residencial. 

📏 ¿Cuál es el área total en m²?"

Usuario: "120"

PILI: "✅ Área: 120 m²

🏢 ¿Cuántos pisos tiene?"

Usuario: "2"

PILI: "✅ Pisos: 2

💡 ¿Cuántos puntos de luz necesitas?"

Usuario: "25"

PILI: "✅ Puntos de luz: 25

🔌 ¿Cuántos tomacorrientes?"

Usuario: "15"

PILI: "✅ Tomacorrientes: 15

⚡ ¿Cuántos tableros eléctricos?"

Usuario: "2"

PILI: "✅ Tableros: 2

📊 Generando cotización...

COTIZACIÓN INSTALACIÓN ELÉCTRICA RESIDENCIAL
━━━━━━━━━━━━━━━━━━━━━━━
Cliente: Rogelio Infantas Contreras
Área: 120 m²
Pisos: 2
Puntos luz: 25
Tomacorrientes: 15
Tableros: 2

ITEMS CALCULADOS:
1. Puntos de luz (25) - S/ 1,875.00
2. Tomacorrientes (15) - S/ 900.00
3. Tableros (2) - S/ 1,600.00
4. Cable THW 2.5mm² - S/ 480.00
...

TOTAL: S/ 8,450.00
━━━━━━━━━━━━━━━━━━━━━━━"
```

---

### **2. 📋 ITSE**

| Campo en Plantilla | Pregunta de PILI | Tipo Respuesta |
|-------------------|------------------|----------------|
| Tipo establecimiento | "🏢 ¿Qué tipo de establecimiento es?" | Botones (8 categorías) |
| Tipo específico | "📋 ¿Qué tipo específico?" (ej: Hospital, Clínica) | Botones |
| Área (m²) | "📏 ¿Cuál es el área total en m²?" | Número |
| Número de pisos | "🏢 ¿Cuántos pisos tiene?" | Número |
| Nivel de riesgo | ✅ Auto (calculado por PILI) | - |
| Precio municipal | ✅ Auto (según nivel) | - |
| Precio servicio | ✅ Auto (según nivel) | - |

---

### **3. 🔌 PUESTA A TIERRA**

| Campo en Plantilla | Pregunta de PILI | Tipo Respuesta |
|-------------------|------------------|----------------|
| Tipo de suelo | "🌍 ¿Qué tipo de suelo es?" | Botones (Arcilloso/Arenoso/Rocoso) |
| Potencia (kW) | "⚡ ¿Cuál es la potencia instalada en kW?" | Número |
| Área (m²) | "📏 ¿Cuál es el área del proyecto?" | Número |
| Número de pozos | "🔌 ¿Cuántos pozos a tierra necesitas?" | Número |
| Resistencia objetivo (Ω) | "⚡ ¿Cuál es la resistencia objetivo en Ohmios?" | Número (default: 25) |

---

### **4. 🔥 CONTRA INCENDIOS**

| Campo en Plantilla | Pregunta de PILI | Tipo Respuesta |
|-------------------|------------------|----------------|
| Tipo de sistema | "🔥 ¿Qué sistema necesitas?" | Botones (Detección/Extinción/Completo) |
| Área (m²) | "📏 ¿Cuál es el área a proteger?" | Número |
| Número de pisos | "🏢 ¿Cuántos pisos?" | Número |
| Detectores de humo | "🚨 ¿Cuántos detectores de humo?" | Número |
| Extintores | "🧯 ¿Cuántos extintores?" | Número |
| Rociadores | "💧 ¿Sistema de rociadores?" | Sí/No |

---

### **5. 🏠 DOMÓTICA**

| Campo en Plantilla | Pregunta de PILI | Tipo Respuesta |
|-------------------|------------------|----------------|
| Tipo de proyecto | "🏠 ¿Qué quieres automatizar?" | Botones (Casa/Oficina/Edificio) |
| Área (m²) | "📏 ¿Cuál es el área?" | Número |
| Interruptores inteligentes | "💡 ¿Cuántos interruptores inteligentes?" | Número |
| Sensores de movimiento | "🚶 ¿Cuántos sensores de movimiento?" | Número |
| Cámaras IP | "📹 ¿Cuántas cámaras IP?" | Número |
| Central domótica | "🤖 ¿Necesitas central domótica?" | Sí/No |

---

### **6. 📹 CCTV**

| Campo en Plantilla | Pregunta de PILI | Tipo Respuesta |
|-------------------|------------------|----------------|
| Tipo de cámaras | "📹 ¿Qué tipo de cámaras?" | Botones (Analógicas/IP/Híbrido) |
| Número de cámaras | "📹 ¿Cuántas cámaras necesitas?" | Número |
| Resolución | "🎥 ¿Qué resolución?" | Botones (2MP/4MP/8MP) |
| DVR/NVR | "💾 ¿Cuántos canales de grabación?" | Número |
| Disco duro (TB) | "💿 ¿Cuántos TB de almacenamiento?" | Número |
| Días de grabación | "📅 ¿Cuántos días de grabación?" | Número (default: 30) |

---

### **7. 🌐 REDES**

| Campo en Plantilla | Pregunta de PILI | Tipo Respuesta |
|-------------------|------------------|----------------|
| Tipo de red | "🌐 ¿Qué tipo de red?" | Botones (Cat5e/Cat6/Cat6a/Fibra) |
| Área (m²) | "📏 ¿Cuál es el área?" | Número |
| Puntos de red | "🔌 ¿Cuántos puntos de red?" | Número |
| Access Points | "📡 ¿Cuántos Access Points WiFi?" | Número |
| Switch | "🔀 ¿Cuántos switches necesitas?" | Número |
| Rack | "📦 ¿Necesitas rack?" | Sí/No |

---

### **8. ⚙️ AUTOMATIZACIÓN INDUSTRIAL**

| Campo en Plantilla | Pregunta de PILI | Tipo Respuesta |
|-------------------|------------------|----------------|
| Tipo de proceso | "⚙️ ¿Qué proceso automatizar?" | Texto |
| PLCs | "🤖 ¿Cuántos PLCs?" | Número |
| Entradas digitales | "🔢 ¿Cuántas entradas digitales?" | Número |
| Salidas digitales | "🔢 ¿Cuántas salidas digitales?" | Número |
| Entradas analógicas | "📊 ¿Cuántas entradas analógicas?" | Número |
| HMI | "🖥️ ¿Necesitas HMI?" | Sí/No |
| SCADA | "💻 ¿Sistema SCADA?" | Sí/No |

---

### **9. 📄 EXPEDIENTES TÉCNICOS**

| Campo en Plantilla | Pregunta de PILI | Tipo Respuesta |
|-------------------|------------------|----------------|
| Tipo de proyecto | "📄 ¿Para qué proyecto?" | Botones (Eléctrico/Sanitario/Estructural) |
| Área (m²) | "📏 ¿Cuál es el área del proyecto?" | Número |
| Número de planos | "📐 ¿Cuántos planos necesitas?" | Número |
| Memoria descriptiva | "📝 ¿Incluir memoria descriptiva?" | Sí/No |
| Especificaciones técnicas | "📋 ¿Incluir especificaciones técnicas?" | Sí/No |
| Metrados | "📊 ¿Incluir metrados?" | Sí/No |

---

### **10. 💧 SANEAMIENTO**

| Campo en Plantilla | Pregunta de PILI | Tipo Respuesta |
|-------------------|------------------|----------------|
| Tipo de sistema | "💧 ¿Qué sistema?" | Botones (Agua/Desagüe/Completo) |
| Área (m²) | "📏 ¿Cuál es el área?" | Número |
| Número de baños | "🚽 ¿Cuántos baños?" | Número |
| Puntos de agua | "💧 ¿Cuántos puntos de agua?" | Número |
| Desagües | "🚰 ¿Cuántos desagües?" | Número |
| Tanque elevado | "🏗️ ¿Necesitas tanque elevado?" | Sí/No |
| Cisterna | "💦 ¿Necesitas cisterna?" | Sí/No |

---

## 🔄 Sincronización Automática

### **Cómo funciona:**

```javascript
// Cuando PILI obtiene un dato
PILI pregunta: "📏 ¿Área?"
Usuario responde: "120"

// Backend extrae
datos_extraidos = { area_m2: 120 }

// Frontend actualiza
setDatosEditables(prev => ({
  ...prev,
  area_m2: 120,
  cliente: datosCliente  // Del paso 1
}));

// Plantilla se actualiza automáticamente
<input value={datosEditables.area_m2} />  // Muestra: 120
```

---

## ✅ Reglas de PILI

1. **PILI DIRIGE** la conversación
2. **Usuario SOLO responde**
3. **Una pregunta a la vez**
4. **Datos se sincronizan** automáticamente
5. **Plantilla se rellena** en tiempo real
6. **PILI calcula** totales y precios
7. **PILI genera** items automáticamente

---

## 🎯 Próximos Pasos

1. ✅ Crear componente base `PiliEspecialista.jsx`
2. ✅ Implementar lógica de preguntas por servicio
3. ✅ Sincronizar con `datosEditables`
4. ✅ Actualizar plantilla en tiempo real
5. ✅ Generar items automáticamente
6. ✅ Calcular totales

¿Procedo con la implementación?
