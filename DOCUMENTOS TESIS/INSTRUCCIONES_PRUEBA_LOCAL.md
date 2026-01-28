# 🧪 Instrucciones para Probar Chatbot ITSE en tu PC Local

**Fecha:** 2025-12-30
**Versión:** 3.0 - Chatbot ITSE Caja Negra Integrado

---

## 📋 Prerrequisitos

- Python 3.11 o 3.12
- Node.js 18+
- Git configurado

---

## 🔄 Paso 1: Actualizar código desde repositorio

```bash
cd /ruta/a/TESLA_COTIZADOR-V3.0

# Traer todos los cambios
git fetch origin

# Cambiar al branch correcto
git checkout claude/claude-md-mifgupwu28q5qjdd-01DXJ3Tf3TXpPfvV7gqqkWf8

# Actualizar con los últimos cambios
git pull origin claude/claude-md-mifgupwu28q5qjdd-01DXJ3Tf3TXpPfvV7gqqkWf8
```

**Verificar que tienes los cambios:**
```bash
git log --oneline -3
```

Deberías ver:
```
cdd17b7 fix(itse): Integración correcta chatbot caja negra ITSE
ab078ea fix(itse): Chatbot ITSE genera items correctos para tabla detalle cotización
f8e7f4f docs: Flujo completo chat inteligente + vista previa en tiempo real
```

---

## 🧪 Paso 2: Probar chatbot directamente (sin backend)

```bash
cd /ruta/a/TESLA_COTIZADOR-V3.0

python3 << 'EOF'
from Pili_ChatBot.pili_itse_chatbot import PILIITSEChatBot

print("=" * 80)
print("🧪 PRUEBA CHATBOT ITSE - Caja Negra")
print("=" * 80)

chatbot = PILIITSEChatBot()

# Conversación completa
r1 = chatbot.procesar("", None)
print("\n1️⃣ PILI:", r1['respuesta'][:100], "...")

r2 = chatbot.procesar("COMERCIO", r1['estado'])
print("\n2️⃣ PILI:", r2['respuesta'][:80], "...")

r3 = chatbot.procesar("Tienda de ropa", r2['estado'])
print("\n3️⃣ PILI:", r3['respuesta'][:80], "...")

r4 = chatbot.procesar("250", r3['estado'])
print("\n4️⃣ PILI:", r4['respuesta'][:80], "...")

r5 = chatbot.procesar("2", r4['estado'])

if 'datos_generados' in r5:
    datos = r5['datos_generados']
    print("\n" + "=" * 80)
    print("✅ COTIZACIÓN GENERADA")
    print("=" * 80)
    print(f"Proyecto: {datos['proyecto']['nombre']}")
    print(f"Área: {datos['proyecto']['area_m2']} m²")
    print(f"Pisos: {datos['proyecto']['pisos']}")
    print(f"Riesgo: {datos['proyecto']['nivel_riesgo']}")
    print()
    print("ITEMS:")
    for i, item in enumerate(datos['items'], 1):
        print(f"  {i}. {item['descripcion'][:50]:50} | S/ {item['precio_unitario']:8.2f}")
    print()
    print(f"SUBTOTAL: S/ {datos['subtotal']:.2f}")
    print(f"IGV 18%:  S/ {datos['igv']:.2f}")
    print(f"TOTAL:    S/ {datos['total']:.2f}")
    print("=" * 80)
    print("✅ CHATBOT FUNCIONA CORRECTAMENTE")
else:
    print("\n❌ ERROR: No se generaron datos")
    print("Revisa que tengas los últimos cambios del repositorio")
EOF
```

**Resultado esperado:**
```
✅ COTIZACIÓN GENERADA
Proyecto: Certificado ITSE - COMERCIO
Área: 250.0 m²
Pisos: 2
Riesgo: MEDIO

ITEMS:
  1. Certificado ITSE - Nivel MEDIO              | S/   208.60
  2. Servicio técnico profesional - Evaluación.. | S/   550.00
  3. Visita técnica gratuita                      | S/     0.00

SUBTOTAL: S/ 758.60
IGV 18%:  S/ 136.55
TOTAL:    S/ 895.15
✅ CHATBOT FUNCIONA CORRECTAMENTE
```

---

## 🚀 Paso 3: Levantar Backend

### Opción A: Con entorno virtual (Recomendado)

```bash
cd /ruta/a/TESLA_COTIZADOR-V3.0/backend

# Crear entorno virtual (solo primera vez)
python3 -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar .env
cp .env.example .env

# Editar .env y agregar tu GEMINI_API_KEY
nano .env  # o notepad .env en Windows

# Levantar backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Opción B: Sin entorno virtual

```bash
cd /ruta/a/TESLA_COTIZADOR-V3.0/backend

# Instalar dependencias
pip3 install -r requirements.txt

# Configurar .env
cp .env.example .env
# Editar .env con tu editor favorito

# Levantar backend
python3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Backend corriendo correctamente si ves:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Verificar backend:**

Abre http://localhost:8000/docs en tu navegador.
Deberías ver la documentación de Swagger/FastAPI.

---

## 🧪 Paso 4: Probar endpoint desde terminal

En **otra terminal** (mientras el backend corre):

