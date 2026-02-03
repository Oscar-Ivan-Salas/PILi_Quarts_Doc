@echo off
echo ===================================================
echo   REINICIO TOTAL DEL SISTEMA PILI QUARTS
echo ===================================================
echo.
echo 1. Cerrando procesos Zombie (Python y Node)...
taskkill /F /IM python.exe /T 2>nul
taskkill /F /IM node.exe /T 2>nul
echo.
echo 2. Esperando limpieza de puertos...
timeout /t 3 /nobreak >nul
echo.
echo 3. Iniciando Backend (Nueva ventana)...
start "Backend PILI" cmd /k "cd workspace-modern && start_backend.bat"
echo.
echo 4. Iniciando Frontend (Nueva ventana)...
start "Frontend PILI" cmd /k "cd workspace-modern && start_frontend.bat"
echo.
echo ===================================================
echo   SISTEMA REINICIADO - ESPERA 30 SEGUNDOS Y REFRESCA
echo ===================================================
pause
