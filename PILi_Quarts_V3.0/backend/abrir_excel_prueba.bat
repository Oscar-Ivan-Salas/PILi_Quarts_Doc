@echo off
echo ================================================================================
echo ABRIR EXCEL GENERADO POR N04_Binary_Factory
echo ================================================================================
echo.
echo Ubicacion: e:\PILi_Quarts\PILi_Quarts_V3.0\backend\PRUEBA_EXCEL_N04.xlsx
echo.

if exist "PRUEBA_EXCEL_N04.xlsx" (
    echo ✅ Archivo encontrado
    echo 📊 Abriendo Excel...
    start PRUEBA_EXCEL_N04.xlsx
    echo.
    echo ✅ Excel abierto
) else (
    echo ❌ Archivo NO encontrado
    echo.
    echo Generando nuevo Excel...
    python test_excel_n04.py
    echo.
    if exist "PRUEBA_EXCEL_N04.xlsx" (
        echo ✅ Excel generado
        start PRUEBA_EXCEL_N04.xlsx
    ) else (
        echo ❌ Error al generar Excel
    )
)

echo.
echo ================================================================================
pause
