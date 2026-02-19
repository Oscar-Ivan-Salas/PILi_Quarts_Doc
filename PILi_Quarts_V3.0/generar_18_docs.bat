@echo off
REM Generacion RALFTH - 18 Documentos (6 tipos x 3 formatos)
REM Usuario: ACEROS DEL PERU S.A.C.

echo ================================================================================
echo GENERACION RALFTH - 18 Documentos
echo Usuario: ACEROS DEL PERU S.A.C.
echo ================================================================================
echo.

REM ============================================================================
REM 1. COTIZACION SIMPLE (Word, Excel, PDF)
REM ============================================================================
echo [1/18] Generando: Cotizacion Simple - WORD
curl -X POST http://localhost:8005/api/generate/word -H "Content-Type: application/json" -d "{\"title\":\"Cotizacion_Simple_ACEROS\",\"user_id\":\"aceros_peru\",\"doc_type\":\"Cotizacion_Simple\",\"data\":{\"emisor\":{\"nombre\":\"ACEROS DEL PERU S.A.C.\",\"empresa\":\"ACEROS DEL PERU S.A.C.\",\"ruc\":\"20456789012\",\"direccion\":\"Av. Industrial 456, Callao\",\"telefono\":\"01-4567890\",\"email\":\"ventas@acerosdelperu.com\"},\"cliente\":{\"nombre\":\"MINERA DEL SUR S.A.\",\"ruc\":\"20123456789\"},\"proyecto\":{\"nombre\":\"Estructuras Metalicas Planta Lima\"},\"numero\":\"COT-001-2026\",\"fecha\":\"17/02/2026\",\"vigencia\":\"30 dias\",\"servicio\":\"Fabricacion de Estructuras Metalicas\",\"area_m2\":\"500\",\"items\":[{\"descripcion\":\"Vigas de Acero H 200x200\",\"cantidad\":50,\"unidad\":\"und\",\"precio_unitario\":850.00,\"precioUnitario\":850.00},{\"descripcion\":\"Columnas Metalicas 300x300\",\"cantidad\":30,\"unidad\":\"und\",\"precio_unitario\":1200.00,\"precioUnitario\":1200.00}],\"suministros\":[{\"descripcion\":\"Vigas de Acero H 200x200\",\"cantidad\":50,\"precioUnitario\":850.00,\"precioTotal\":42500.00},{\"descripcion\":\"Columnas Metalicas 300x300\",\"cantidad\":30,\"precioUnitario\":1200.00,\"precioTotal\":36000.00}]},\"personalizacion\":{\"esquemaColores\":\"azul-tesla\",\"logoBase64\":null,\"ocultarIGV\":false}}" --output "backend\generated\01_Cotizacion_Simple.docx"

echo [2/18] Generando: Cotizacion Simple - EXCEL
curl -X POST http://localhost:8005/api/generate/excel -H "Content-Type: application/json" -d "{\"title\":\"Cotizacion_Simple_ACEROS\",\"user_id\":\"aceros_peru\",\"data\":{\"emisor\":{\"nombre\":\"ACEROS DEL PERU S.A.C.\",\"ruc\":\"20456789012\",\"direccion\":\"Av. Industrial 456, Callao\",\"email\":\"ventas@acerosdelperu.com\"},\"cliente\":{\"nombre\":\"MINERA DEL SUR S.A.\"},\"items\":[{\"descripcion\":\"Vigas de Acero H 200x200\",\"cantidad\":50,\"precio_unitario\":850.00},{\"descripcion\":\"Columnas Metalicas 300x300\",\"cantidad\":30,\"precio_unitario\":1200.00}]},\"personalizacion\":{\"esquemaColores\":\"azul-tesla\"}}" --output "backend\generated\01_Cotizacion_Simple.xlsx"

echo [3/18] Generando: Cotizacion Simple - PDF
curl -X POST http://localhost:8005/api/generate/pdf -H "Content-Type: application/json" -d "{\"title\":\"Cotizacion_Simple_ACEROS\",\"user_id\":\"aceros_peru\",\"data\":{\"emisor\":{\"nombre\":\"ACEROS DEL PERU S.A.C.\",\"ruc\":\"20456789012\"},\"cliente\":{\"nombre\":\"MINERA DEL SUR S.A.\"},\"items\":[{\"descripcion\":\"Vigas de Acero\",\"cantidad\":50,\"precio_unitario\":850.00}]},\"personalizacion\":{\"esquemaColores\":\"azul-tesla\"}}" --output "backend\generated\01_Cotizacion_Simple.pdf"

