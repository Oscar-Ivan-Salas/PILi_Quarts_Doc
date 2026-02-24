@echo off
REM Script para configurar HOME permanentemente en Windows
echo Configurando variable HOME en el sistema...

REM Configurar HOME para el usuario actual
setx HOME "%USERPROFILE%"

echo.
echo Variable HOME configurada a: %USERPROFILE%
echo.
echo IMPORTANTE: Debes cerrar y reabrir todas las ventanas de PowerShell/CMD
echo y reiniciar Antigravity para que los cambios surtan efecto.
echo.
pause
