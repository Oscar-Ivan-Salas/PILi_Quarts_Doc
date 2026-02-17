# Script para aplicar diseño minimalista a todos los formularios
# Este script reemplaza los estilos antiguos por los nuevos con transparencias

$files = @(
    "e:\PILi_Quarts\PILi_Quarts_V3.0\frontend\src\components\ComplexProjectForm.tsx",
    "e:\PILi_Quarts\PILi_Quarts_V3.0\frontend\src\components\forms\ProjectForm.tsx",
    "e:\PILi_Quarts\PILi_Quarts_V3.0\frontend\src\components\forms\QuoteForm.tsx",
    "e:\PILi_Quarts\PILi_Quarts_V3.0\frontend\src\components\forms\ReportForm.tsx"
)

foreach ($file in $files) {
    if (Test-Path $file) {
        Write-Host "Procesando: $file"
        
        $content = Get-Content $file -Raw
        
        # 1. Contenedores de secciones
        $content = $content -replace 'bg-gradient-to-br from-gray-900 to-black rounded-2xl p-6 border-2 border-yellow-600 shadow-xl', 'bg-gray-900/40 backdrop-blur-xl rounded-2xl p-6 border border-yellow-600/30 shadow-2xl'
        
        # 2. Botones con gradiente amarillo (texto negro -> blanco)
        $content = $content -replace 'bg-gradient-to-r from-yellow-600 via-yellow-500 to-yellow-600 hover:from-yellow-500 hover:to-yellow-400 text-black', 'bg-gradient-to-r from-yellow-600/30 via-yellow-500/40 to-yellow-600/30 hover:from-yellow-500/40 hover:to-yellow-400/50 backdrop-blur-sm text-white border border-yellow-400/30'
        
        # 3. Campos de entrada (inputs, selects, textareas)
        $content = $content -replace 'w-full px-4 py-3 bg-gray-950 border border-yellow-700 rounded-xl focus:ring-2 focus:ring-yellow-500 focus:outline-none text-white placeholder-gray-600', 'w-full px-4 py-3 bg-gray-950/50 backdrop-blur-sm border border-yellow-700/30 rounded-xl focus:ring-2 focus:ring-yellow-500/50 focus:outline-none text-white placeholder-gray-500 transition-all'
        
        # 4. Contenedores de vista previa/logo
        $content = $content -replace 'bg-white rounded-xl p-3 border-2 border-yellow-400 shadow-lg', 'bg-white/10 backdrop-blur-sm rounded-xl p-3 border border-yellow-400/30 shadow-lg'
        
        # 5. Bordes de botones
        $content = $content -replace 'border-2 border-yellow-400', 'border border-yellow-400/30'
        
        # 6. Inputs sin placeholder específico
        $content = $content -replace 'bg-gray-950 border border-yellow-700 rounded-xl focus:ring-2 focus:ring-yellow-500 focus:outline-none text-white', 'bg-gray-950/50 backdrop-blur-sm border border-yellow-700/30 rounded-xl focus:ring-2 focus:ring-yellow-500/50 focus:outline-none text-white transition-all'
        
        # 7. Selects
        $content = $content -replace 'bg-gray-950 border border-yellow-700 rounded-xl focus:ring-2 focus:ring-yellow-500 focus:outline-none', 'bg-gray-950/50 backdrop-blur-sm border border-yellow-700/30 rounded-xl focus:ring-2 focus:ring-yellow-500/50 focus:outline-none transition-all'
        
        Set-Content $file $content
        Write-Host "✓ Completado: $file"
    } else {
        Write-Host "✗ No encontrado: $file"
    }
}

Write-Host "`n✅ Proceso completado para todos los formularios"
