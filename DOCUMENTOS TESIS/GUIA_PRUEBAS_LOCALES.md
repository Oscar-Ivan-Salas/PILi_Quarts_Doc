# 🧪 GUÍA DE PRUEBAS LOCALES - SISTEMA HTML EDITABLE → WORD

**Proyecto:** Tesla Cotizador V3.0
**Fecha:** 14 de Diciembre de 2025
**Versión:** 1.0

---

## 📋 PRE-REQUISITOS

### 1. Verificar Instalación de Python
```bash
python --version
# Debe ser Python 3.11 o superior
```

### 2. Verificar Dependencias Instaladas
```bash
cd backend
pip list | grep -E "beautifulsoup4|python-docx|htmldocx|fastapi"
```

**Dependencias necesarias:**
- ✅ `beautifulsoup4` - Parser HTML
- ✅ `python-docx` - Generación Word
- ✅ `htmldocx` - Conversión HTML→Word
- ✅ `fastapi` - Framework backend
- ✅ `uvicorn` - Servidor ASGI

**Si falta alguna:**
```bash
cd backend
pip install -r requirements.txt
```

---

## 🚀 OPCIÓN 1: PRUEBA RÁPIDA (Test Script)

### Ejecutar el test completo de 6 documentos

```bash
# Desde la raíz del proyecto
python test_6_documentos_completos.py
```

**Resultado esperado:**
```
================================================================================
🚀 PRUEBA COMPLETA - SISTEMA TESLA COTIZADOR V3.0
================================================================================
📁 Directorio salida: /home/user/TESLA_COTIZADOR-V3.0/storage/generados
📅 Fecha: [FECHA ACTUAL]
================================================================================

📄 1/6: Generando Cotización Simple...
   ✅ Generado: COTIZACION_SIMPLE_PROFESIONAL.docx (36.9 KB)
📄 2/6: Generando Cotización Compleja...
   ✅ Generado: COTIZACION_COMPLEJA_PROFESIONAL.docx (37.5 KB)
📄 3/6: Generando Proyecto Simple...
   ✅ Generado: PROYECTO_SIMPLE_PROFESIONAL.docx (37.4 KB)
📄 4/6: Generando Proyecto Complejo PMI...
   ✅ Generado: PROYECTO_PMI_COMPLEJO_PROFESIONAL.docx (37.8 KB)
📄 5/6: Generando Informe Técnico...
   ✅ Generado: INFORME_TECNICO_PROFESIONAL.docx (38.3 KB)
📄 6/6: Generando Informe Ejecutivo APA...
   ✅ Generado: INFORME_EJECUTIVO_APA_PROFESIONAL.docx (39.1 KB)

================================================================================
🎯 TOTAL: 6/6 documentos generados correctamente
================================================================================
```

**Abrir documentos generados:**
```bash
# Windows
start storage/generados/*.docx

# Linux
xdg-open storage/generados/*.docx

# macOS
open storage/generados/*.docx
```

---

## 🌐 OPCIÓN 2: PRUEBA CON SERVIDOR (Completo)

### Paso 1: Iniciar Backend

```bash
# Terminal 1 - Backend
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Esperar mensaje:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Paso 2: Probar Endpoint de Salud

```bash
# Terminal 2 - Pruebas
curl http://localhost:8000/api/system/health
```

**Respuesta esperada:**
```json
{
  "status": "healthy",
  "version": "3.0.0",
  "timestamp": "2025-12-14T..."
}
```

### Paso 3: Probar Generación Directa de Documento

#### 3.1 Cotización Simple

```bash
curl -X POST "http://localhost:8000/api/generar-documento-directo?formato=word" \
  -H "Content-Type: application/json" \
  -d '{
    "tipo_plantilla": "cotizacion-simple",
    "numero": "COT-202512-TEST-001",
    "fecha": "14/12/2025",
    "cliente": "CLIENTE PRUEBA LOCAL S.A.C.",
    "proyecto": "Proyecto de Prueba Local",
    "atencion": "Ing. Pruebas",
    "items": [
      {
        "descripcion": "Tablero eléctrico de prueba",
        "cantidad": 1,
        "unidad": "und",
        "precio_unitario": 500.00
      },
      {
        "descripcion": "Cable de prueba 10mm",
        "cantidad": 10,
        "unidad": "m",
        "precio_unitario": 5.50
      }
    ],
    "observaciones": "Documento de prueba generado localmente",
    "vigencia": "15 días"
  }' \
  --output storage/generados/PRUEBA_LOCAL.docx
