# 🔄 PLAN DE MIGRACIÓN: De 3,500 Líneas a Arquitectura Modular

## 🎯 TU PREGUNTA

**"¿Qué pasa con nuestro código de 3,500 líneas? ¿Dónde vas a crear la nueva estructura? ¿Cómo lo vas a integrar?"**

---

## 📋 RESPUESTA DIRECTA

### **¿Qué pasa con el código actual?**

**OPCIÓN 1: Migración Gradual (RECOMENDADO)**
```
✅ Mantenemos pili_local_specialists.py como FALLBACK
✅ Creamos nueva estructura en paralelo
✅ Migramos servicio por servicio
✅ Sistema funciona durante toda la migración
```

**OPCIÓN 2: Reemplazo Total**
```
❌ Borramos pili_local_specialists.py
❌ Creamos todo nuevo
❌ Sistema no funciona hasta terminar
❌ Alto riesgo
```

**Vamos con OPCIÓN 1 (Migración Gradual)**

---

## 📁 ESTRUCTURA COMPLETA

### **Dónde se crea todo:**

```
backend/app/services/
├── pili_local_specialists.py          # ← MANTENER (fallback)
│                                       #    3,500 líneas actuales
│
├── pili_integrator.py                 # ← MODIFICAR (agregar lógica)
│
└── pili/                              # ← NUEVA CARPETA
    ├── __init__.py
    │
    ├── core/                          # ← MOTORES REUTILIZABLES
    │   ├── __init__.py
    │   ├── conversation_engine.py     # 200 líneas
    │   ├── validation_engine.py       # 100 líneas
    │   └── calculation_engine.py      # 100 líneas
    │
    ├── config/                        # ← CONFIGURACIONES YAML
    │   ├── itse.yaml                  # 50 líneas
    │   ├── electricidad.yaml          # 50 líneas
    │   ├── pozo_tierra.yaml           # 50 líneas
    │   ├── contraincendios.yaml       # 50 líneas
    │   ├── domotica.yaml              # 50 líneas
    │   ├── cctv.yaml                  # 50 líneas
    │   ├── redes.yaml                 # 50 líneas
    │   ├── automatizacion.yaml        # 50 líneas
    │   ├── expedientes.yaml           # 50 líneas
    │   └── saneamiento.yaml           # 50 líneas
    │
    ├── templates/                     # ← PLANTILLAS DE MENSAJES
    │   └── messages.yaml              # 200 líneas
    │
    ├── knowledge/                     # ← BASES DE CONOCIMIENTO
    │   ├── __init__.py
    │   ├── itse_kb.py                 # 100 líneas
    │   ├── electricidad_kb.py         # 100 líneas
    │   └── ... (8 más)
    │
    └── specialist.py                  # ← CLASE UNIVERSAL
                                       # 300 líneas
```

**Total archivos nuevos:** ~25 archivos
**Total líneas nuevas:** ~2,000 líneas
**Código actual:** Se mantiene como fallback

---

## 🔄 ESTRATEGIA DE INTEGRACIÓN

### **Sistema de Fallback de 4 Niveles:**

```
┌─────────────────────────────────────────────────────────┐
│  NIVEL 1: Gemini (si está disponible)                  │
└────────────────────┬────────────────────────────────────┘
                     │ si falla
                     ▼
┌─────────────────────────────────────────────────────────┐
│  NIVEL 2: NUEVA ARQUITECTURA (pili/)                    │
│  - Usa UniversalSpecialist                              │
│  - Lee configuración YAML                               │
│  - Motores reutilizables                                │
└────────────────────┬────────────────────────────────────┘
                     │ si falla o servicio no migrado
                     ▼
┌─────────────────────────────────────────────────────────┐
│  NIVEL 3: CÓDIGO ACTUAL (pili_local_specialists.py)    │
│  - 3,500 líneas actuales                                │
│  - Funciona como siempre                                │
└────────────────────┬────────────────────────────────────┘
                     │ si falla
                     ▼
┌─────────────────────────────────────────────────────────┐
│  NIVEL 4: PILI Brain (básico)                          │
└─────────────────────────────────────────────────────────┘
```

---

## 💻 CÓDIGO DE INTEGRACIÓN

### **Modificación en `pili_integrator.py`:**

