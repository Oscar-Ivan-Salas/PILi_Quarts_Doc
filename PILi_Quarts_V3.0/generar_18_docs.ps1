# Generación RALFTH - 18 Documentos con PowerShell
# Usuario: ACEROS DEL PERU S.A.C.

Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "GENERACION RALFTH - 18 Documentos" -ForegroundColor Cyan
Write-Host "Usuario: ACEROS DEL PERU S.A.C." -ForegroundColor Cyan
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host ""

$baseUrl = "http://localhost:8005/api/generate"
$outputDir = "backend\generated"

# Datos del emisor
$emisor = @{
    nombre = "ACEROS DEL PERU S.A.C."
    empresa = "ACEROS DEL PERU S.A.C."
    ruc = "20456789012"
    direccion = "Av. Industrial 456, Callao"
    telefono = "01-4567890"
    email = "ventas@acerosdelperu.com"
}

# Función para generar documento
function Generate-Document {
    param(
        [string]$Number,
        [string]$Type,
        [string]$Format,
        [string]$DocType,
        [hashtable]$Data
    )
    
    $filename = "${Number}_${Type}.${Format}"
    $endpoint = "$baseUrl/$Format"
    
    $payload = @{
        title = "${Type}_ACEROS"
        user_id = "aceros_peru"
        doc_type = $DocType
        data = $Data
        personalizacion = @{
            esquemaColores = "azul-tesla"
            logoBase64 = $null
            ocultarIGV = $false
        }
    } | ConvertTo-Json -Depth 10
    
    Write-Host "[$Number/18] Generando: $Type - $Format" -ForegroundColor Yellow
    
    try {
        $response = Invoke-WebRequest -Uri $endpoint -Method POST -Body $payload -ContentType "application/json" -OutFile "$outputDir\$filename"
        Write-Host "  ✓ Guardado: $filename" -ForegroundColor Green
    } catch {
        Write-Host "  ✗ Error: $_" -ForegroundColor Red
    }
}

# 1. COTIZACION SIMPLE
$dataSimple = @{
    emisor = $emisor
    cliente = @{ nombre = "MINERA DEL SUR S.A."; ruc = "20123456789" }
    proyecto = @{ nombre = "Estructuras Metalicas Planta Lima" }
    numero = "COT-001-2026"
    fecha = "17/02/2026"
    items = @(
        @{ descripcion = "Vigas de Acero H 200x200"; cantidad = 50; precio_unitario = 850.00; precioUnitario = 850.00 }
        @{ descripcion = "Columnas Metalicas 300x300"; cantidad = 30; precio_unitario = 1200.00; precioUnitario = 1200.00 }
    )
}

Generate-Document "01" "Cotizacion_Simple" "docx" "Cotizacion_Simple" $dataSimple
Generate-Document "02" "Cotizacion_Simple" "xlsx" "Cotizacion_Simple" $dataSimple
Generate-Document "03" "Cotizacion_Simple" "pdf" "Cotizacion_Simple" $dataSimple

# 2. COTIZACION COMPLEJA
$dataCompleja = @{
    emisor = $emisor
    cliente = @{ nombre = "MINERA DEL SUR S.A." }
    numero = "COT-002-2026"
    items = @(
        @{ descripcion = "Vigas de Acero"; cantidad = 50; precio_unitario = 850.00 }
        @{ descripcion = "Columnas"; cantidad = 30; precio_unitario = 1200.00 }
    )
}

Generate-Document "04" "Cotizacion_Compleja" "docx" "Cotizacion_Compleja" $dataCompleja
Generate-Document "05" "Cotizacion_Compleja" "xlsx" "Cotizacion_Compleja" $dataCompleja
Generate-Document "06" "Cotizacion_Compleja" "pdf" "Cotizacion_Compleja" $dataCompleja

# 3. PROYECTO SIMPLE
$dataProySimple = @{
    emisor = $emisor
    cliente = @{ nombre = "MINERA DEL SUR S.A." }
    proyecto = @{ nombre = "Estructuras Metalicas" }
    fases = @(
        @{ nombre = "Diseno"; duracion = 15; costo = 8500.00 }
        @{ nombre = "Fabricacion"; duracion = 45; costo = 85000.00 }
    )
}

Generate-Document "07" "Proyecto_Simple" "docx" "Proyecto_Simple" $dataProySimple
Generate-Document "08" "Proyecto_Simple" "xlsx" "Proyecto_Simple" $dataProySimple
Generate-Document "09" "Proyecto_Simple" "pdf" "Proyecto_Simple" $dataProySimple

# 4. PROYECTO COMPLEJO PMI
$dataProyPMI = @{
    emisor = $emisor
    cliente = @{ nombre = "MINERA DEL SUR S.A." }
    proyecto = @{ nombre = "Estructuras Metalicas" }
    fases = @(
        @{ nombre = "Diseno"; duracion = 15; costo = 8500.00 }
    )
    riesgos = @(
        @{ descripcion = "Retraso materiales"; probabilidad = "Media"; impacto = "Alto"; mitigacion = "Proveedores alternativos" }
    )
}

Generate-Document "10" "Proyecto_Complejo_PMI" "docx" "Proyecto_Complejo_PMI" $dataProyPMI
Generate-Document "11" "Proyecto_Complejo_PMI" "xlsx" "Proyecto_Complejo_PMI" $dataProyPMI
Generate-Document "12" "Proyecto_Complejo_PMI" "pdf" "Proyecto_Complejo_PMI" $dataProyPMI

# 5. INFORME TECNICO
$dataInfTec = @{
    emisor = $emisor
    cliente = @{ nombre = "MINERA DEL SUR S.A." }
    informe = @{ titulo = "Inspeccion Tecnica"; fecha = "17/02/2026"; inspector = "Ing. Mendoza" }
    hallazgos = @(
        @{ descripcion = "Corrosion en vigas"; severidad = "Media"; recomendacion = "Tratamiento anticorrosivo" }
    )
}

Generate-Document "13" "Informe_Tecnico" "docx" "Informe_Tecnico" $dataInfTec
Generate-Document "14" "Informe_Tecnico" "xlsx" "Informe_Tecnico" $dataInfTec
Generate-Document "15" "Informe_Tecnico" "pdf" "Informe_Tecnico" $dataInfTec

# 6. INFORME EJECUTIVO APA
$dataInfEjec = @{
    emisor = $emisor
    cliente = @{ nombre = "MINERA DEL SUR S.A." }
    informe = @{ titulo = "Informe Ejecutivo"; fecha = "17/02/2026" }
    conclusiones = @(
        "Mantenimiento preventivo requerido"
        "Inspeccion trimestral recomendada"
    )
}

Generate-Document "16" "Informe_Ejecutivo_APA" "docx" "Informe_Ejecutivo_APA" $dataInfEjec
Generate-Document "17" "Informe_Ejecutivo_APA" "xlsx" "Informe_Ejecutivo_APA" $dataInfEjec
Generate-Document "18" "Informe_Ejecutivo_APA" "pdf" "Informe_Ejecutivo_APA" $dataInfEjec

Write-Host ""
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "RESUMEN FINAL" -ForegroundColor Cyan
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "Documentos generados en: $outputDir" -ForegroundColor Green
Get-ChildItem $outputDir | Format-Table Name, Length -AutoSize