```bash
curl -X POST http://localhost:8000/api/chat/chat-contextualizado \
  -H "Content-Type: application/json" \
  -d '{
    "tipo_flujo": "itse",
    "mensaje": "",
    "conversation_state": null
  }'
```

**Deberías recibir:**
```json
{
  "success": true,
  "respuesta": "¡Hola! 👋 Soy **Pili**, tu especialista en certificados ITSE...",
  "botones_sugeridos": [
    {"text": "🏥 Salud", "value": "SALUD"},
    {"text": "🎓 Educación", "value": "EDUCACION"},
    ...
  ],
  "state": {"etapa": "categoria", ...}
}
```

---

## 🎨 Paso 5: Levantar Frontend

En **otra terminal nueva**:

```bash
cd /ruta/a/TESLA_COTIZADOR-V3.0/frontend

# Instalar dependencias (solo primera vez)
npm install

# Levantar frontend
npm start
```

**Frontend corriendo si ves:**
```
Compiled successfully!

You can now view tesla-cotizador-frontend in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.X.X:3000
```

---

## 🧪 Paso 6: Probar en el navegador

1. Abre **http://localhost:3000**

2. **IMPORTANTE**: Abre las **DevTools del navegador**:
   - Chrome/Edge: `F12` o `Ctrl+Shift+I`
   - Firefox: `F12`

3. Ve a la pestaña **Console** de DevTools

4. Navega al chat ITSE

5. En la consola deberías ver:
   ```
   🔄 Estado de conversación actualizado: {etapa: "categoria", ...}
   📊 Datos generados recibidos: {proyecto: {...}, items: [...]}
   ```

6. **Prueba el flujo completo:**
   - Selecciona "🏪 Comercio"
   - Escribe "Tienda de ropa"
   - Escribe "250"
   - Escribe "2"

7. **Verifica la tabla de cotización:**
   - Debería actualizarse en tiempo real
   - Mostrando 3 items
   - Total: S/ 895.15

---

## 🔍 Solución de Problemas

### ❌ Problema: "ModuleNotFoundError: No module named 'fastapi'"

**Solución:**
```bash
cd backend
pip install -r requirements.txt
```

### ❌ Problema: "Error de conexión" en frontend

**Solución:**
1. Verifica que el backend esté corriendo en http://localhost:8000
2. Verifica CORS en backend (debería estar configurado)
3. Revisa la consola del backend para ver errores

### ❌ Problema: "No such file or directory: Pili_ChatBot"

**Solución:**
```bash
# Verifica que tienes la carpeta Pili_ChatBot
ls -la Pili_ChatBot/

# Si no existe, asegúrate de hacer git pull correctamente
git status
git pull origin claude/claude-md-mifgupwu28q5qjdd-01DXJ3Tf3TXpPfvV7gqqkWf8
```

### ❌ Problema: Veo mensajes viejos (como la imagen que mostraste)

**Causa:** El backend NO está corriendo, el frontend usa respuestas simuladas.

**Solución:**
1. Limpia caché del navegador: `Ctrl+Shift+R` (Chrome/Edge) o `Ctrl+F5`
2. Abre modo incógnito: `Ctrl+Shift+N`
3. Verifica que el backend esté corriendo
4. Revisa la consola del navegador para ver errores de conexión

### ❌ Problema: Tabla no se actualiza

**Solución:**
1. Abre DevTools → Console
2. Busca errores en rojo
3. Verifica que llegue `datos_generados`:
   ```javascript
   console.log('📊 Datos generados recibidos:', data.datos_generados);
   ```
4. Si no llega, el backend no está enviándolo correctamente

---

## 📊 Estructura esperada de datos_generados

```json
{
  "proyecto": {
    "nombre": "Certificado ITSE - COMERCIO",
    "area_m2": 250.0,
    "pisos": 2,
    "nivel_riesgo": "MEDIO"
  },
  "items": [
    {
      "descripcion": "Certificado ITSE - Nivel MEDIO",
      "cantidad": 1,
      "unidad": "servicio",
      "precio_unitario": 208.60
    },
    {
      "descripcion": "Servicio técnico profesional - Evaluación + Planos + Gestión",
      "cantidad": 1,
      "unidad": "servicio",
      "precio_unitario": 550.00
    },
    {
      "descripcion": "Visita técnica gratuita",
      "cantidad": 1,
      "unidad": "servicio",
      "precio_unitario": 0.00
    }
  ],
  "subtotal": 758.60,
  "igv": 136.55,
  "total": 895.15
}
```

---

## ✅ Checklist de Verificación

- [ ] `git pull` ejecutado correctamente
- [ ] Chatbot funciona en prueba directa (Paso 2)
- [ ] Backend corriendo en http://localhost:8000
- [ ] Endpoint `/docs` accesible
- [ ] curl test exitoso (Paso 4)
- [ ] Frontend corriendo en http://localhost:3000
- [ ] DevTools abierta para ver logs
- [ ] Conversación completa hasta generar cotización
- [ ] Tabla se actualiza con 3 items
- [ ] Total muestra S/ 895.15

---

## 📞 Soporte

Si después de seguir todos los pasos sigues teniendo problemas:

1. Captura de pantalla del error en DevTools Console
2. Logs del backend (terminal donde corre uvicorn)
3. Output del comando `git log --oneline -3`

---

**Última actualización:** 2025-12-30
**Versión:** Chatbot ITSE Caja Negra v1.0
