# 🚀 COMANDOS DE INICIO CON ENTORNO VIRTUAL - PILi Quarts

## ✅ PASO 1: BACKEND (Puerto 8005) - CON VENV

Abre una terminal PowerShell y ejecuta:

```powershell
cd e:\PILi_Quarts\workspace-modern\backend

# Activar entorno virtual
.\venv\Scripts\Activate.ps1

# Iniciar backend
uvicorn app.main:app --host 0.0.0.0 --port 8005 --reload
```

**Verificar**: Deberías ver `(venv)` al inicio de tu prompt de PowerShell

---

## ✅ PASO 2: FRONTEND (Puerto 3010)

Abre OTRA terminal PowerShell y ejecuta:

```powershell
cd e:\PILi_Quarts\workspace-modern\frontend
npm run dev
```

---

## 🔍 VERIFICACIÓN

- Backend Health: http://localhost:8005/health
- Backend API Docs: http://localhost:8005/docs  
- Frontend App: http://localhost:3010

---

## 🛑 DETENER TODO

```powershell
# Detener procesos en puertos 3010 y 8005
Get-Process -Id (Get-NetTCPConnection -LocalPort 3010,8005 -ErrorAction SilentlyContinue).OwningProcess -ErrorAction SilentlyContinue | Stop-Process -Force
```

---

## 📝 NOTAS IMPORTANTES

1. ✅ **Siempre activa el venv** antes de iniciar el backend
2. ✅ El prompt debe mostrar `(venv)` cuando el entorno está activo
3. ✅ Si el venv no existe, créalo con: `python -m venv venv`
4. ✅ Instala dependencias con: `pip install -r requirements.txt`
