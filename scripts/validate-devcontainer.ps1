# 🐳 DevContainer Setup Validator para Windows
# Este script verifica que todo esté listo para usar DevContainer

Write-Host "🐳 Validando configuración para DevContainer..." -ForegroundColor Blue

# Función para mostrar mensajes con colores
function Show-Success($message) {
    Write-Host "✅ $message" -ForegroundColor Green
}

function Show-Warning($message) {
    Write-Host "⚠️  $message" -ForegroundColor Yellow
}

function Show-Error($message) {
    Write-Host "❌ $message" -ForegroundColor Red
}

function Show-Info($message) {
    Write-Host "ℹ️  $message" -ForegroundColor Cyan
}

# Verificar Docker Desktop
Write-Host "`n📋 Verificando prerequisitos..." -ForegroundColor Blue

if (Get-Command docker -ErrorAction SilentlyContinue) {
    try {
        $dockerVersion = docker --version
        Show-Success "Docker está instalado: $dockerVersion"
        
        # Verificar que Docker esté corriendo
        docker ps | Out-Null
        if ($LASTEXITCODE -eq 0) {
            Show-Success "Docker Desktop está corriendo"
        } else {
            Show-Error "Docker Desktop no está corriendo. Inicia Docker Desktop primero."
            exit 1
        }
    } catch {
        Show-Error "Error al comunicarse con Docker. Verifica que Docker Desktop esté corriendo."
        exit 1
    }
} else {
    Show-Error "Docker no está instalado o no está en el PATH"
    Show-Info "Instala Docker Desktop desde: https://www.docker.com/products/docker-desktop"
    exit 1
}

# Verificar VS Code
if (Get-Command code -ErrorAction SilentlyContinue) {
    Show-Success "VS Code está instalado y disponible en PATH"
} else {
    Show-Warning "VS Code no está en PATH o no está instalado"
    Show-Info "Si VS Code está instalado, agrégalo al PATH o úsalo desde el menú"
}

# Verificar archivos de configuración DevContainer
Write-Host "`n📁 Verificando archivos de configuración..." -ForegroundColor Blue

$devcontainerFiles = @(
    ".devcontainer\devcontainer.json",
    ".devcontainer\docker-compose.yml",
    "docker-compose.yml",
    "backend\requirements\development.txt",
    "frontend\package.json"
)

foreach ($file in $devcontainerFiles) {
    if (Test-Path $file) {
        Show-Success "Encontrado: $file"
    } else {
        Show-Error "Falta archivo: $file"
    }
}

# Verificar estructura de directorios
Write-Host "`n📂 Verificando estructura de directorios..." -ForegroundColor Blue

$directories = @(
    "backend",
    "frontend", 
    "database",
    "docker",
    "scripts",
    ".devcontainer"
)

foreach ($dir in $directories) {
    if (Test-Path $dir -PathType Container) {
        Show-Success "Directorio encontrado: $dir"
    } else {
        Show-Warning "Directorio faltante: $dir"
    }
}

# Información sobre próximos pasos
Write-Host "`n🚀 Próximos pasos:" -ForegroundColor Blue
Write-Host "1. Abre VS Code en este directorio:" -ForegroundColor White
Write-Host "   code ." -ForegroundColor Gray
Write-Host "2. Instala la extensión 'Dev Containers' si no la tienes" -ForegroundColor White
Write-Host "3. VS Code debería detectar automáticamente la configuración DevContainer" -ForegroundColor White
Write-Host "4. Selecciona 'Reopen in Container' cuando aparezca la notificación" -ForegroundColor White
Write-Host "5. Una vez en el container, ejecuta: ./scripts/devcontainer-setup.sh" -ForegroundColor White

Write-Host "`n📚 Documentación:" -ForegroundColor Blue
Write-Host "- Guía DevContainer: DEVCONTAINER_QUICKSTART.md" -ForegroundColor White
Write-Host "- Documentación general: README.md" -ForegroundColor White

Write-Host "`n🌐 URLs después de iniciar:" -ForegroundColor Blue
Write-Host "- Frontend:  http://localhost:3000" -ForegroundColor White
Write-Host "- Backend:   http://localhost:8000" -ForegroundColor White
Write-Host "- Admin:     http://localhost:8000/admin" -ForegroundColor White
Write-Host "- PgAdmin:   http://localhost:5050" -ForegroundColor White

Write-Host "`n✨ ¡Todo listo para DevContainer! 🎉" -ForegroundColor Green