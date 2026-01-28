# 🧹 COMANDOS PARA LIMPIAR CACHE COMPLETO

## 📍 Ejecuta estos comandos en PowerShell desde la carpeta frontend

```powershell
# 1. Detener npm (Ctrl+C en la terminal donde corre npm start)

# 2. Limpiar cache de node_modules
Remove-Item -Path "node_modules\.cache" -Recurse -Force -ErrorAction SilentlyContinue

# 3. Limpiar build (si existe)
Remove-Item -Path "build" -Recurse -Force -ErrorAction SilentlyContinue

# 4. Limpiar cache de React
Remove-Item -Path ".cache" -Recurse -Force -ErrorAction SilentlyContinue

# 5. Reiniciar npm
npm start
```

## 🌐 EN EL NAVEGADOR (IMPORTANTE)

Después de reiniciar npm, en el navegador:

1. **Abre DevTools:** Presiona `F12`
2. **Click derecho en el botón de recarga** (junto a la barra de direcciones)
3. **Selecciona:** "Vaciar caché y volver a cargar de manera forzada" o "Empty Cache and Hard Reload"

O simplemente:
- `Ctrl + Shift + R` (recarga forzada)
- `Ctrl + F5`

## 📋 COMANDO TODO-EN-UNO

Copia y pega esto en PowerShell (desde carpeta frontend):

```powershell
Remove-Item -Path "node_modules\.cache" -Recurse -Force -ErrorAction SilentlyContinue; Remove-Item -Path "build" -Recurse -Force -ErrorAction SilentlyContinue; Remove-Item -Path ".cache" -Recurse -Force -ErrorAction SilentlyContinue; Write-Host "✅ Cache limpiado - Ahora reinicia npm start"
```
