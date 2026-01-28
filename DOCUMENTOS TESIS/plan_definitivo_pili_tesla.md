# 🎯 Plan Definitivo: PILI Modo Especialista con Colores Tesla

## 📸 Análisis de las Imágenes

### **Imagen 1: Chat de PILI (Izquierda) + Vista Previa (Derecha)**
![Chat y Vista Previa](file:///C:/Users/USUARIO/.gemini/antigravity/brain/e49dd4cc-507e-428d-8803-bba3270b39d6/uploaded_image_0_1766754531051.png)

**Observaciones:**
- ✅ Chat con fondo claro (a cambiar a oscuro)
- ✅ Botones amarillos/dorados
- ✅ Vista previa a la derecha (azul)
- ✅ Split screen (50/50)

### **Imagen 2: Selección de Tipo de Documento**
![Selección Documento](file:///C:/Users/USUARIO/.gemini/antigravity/brain/e49dd4cc-507e-428d-8803-bba3270b39d6/uploaded_image_1_1766754531051.png)

**Observaciones:**
- ✅ Fondo oscuro/negro
- ✅ Título amarillo/dorado
- ✅ Cotización Simple resaltada en dorado
- ✅ Cotización Compleja en azul oscuro

### **Imagen 3: Datos del Cliente**
![Datos Cliente](file:///C:/Users/USUARIO/.gemini/antigravity/brain/e49dd4cc-507e-428d-8803-bba3270b39d6/uploaded_image_2_1766754531051.png)

**Observaciones:**
- ✅ Fondo negro/oscuro
- ✅ Bordes amarillos/dorados
- ✅ Texto amarillo para labels
- ✅ Inputs con fondo oscuro y borde dorado
- ✅ Botón "Guardar Cliente" amarillo/dorado

### **Imagen 4: Tipo de Servicio (10 Servicios)**
![Tipo Servicio](file:///C:/Users/USUARIO/.gemini/antigravity/brain/e49dd4cc-507e-428d-8803-bba3270b39d6/uploaded_image_3_1766754531051.png)

**Observaciones:**
- ✅ Grid de 4 columnas x 2 filas
- ✅ Fondo oscuro
- ✅ Cada servicio con icono y nombre
- ✅ Servicios:
  1. ⚡ Electricidad
  2. 📋 Certificado ITSE
  3. 🔌 Puesta a Tierra
  4. 🔥 Contra Incendios
  5. 🏠 Domótica
  6. 📹 CCTV
  7. 🌐 Redes
  8. ⚙️ Automatización Industrial

---

## 🎨 Colores Tesla (Definitivos)

```javascript
const TESLA_COLORS = {
  // Fondos
  background: {
    primary: '#0A0A0A',        // Negro profundo
    secondary: '#1A1A1A',      // Gris muy oscuro
    card: 'rgba(26, 26, 26, 0.8)', // Transparente oscuro
    overlay: 'rgba(0, 0, 0, 0.7)'  // Overlay transparente
  },
  
  // Acentos principales
  accent: {
    gold: '#EAB308',           // Amarillo/Dorado Tesla
    goldDark: '#CA8A04',       // Dorado oscuro
    red: '#DC2626',            // Rojo Tesla
    redDark: '#991B1B'         // Rojo oscuro
  },
  
  // Texto
  text: {
    primary: '#FFFFFF',        // Blanco
    secondary: '#D1D5DB',      // Gris claro
    muted: '#9CA3AF',          // Gris medio
    gold: '#EAB308'            // Dorado para labels
  },
  
  // Bordes
  border: {
    gold: '#EAB308',
    dark: '#374151',
    light: 'rgba(234, 179, 8, 0.3)'
  },
  
  // Estados
  success: '#10B981',          // Verde
  warning: '#F59E0B',          // Naranja
  error: '#EF4444',            // Rojo
  info: '#3B82F6'              // Azul
};
```

---

## 🔄 Flujo Completo del Usuario

```
PASO 1: Inicio
┌─────────────────────────────────────┐
│ ¿Qué necesitas hacer?               │
│                                     │
│ 📊 COTIZACIONES                     │
│ ├─ ⚡ Cotización Simple ← SELECCIONA│
│ └─ 📑 Cotización Compleja           │
│                                     │
│ 📋 PROYECTOS                        │
│ 📄 INFORMES                         │
└─────────────────────────────────────┘

PASO 2: Datos del Cliente
┌─────────────────────────────────────┐
│ 👥 Datos del Cliente                │
│                                     │
│ 📝 Seleccionar Cliente              │
│ [+ Nuevo Cliente ▼]                 │
│                                     │
│ Nombre/Razón Social *               │
│ [Rogelio Infantas Contreras]        │
│                                     │
│ RUC *                               │
│ [10204438189]                       │
│                                     │
│ 📍 Dirección                        │
│ [Concepción]                        │
│                                     │
│ 📞 Teléfono        📧 Email         │
│ [906315971]        [rogelio@...]    │
│                                     │
│ [💾 Guardar Cliente]                │
└─────────────────────────────────────┘

PASO 3: Tipo de Servicio (10 Servicios)
┌─────────────────────────────────────┐
│ ⚙️ Tipo de Servicio                 │
│                                     │
│ ┌────────┬────────┬────────┬──────┐│
│ │⚡      │📋      │🔌      │🔥    ││
│ │Electric│ITSE    │Puesta  │Contra││
│ │idad    │        │Tierra  │Incen ││
│ ├────────┼────────┼────────┼──────┤│
│ │🏠      │📹      │🌐      │⚙️    ││
│ │Domótica│CCTV    │Redes   │Autom ││
│ │        │        │        │Indust││
│ └────────┴────────┴────────┴──────┘│
│                                     │
│ [Continuar →]                       │
└─────────────────────────────────────┘

PASO 4: PILI Especialista Activa
┌──────────────────┬──────────────────┐
│ 🤖 PILI          │ 👁️ Vista Previa  │
│ Electricidad     │                  │
├──────────────────┤                  │
│ ⚡ Instalación   │  COTIZACIÓN      │
│ Residencial      │                  │
│                  │  Cliente:        │
│ Perfecto, estoy  │  Rogelio...      │
│ analizando tu    │                  │
│ solicitud para   │  Servicio:       │
│ Instalaciones    │  Eléctrico       │
│ Eléctricas       │  Residencial     │
│ Residenciales.   │                  │
│                  │  Área: 80 m²     │
│ 📏 ¿Cuál es el   │  Puntos: 25      │
│ área del         │                  │
│ proyecto en m²?  │  Total:          │
│                  │  S/ 4,850.00     │
│ [80 M2]          │                  │
│                  │                  │
│ [Enviar]         │  [Descargar]     │
└──────────────────┴──────────────────┘
```

---

## 📁 Estructura de Archivos Definitiva

```
frontend/src/
├── components/
│   ├── PiliEspecialista.jsx           # Componente base
│   └── especialistas/
│       ├── PiliElectricidad.jsx       # ⚡ Electricidad (Residencial/Comercial/Industrial)
│       ├── PiliITSE.jsx               # 📋 ITSE
│       ├── PiliPozoTierra.jsx         # 🔌 Puesta a Tierra
│       ├── PiliContraincendios.jsx    # 🔥 Contra Incendios
│       ├── PiliDomotica.jsx           # 🏠 Domótica
│       ├── PiliCCTV.jsx               # 📹 CCTV
│       ├── PiliRedes.jsx              # 🌐 Redes
│       ├── PiliAutomatizacion.jsx     # ⚙️ Automatización Industrial
│       ├── PiliExpedientes.jsx        # 📄 Expedientes Técnicos
│       └── PiliSaneamiento.jsx        # 💧 Saneamiento
│
├── data/
│   ├── teslaColors.js                 # Colores Tesla
│   └── serviciosConfig.js             # Config de 10 servicios
│
└── styles/
    └── piliEspecialista.css           # Estilos Tesla
```

---

## 🎨 Componente Base: PiliEspecialista.jsx

```javascript
import React, { useState, useRef, useEffect } from 'react';
import { Send, Zap } from 'lucide-react';
import { TESLA_COLORS } from '../data/teslaColors';

const PiliEspecialista = ({ 
  servicio,           // "electricidad", "itse", etc.
  datosCliente,       // Del paso 2
  onCotizacionGenerada 
}) => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [conversationState, setConversationState] = useState({
    stage: 'initial',
    data: {}
  });
  
  const messagesEndRef = useRef(null);

  // Configuración por servicio
  const servicioConfig = getServicioConfig(servicio);

  useEffect(() => {
    // Mensaje inicial de PILI
    addBotMessage(servicioConfig.mensajeInicial, servicioConfig.botonesIniciales);
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const addBotMessage = (text, buttons = null) => {
    setMessages(prev => [...prev, { 
      sender: 'bot', 
      text, 
      buttons, 
      timestamp: new Date() 
    }]);
  };

  const addUserMessage = (text) => {
    setMessages(prev => [...prev, { 
      sender: 'user', 
      text, 
      timestamp: new Date() 
    }]);
  };

  const handleButtonClick = (value, label) => {
    addUserMessage(label);
    setIsTyping(true);

    setTimeout(() => {
      processResponse(value);
      setIsTyping(false);
    }, 800);
  };

  const processResponse = (value) => {
    // Lógica específica por servicio
    servicioConfig.processStage(
      conversationState,
      value,
      inputValue,
      {
        addBotMessage,
        setConversationState,
        onCotizacionGenerada
      }
    );
  };

  const handleSendMessage = () => {
    if (!inputValue.trim()) return;
    
    const message = inputValue.trim();
    addUserMessage(message);
    setInputValue('');
    setIsTyping(true);

    setTimeout(() => {
      processResponse(message);
      setIsTyping(false);
    }, 800);
  };

  return (
    <div style={{ 
      display: 'grid',
      gridTemplateColumns: '1fr 1fr',
      gap: '20px',
      height: '100vh',
      background: TESLA_COLORS.background.primary,
      padding: '20px'
    }}>
      {/* CHAT PILI (Izquierda) */}
      <div style={{
        background: TESLA_COLORS.background.card,
        borderRadius: '20px',
        border: `2px solid ${TESLA_COLORS.border.gold}`,
        display: 'flex',
        flexDirection: 'column',
        overflow: 'hidden'
      }}>
        {/* Header */}
        <div style={{
          background: `linear-gradient(135deg, ${TESLA_COLORS.background.secondary}, ${TESLA_COLORS.accent.goldDark})`,
          padding: '20px',
          borderBottom: `3px solid ${TESLA_COLORS.accent.gold}`,
          display: 'flex',
          alignItems: 'center',
          gap: '15px'
        }}>
          <div style={{
            width: '60px',
            height: '60px',
            borderRadius: '50%',
            background: `linear-gradient(135deg, ${TESLA_COLORS.accent.gold}, ${TESLA_COLORS.accent.goldDark})`,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            border: `3px solid ${TESLA_COLORS.background.primary}`
          }}>
            <Zap size={32} color={TESLA_COLORS.background.primary} strokeWidth={3} />
          </div>
          <div>
            <h1 style={{ 
              color: TESLA_COLORS.accent.gold, 
              margin: 0, 
              fontSize: '24px',
              fontWeight: 'bold'
            }}>
              🤖 PILI - {servicioConfig.nombre}
            </h1>
            <p style={{ 
              color: TESLA_COLORS.text.secondary, 
              margin: 0, 
              fontSize: '14px'
            }}>
              Tesla Electricidad
            </p>
          </div>
        </div>

        {/* Messages */}
        <div style={{
          flex: 1,
          overflowY: 'auto',
          padding: '20px',
          background: TESLA_COLORS.background.primary
        }}>
          {messages.map((msg, index) => (
            <div key={index} style={{
              display: 'flex',
              justifyContent: msg.sender === 'bot' ? 'flex-start' : 'flex-end',
              marginBottom: '15px'
            }}>
              <div style={{
                maxWidth: '75%',
                padding: '12px 18px',
                borderRadius: msg.sender === 'bot' ? '20px 20px 20px 5px' : '20px 20px 5px 20px',
                background: msg.sender === 'bot' 
                  ? `linear-gradient(135deg, ${TESLA_COLORS.background.secondary}, ${TESLA_COLORS.accent.goldDark})`
                  : `linear-gradient(135deg, ${TESLA_COLORS.accent.gold}, ${TESLA_COLORS.accent.goldDark})`,
                color: msg.sender === 'bot' ? TESLA_COLORS.text.primary : TESLA_COLORS.background.primary,
                boxShadow: '0 4px 15px rgba(234, 179, 8, 0.3)',
                whiteSpace: 'pre-line'
              }}>
                <div dangerouslySetInnerHTML={{ __html: msg.text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') }} />
                
                {msg.buttons && (
                  <div style={{ marginTop: '15px', display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
                    {msg.buttons.map((btn, btnIndex) => (
                      <button
                        key={btnIndex}
                        onClick={() => handleButtonClick(btn.value, btn.text)}
                        style={{
                          background: TESLA_COLORS.accent.gold,
                          color: TESLA_COLORS.background.primary,
                          border: 'none',
                          padding: '10px 20px',
                          borderRadius: '20px',
                          cursor: 'pointer',
                          fontWeight: 'bold',
                          fontSize: '14px',
                          transition: 'all 0.2s',
                          boxShadow: '0 2px 10px rgba(234, 179, 8, 0.4)'
                        }}
                      >
                        {btn.text}
                      </button>
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))}
          
          {isTyping && (
            <div style={{ display: 'flex', gap: '5px', padding: '10px' }}>
              <div style={{ width: '10px', height: '10px', borderRadius: '50%', background: TESLA_COLORS.accent.gold, animation: 'bounce 1.4s infinite' }} />
              <div style={{ width: '10px', height: '10px', borderRadius: '50%', background: TESLA_COLORS.accent.goldDark, animation: 'bounce 1.4s infinite 0.2s' }} />
              <div style={{ width: '10px', height: '10px', borderRadius: '50%', background: TESLA_COLORS.accent.red, animation: 'bounce 1.4s infinite 0.4s' }} />
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>

        {/* Input */}
        {shouldShowInput(conversationState.stage) && (
          <div style={{
            padding: '15px',
            borderTop: `2px solid ${TESLA_COLORS.border.gold}`,
            background: TESLA_COLORS.background.secondary,
            display: 'flex',
            gap: '10px'
          }}>
            <input
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
              placeholder="Escribe tu respuesta..."
              style={{
                flex: 1,
                padding: '12px 20px',
                border: `2px solid ${TESLA_COLORS.border.gold}`,
                borderRadius: '25px',
                fontSize: '15px',
                outline: 'none',
                background: TESLA_COLORS.background.primary,
                color: TESLA_COLORS.text.primary
              }}
            />
            <button
              onClick={handleSendMessage}
              style={{
                background: TESLA_COLORS.accent.gold,
                border: 'none',
                borderRadius: '50%',
                width: '50px',
                height: '50px',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                boxShadow: '0 2px 10px rgba(234, 179, 8, 0.4)'
              }}
            >
              <Send size={24} color={TESLA_COLORS.background.primary} />
            </button>
          </div>
        )}
      </div>

      {/* VISTA PREVIA (Derecha) */}
      <div style={{
        background: 'white',
        borderRadius: '20px',
        border: `2px solid ${TESLA_COLORS.border.gold}`,
        overflow: 'auto',
        padding: '20px'
      }}>
        {/* Aquí va la vista previa del documento */}
        <h2>Vista Previa</h2>
        {/* Renderizar plantilla editable */}
      </div>
    </div>
  );
};

export default PiliEspecialista;
```

---

## 🎯 Configuración de 10 Servicios

```javascript
// data/serviciosConfig.js

export const SERVICIOS_CONFIG = {
  'electricidad': {
    nombre: 'Instalaciones Eléctricas',
    icono: '⚡',
    mensajeInicial: `¡Hola! Soy PILI, especialista en Instalaciones Eléctricas de Tesla.

¿Qué tipo de instalación necesitas?`,
    botonesIniciales: [
      { text: '🏠 Residencial', value: 'RESIDENCIAL' },
      { text: '🏢 Comercial', value: 'COMERCIAL' },
      { text: '🏭 Industrial', value: 'INDUSTRIAL' }
    ],
    // ... más config
  },
  
  'itse': {
    nombre: 'Certificado ITSE',
    icono: '📋',
    // ... config ITSE
  },
  
  'pozo-tierra': {
    nombre: 'Puesta a Tierra',
    icono: '🔌',
    // ... config
  },
  
  // ... 7 servicios más
};
```

---

## ✅ Plan de Implementación

### **Fase 1: Actualizar Colores (30 min)**
1. Crear `teslaColors.js` con paleta definitiva
2. Actualizar artefacto ITSE con nuevos colores
3. Probar visualmente

### **Fase 2: Componente Base (1 hora)**
1. Crear `PiliEspecialista.jsx` con diseño Tesla
2. Split screen (Chat | Vista Previa)
3. Estilos oscuros con dorado/rojo

### **Fase 3: Implementar 3 Servicios (2 horas)**
1. Electricidad (Residencial/Comercial/Industrial)
2. ITSE (ya existe, adaptar)
3. Pozo a Tierra

### **Fase 4: Servicios Restantes (3 horas)**
4-10. Resto de servicios

### **Fase 5: Integración (1 hora)**
1. Conectar con flujo existente
2. Paso 3 → Selección de servicio → Activa PILI

---

## 🚀 ¿Comenzamos?

¿Procedo con la implementación?
