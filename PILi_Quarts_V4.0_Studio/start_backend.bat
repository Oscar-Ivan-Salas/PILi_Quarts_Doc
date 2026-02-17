@echo off
title PILi Quarts - BACKEND (Puerto 8005)
color 0A
cd /d "%~dp0"

echo [1/4] Verificando Entorno...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    color 0C
    echo ERROR CRITICO: Python no detectado.
    pause
    exit /b
)

echo [2/4] Liberando puerto 8002...
for /f "tokens=5" %%a in ('netstat -aon ^| find ":8002" ^| find "LISTENING"') do (
    taskkill /f /pid %%a >nul 2>&1
)

echo [3/4] Inicializando...
cd backend

echo Iniciando Backend con VENV explicito...
venv\Scripts\python.exe -m uvicorn main:app --host 0.0.0.0 --port 8005 --reload

pause
