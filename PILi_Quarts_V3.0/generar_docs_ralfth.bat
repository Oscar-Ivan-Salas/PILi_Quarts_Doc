@echo off
REM Script de Generación Masiva RALFTH - 54 Documentos
REM 3 Usuarios × 6 Tipos × 3 Formatos = 54 archivos

echo ================================================================================
echo SIMULACION RALFTH - Generacion Masiva de Documentos
echo ================================================================================
echo.

REM Usuario 1: ACEROS DEL PERU - Cotizacion Simple - Word
echo [1/54] Generando: ACEROS_DEL_PERU - Cotizacion_Simple - WORD
curl -X POST http://localhost:8005/api/generate/word ^
  -H "Content-Type: application/json" ^
  -d "{\"title\":\"ACEROS_DEL_PERU_Cotizacion_Simple\",\"user_id\":\"aceros_del_peru\",\"doc_type\":\"Cotizacion_Simple\",\"data\":{\"emisor\":{\"nombre\":\"ACEROS DEL PERU S.A.C.\",\"empresa\":\"ACEROS DEL PERU S.A.C.\",\"ruc\":\"20456789012\",\"direccion\":\"Av. Industrial 456, Callao\",\"telefono\":\"01-4567890\",\"email\":\"ventas@acerosdelperu.com\"},\"cliente\":{\"nombre\":\"MINERA DEL SUR S.A.\",\"ruc\":\"20123456789\"},\"proyecto\":{\"nombre\":\"Estructuras Metalicas Planta Lima\"},\"items\":[{\"descripcion\":\"Vigas de Acero H 200x200\",\"cantidad\":50,\"unidad\":\"und\",\"precio_unitario\":850.00,\"precioUnitario\":850.00},{\"descripcion\":\"Columnas Metalicas 300x300\",\"cantidad\":30,\"unidad\":\"und\",\"precio_unitario\":1200.00,\"precioUnitario\":1200.00}]},\"personalizacion\":{\"esquemaColores\":\"azul-tesla\",\"logoBase64\":null,\"ocultarIGV\":false}}" ^
  --output "backend\generated\ACEROS_DEL_PERU_Cotizacion_Simple.docx"

echo [2/54] Generando: ACEROS_DEL_PERU - Cotizacion_Simple - EXCEL
curl -X POST http://localhost:8005/api/generate/excel ^
  -H "Content-Type: application/json" ^
  -d "{\"title\":\"ACEROS_DEL_PERU_Cotizacion_Simple\",\"user_id\":\"aceros_del_peru\",\"data\":{\"emisor\":{\"nombre\":\"ACEROS DEL PERU S.A.C.\",\"ruc\":\"20456789012\",\"direccion\":\"Av. Industrial 456, Callao\",\"email\":\"ventas@acerosdelperu.com\"},\"cliente\":{\"nombre\":\"MINERA DEL SUR S.A.\"},\"items\":[{\"descripcion\":\"Vigas de Acero\",\"cantidad\":50,\"precio_unitario\":850.00}]},\"personalizacion\":{\"esquemaColores\":\"azul-tesla\"}}" ^
  --output "backend\generated\ACEROS_DEL_PERU_Cotizacion_Simple.xlsx"

echo [3/54] Generando: ACEROS_DEL_PERU - Cotizacion_Simple - PDF
curl -X POST http://localhost:8005/api/generate/pdf ^
  -H "Content-Type: application/json" ^
  -d "{\"title\":\"ACEROS_DEL_PERU_Cotizacion_Simple\",\"user_id\":\"aceros_del_peru\",\"data\":{\"emisor\":{\"nombre\":\"ACEROS DEL PERU S.A.C.\",\"ruc\":\"20456789012\"},\"cliente\":{\"nombre\":\"MINERA DEL SUR S.A.\"}},\"personalizacion\":{\"esquemaColores\":\"azul-tesla\"}}" ^
  --output "backend\generated\ACEROS_DEL_PERU_Cotizacion_Simple.pdf"

echo.
echo ================================================================================
echo RESUMEN: 3 documentos generados para ACEROS DEL PERU
echo Ubicacion: backend\generated\
echo ================================================================================
pause
