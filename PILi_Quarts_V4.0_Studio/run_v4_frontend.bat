@echo off
set "V4_DIR=e:\PILi_Quarts\PILi_Quarts_V4.0_Studio\frontend"
cd /d "%V4_DIR%"
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] No se encuentra el directorio %V4_DIR%
    pause
    exit /b 1
)

echo.
echo ===================================================
echo   INICIANDO PILI QUARTS V4.0 STUDIO (PUERTO 3014)
echo ===================================================
echo.
echo Limpiando procesos en puerto 3014...
for /f "tokens=5" %%a in ('netstat -aon ^| find ":3014" ^| find "LISTENING"') do taskkill /f /pid %%a >nul 2>&1

echo Iniciando servidor de desarrollo...
call npm run dev -- --port 3014
pause
