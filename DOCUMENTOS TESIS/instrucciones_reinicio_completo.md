# 🔧 INSTRUCCIONES DE REINICIO COMPLETO DEL SERVIDOR

## 🎯 Problema Identificado

El servidor backend está ejecutando **código desactualizado en memoria**.

**Evidencia:**
```
Error: PILIIntegrator.procesar_solicitud_completa() got an unexpected keyword argument 'conversation_state'
```

El archivo en disco SÍ tiene el parámetro, pero el servidor en memoria NO.

---

## ✅ SOLUCIÓN: Reinicio Completo Forzado

### Paso 1: Detener el Servidor Actual

1. Ve a la terminal donde corre el backend
2. Presiona `Ctrl + C`
3. **Espera 5-10 segundos** para que se detenga completamente
4. Si no se detiene, **cierra la terminal completamente**

### Paso 2: Abrir Nueva Terminal

**IMPORTANTE:** No reutilices la terminal anterior. Abre una **NUEVA** terminal de PowerShell.

### Paso 3: Navegar al Directorio del Backend

```powershell
cd e:\TESLA_COTIZADOR-V3.0\backend
```

### Paso 4: Activar Entorno Virtual

```powershell
.\venv\Scripts\activate
```

Deberías ver `(venv)` al inicio de la línea de comandos.

### Paso 5: Iniciar el Servidor

```powershell
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Paso 6: Verificar Inicio Correcto

Deberías ver en los logs:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

---

## 🧪 PRUEBA DE VERIFICACIÓN

### Opción 1: Desde Python

Abre otra terminal y ejecuta:
```powershell
cd e:\TESLA_COTIZADOR-V3.0
python test_simple.py
```

Deberías ver:
```
STATUS: OK
RESULTADO: CORRECTO - Es respuesta de ITSE
```

### Opción 2: Desde el Navegador

1. Abre `http://localhost:3001`
2. Ve al Chat ITSE
3. Escribe "Hola"
4. Deberías ver botones: Salud, Educación, Comercio, etc.

---

## 📋 Logs Esperados en el Backend

Cuando funcione correctamente, verás:

```
🔒 Contexto ITSE detectado: Forzando servicio a 'itse'
📚 NIVEL 3: Usando ESPECIALISTAS LOCALES LEGACY para itse
🔍 NIVEL 3: Respuesta recibida: {...}
✅✅✅ NIVEL 3: ÉXITO - Retornando respuesta de especialista local ✅✅✅
```

---

## ❌ Si Aún No Funciona

Si después del reinicio completo aún ves "Instalaciones Eléctricas", ejecuta:

```powershell
cd e:\TESLA_COTIZADOR-V3.0
python test_simple.py
```

Y comparte el output completo.

---

## 🔍 Verificación de Código Cargado

Para confirmar que el servidor cargó el código correcto, busca en los logs de inicio:

```
INFO:     Started server process [XXXXX]
```

El número de proceso debe ser DIFERENTE al anterior. Si es el mismo, el servidor no se reinició.

