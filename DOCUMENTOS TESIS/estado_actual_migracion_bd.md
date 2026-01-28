# Estado Actual del Sistema - Análisis Crítico

**Fecha:** 2026-01-08 23:23  
**Tiempo invertido:** 4 horas  
**Objetivo original:** Integrar BD como SSOT para que chat solo pregunte lo que falta

---

## ✅ Lo que SÍ se logró (Infraestructura)

### 1. Base de Datos Migrada
- ✅ 11 campos PMI agregados a tabla `proyectos`
- ✅ Migración con Alembic exitosa
- ✅ Backup de BD creado
- ✅ Campos nullable (datos antiguos preservados)

**Campos agregados:**
```sql
servicio VARCHAR(50)
industria VARCHAR(50)
presupuesto NUMERIC(12,2)
moneda VARCHAR(3)
duracion_total INTEGER
tipo_dias VARCHAR(20)
area_m2 NUMERIC(10,2)
tiene_area BOOLEAN
alcance_proyecto TEXT
ubicacion VARCHAR(200)
normativa VARCHAR(200)
```

### 2. Backend Actualizado
- ✅ Schemas Pydantic con 11 campos PMI
- ✅ Endpoint `POST /api/proyectos/` guarda todos los campos
- ✅ Endpoint `GET /api/proyectos/{id}` retorna datos completos

### 3. Frontend Conectado
- ✅ `App.jsx` llama `guardarProyectoEnBD()` al iniciar chat
- ✅ Proyecto se guarda en BD (verificado)
- ✅ `proyectoId` se pasa al componente chat

### 4. Chatbot Mejorado
- ✅ Mensaje inicial muestra servicio e industria
- ✅ Guarda datos del formulario en estado
- ✅ Incluye servicio e industria en `datos_generados`

---

## ❌ Lo que NO se implementó (Funcionalidad)

### 1. Chat NO lee desde BD
**Estado actual:**
```javascript
// Chat recibe proyectoId pero NO lo usa
<PiliElectricidadProyectoComplejoPMIChat 
  proyectoId={proyectoId}  // ✅ Se pasa
  // ❌ Pero chatbot backend NO lee desde BD
/>
```

**Lo que falta:**
- Chatbot backend debe hacer `GET /api/proyectos/{proyecto_id}`
- Cargar datos en el estado inicial
- Usar esos datos en lugar de preguntar

### 2. Chat NO salta preguntas
**Estado actual:**
- Chat muestra datos del formulario
- Pero sigue preguntando TODO desde cero
- No hay lógica para saltar preguntas respondidas

**Lo que falta:**
- Verificar qué datos ya existen
- Saltar a la siguiente pregunta no respondida
- Solo preguntar lo que falta

### 3. Vista Previa NO lee desde BD
**Estado actual:**
```javascript
// Vista previa lee de datosEditables (memoria)
<EDITABLE_PROYECTO_COMPLEJO datos={datosEditables} />
```

**Lo que falta:**
- Vista previa debe leer desde BD si existe proyectoId
- Mostrar datos guardados + datos del chat
- Actualizar BD cuando se edita

---

## 🔄 Flujo ACTUAL (Como funciona HOY)

```
1. Usuario llena formulario
   ↓
2. Click "Comenzar Chat"
   ├─→ Guarda en BD ✅ (proyecto_id=13)
   └─→ Abre chat
   ↓
3. Chat pregunta TODO ❌
   (No usa datos de BD ni formulario)
   ↓
4. Chat genera datos_generados
   ├─→ servicio: "electricidad"
   ├─→ industria: "construccion"
   └─→ Otros datos...
   ↓
5. setDatosEditables(datos_generados)
   ↓
6. Vista Previa lee datosEditables ✅
   (Muestra datos del chat)
   ↓
7. Usuario genera documento
   ↓
8. Backend recibe datos del chat
   ↓
9. Generador usa servicio/industria
   ↓
10. Título: "ELECTRICIDAD - CONSTRUCCIÓN" ✅
```

**Problema:** El flujo funciona PERO:
- BD se usa solo para guardar (no para leer)
- Chat pregunta todo (no aprovecha formulario)
- Vista previa no muestra datos de BD

---

## 🎯 Flujo DESEADO (SSOT con BD)