REM ============================================================================
REM 2. COTIZACION COMPLEJA (Word, Excel, PDF)
REM ============================================================================
echo [4/18] Generando: Cotizacion Compleja - WORD
curl -X POST http://localhost:8005/api/generate/word -H "Content-Type: application/json" -d "{\"title\":\"Cotizacion_Compleja_ACEROS\",\"user_id\":\"aceros_peru\",\"doc_type\":\"Cotizacion_Compleja\",\"data\":{\"emisor\":{\"nombre\":\"ACEROS DEL PERU S.A.C.\",\"ruc\":\"20456789012\",\"direccion\":\"Av. Industrial 456, Callao\",\"email\":\"ventas@acerosdelperu.com\"},\"cliente\":{\"nombre\":\"MINERA DEL SUR S.A.\"},\"numero\":\"COT-002-2026\",\"items\":[{\"descripcion\":\"Vigas de Acero H 200x200\",\"cantidad\":50,\"precio_unitario\":850.00},{\"descripcion\":\"Columnas Metalicas 300x300\",\"cantidad\":30,\"precio_unitario\":1200.00},{\"descripcion\":\"Planchas de Acero A36 6mm\",\"cantidad\":100,\"precio_unitario\":180.00}]},\"personalizacion\":{\"esquemaColores\":\"azul-tesla\"}}" --output "backend\generated\02_Cotizacion_Compleja.docx"

echo [5/18] Generando: Cotizacion Compleja - EXCEL
curl -X POST http://localhost:8005/api/generate/excel -H "Content-Type: application/json" -d "{\"title\":\"Cotizacion_Compleja_ACEROS\",\"user_id\":\"aceros_peru\",\"data\":{\"emisor\":{\"nombre\":\"ACEROS DEL PERU S.A.C.\",\"ruc\":\"20456789012\"},\"items\":[{\"descripcion\":\"Vigas\",\"cantidad\":50,\"precio_unitario\":850.00}]},\"personalizacion\":{\"esquemaColores\":\"azul-tesla\"}}" --output "backend\generated\02_Cotizacion_Compleja.xlsx"

echo [6/18] Generando: Cotizacion Compleja - PDF
curl -X POST http://localhost:8005/api/generate/pdf -H "Content-Type: application/json" -d "{\"title\":\"Cotizacion_Compleja_ACEROS\",\"user_id\":\"aceros_peru\",\"data\":{\"emisor\":{\"nombre\":\"ACEROS DEL PERU S.A.C.\",\"ruc\":\"20456789012\"},\"items\":[{\"descripcion\":\"Vigas\",\"cantidad\":50,\"precio_unitario\":850.00}]},\"personalizacion\":{\"esquemaColores\":\"azul-tesla\"}}" --output "backend\generated\02_Cotizacion_Compleja.pdf"

REM ============================================================================
REM 3. PROYECTO SIMPLE (Word, Excel, PDF)
REM ============================================================================
echo [7/18] Generando: Proyecto Simple - WORD
curl -X POST http://localhost:8005/api/generate/word -H "Content-Type: application/json" -d "{\"title\":\"Proyecto_Simple_ACEROS\",\"user_id\":\"aceros_peru\",\"doc_type\":\"Proyecto_Simple\",\"data\":{\"emisor\":{\"nombre\":\"ACEROS DEL PERU S.A.C.\",\"ruc\":\"20456789012\",\"direccion\":\"Av. Industrial 456, Callao\",\"email\":\"ventas@acerosdelperu.com\"},\"cliente\":{\"nombre\":\"MINERA DEL SUR S.A.\"},\"proyecto\":{\"nombre\":\"Estructuras Metalicas Planta Lima\"},\"fases\":[{\"nombre\":\"Diseno Estructural\",\"duracion\":15,\"costo\":8500.00},{\"nombre\":\"Fabricacion\",\"duracion\":45,\"costo\":85000.00},{\"nombre\":\"Montaje\",\"duracion\":20,\"costo\":25000.00}]},\"personalizacion\":{\"esquemaColores\":\"azul-tesla\"}}" --output "backend\generated\03_Proyecto_Simple.docx"

echo [8/18] Generando: Proyecto Simple - EXCEL
curl -X POST http://localhost:8005/api/generate/excel -H "Content-Type: application/json" -d "{\"title\":\"Proyecto_Simple_ACEROS\",\"user_id\":\"aceros_peru\",\"data\":{\"emisor\":{\"nombre\":\"ACEROS DEL PERU S.A.C.\",\"ruc\":\"20456789012\"},\"fases\":[{\"nombre\":\"Diseno\",\"duracion\":15,\"costo\":8500.00}]},\"personalizacion\":{\"esquemaColores\":\"azul-tesla\"}}" --output "backend\generated\03_Proyecto_Simple.xlsx"

