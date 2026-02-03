@echo off
title PILi Quarts - FRONTEND (Puerto 3009)
color 0B
cd /d "%~dp0"

echo [1/4] Verificando Entorno...
call npm --version >nul 2>&1
if %errorlevel% neq 0 (
    color 0C
    echo ERROR CRITICO: Node.js no detectado.
    pause
    exit /b
)

echo [2/4] Liberando puerto 3009...
for /f "tokens=5" %%a in ('netstat -aon ^| find ":3009" ^| find "LISTENING"') do (
    taskkill /f /pid %%a >nul 2>&1
)

echo [3/4] Inicializando...
cd frontend

echo [4/4] Arrancando Web (Puerto 3009)...
echo.
echo Espera y abre: http://localhost:3009
echo.
call npm run dev

pause
