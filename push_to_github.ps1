# Script de Automatización de Subida a GitHub - PILi_Quarts
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "   🚀 ASISTENTE DE SUBIDA A GITHUB (PILi)    " -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Este script conectará tu repositorio local con GitHub."
Write-Host "Asegúrate de haber creado un repositorio VACÍO en https://github.com/new"
Write-Host ""

# 1. Solicitar URL
$repoUrl = Read-Host "👉 Pega aquí la URL de tu repositorio (ej. https://github.com/usuario/repo.git)"

if ([string]::IsNullOrWhiteSpace($repoUrl)) {
    Write-Error "❌ No ingresaste ninguna URL. Abortando."
    exit 1
}

# 2. Configurar Remoto
Write-Host ""
Write-Host "🔗 Conectando con: $repoUrl..." -ForegroundColor Yellow
git remote remove origin 2>$null # Limpiar si existe
git remote add origin $repoUrl

# 3. Renombrar rama y subir
Write-Host "🌳 Configurando rama 'main'..." -ForegroundColor Yellow
git branch -M main

Write-Host "⬆️ Subiendo código (Se abrirá una ventana de login si es necesario)..." -ForegroundColor Green
git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ ¡ÉXITO! Tu código está en GitHub." -ForegroundColor Green
    Write-Host "🔗 Ver aquí: $repoUrl"
}
else {
    Write-Error "❌ Hubo un error al subir. Verifica tus permisos o la URL."
}

Pause
