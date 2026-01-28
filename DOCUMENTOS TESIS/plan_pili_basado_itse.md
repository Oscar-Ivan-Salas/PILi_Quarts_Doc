# 🎯 Plan Definitivo: PILI Especialista (Basado en Artefacto ITSE)

## ✅ LO QUE NO SE TOCA

- ❌ **NO tocar** generación de Word/PDF (ya funciona)
- ❌ **NO tocar** plantillas HTML (ya funcionan)
- ❌ **NO tocar** datos del cliente (ya funciona)
- ❌ **NO tocar** colores del frontend (ya están)

## ✅ LO QUE SE AGREGA

- ✅ **SÍ agregar** PILI especialista por servicio
- ✅ **SÍ agregar** conversación inteligente
- ✅ **SÍ agregar** cálculo automático
- ✅ **SÍ agregar** sincronización con `datosEditables`

---

## 📊 ANÁLISIS DEL ARTEFACTO ITSE

### **7 Patrones Clave Identificados:**

#### **1. CONVERSATION STATE (Estado por Etapas)**
```javascript
const [conversationState, setConversationState] = useState({
  stage: 'initial',           // Etapa actual
  selectedCategory: null,     // Primera selección
  businessType: null,         // Segunda selección
  area: null,                 // Dato numérico 1
  floors: 1,                  // Dato numérico 2
  riskLevel: null,            // Calculado automáticamente
  clientName: null,           // Captura final
  phone: null,
  address: null
});
```

**Etapas:**
- `initial` → Selección de categoría (botones)
- `businessType` → Tipo específico (botones dinámicos)
- `area` → Input numérico
- `floors` → Input numérico
- `quotation` → Muestra cotización calculada
- `clientName` → Captura nombre
- `phone` → Captura teléfono
- `address` → Captura dirección
- `confirmation` → Resumen final

#### **2. KNOWLEDGE BASE (Base de Conocimiento)**
```javascript
const knowledgeBase = {
  // Precios por nivel
  municipalPrices: {
    BAJO: { price: 168.30, renewal: 90.30, days: 7 },
    MEDIO: { price: 208.60, renewal: 109.40, days: 7 },
    ALTO: { price: 703.00, renewal: 417.40, days: 7 },
    MUY_ALTO: { price: 1084.60, renewal: 629.20, days: 7 }
  },
  
  // Servicios Tesla
  teslaServices: {
    BAJO: { min: 300, max: 500 },
    MEDIO: { min: 450, max: 650 },
    ALTO: { min: 800, max: 1200 },
    MUY_ALTO: { min: 1200, max: 1800 }
  },
  
  // Categorías con reglas
  categories: {
    SALUD: {
      types: ['Hospital', 'Clínica', ...],
      defaultRisk: 'ALTO',
      specialRules: 'Más de 500m² o 2+ pisos = MUY ALTO'
    }
  }
};
```

#### **3. CÁLCULO AUTOMÁTICO INTELIGENTE**
```javascript
const determineRiskLevel = (category, area, floors, businessType) => {
  // Reglas específicas por categoría
  if (category === 'SALUD') {
    if (area > 500 || floors >= 2) return 'MUY_ALTO';
    return 'ALTO';
  }
  
  if (category === 'EDUCACION') {
    if (area > 1000 || floors >= 3) return 'ALTO';
    return 'MEDIO';
  }
  
  // ... más reglas
  
  return cat.defaultRisk;
};
```

#### **4. BOTONES DINÁMICOS**
```javascript
// Botones cambian según la etapa
if (state.stage === 'initial') {
  addBotMessage("Selecciona categoría:", [
    { text: '🏥 Salud', value: 'SALUD' },
    { text: '🎓 Educación', value: 'EDUCACION' },
    // ...
  ]);
}

if (state.stage === 'businessType') {
  const types = knowledgeBase.categories[value].types;
  addBotMessage("¿Qué tipo específico?", 
    types.map(t => ({ text: t, value: t }))
  );
}
```

#### **5. VALIDACIÓN DE INPUTS**
```javascript
if (state.stage === 'area') {
  const area = parseFloat(inputValue);
  if (isNaN(area) || area <= 0) {
    addBotMessage('Por favor ingresa un número válido de área en m²');
    return;
  }
  
  state.area = area;
  state.stage = 'floors';
  // ...
}
```

#### **6. COTIZACIÓN FORMATEADA**
```javascript
const showQuotation = (riskLevel) => {
  const municipal = knowledgeBase.municipalPrices[riskLevel];
  const tesla = knowledgeBase.teslaServices[riskLevel];
  const totalMin = municipal.price + tesla.min;
  const totalMax = municipal.price + tesla.max;

  addBotMessage(`📊 **COTIZACIÓN ITSE - NIVEL ${riskLevel}**

━━━━━━━━━━━━━━━━━━━━━━━
**💰 COSTOS DESGLOSADOS:**

🏛️ **Derecho Municipal (TUPA):**
└ S/ ${municipal.price.toFixed(2)}

⚡ **Servicio Técnico TESLA:**
└ S/ ${tesla.min} - ${tesla.max}