```

**Verificar archivo:**
```bash
ls -lh storage/generados/PRUEBA_LOCAL.docx
```

#### 3.2 Proyecto PMI

```bash
curl -X POST "http://localhost:8000/api/generar-documento-directo?formato=word" \
  -H "Content-Type: application/json" \
  -d '{
    "tipo_plantilla": "proyecto-complejo",
    "nombre": "Proyecto PMI de Prueba Local",
    "codigo": "PROY-TEST-001",
    "cliente": "CLIENTE PRUEBA S.A.C.",
    "fecha_inicio": "15/01/2025",
    "fecha_fin": "15/03/2025",
    "presupuesto": 50000.00,
    "spi": "1.05",
    "cpi": "0.98",
    "ev": 25000,
    "pv": 23800,
    "ac": 25500,
    "alcance": "Proyecto de prueba para validar sistema PMI localmente"
  }' \
  --output storage/generados/PRUEBA_PMI_LOCAL.docx
```

#### 3.3 Informe Ejecutivo APA

```bash
curl -X POST "http://localhost:8000/api/generar-documento-directo?formato=word" \
  -H "Content-Type: application/json" \
  -d '{
    "tipo_plantilla": "informe-ejecutivo",
    "titulo": "Informe Ejecutivo de Prueba Local",
    "codigo": "INF-TEST-001",
    "cliente": "CLIENTE PRUEBA S.A.C.",
    "fecha": "14/12/2025",
    "presupuesto": 80000.00,
    "roi": "25",
    "tir": "30",
    "payback": "18",
    "resumen": "Este es un informe de prueba generado localmente para validar el sistema"
  }' \
  --output storage/generados/PRUEBA_INFORME_LOCAL.docx
```

---

## 🧪 OPCIÓN 3: PRUEBA DEL PARSER HTML→JSON

### Crear archivo HTML de prueba

```bash
cat > /tmp/test_html.html << 'EOF'
<html>
<body>
    <input name="cliente" value="CLIENTE PRUEBA HTML S.A.C.">
    <input name="proyecto" value="Proyecto desde HTML">
    <input name="numero" value="COT-202512-HTML-001">
    <input type="checkbox" name="mostrar_igv" checked>

    <table class="items-table">
        <tr><th>Desc</th><th>Cant</th><th>Unidad</th><th>Precio</th></tr>
        <tr>
            <td><input value="Item desde HTML"></td>
            <td><input type="number" value="5"></td>
            <td>und</td>
            <td><input type="number" value="100.00"></td>
        </tr>
    </table>
</body>
</html>
EOF

echo "✅ Archivo HTML de prueba creado en /tmp/test_html.html"
```

### Probar parser directamente

```python
# Ejecutar en Python
cd backend
python << 'EOF'
from app.services.html_parser import html_parser

# Leer HTML de prueba
with open('/tmp/test_html.html', 'r') as f:
    html = f.read()

# Parsear
resultado = html_parser.parsear_html_editado(html, "cotizacion-simple")

# Mostrar resultado
print("=" * 60)
print("RESULTADO DEL PARSER:")
print("=" * 60)
print(f"Cliente: {resultado['cliente']}")
print(f"Proyecto: {resultado['proyecto']}")
print(f"Número: {resultado['numero']}")
print(f"Mostrar IGV: {resultado['mostrar_igv']}")
print(f"Items: {len(resultado['items'])}")
for i, item in enumerate(resultado['items'], 1):
    print(f"  {i}. {item['descripcion']}: {item['cantidad']} x S/ {item['precio_unitario']}")
print(f"Subtotal: S/ {resultado['subtotal']:.2f}")
print(f"IGV: S/ {resultado['igv']:.2f}")
print(f"Total: S/ {resultado['total']:.2f}")
print("=" * 60)
EOF
```

---

## 🔍 OPCIÓN 4: PRUEBA COMPLETA CON HTML EDITADO

### Enviar HTML editado al endpoint

```bash
# Crear JSON con HTML embebido
cat > /tmp/request_html.json << 'EOF'
{
  "tipo_plantilla": "cotizacion-simple",
  "html_editado": "<html><body><input name=\"cliente\" value=\"CLIENTE HTML EDITADO S.A.C.\"><input name=\"proyecto\" value=\"Proyecto HTML Editado\"><input name=\"numero\" value=\"COT-HTML-001\"><table class=\"items-table\"><tr><th>Desc</th><th>Cant</th><th>U</th><th>Precio</th></tr><tr><td><input value=\"Item editado manualmente\"></td><td><input type=\"number\" value=\"3\"></td><td>und</td><td><input type=\"number\" value=\"250.00\"></td></tr></table></body></html>",
  "datos": {}
}
EOF

# Enviar al endpoint
curl -X POST "http://localhost:8000/api/generar-documento-directo?formato=word" \
  -H "Content-Type: application/json" \
  -d @/tmp/request_html.json \
  --output storage/generados/PRUEBA_HTML_EDITADO.docx

