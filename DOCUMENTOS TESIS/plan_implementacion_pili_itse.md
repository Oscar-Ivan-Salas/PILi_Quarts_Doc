# 🎯 PLAN DE IMPLEMENTACIÓN QUIRÚRGICA - PILI ITSE PROFESIONAL

## ✅ OBJETIVO

Crear diseño profesional con burbujas rojas y botones dorados para PILI ITSE, **SIN TOCAR:**
- ❌ Generación de documentos
- ❌ Base de datos
- ❌ Resto del frontend
- ❌ Backend (solo conectar)

---

## 📁 ARCHIVOS A CREAR (NUEVOS)

### 1. `frontend/src/components/PiliITSEChat.jsx`
**Descripción:** Componente React con diseño profesional

**Características:**
- Fondo degradado rojo-naranja (#2C0000 → #8B0000 → #FF4500)
- Header con logo de rayo dorado
- Burbujas de chat rojas para PILI
- Burbujas doradas para usuario
- Botones blancos con borde dorado
- Footer con información de contacto
- Conecta con `/api/chat/chat-contextualizado`

**Tamaño estimado:** ~400 líneas

---

## 📝 ARCHIVOS A MODIFICAR (MÍNIMO)

### 1. `frontend/src/App.jsx`
**Cambios quirúrgicos:**

#### Línea ~107 (import)
```javascript
// ANTES
import ChatIA from './components/ChatIA';

// DESPUÉS
import ChatIA from './components/ChatIA';
import PiliITSEChat from './components/PiliITSEChat';  // ← AGREGAR
```

#### Línea ~2000 (renderizado condicional)
```javascript
// AGREGAR CONDICIÓN
{tipoFlujo === 'cotizacion-simple' && servicioSeleccionado === 'itse' ? (
  <PiliITSEChat
    onCotizacionGenerada={(cot) => {
      setCotizacion(cot);
      setDatosEditables(cot);
    }}
    onBotonesUpdate={(botones) => setBotonesContextuales(botones)}
  />
) : (
  <ChatIA
    tipoFlujo={tipoFlujo}
    contexto={{
      servicioSeleccionado,
      industriaSeleccionada,
      contextoUsuario,
      // ... resto igual
    }}
    // ... props existentes
  />
)}
```

**Total de líneas modificadas:** ~15 líneas

---

## 🎨 DISEÑO DEL COMPONENTE

### Estructura Visual

```
┌─────────────────────────────────────────────┐
│ 🔴 HEADER (Degradado Rojo-Naranja)        │
│   ⚡ Logo   Pili - Especialista ITSE      │
│            Tesla Electricidad • Huancayo   │
└─────────────────────────────────────────────┘
│                                             │
│  ┌──────────────────────────────────┐      │
│  │ 🔴 PILI: ¡Hola! Soy Pili...     │      │
│  │                                  │      │
│  │  [🏥 Salud] [🎓 Educación]      │      │
│  │  [🏨 Hospedaje] [🏪 Comercio]   │      │
│  └──────────────────────────────────┘      │
│                                             │
│      ┌──────────────────────────────┐      │
│      │ 🟡 Usuario: Certificado ITSE │      │
│      └──────────────────────────────┘      │
│                                             │
│  ┌──────────────────────────────────┐      │
│  │ 🔴 PILI: Perfecto, sector SALUD │      │
│  │  [Hospital] [Clínica]           │      │
│  └──────────────────────────────────┘      │
│                                             │
└─────────────────────────────────────────────┘
│ 📝 Input: [Escribe tu respuesta...]  [📤] │
└─────────────────────────────────────────────┘
│ 📞 906 315 961  📍 San Juan  🕐 Lun-Sáb   │
└─────────────────────────────────────────────┘
```

---

## 🔌 INTEGRACIÓN CON BACKEND

### Endpoint usado
```
POST /api/chat/chat-contextualizado
```

### Payload
```json
{
  "tipo_flujo": "cotizacion-simple",
  "mensaje": "Certificado ITSE",
  "historial": [],
  "contexto_adicional": "Servicio: itse",
  "generar_html": true
}
```

### Respuesta esperada
```json
{
  "success": true,
  "respuesta": "Perfecto, sector SALUD...",
  "botones": [
    {"text": "Hospital", "value": "Hospital"},
    {"text": "Clínica", "value": "Clínica"}
  ],
  "stage": "tipo",
  "progreso": "2/5"
}
```

---

## 🎨 PALETA DE COLORES

```css
/* Fondo principal */
background: linear-gradient(135deg, #2C0000 0%, #8B0000 50%, #FF4500 100%);

/* Header */
background: linear-gradient(90deg, #8B0000, #FF4500);
border-bottom: 3px solid #D4AF37;

/* Logo circle */
background: linear-gradient(135deg, #D4AF37, #FFA500);
box-shadow: 0 0 20px rgba(255, 215, 0, 0.5);
border: 3px solid #8B0000;

/* Burbujas PILI */
background: linear-gradient(135deg, #8B0000, #FF4500);
color: white;

/* Burbujas Usuario */
background: linear-gradient(135deg, #D4AF37, #FFA500);
color: #2C0000;

/* Botones */
background: white;
color: #8B0000;
border: 2px solid #D4AF37;
/* Hover */
background: #D4AF37;
transform: scale(1.05);

/* Footer */
background: rgba(0, 0, 0, 0.3);
color: white;
```

---

## ✅ VERIFICACIONES DE SEGURIDAD

### Antes de implementar
- [x] Confirmar que NO se toca generación de documentos
- [x] Confirmar que NO se toca base de datos
- [x] Confirmar que solo se crea 1 archivo nuevo
- [x] Confirmar que solo se modifica App.jsx (15 líneas)

### Durante implementación
- [ ] Probar que ChatIA.jsx sigue funcionando para otros servicios
- [ ] Probar que generación de documentos sigue funcionando
- [ ] Probar que base de datos sigue funcionando

### Después de implementar
- [ ] Verificar que ITSE usa PiliITSEChat
- [ ] Verificar que otros servicios usan ChatIA
- [ ] Verificar que documentos se generan correctamente
- [ ] Verificar que BD guarda datos correctamente

---

## 📊 IMPACTO ESTIMADO

| Componente | Cambios | Riesgo |
|------------|---------|--------|
| **PiliITSEChat.jsx** | Nuevo archivo | ✅ Bajo (no afecta nada) |
| **App.jsx** | 15 líneas | ✅ Bajo (solo condicional) |
| **ChatIA.jsx** | 0 líneas | ✅ Sin cambios |
| **Generación docs** | 0 líneas | ✅ Sin cambios |
| **Base de datos** | 0 líneas | ✅ Sin cambios |
| **Backend** | 0 líneas | ✅ Sin cambios |

---

## 🚀 ORDEN DE EJECUCIÓN

1. ✅ Crear `PiliITSEChat.jsx` con diseño completo
2. ✅ Probar componente aislado
3. ✅ Modificar `App.jsx` con condicional
4. ✅ Probar integración
5. ✅ Verificar que otros servicios siguen funcionando
6. ✅ Verificar que documentos se generan
7. ✅ Verificar que BD funciona

**Tiempo estimado:** 30-40 minutos

---

## ⚠️ REGLAS QUIRÚRGICAS

1. **NO tocar** archivos de generación de documentos
2. **NO tocar** archivos de base de datos
3. **NO tocar** `ChatIA.jsx` (otros servicios lo usan)
4. **SOLO crear** `PiliITSEChat.jsx`
5. **SOLO modificar** `App.jsx` (condicional de 15 líneas)
6. **PROBAR** después de cada cambio

---

## ✅ APROBACIÓN REQUERIDA

**¿Proceder con este plan?**

- ✅ Crea SOLO 1 archivo nuevo
- ✅ Modifica SOLO 15 líneas en App.jsx
- ✅ NO toca generación de documentos
- ✅ NO toca base de datos
- ✅ NO rompe funcionalidad existente

**Esperando confirmación para proceder...**
