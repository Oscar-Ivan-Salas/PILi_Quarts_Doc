# 🚀 COMANDOS DE INICIO - PILi Quarts
# Configuración: Backend 8005 | Frontend 3010

## ✅ PASO 1: BACKEND (Terminal 1)

Set-Location "e:\PILi_Quarts\PILi_Quarts_V3.0\backend"
uvicorn app.main:app --host 0.0.0.0 --port 8005 --reload

## ✅ PASO 2: FRONTEND (Terminal 2)

Set-Location "e:\PILi_Quarts\PILi_Quarts_V3.0\frontend"
npm run dev

## 🔍 VERIFICACIÓN

# Backend Health Check
Start-Process "http://localhost:8005/health"

# Frontend App
Start-Process "http://localhost:3010"

# API Documentation
Start-Process "http://localhost:8005/docs"

## 🛑 DETENER TODO (Si necesitas reiniciar)

Get-Process -Id (Get-NetTCPConnection -LocalPort 3010, 8005 -ErrorAction SilentlyContinue).OwningProcess -ErrorAction SilentlyContinue | Stop-Process -Force

## 🧹 LIMPIAR CACHÉ (Si hay problemas)

# Frontend
Set-Location "e:\PILi_Quarts\PILi_Quarts_V3.0\frontend"
Remove-Item -Recurse -Force node_modules\.vite -ErrorAction SilentlyContinue

# Backend
Set-Location "e:\PILi_Quarts\PILi_Quarts_V3.0\backend"
Get-ChildItem -Path . -Filter __pycache__ -Recurse -Directory -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force
