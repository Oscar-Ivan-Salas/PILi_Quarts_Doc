# ☁️ GUÍA MAESTRA DE DESPLIEGUE CLOUD - N04 (SOBERANO V10)
# ========================================================

Este documento resume los pasos para subir el Nodo N04 a producción en una arquitectura hibrida profesional.

## 1. Arquitectura Recomendada
- **Frontend (Studio)**: [Vercel](https://vercel.com) (Deploy desde GitHub / Carpeta `studio`).
- **Backend (Motores)**: [Render](https://render.com) o [Railway](https://railway.app) (Despliegue con el `Dockerfile` local).
- **Base de Datos / Almacenamiento**: [Supabase](https://supabase.com).

## 2. Preparación del Backend (Render/Railway)
1. **GitHub**: Sube la carpeta `N04_Binary_Factory` a un repositorio.
2. **Docker**: Conecta el repositorio a Render/Railway. El sistema detectará el `Dockerfile` automáticamente.
3. **Variables de Entorno**:
   - `CORS_ORIGINS`: La URL de tu frontend en Vercel (ej: `https://n04-studio.vercel.app`).
   - `PORT`: 8005 (Render lo gestiona automáticamente).

## 3. Preparación del Frontend (Vercel)
1. **Importar**: En Vercel, selecciona solo la carpeta `studio`.
2. **Framework**: Selecciona "Vite".
3. **Variables de Entorno**:
   - `VITE_API_URL`: La URL de tu backend en Render (ej: `https://n04-api.onrender.com`).

## 4. Setup de Supabase
1. **SQL**: Ejecuta el contenido de `supabase_setup.sql` en el SQL Editor de Supabase.
2. **Storage**: Crea un bucket llamado `binary-factory-storage` si deseas persistir los documentos generados en la nube.

## 5. Archivos Listos en tu Carpeta
- `[Dockerfile](file:///e:/PILi_Quarts/PILi_Quarts_V4.0_Studio/backend/modules/N04_Binary_Factory/Dockerfile)`: Configuración del contenedor.
- `[vercel.json](file:///e:/PILi_Quarts/PILi_Quarts_V4.0_Studio/backend/modules/N04_Binary_Factory/studio/vercel.json)`: Ruteo del frontend.
- `[supabase_setup.sql](file:///e:/PILi_Quarts/PILi_Quarts_V4.0_Studio/backend/modules/N04_Binary_Factory/supabase_setup.sql)`: Esquema de base de datos.
- `[.env.production](file:///e:/PILi_Quarts/PILi_Quarts_V4.0_Studio/backend/modules/N04_Binary_Factory/studio/.env.production)`: Configuración de producción para el frontend.

**EL NODO N04 ESTÁ LISTO PARA EL DESPEGUE.** 🚀
