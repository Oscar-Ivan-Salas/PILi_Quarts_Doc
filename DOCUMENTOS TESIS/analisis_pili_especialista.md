# 🎯 Análisis: PILI Modo Especialista (Patrón ITSE)

## 📊 Lógica del Artefacto ITSE

### **Estructura de Conversación por Etapas:**

```javascript
conversationState = {
  stage: 'initial',           // Etapa actual
  selectedCategory: null,     // Categoría seleccionada
  businessType: null,         // Tipo específico
  area: null,                 // Área en m²
  floors: 1,                  // Número de pisos
  riskLevel: null,            // Nivel de riesgo calculado
  clientName: null,           // Datos del cliente
  phone: null,
  address: null
}
```

### **Flujo de Conversación:**

```
1. initial → Selecciona categoría (8 opciones con botones)
   ↓
2. businessType → Selecciona tipo específico (botones dinámicos)
   ↓
3. area → Ingresa área en m² (input numérico)
   ↓
4. floors → Ingresa número de pisos (input numérico)
   ↓
5. quotation → Muestra cotización automática
   ↓
6. clientName → Captura nombre (si agenda)
   ↓
7. phone → Captura teléfono
   ↓
8. address → Captura dirección
   ↓
9. confirmation → Resumen y confirmación
```

### **Base de Conocimiento:**

```javascript
knowledgeBase = {
  // Precios municipales por nivel de riesgo
  municipalPrices: {
    BAJO: { price: 168.30, renewal: 90.30, days: 7 },
    MEDIO: { price: 208.60, renewal: 109.40, days: 7 },
    ALTO: { price: 703.00, renewal: 417.40, days: 7 },
    MUY_ALTO: { price: 1084.60, renewal: 629.20, days: 7 }
  },
  
  // Precios de servicio Tesla por nivel
  teslaServices: {
    BAJO: { min: 300, max: 500 },
    MEDIO: { min: 450, max: 650 },
    ALTO: { min: 800, max: 1200 },
    MUY_ALTO: { min: 1200, max: 1800 }
  },
  
  // Categorías con reglas de negocio
  categories: {
    SALUD: {
      types: ['Hospital', 'Clínica', ...],
      defaultRisk: 'ALTO',
      specialRules: 'Más de 500m² o 2+ pisos = MUY ALTO'
    },
    // ... más categorías
  }
}
```

### **Cálculo Inteligente de Riesgo:**

```javascript
determineRiskLevel(category, area, floors, businessType) {
  // Reglas específicas por categoría
  if (category === 'SALUD') {
    if (area > 500 || floors >= 2) return 'MUY_ALTO';
    return 'ALTO';
  }
  // ... más reglas
}
```

### **Generación Automática de Cotización:**

```javascript
showQuotation(riskLevel) {
  const municipal = knowledgeBase.municipalPrices[riskLevel];
  const tesla = knowledgeBase.teslaServices[riskLevel];
  const totalMin = municipal.price + tesla.min;
  const totalMax = municipal.price + tesla.max;
  
  // Muestra cotización formateada con desglose
}
```

---

## 🎨 Actualización de Colores

### **Colores Actuales del Frontend:**

```javascript
// App.jsx usa:
const colors = {
  primary: '#EAB308',      // Amarillo Tesla (yellow-600)
  secondary: '#1E40AF',    // Azul (blue-800)
  dark: '#1F2937',         // Gris oscuro (gray-800)
  accent: '#10B981'        // Verde (green-500)
}
```

### **Colores del Artefacto ITSE (a actualizar):**

```javascript
// ANTES (rojo/dorado):
const colors = {
  primary: '#8B0000',      // Rojo oscuro
  secondary: '#FFD700',    // Dorado
  fire: '#FF4500',         // Naranja fuego
  dark: '#2C0000'          // Rojo muy oscuro
}

// DESPUÉS (amarillo/azul Tesla):
const colors = {
  primary: '#EAB308',      // Amarillo Tesla
  secondary: '#1E40AF',    // Azul
  accent: '#10B981',       // Verde
  dark: '#1F2937'          // Gris oscuro
}
```

---

## 🔧 Patrón para los 10 Servicios Eléctricos

### **Servicios a Implementar:**

1. **Instalaciones Eléctricas Residenciales** 🏠
2. **Instalaciones Eléctricas Comerciales** 🏢
3. **Instalaciones Eléctricas Industriales** 🏭
4. **Sistemas de Puesta a Tierra** ⚡
5. **Sistemas Contraincendios** 🔥
6. **Domótica y Automatización** 🤖
7. **Expedientes Técnicos** 📋
8. **Saneamiento** 💧
9. **ITSE** ✅ (ya existe)
10. **Redes y CCTV** 📹

### **Estructura Base para Cada Servicio:**