━━━━━━━━━━━━━━━━━━━━━━━
**📈 TOTAL ESTIMADO:**
**S/ ${totalMin} - ${totalMax}**
━━━━━━━━━━━━━━━━━━━━━━━

⏱️ **Tiempo:** ${municipal.days} días hábiles
🎁 **Visita técnica:** GRATUITA
✅ **Garantía:** 100% aprobación`, [
    { text: '📅 Agendar visita', value: 'AGENDAR' },
    { text: '💬 Más información', value: 'CONSULTA' }
  ]);
};
```

#### **7. CAPTURA DE DATOS DEL CLIENTE**
```javascript
if (state.stage === 'clientName') {
  state.clientName = inputValue;
  state.stage = 'phone';
  addBotMessage(`Mucho gusto **${inputValue}** 👋\n\n¿Cuál es tu número de teléfono?`);
}

if (state.stage === 'phone') {
  state.phone = inputValue;
  state.stage = 'address';
  addBotMessage(`Perfecto. ¿Cuál es la dirección del establecimiento?`);
}
```

---

## 🎯 APLICACIÓN A ELECTRICIDAD

### **Conversation State:**
```javascript
const [conversationState, setConversationState] = useState({
  stage: 'initial',
  tipoInstalacion: null,      // Residencial/Comercial/Industrial
  area: null,
  pisos: null,
  puntosLuz: null,
  tomacorrientes: null,
  tableros: null,
  potencia: null,
  items: [],                  // Calculados automáticamente
  total: 0                    // Calculado automáticamente
});
```

### **Knowledge Base:**
```javascript
const knowledgeBase = {
  precios: {
    RESIDENCIAL: {
      puntoLuz: 80,
      tomacorriente: 60,
      tablero: 800,
      cableM2: 2.5
    },
    COMERCIAL: {
      puntoLuz: 95,
      tomacorriente: 75,
      tablero: 1200,
      cableM2: 3.2
    },
    INDUSTRIAL: {
      puntoLuz: 120,
      tomacorriente: 95,
      tablero: 2800,
      cableM2: 4.5
    }
  },
  
  calcularItems: (tipo, area, puntos, tomas, tableros) => {
    const precios = knowledgeBase.precios[tipo];
    
    return [
      {
        descripcion: `Puntos de luz empotrados (${puntos})`,
        cantidad: puntos,
        precioUnitario: precios.puntoLuz,
        total: puntos * precios.puntoLuz
      },
      {
        descripcion: `Tomacorrientes dobles (${tomas})`,
        cantidad: tomas,
        precioUnitario: precios.tomacorriente,
        total: tomas * precios.tomacorriente
      },
      {
        descripcion: `Tableros eléctricos (${tableros})`,
        cantidad: tableros,
        precioUnitario: precios.tablero,
        total: tableros * precios.tablero
      },
      {
        descripcion: `Cable THW 2.5mm² (${area * 1.5}m)`,
        cantidad: area * 1.5,
        precioUnitario: precios.cableM2,
        total: area * 1.5 * precios.cableM2
      }
    ];
  }
};
```

### **Flujo de Conversación:**
```javascript
const processResponse = (value) => {
  const state = conversationState;

  // ETAPA 1: Tipo de instalación
  if (state.stage === 'initial') {
    state.tipoInstalacion = value;
    state.stage = 'area';
    setConversationState({...state});
    
    addBotMessage(`Perfecto, instalación **${value}**.\n\n📏 ¿Cuál es el área total en m²?\n\n_Escribe el número (ejemplo: 120)_`);
    return;
  }

  // ETAPA 2: Área
  if (state.stage === 'area') {
    const area = parseFloat(inputValue);
    if (isNaN(area) || area <= 0) {
      addBotMessage('Por favor ingresa un número válido de área en m²');
      return;
    }
    
    state.area = area;
    state.stage = 'pisos';
    setConversationState({...state});
    
    addBotMessage(`📐 Área: **${area} m²**\n\n🏢 ¿Cuántos pisos tiene?\n\n_Escribe el número (ejemplo: 2)_`);
    return;
  }

  // ETAPA 3: Pisos
  if (state.stage === 'pisos') {
    const pisos = parseInt(inputValue);
    if (isNaN(pisos) || pisos <= 0) {
      addBotMessage('Por favor ingresa un número válido de pisos');
      return;
    }
    
    state.pisos = pisos;
    state.stage = 'puntosLuz';
    setConversationState({...state});
    
    addBotMessage(`🏢 Pisos: **${pisos}**\n\n💡 ¿Cuántos puntos de luz necesitas?\n\n_Escribe el número (ejemplo: 25)_`);
    return;
  }

  // ETAPA 4: Puntos de luz
  if (state.stage === 'puntosLuz') {
    const puntos = parseInt(inputValue);
    if (isNaN(puntos) || puntos <= 0) {
      addBotMessage('Por favor ingresa un número válido de puntos de luz');
      return;
    }
    
    state.puntosLuz = puntos;
    state.stage = 'tomacorrientes';
    setConversationState({...state});
    
    addBotMessage(`💡 Puntos de luz: **${puntos}**\n\n🔌 ¿Cuántos tomacorrientes?\n\n_Escribe el número (ejemplo: 15)_`);
    return;
  }

  // ETAPA 5: Tomacorrientes
  if (state.stage === 'tomacorrientes') {
    const tomas = parseInt(inputValue);
    if (isNaN(tomas) || tomas <= 0) {
      addBotMessage('Por favor ingresa un número válido de tomacorrientes');
      return;
    }
    
    state.tomacorrientes = tomas;
    state.stage = 'tableros';
    setConversationState({...state});
    
    addBotMessage(`🔌 Tomacorrientes: **${tomas}**\n\n⚡ ¿Cuántos tableros eléctricos?\n\n_Escribe el número (ejemplo: 2)_`);
    return;
  }

  // ETAPA 6: Tableros
  if (state.stage === 'tableros') {
    const tableros = parseInt(inputValue);
    if (isNaN(tableros) || tableros <= 0) {
      addBotMessage('Por favor ingresa un número válido de tableros');
      return;
    }
    
    state.tableros = tableros;
    
    // CALCULAR ITEMS Y TOTAL
    const items = knowledgeBase.calcularItems(
      state.tipoInstalacion,
      state.area,
      state.puntosLuz,
      state.tomacorrientes,
      tableros
    );
    
    const total = items.reduce((sum, item) => sum + item.total, 0);
    
    state.items = items;
    state.total = total;
    state.stage = 'quotation';
    setConversationState({...state});
    
    showQuotation(state);
    return;
  }
};
```