echo "✅ Documento generado desde HTML editado"
ls -lh storage/generados/PRUEBA_HTML_EDITADO.docx
```

---

## 📂 VERIFICAR RESULTADOS

### Listar todos los documentos generados

```bash
ls -lh storage/generados/*.docx
```

### Contar documentos exitosos

```bash
echo "Documentos generados: $(ls storage/generados/*.docx 2>/dev/null | wc -l)"
```

### Abrir carpeta de documentos

```bash
# Windows
explorer storage\generados

# Linux
nautilus storage/generados &

# macOS
open storage/generados
```

---

## 🐛 SOLUCIÓN DE PROBLEMAS

### Error: "ModuleNotFoundError: No module named 'bs4'"

**Solución:**
```bash
cd backend
pip install beautifulsoup4
```

### Error: "ModuleNotFoundError: No module named 'htmldocx'"

**Solución:**
```bash
cd backend
pip install htmldocx
```

### Error: "FileNotFoundError: storage/generados"

**Solución:**
```bash
mkdir -p storage/generados
chmod 755 storage/generados
```

### Error: "Connection refused" al hacer curl

**Solución:**
```bash
# Verificar que el backend esté corriendo
curl http://localhost:8000/api/system/health

# Si no responde, iniciar backend
cd backend
uvicorn app.main:app --reload
```

### Error: "ImportError: cannot import name 'html_parser'"

**Solución:**
```bash
# Verificar que el archivo existe
ls -l backend/app/services/html_parser.py

# Si no existe, revisar el commit
git log --oneline | head -5
git status
```

### Documentos generados tienen 0 KB

**Solución:**
```bash
# Verificar logs del backend
# Buscar errores en la terminal donde corre uvicorn

# Verificar que html_to_word_generator existe
ls -l backend/app/services/html_to_word_generator.py
```

---

## ✅ CHECKLIST DE PRUEBAS

Marca cada prueba conforme la completes:

- [ ] **Prueba 1:** Ejecutar `test_6_documentos_completos.py` → 6/6 exitosos
- [ ] **Prueba 2:** Iniciar backend con `uvicorn` → Sin errores
- [ ] **Prueba 3:** Health check → Responde correctamente
- [ ] **Prueba 4:** Generar cotización simple vía API → Archivo creado
- [ ] **Prueba 5:** Generar proyecto PMI vía API → Archivo creado
- [ ] **Prueba 6:** Generar informe APA vía API → Archivo creado
- [ ] **Prueba 7:** Parser HTML→JSON → Extrae datos correctamente
- [ ] **Prueba 8:** Endpoint con HTML editado → Documento generado
- [ ] **Prueba 9:** Abrir documentos en Word → Se abren correctamente
- [ ] **Prueba 10:** Verificar colores AZUL Tesla en documentos → Correctos

---

## 📊 RESULTADOS ESPERADOS

Si todas las pruebas pasan correctamente, deberías tener:

```
storage/generados/
├── COTIZACION_SIMPLE_PROFESIONAL.docx          (36.9 KB)
├── COTIZACION_COMPLEJA_PROFESIONAL.docx        (37.5 KB)
├── PROYECTO_SIMPLE_PROFESIONAL.docx            (37.4 KB)
├── PROYECTO_PMI_COMPLEJO_PROFESIONAL.docx      (37.8 KB)
├── INFORME_TECNICO_PROFESIONAL.docx            (38.3 KB)
├── INFORME_EJECUTIVO_APA_PROFESIONAL.docx      (39.1 KB)
├── PRUEBA_LOCAL.docx                           (~30-40 KB)
├── PRUEBA_PMI_LOCAL.docx                       (~30-40 KB)
├── PRUEBA_INFORME_LOCAL.docx                   (~30-40 KB)
└── PRUEBA_HTML_EDITADO.docx                    (~30-40 KB)

Total: 10 documentos Word profesionales
```

---

## 🎯 CRITERIOS DE ÉXITO

### ✅ El sistema funciona correctamente si:

1. **Test script** genera 6/6 documentos sin errores
2. **Backend** inicia sin errores y responde en `/api/system/health`
3. **Endpoint** `/api/generar-documento-directo` genera documentos Word
4. **Parser HTML** extrae correctamente todos los campos
5. **Documentos Word** se abren en Microsoft Word/LibreOffice
6. **Colores** son AZUL Tesla (#0052A3, #1E40AF, #3B82F6)
7. **Datos** se muestran correctamente en los documentos
8. **Tablas** están formateadas profesionalmente
9. **Tamaños** de archivo son consistentes (~30-40 KB)
10. **Sin errores** en logs del backend

---

## 📞 SOPORTE

Si encuentras algún problema durante las pruebas:

1. **Revisar logs del backend** en la terminal de uvicorn
2. **Verificar archivos** con `ls -l` y `git status`
3. **Consultar reporte completo** en `REPORTE_IMPLEMENTACION_SISTEMA_HTML_WORD.md`
4. **Revisar checkpoint** en `RESTAURAR_CHECKPOINT.md` si necesitas rollback

---

**Última actualización:** 14 de Diciembre de 2025
**Versión:** 1.0
**Autor:** Claude Code (Sonnet 4.5)
