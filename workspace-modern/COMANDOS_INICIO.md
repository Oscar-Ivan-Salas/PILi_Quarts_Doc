# 🚀 Comandos de Inicio - PILi Quarts (Puertos 8005/3010)

## 1️⃣ BACKEND (Puerto 8005)

Abre una terminal PowerShell y ejecuta:

```powershell
cd e:\PILi_Quarts\workspace-modern\backend
uvicorn app.main:app --host 0.0.0.0 --port 8005 --reload
```

**Verificar**: Abre http://localhost:8005/health en tu navegador

---

## 2️⃣ FRONTEND (Puerto 3010)

Abre OTRA terminal PowerShell y ejecuta:

```powershell
cd e:\PILi_Quarts\workspace-modern\frontend
npm run dev
```

**Verificar**: Abre http://localhost:3010 en tu navegador

---

## ✅ Verificación Rápida

- Backend Health: http://localhost:8005/health
- Backend API Docs: http://localhost:8005/docs
- Frontend App: http://localhost:3010

---

## 🧹 Limpiar Caché (Si hay problemas)

### Frontend:
```powershell
cd e:\PILi_Quarts\workspace-modern\frontend
Remove-Item -Recurse -Force node_modules\.vite -ErrorAction SilentlyContinue
npm run dev
```

### Backend:
```powershell
cd e:\PILi_Quarts\workspace-modern\backend
Remove-Item -Recurse -Force __pycache__ -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force app\__pycache__ -ErrorAction SilentlyContinue
uvicorn app.main:app --host 0.0.0.0 --port 8005 --reload
```

---

## 🛑 Detener Todo (Si necesitas reiniciar)

```powershell
Get-Process -Id (Get-NetTCPConnection -LocalPort 3010,8005 -ErrorAction SilentlyContinue).OwningProcess -ErrorAction SilentlyContinue | Stop-Process -Force
```