### **Mostrar Cotización:**
```javascript
const showQuotation = (state) => {
  const { tipoInstalacion, area, pisos, puntosLuz, tomacorrientes, tableros, items, total } = state;
  
  let itemsText = '';
  items.forEach((item, index) => {
    itemsText += `${index + 1}. ${item.descripcion}\n   └ S/ ${item.total.toFixed(2)}\n\n`;
  });
  
  addBotMessage(`📊 **COTIZACIÓN INSTALACIÓN ELÉCTRICA ${tipoInstalacion}**

━━━━━━━━━━━━━━━━━━━━━━━
**📋 DATOS DEL PROYECTO:**

📏 Área: ${area} m²
🏢 Pisos: ${pisos}
💡 Puntos de luz: ${puntosLuz}
🔌 Tomacorrientes: ${tomacorrientes}
⚡ Tableros: ${tableros}

━━━━━━━━━━━━━━━━━━━━━━━
**💰 ITEMS CALCULADOS:**

${itemsText}
━━━━━━━━━━━━━━━━━━━━━━━
**📈 TOTAL ESTIMADO:**
**S/ ${total.toFixed(2)}**
━━━━━━━━━━━━━━━━━━━━━━━

✅ Incluye: Materiales + Mano de obra
⏱️ Tiempo: 5-7 días hábiles
🎁 Garantía: 1 año

¿Deseas generar el documento?`, [
    { text: '📄 Generar Cotización', value: 'GENERAR' },
    { text: '🔄 Nueva consulta', value: 'RESTART' }
  ]);
  
  // ✅ SINCRONIZAR CON datosEditables
  onCotizacionGenerada({
    cliente: datosCliente,  // Del paso 1
    proyecto: `Instalación Eléctrica ${tipoInstalacion}`,
    area: area,
    items: items,
    subtotal: total,
    igv: total * 0.18,
    total: total * 1.18
  });
};
```

---

## ✅ INTEGRACIÓN CON SISTEMA EXISTENTE

### **1. Crear Componente PiliElectricidad.jsx**
```javascript
import React, { useState, useRef, useEffect } from 'react';
import { Send, Zap } from 'lucide-react';

const PiliElectricidad = ({ datosCliente, onCotizacionGenerada }) => {
  // Estado de conversación
  const [conversationState, setConversationState] = useState({...});
  
  // Base de conocimiento
  const knowledgeBase = {...};
  
  // Funciones
  const processResponse = (value) => {...};
  const showQuotation = (state) => {...};
  
  // Render
  return (
    <div>
      {/* Chat con colores Tesla */}
      {/* Mensajes */}
      {/* Input cuando corresponda */}
    </div>
  );
};

export default PiliElectricidad;
```

### **2. Integrar en App.jsx**
```javascript
// En App.jsx, paso 2 (después de seleccionar servicio)

{paso === 2 && servicioSeleccionado === 'electricidad' && (
  <PiliElectricidad
    datosCliente={datosCliente}
    onCotizacionGenerada={(datos) => {
      // Actualizar datosEditables
      setDatosEditables(datos);
      
      // Actualizar cotizacion
      setCotizacion(datos);
      
      // Mostrar vista previa
      setMostrarPreview(true);
    }}
  />
)}
```

---

## 🎯 PRÓXIMOS PASOS

1. ✅ Crear `PiliElectricidad.jsx` con patrón ITSE
2. ✅ Probar flujo completo
3. ✅ Replicar para otros 9 servicios

¿Procedo a crear `PiliElectricidad.jsx` siguiendo EXACTAMENTE este patrón?
