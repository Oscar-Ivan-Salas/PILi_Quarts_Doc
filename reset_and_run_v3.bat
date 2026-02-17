@echo off
echo ===================================================
echo   REINICIO MAESTRO - PILI QUARTS V3.0 (ALTA FIDELIDAD)
echo ===================================================
echo.
echo 1. Limpiando procesos bloqueados (Python/Node)...
taskkill /F /IM python.exe /T 2>nul
taskkill /F /IM node.exe /T 2>nul
echo.
echo 2. Esperando liberacion de puertos (8005, 3010)...
timeout /t 3 /nobreak >nul
echo.
echo 3. Iniciando BACKEND V3.0 (Puerto 8005)...
start "Backend V3.0" cmd /k "cd PILi_Quarts_V3.0 && start_backend.bat"
echo.
echo 4. Iniciando FRONTEND V3.0 (Puerto 3010)...
start "Frontend V3.0" cmd /k "cd PILi_Quarts_V3.0 && start_frontend.bat"
echo.
echo ===================================================
echo   SISTEMA V3.0 INICIADO - REVISA LAS NUEVAS VENTANAS
echo ===================================================
pause