```python
# pili_integrator.py

# Imports existentes
from app.services.pili_local_specialists import process_with_local_specialist

# NUEVO: Import de nueva arquitectura
try:
    from app.services.pili.specialist import UniversalSpecialist
    NUEVA_ARQUITECTURA_DISPONIBLE = True
except ImportError:
    NUEVA_ARQUITECTURA_DISPONIBLE = False
    logger.warning("Nueva arquitectura no disponible, usando código legacy")

# Lista de servicios migrados a nueva arquitectura
SERVICIOS_MIGRADOS = [
    "itse",  # Primer servicio migrado
    # "electricidad",  # Agregar cuando se migre
    # "pozo-tierra",   # Agregar cuando se migre
]

class PILIIntegrator:
    # ... código existente ...
    
    def _generar_respuesta_chat(self, mensaje, tipo_flujo, historial, servicio, datos_acumulados):
        """
        Genera respuesta con sistema de fallback de 4 niveles
        """
        
        # NIVEL 1: Intentar con Gemini
        if GEMINI_DISPONIBLE:
            try:
                respuesta = gemini_service.chat_conversacional(...)
                if respuesta:
                    return respuesta
            except Exception as e:
                logger.warning(f"Gemini falló: {e}")
        
        # NIVEL 2: NUEVA ARQUITECTURA (si servicio está migrado)
        if NUEVA_ARQUITECTURA_DISPONIBLE and servicio in SERVICIOS_MIGRADOS:
            try:
                logger.info(f"Usando NUEVA arquitectura para {servicio}")
                
                # Crear especialista universal
                specialist = UniversalSpecialist(servicio, tipo_flujo)
                
                # Procesar mensaje
                state = datos_acumulados or {}
                respuesta = specialist.process(mensaje, state)
                
                # Retornar respuesta
                return {
                    "texto": respuesta.get("texto", ""),
                    "botones": respuesta.get("botones", []),
                    "datos_generados": respuesta.get("datos_generados"),
                    "stage": respuesta.get("stage"),
                    "state": respuesta.get("state", state),
                    "progreso": respuesta.get("progreso", "")
                }
            
            except Exception as e:
                logger.error(f"Nueva arquitectura falló: {e}")
                logger.info("Fallback a código legacy")
        
        # NIVEL 3: CÓDIGO ACTUAL (pili_local_specialists.py)
        if ESPECIALISTAS_LOCALES_DISPONIBLES:
            try:
                logger.info(f"Usando código LEGACY para {servicio}")
                
                # Usar código actual
                respuesta = process_with_local_specialist(
                    service=servicio,
                    message=mensaje,
                    conversation_state=datos_acumulados or {}
                )
                
                return respuesta
            
            except Exception as e:
                logger.error(f"Código legacy falló: {e}")
        
        # NIVEL 4: PILI Brain (fallback final)
        logger.info("Usando PILI Brain como último recurso")
        return self._generar_respuesta_pili_local(mensaje, servicio, tipo_flujo, datos_acumulados)
```

---

## 📅 PLAN DE MIGRACIÓN PASO A PASO

### **FASE 1: Setup Inicial (Día 1 - 2 horas)**

**Objetivo:** Crear estructura base sin romper nada

```bash
# 1. Crear carpeta pili/
mkdir backend/app/services/pili
mkdir backend/app/services/pili/core
mkdir backend/app/services/pili/config
mkdir backend/app/services/pili/templates
mkdir backend/app/services/pili/knowledge

# 2. Crear archivos __init__.py
touch backend/app/services/pili/__init__.py
touch backend/app/services/pili/core/__init__.py
touch backend/app/services/pili/knowledge/__init__.py
```

**Archivos a crear:**
- ✅ `pili/__init__.py`
- ✅ `pili/core/__init__.py`
- ✅ `pili/core/conversation_engine.py`
- ✅ `pili/core/validation_engine.py`
- ✅ `pili/core/calculation_engine.py`
- ✅ `pili/specialist.py`

**Estado del sistema:** ✅ Funciona normal (usa código actual)

---

### **FASE 2: Migrar ITSE (Día 2 - 4 horas)**

**Objetivo:** Migrar primer servicio como piloto

**Archivos a crear:**
- ✅ `pili/config/itse.yaml`
- ✅ `pili/templates/messages.yaml` (solo sección ITSE)
- ✅ `pili/knowledge/itse_kb.py`

**Modificar:**
- ✅ `pili_integrator.py` (agregar lógica de fallback)
- ✅ Agregar `"itse"` a `SERVICIOS_MIGRADOS`

**Probar:**
```python
# Test manual
specialist = UniversalSpecialist("itse", "cotizacion-simple")
response = specialist.process("Hola", {})
print(response)
```

**Estado del sistema:** 
- ✅ ITSE usa nueva arquitectura
- ✅ Otros 9 servicios usan código actual
- ✅ Todo funciona

---

### **FASE 3: Migrar Electricidad (Día 3 - 3 horas)**

**Objetivo:** Migrar segundo servicio