echo [9/18] Generando: Proyecto Simple - PDF
curl -X POST http://localhost:8005/api/generate/pdf -H "Content-Type: application/json" -d "{\"title\":\"Proyecto_Simple_ACEROS\",\"user_id\":\"aceros_peru\",\"data\":{\"emisor\":{\"nombre\":\"ACEROS DEL PERU S.A.C.\",\"ruc\":\"20456789012\"},\"fases\":[{\"nombre\":\"Diseno\",\"duracion\":15,\"costo\":8500.00}]},\"personalizacion\":{\"esquemaColores\":\"azul-tesla\"}}" --output "backend\generated\03_Proyecto_Simple.pdf"

REM ============================================================================
REM 4. PROYECTO COMPLEJO PMI (Word, Excel, PDF)
REM ============================================================================
echo [10/18] Generando: Proyecto Complejo PMI - WORD
curl -X POST http://localhost:8005/api/generate/word -H "Content-Type: application/json" -d "{\"title\":\"Proyecto_Complejo_PMI_ACEROS\",\"user_id\":\"aceros_peru\",\"doc_type\":\"Proyecto_Complejo_PMI\",\"data\":{\"emisor\":{\"nombre\":\"ACEROS DEL PERU S.A.C.\",\"ruc\":\"20456789012\",\"direccion\":\"Av. Industrial 456, Callao\",\"email\":\"ventas@acerosdelperu.com\"},\"cliente\":{\"nombre\":\"MINERA DEL SUR S.A.\"},\"proyecto\":{\"nombre\":\"Estructuras Metalicas Planta Lima\"},\"fases\":[{\"nombre\":\"Diseno\",\"duracion\":15,\"costo\":8500.00}],\"riesgos\":[{\"descripcion\":\"Retraso en entrega de materiales\",\"probabilidad\":\"Media\",\"impacto\":\"Alto\",\"mitigacion\":\"Contratos con proveedores alternativos\"}]},\"personalizacion\":{\"esquemaColores\":\"azul-tesla\"}}" --output "backend\generated\04_Proyecto_Complejo_PMI.docx"

echo [11/18] Generando: Proyecto Complejo PMI - EXCEL
curl -X POST http://localhost:8005/api/generate/excel -H "Content-Type: application/json" -d "{\"title\":\"Proyecto_Complejo_PMI_ACEROS\",\"user_id\":\"aceros_peru\",\"data\":{\"emisor\":{\"nombre\":\"ACEROS DEL PERU S.A.C.\",\"ruc\":\"20456789012\"},\"fases\":[{\"nombre\":\"Diseno\",\"duracion\":15,\"costo\":8500.00}]},\"personalizacion\":{\"esquemaColores\":\"azul-tesla\"}}" --output "backend\generated\04_Proyecto_Complejo_PMI.xlsx"

echo [12/18] Generando: Proyecto Complejo PMI - PDF
curl -X POST http://localhost:8005/api/generate/pdf -H "Content-Type: application/json" -d "{\"title\":\"Proyecto_Complejo_PMI_ACEROS\",\"user_id\":\"aceros_peru\",\"data\":{\"emisor\":{\"nombre\":\"ACEROS DEL PERU S.A.C.\",\"ruc\":\"20456789012\"},\"fases\":[{\"nombre\":\"Diseno\",\"duracion\":15,\"costo\":8500.00}]},\"personalizacion\":{\"esquemaColores\":\"azul-tesla\"}}" --output "backend\generated\04_Proyecto_Complejo_PMI.pdf"

REM ============================================================================
REM 5. INFORME TECNICO (Word, Excel, PDF)
REM ============================================================================
echo [13/18] Generando: Informe Tecnico - WORD
curl -X POST http://localhost:8005/api/generate/word -H "Content-Type: application/json" -d "{\"title\":\"Informe_Tecnico_ACEROS\",\"user_id\":\"aceros_peru\",\"doc_type\":\"Informe_Tecnico\",\"data\":{\"emisor\":{\"nombre\":\"ACEROS DEL PERU S.A.C.\",\"ruc\":\"20456789012\",\"direccion\":\"Av. Industrial 456, Callao\",\"email\":\"ventas@acerosdelperu.com\"},\"cliente\":{\"nombre\":\"MINERA DEL SUR S.A.\"},\"informe\":{\"titulo\":\"Inspeccion Tecnica Estructuras Metalicas\",\"fecha\":\"17/02/2026\",\"inspector\":\"Ing. Carlos Mendoza\"},\"hallazgos\":[{\"descripcion\":\"Corrosion en vigas principales\",\"severidad\":\"Media\",\"recomendacion\":\"Aplicar tratamiento anticorrosivo\"}]},\"personalizacion\":{\"esquemaColores\":\"azul-tesla\"}}" --output "backend\generated\05_Informe_Tecnico.docx"

