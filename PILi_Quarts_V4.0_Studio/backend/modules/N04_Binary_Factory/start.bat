@echo off
title N04 Binary Factory - Microservicio Studio
color 0A

echo ============================================
echo   N04 BINARY FACTORY - STUDIO AUTONOMO
echo   Backend:  http://localhost:8005
echo   Frontend: http://localhost:5173
echo ============================================
echo.

:: Directorio raiz del modulo N04
cd /d "%~dp0"

:: Liberar puertos si estaban ocupados
echo [1/4] Liberando puertos 8005 y 5173...
for /f "tokens=5" %%a in ('netstat -aon ^| find ":8005" ^| find "LISTENING" 2^>nul') do (
    taskkill /f /pid %%a >nul 2>&1
)
for /f "tokens=5" %%a in ('netstat -aon ^| find ":5173" ^| find "LISTENING" 2^>nul') do (
    taskkill /f /pid %%a >nul 2>&1
)

:: Verificar Python
echo [2/4] Verificando entorno Python...
if exist "venv\Scripts\python.exe" (
    set PYTHON=venv\Scripts\python.exe
) else (
    set PYTHON=python
)
%PYTHON% --version >nul 2>&1
if %errorlevel% neq 0 (
    color 0C
    echo ERROR: Python no encontrado. Instala Python 3.10+
    pause
    exit /b 1
)

:: Verificar Node
echo [3/4] Verificando entorno Node...
call npm --version >nul 2>&1
if %errorlevel% neq 0 (
    color 0C
    echo ERROR: Node.js no encontrado. Instala Node.js 18+
    pause
    exit /b 1
)

:: Arrancar Backend en nueva ventana
echo [4/4] Iniciando servicios...
start "N04-Backend (8005)" cmd /k "%PYTHON% -m uvicorn studio_api:app --host 0.0.0.0 --port 8005 --reload"

:: Esperar 3 segundos para que el backend arranque
timeout /t 3 /nobreak >nul

:: Arrancar Frontend en nueva ventana
start "N04-Frontend (5173)" cmd /k "cd studio && npm run dev"

echo.
echo ============================================
echo   ✅ N04 Studio iniciado correctamente
echo   Abre: http://localhost:5173
echo ============================================
echo.
echo Presiona cualquier tecla para cerrar esta ventana...
echo (Los servicios seguiran corriendo en segundo plano)
pause >nul