```
1. Usuario llena formulario
   ↓
2. Click "Comenzar Chat"
   ├─→ Guarda en BD ✅
   └─→ proyecto_id=13
   ↓
3. Chat backend lee BD ❌ (FALTA)
   GET /api/proyectos/13
   ├─→ servicio: "electricidad"
   ├─→ industria: "construccion"
   ├─→ nombre_proyecto: "..."
   └─→ presupuesto: 150000
   ↓
4. Chat verifica qué falta ❌ (FALTA)
   ✅ Tiene: servicio, industria, nombre, presupuesto
   ❌ Falta: descripción detallada, stakeholders, riesgos
   ↓
5. Chat solo pregunta lo que falta ✅
   "Describe los stakeholders principales..."
   ↓
6. Chat completa datos
   datos_completos = datos_bd + datos_chat
   ↓
7. Vista Previa lee BD + Chat ❌ (FALTA)
   GET /api/proyectos/13
   + datos del chat
   ↓
8. Usuario edita y genera
   ↓
9. Título: "ELECTRICIDAD - CONSTRUCCIÓN" ✅
```

---

## 📋 Lo que REALMENTE falta implementar

### Paso 1: Chat Backend lee desde BD (1 hora)

**Archivo:** `Pili_ChatBot/pili_electricidad_proyecto_complejo_pmi_chatbot.py`

```python
def procesar(self, mensaje: str, estado: Dict) -> Dict:
    # Si viene proyecto_id, leer desde BD
    proyecto_id = estado.get("proyecto_id")
    
    if proyecto_id and etapa == "inicial":
        # Hacer request a BD
        import requests
        response = requests.get(f"http://localhost:8000/api/proyectos/{proyecto_id}")
        if response.ok:
            proyecto_data = response.json()
            # Cargar datos en estado
            estado["servicio"] = proyecto_data.get("servicio")
            estado["industria"] = proyecto_data.get("industria")
            estado["nombre_proyecto"] = proyecto_data.get("nombre")
            # ... resto de campos
```

### Paso 2: Chat salta preguntas respondidas (2 horas)

**Lógica:**
```python
# Verificar qué datos ya existen
datos_existentes = []
if estado.get("servicio"):
    datos_existentes.append("servicio")
if estado.get("nombre_proyecto"):
    datos_existentes.append("nombre")

# Saltar a primera pregunta no respondida
if "descripcion" not in datos_existentes:
    estado["etapa"] = "descripcion"
elif "stakeholders" not in datos_existentes:
    estado["etapa"] = "stakeholders"
# ...
```

### Paso 3: Vista Previa lee desde BD (30 min)

**Archivo:** `frontend/src/components/EDITABLE_PROYECTO_COMPLEJO.jsx`

```javascript
useEffect(() => {
  if (proyectoId) {
    // Leer desde BD
    fetch(`http://localhost:8000/api/proyectos/${proyectoId}`)
      .then(res => res.json())
      .then(data => {
        // Combinar con datos del chat
        const datosCombinados = {
          ...data,
          ...datos  // datos del chat tienen prioridad
        };
        setDatosCompletos(datosCombinados);
      });
  }
}, [proyectoId, datos]);
```

---

## 💡 Recomendación

**Opción A: Completar SSOT (3.5 horas más)**
- Implementar los 3 pasos faltantes
- Sistema completo con BD como SSOT
- Chat inteligente que salta preguntas

**Opción B: Dejar como está (0 horas)**
- BD sirve para guardar proyectos
- Flujo actual funciona (chat → vista previa → generador)
- Título dinámico funciona si usas conversación nueva
- En el futuro se puede completar SSOT

**Opción C: Arreglo mínimo (30 min)**
- Solo asegurar que título dinámico funcione
- Verificar que servicio/industria lleguen al generador
- No tocar BD ni chat

---

## 🔍 Verificación del Título Dinámico

**Para verificar si funciona:**

1. F5 (recargar página)
2. Llenar formulario PMI
3. Seleccionar **Electricidad** y **Construcción**
4. Iniciar chat NUEVO
5. Completar conversación
6. Generar documento
7. Abrir Word
8. **Verificar título:** Debe ser "ELECTRICIDAD - CONSTRUCCIÓN"

**Si NO funciona:**
- Revisar console logs
- Verificar que `datos_generados` tenga servicio/industria
- Verificar que generador reciba opciones correctas

---

## 📊 Resumen Ejecutivo

**Tiempo invertido:** 4 horas  
**Progreso real:** 40% del objetivo original

**Completado:**
- ✅ Infraestructura BD (100%)
- ✅ Endpoints backend (100%)
- ✅ Frontend guarda en BD (100%)

**Pendiente:**
- ❌ Chat lee desde BD (0%)
- ❌ Chat salta preguntas (0%)
- ❌ Vista previa lee BD (0%)

**Próxima decisión:** ¿Completar SSOT o dejar funcional como está?
