# 🔴 PROBLEMA ACTUAL - Descarga JSON en lugar de Word/PDF

## 📊 SÍNTOMAS

Usuario reporta que al hacer click en botones DOCX/PDF, se descargan archivos:
- Nombres extraños: `48d6addd-c53f-4a72-a013-5894aa8f4497`
- Tamaño pequeño: 2.8 KB, 37 KB
- Probablemente son JSON en lugar de documentos

## 🔍 ANÁLISIS

### Backend (`generar_directo.py`)
El código se ve correcto:
```python
return FileResponse(
    path=archivo,
    media_type=media_type,
    filename=filename,
    headers={"Content-Disposition": f'attachment; filename="{filename}"'}
)
```

### Posibles Causas

1. **Error en generación de Word**
   - `html_to_word_generator.generar_cotizacion_simple()` falla
   - Archivo no se crea en `storage/generados/`
   - Backend devuelve error como JSON

2. **Ruta incorrecta**
   - `archivo` apunta a ubicación incorrecta
   - FileResponse no encuentra el archivo
   - Devuelve error como JSON

3. **Excepción capturada**
   - Línea 163-167: `except Exception` captura error
   - Devuelve `HTTPException` con JSON

## 🎯 SOLUCIÓN NECESARIA

1. **Revisar logs del backend** para ver errores exactos
2. **Verificar que archivos se generen** en `E:\TESLA_COTIZADOR-V3.0\storage\generados\`
3. **Agregar logging detallado** antes de FileResponse
4. **Verificar que html_to_word_generator funcione** correctamente

## 📝 PRÓXIMOS PASOS

1. Ver logs del backend cuando se genera documento
2. Verificar si archivo Word se crea físicamente
3. Si no se crea, revisar `html_to_word_generator.py`
4. Si se crea pero no se descarga, revisar FileResponse