```javascript
// Ejemplo: Instalaciones Eléctricas Residenciales

const SERVICIO_RESIDENCIAL = {
  nombre: "Instalaciones Eléctricas Residenciales",
  icono: "🏠",
  
  // Etapas de conversación
  stages: [
    'initial',
    'tipoVivienda',    // Casa, Departamento, Dúplex
    'area',            // m²
    'numPisos',        // Pisos
    'puntos',          // Puntos de luz
    'tomacorrientes',  // Tomacorrientes
    'quotation',       // Cotización
    'clientData',      // Datos del cliente
    'confirmation'     // Confirmación
  ],
  
  // Opciones por etapa
  options: {
    tipoVivienda: [
      { text: '🏠 Casa', value: 'CASA' },
      { text: '🏢 Departamento', value: 'DEPTO' },
      { text: '🏘️ Dúplex', value: 'DUPLEX' }
    ]
  },
  
  // Base de conocimiento
  knowledgeBase: {
    precios: {
      CASA: {
        base: 50,        // S/ por m²
        puntoLuz: 80,    // S/ por punto
        tomacorriente: 60 // S/ por toma
      },
      DEPTO: {
        base: 45,
        puntoLuz: 75,
        tomacorriente: 55
      },
      DUPLEX: {
        base: 55,
        puntoLuz: 85,
        tomacorriente: 65
      }
    },
    
    // Reglas de cálculo
    calcularCotizacion: (tipo, area, puntos, tomas) => {
      const precios = this.precios[tipo];
      const costoBase = area * precios.base;
      const costoPuntos = puntos * precios.puntoLuz;
      const costoTomas = tomas * precios.tomacorriente;
      const subtotal = costoBase + costoPuntos + costoTomas;
      const materiales = subtotal * 0.4;
      const manoObra = subtotal * 0.6;
      
      return {
        subtotal,
        materiales,
        manoObra,
        total: subtotal
      };
    }
  },
  
  // Mensajes por etapa
  messages: {
    initial: "¡Hola! Soy PILI, especialista en Instalaciones Eléctricas Residenciales.\n\n¿Qué tipo de vivienda es?",
    tipoVivienda: (tipo) => `Perfecto, es un ${tipo}.\n\n¿Cuál es el área total en m²?`,
    area: (area) => `📐 Área: ${area} m²\n\n¿Cuántos pisos tiene?`,
    numPisos: (pisos) => `🏢 Pisos: ${pisos}\n\n¿Cuántos puntos de luz necesitas?`,
    puntos: (puntos) => `💡 Puntos: ${puntos}\n\n¿Cuántos tomacorrientes?`,
    quotation: (cotizacion) => `
📊 COTIZACIÓN INSTALACIÓN ELÉCTRICA RESIDENCIAL

━━━━━━━━━━━━━━━━━━━━━━━
💰 DESGLOSE:

🏗️ Instalación base:
└ S/ ${cotizacion.costoBase.toFixed(2)}

💡 Puntos de luz (${cotizacion.puntos}):
└ S/ ${cotizacion.costoPuntos.toFixed(2)}

🔌 Tomacorrientes (${cotizacion.tomas}):
└ S/ ${cotizacion.costoTomas.toFixed(2)}

━━━━━━━━━━━━━━━━━━━━━━━
📈 TOTAL: S/ ${cotizacion.total.toFixed(2)}
━━━━━━━━━━━━━━━━━━━━━━━

✅ Incluye: Materiales + Mano de obra
⏱️ Tiempo: 5-7 días
🎁 Garantía: 1 año

¿Qué deseas hacer?`
  }
};
```

---

## 📁 Estructura de Archivos

```
frontend/src/
├── components/
│   ├── PiliModoEspecialista.jsx        # Componente base
│   └── especialistas/
│       ├── PiliResidencial.jsx         # 🏠 Residencial
│       ├── PiliComercial.jsx           # 🏢 Comercial
│       ├── PiliIndustrial.jsx          # 🏭 Industrial
│       ├── PiliPozoTierra.jsx          # ⚡ Pozo a Tierra
│       ├── PiliContraincendios.jsx     # 🔥 Contraincendios
│       ├── PiliDomotica.jsx            # 🤖 Domótica
│       ├── PiliExpedientes.jsx         # 📋 Expedientes
│       ├── PiliSaneamiento.jsx         # 💧 Saneamiento
│       ├── PiliITSE.jsx                # ✅ ITSE (actualizado)
│       └── PiliRedesCCTV.jsx           # 📹 Redes y CCTV
│
├── data/
│   └── serviciosConfig/
│       ├── residencial.js              # Config residencial
│       ├── comercial.js                # Config comercial
│       ├── industrial.js               # Config industrial
│       ├── pozoTierra.js               # Config pozo tierra
│       ├── contraincendios.js          # Config contraincendios
│       ├── domotica.js                 # Config domótica
│       ├── expedientes.js              # Config expedientes
│       ├── saneamiento.js              # Config saneamiento
│       ├── itse.js                     # Config ITSE
│       └── redesCCTV.js                # Config redes CCTV
│
└── utils/
    └── piliRouter.js                   # Router de servicios
```