**Archivos a crear:**
- ✅ `pili/config/electricidad.yaml`
- ✅ `pili/knowledge/electricidad_kb.py`

**Modificar:**
- ✅ `pili/templates/messages.yaml` (agregar sección Electricidad)
- ✅ Agregar `"electricidad"` a `SERVICIOS_MIGRADOS`

**Estado del sistema:**
- ✅ ITSE + Electricidad usan nueva arquitectura
- ✅ Otros 8 servicios usan código actual

---

### **FASE 4: Migrar Servicios Restantes (Día 4-5 - 6 horas)**

**Objetivo:** Migrar los 8 servicios restantes

**Por cada servicio:**
1. Crear `config/{servicio}.yaml`
2. Crear `knowledge/{servicio}_kb.py`
3. Agregar mensajes a `templates/messages.yaml`
4. Agregar a `SERVICIOS_MIGRADOS`
5. Probar

**Servicios:**
- ✅ pozo-tierra
- ✅ contraincendios
- ✅ domotica
- ✅ cctv
- ✅ redes
- ✅ automatizacion
- ✅ expedientes
- ✅ saneamiento

**Estado del sistema:**
- ✅ Todos los servicios usan nueva arquitectura
- ✅ Código actual queda como fallback

---

### **FASE 5: Limpieza (Día 6 - 1 hora)**

**Objetivo:** Limpiar código legacy

**Opciones:**

**A) Mantener como fallback (RECOMENDADO)**
```python
# Renombrar archivo
mv pili_local_specialists.py pili_local_specialists_legacy.py

# Mantener por si acaso
# Útil para comparar o si algo falla
```

**B) Eliminar completamente**
```python
# Solo si estás 100% seguro
rm pili_local_specialists.py
```

**Recomendación:** Mantener por 1-2 meses como backup

---

## 📊 COMPARACIÓN ANTES/DESPUÉS

### **ANTES (Actual):**
```
backend/app/services/
├── pili_local_specialists.py    # 3,500 líneas
├── pili_integrator.py            # 1,144 líneas
└── ...

Total: 1 archivo monolítico
```

### **DURANTE (Migración):**
```
backend/app/services/
├── pili_local_specialists.py    # 3,500 líneas (fallback)
├── pili_integrator.py            # 1,200 líneas (con lógica fallback)
└── pili/                         # Nueva arquitectura
    ├── core/                     # 400 líneas
    ├── config/                   # 500 líneas YAML
    ├── templates/                # 200 líneas YAML
    ├── knowledge/                # 1,000 líneas
    └── specialist.py             # 300 líneas

Total: Ambos sistemas coexisten
```

### **DESPUÉS (Final):**
```
backend/app/services/
├── pili_local_specialists_legacy.py  # 3,500 líneas (backup)
├── pili_integrator.py                # 1,200 líneas
└── pili/                             # Arquitectura principal
    ├── core/                         # 400 líneas
    ├── config/                       # 500 líneas YAML
    ├── templates/                    # 200 líneas YAML
    ├── knowledge/                    # 1,000 líneas
    └── specialist.py                 # 300 líneas

Total: Nueva arquitectura + backup
```

---

## ✅ VENTAJAS DE ESTA ESTRATEGIA

| Ventaja | Explicación |
|---------|-------------|
| **Sin riesgo** | Sistema funciona durante toda la migración |
| **Gradual** | Migras servicio por servicio |
| **Reversible** | Puedes volver atrás si algo falla |
| **Testeable** | Pruebas cada servicio antes de continuar |
| **Fallback** | Código actual siempre disponible |

---

## 🎯 CRONOGRAMA COMPLETO

| Día | Tarea | Horas | Estado Sistema |
|-----|-------|-------|----------------|
| 1 | Setup estructura base | 2h | ✅ Funciona normal |
| 2 | Migrar ITSE | 4h | ✅ ITSE nuevo, resto normal |
| 3 | Migrar Electricidad | 3h | ✅ 2 nuevos, 8 normales |
| 4 | Migrar 4 servicios | 3h | ✅ 6 nuevos, 4 normales |
| 5 | Migrar 4 servicios | 3h | ✅ Todos nuevos |
| 6 | Limpieza y testing | 1h | ✅ Todo nuevo |

**Total:** 16 horas de trabajo
**Riesgo:** Bajo (sistema siempre funciona)

---

## 🚀 PRÓXIMO PASO

**¿Empezamos con FASE 1 (Setup Inicial)?**

Voy a:
1. Crear carpeta `pili/`
2. Crear motores (core/)
3. Crear clase UniversalSpecialist
4. Probar que compila sin errores

**Esto NO rompe nada** - tu código actual sigue funcionando.

**¿Procedemos?**