echo [14/18] Generando: Informe Tecnico - EXCEL
curl -X POST http://localhost:8005/api/generate/excel -H "Content-Type: application/json" -d "{\"title\":\"Informe_Tecnico_ACEROS\",\"user_id\":\"aceros_peru\",\"data\":{\"emisor\":{\"nombre\":\"ACEROS DEL PERU S.A.C.\",\"ruc\":\"20456789012\"},\"hallazgos\":[{\"descripcion\":\"Corrosion\",\"severidad\":\"Media\"}]},\"personalizacion\":{\"esquemaColores\":\"azul-tesla\"}}" --output "backend\generated\05_Informe_Tecnico.xlsx"

echo [15/18] Generando: Informe Tecnico - PDF
curl -X POST http://localhost:8005/api/generate/pdf -H "Content-Type: application/json" -d "{\"title\":\"Informe_Tecnico_ACEROS\",\"user_id\":\"aceros_peru\",\"data\":{\"emisor\":{\"nombre\":\"ACEROS DEL PERU S.A.C.\",\"ruc\":\"20456789012\"},\"hallazgos\":[{\"descripcion\":\"Corrosion\",\"severidad\":\"Media\"}]},\"personalizacion\":{\"esquemaColores\":\"azul-tesla\"}}" --output "backend\generated\05_Informe_Tecnico.pdf"

REM ============================================================================
REM 6. INFORME EJECUTIVO APA (Word, Excel, PDF)
REM ============================================================================
echo [16/18] Generando: Informe Ejecutivo APA - WORD
curl -X POST http://localhost:8005/api/generate/word -H "Content-Type: application/json" -d "{\"title\":\"Informe_Ejecutivo_APA_ACEROS\",\"user_id\":\"aceros_peru\",\"doc_type\":\"Informe_Ejecutivo_APA\",\"data\":{\"emisor\":{\"nombre\":\"ACEROS DEL PERU S.A.C.\",\"ruc\":\"20456789012\",\"direccion\":\"Av. Industrial 456, Callao\",\"email\":\"ventas@acerosdelperu.com\"},\"cliente\":{\"nombre\":\"MINERA DEL SUR S.A.\"},\"informe\":{\"titulo\":\"Informe Ejecutivo Estructuras Metalicas\",\"fecha\":\"17/02/2026\"},\"conclusiones\":[\"Las estructuras metalicas requieren mantenimiento preventivo\",\"Se recomienda inspeccion trimestral\"]},\"personalizacion\":{\"esquemaColores\":\"azul-tesla\"}}" --output "backend\generated\06_Informe_Ejecutivo_APA.docx"

echo [17/18] Generando: Informe Ejecutivo APA - EXCEL
curl -X POST http://localhost:8005/api/generate/excel -H "Content-Type: application/json" -d "{\"title\":\"Informe_Ejecutivo_APA_ACEROS\",\"user_id\":\"aceros_peru\",\"data\":{\"emisor\":{\"nombre\":\"ACEROS DEL PERU S.A.C.\",\"ruc\":\"20456789012\"},\"conclusiones\":[\"Mantenimiento requerido\"]},\"personalizacion\":{\"esquemaColores\":\"azul-tesla\"}}" --output "backend\generated\06_Informe_Ejecutivo_APA.xlsx"

echo [18/18] Generando: Informe Ejecutivo APA - PDF
curl -X POST http://localhost:8005/api/generate/pdf -H "Content-Type: application/json" -d "{\"title\":\"Informe_Ejecutivo_APA_ACEROS\",\"user_id\":\"aceros_peru\",\"data\":{\"emisor\":{\"nombre\":\"ACEROS DEL PERU S.A.C.\",\"ruc\":\"20456789012\"},\"conclusiones\":[\"Mantenimiento requerido\"]},\"personalizacion\":{\"esquemaColores\":\"azul-tesla\"}}" --output "backend\generated\06_Informe_Ejecutivo_APA.pdf"

echo.
echo ================================================================================
echo RESUMEN FINAL
echo ================================================================================
echo Total documentos generados: 18
echo - 6 tipos de documentos
echo - 3 formatos por tipo (Word, Excel, PDF)
echo.
echo Ubicacion: backend\generated\
echo ================================================================================
echo.
dir backend\generated /b
echo.
pause
