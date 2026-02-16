# 🚀 Instrucciones de Inicio - PILi Quarts

## Configuración de Puertos
- **Backend**: Puerto 8005
- **Frontend**: Puerto 3010

## Iniciar Backend (Puerto 8005)

```powershell
cd e:\PILi_Quarts\workspace-modern\backend
uvicorn app.main:app --host 0.0.0.0 --port 8005 --reload
```

## Iniciar Frontend (Puerto 3010)

```powershell
cd e:\PILi_Quarts\workspace-modern\frontend
npm run dev
```

El frontend se iniciará automáticamente en el puerto 3010 (configurado en `package.json`).

## Verificar Conexión

1. Backend: http://localhost:8005/health
2. Frontend: http://localhost:3010
3. API Docs: http://localhost:8005/docs

## Notas Importantes

- ✅ El frontend está configurado para conectarse automáticamente a `http://localhost:8005`
- ✅ CORS configurado para permitir peticiones desde puerto 3010
- ✅ Todas las dependencias instaladas (pandas, openpyxl, etc.)
- ⚠️ **IMPORTANTE**: Si cambias el puerto del backend, debes actualizar `frontend/src/lib/api-client.ts`