---

## 🔄 Router de Servicios

```javascript
// utils/piliRouter.js

import PiliResidencial from '../components/especialistas/PiliResidencial';
import PiliComercial from '../components/especialistas/PiliComercial';
// ... imports

export const SERVICIOS_MAP = {
  'electrico-residencial': {
    component: PiliResidencial,
    nombre: 'Instalaciones Eléctricas Residenciales',
    icono: '🏠'
  },
  'electrico-comercial': {
    component: PiliComercial,
    nombre: 'Instalaciones Eléctricas Comerciales',
    icono: '🏢'
  },
  'electrico-industrial': {
    component: PiliIndustrial,
    nombre: 'Instalaciones Eléctricas Industriales',
    icono: '🏭'
  },
  'pozo-tierra': {
    component: PiliPozoTierra,
    nombre: 'Sistemas de Puesta a Tierra',
    icono: '⚡'
  },
  'contraincendios': {
    component: PiliContraincendios,
    nombre: 'Sistemas Contraincendios',
    icono: '🔥'
  },
  'domotica': {
    component: PiliDomotica,
    nombre: 'Domótica y Automatización',
    icono: '🤖'
  },
  'expedientes': {
    component: PiliExpedientes,
    nombre: 'Expedientes Técnicos',
    icono: '📋'
  },
  'saneamiento': {
    component: PiliSaneamiento,
    nombre: 'Saneamiento',
    icono: '💧'
  },
  'itse': {
    component: PiliITSE,
    nombre: 'ITSE',
    icono: '✅'
  },
  'redes-cctv': {
    component: PiliRedesCCTV,
    nombre: 'Redes y CCTV',
    icono: '📹'
  }
};

export const getPiliEspecialista = (servicioKey) => {
  return SERVICIOS_MAP[servicioKey] || SERVICIOS_MAP['electrico-residencial'];
};
```

---

## 🎯 Integración en App.jsx

```javascript
// En App.jsx

import { getPiliEspecialista } from './utils/piliRouter';

// Cuando usuario selecciona servicio
const handleSeleccionarServicio = (servicioKey) => {
  setServicioSeleccionado(servicioKey);
  const especialista = getPiliEspecialista(servicioKey);
  
  // Renderizar especialista correspondiente
  setPaso(2); // Ir al chat
};

// En el render
{paso === 2 && (
  <div>
    {(() => {
      const Especialista = getPiliEspecialista(servicioSeleccionado).component;
      return (
        <Especialista
          datosCliente={datosCliente}
          onCotizacionGenerada={(datos) => {
            setDatosEditables(datos);
            setMostrarPreview(true);
          }}
        />
      );
    })()}
  </div>
)}
```

---

## ✅ Plan de Implementación

### **Fase 1: Actualizar ITSE (30 min)**
1. Actualizar colores del artefacto ITSE
2. Mover a `components/especialistas/PiliITSE.jsx`
3. Crear config en `data/serviciosConfig/itse.js`

### **Fase 2: Crear Componente Base (1 hora)**
1. Crear `PiliModoEspecialista.jsx` (componente reutilizable)
2. Extraer lógica común (conversación por etapas, botones, inputs)
3. Hacer configurable por servicio

### **Fase 3: Implementar 3 Servicios Prioritarios (2 horas)**
1. **Residencial** (más común)
2. **Comercial** (segundo más común)
3. **Pozo a Tierra** (específico)

### **Fase 4: Implementar Servicios Restantes (3 horas)**
4. Industrial
5. Contraincendios
6. Domótica
7. Expedientes
8. Saneamiento
9. Redes y CCTV

### **Fase 5: Router e Integración (1 hora)**
1. Crear `piliRouter.js`
2. Integrar en `App.jsx`
3. Probar flujo completo

---

## 🎯 Resultado Final

**Usuario experimenta:**

```
1. Selecciona "Instalación Eléctrica Residencial"
   ↓
2. PILI activa modo especialista 🏠
   ↓
3. Pregunta específicas del servicio:
   - Tipo de vivienda
   - Área
   - Puntos de luz
   - Tomacorrientes
   ↓
4. Genera cotización automática
   ↓
5. Captura datos del cliente
   ↓
6. Confirmación y resumen
   ↓
7. Documento listo para descargar
```

**⏱️ Tiempo total: 1-2 minutos**

---

## 🚀 ¿Comenzamos?

**Orden sugerido:**
1. Actualizar colores ITSE
2. Crear componente base reutilizable
3. Implementar Residencial (el más importante)
4. Probar flujo completo
5. Replicar para otros servicios

¿Procedo con la implementación?
