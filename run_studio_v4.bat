@echo off
TITLE PILI QUARTS V4.0 STUDIO - LABORATORIO
echo ==========================================
echo INICIANDO ESTUDIO MAGNIFICO V4.0 (AISLADO)
echo ==========================================
echo.
echo [1/3] Verificando entorno...
cd /d e:\PILi_Quarts\PILi_Quarts_V4.0_Studio\frontend

echo [2/3] Instalando dependencias necesarias (Solo la primera vez)...
call npm install --silent

echo [3/3] Lanzando Frontend en http://localhost:3013...
echo (Asegurate de que el backend en el puerto 8006 este activo si necesitas datos reales)
npm run dev
pause
