# ============================================================================
# Portfolio Tracker - Setup Script para Windows
# ============================================================================
# 
# Este script instala y configura todo el sistema automáticamente en Windows.
#
# Requisitos previos:
# - Python 3.11+
# - Node.js 18+
# - Git
#
# Uso:
#   .\scripts\setup_windows.ps1
#
# ============================================================================

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Portfolio Tracker - Setup Wizard" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Función para verificar si un comando existe
function Test-Command($cmdname) {
    return [bool](Get-Command -Name $cmdname -ErrorAction SilentlyContinue)
}

# Función para imprimir con color
function Write-Step($message) {
    Write-Host "`n[STEP] $message" -ForegroundColor Green
}

function Write-Error-Custom($message) {
    Write-Host "[ERROR] $message" -ForegroundColor Red
}

function Write-Success($message) {
    Write-Host "[OK] $message" -ForegroundColor Green
}

# ============================================================================
# STEP 1: Verificar requisitos previos
# ============================================================================

Write-Step "Verificando requisitos previos..."

# Verificar Python
if (Test-Command python) {
    $pythonVersion = python --version 2>&1
    Write-Success "Python encontrado: $pythonVersion"
    
    # Verificar versión mínima (3.11)
    if ($pythonVersion -match "Python 3\.([0-9]+)") {
        $minorVersion = [int]$matches[1]
        if ($minorVersion -lt 11) {
            Write-Error-Custom "Python 3.11 o superior requerido. Versión actual: $pythonVersion"
            Write-Host "Descarga Python desde: https://www.python.org/downloads/"
            exit 1
        }
    }
} else {
    Write-Error-Custom "Python no encontrado"
    Write-Host "Descarga Python 3.11+ desde: https://www.python.org/downloads/"
    exit 1
}

# Verificar Node.js
if (Test-Command node) {
    $nodeVersion = node --version 2>&1
    Write-Success "Node.js encontrado: $nodeVersion"
} else {
    Write-Error-Custom "Node.js no encontrado"
    Write-Host "Descarga Node.js 18+ desde: https://nodejs.org/"
    exit 1
}

# Verificar pip
if (Test-Command pip) {
    Write-Success "pip encontrado"
} else {
    Write-Error-Custom "pip no encontrado"
    exit 1
}

# ============================================================================
# STEP 2: Crear directorios necesarios
# ============================================================================

Write-Step "Creando estructura de directorios..."

$directories = @(
    "backend/app/api/v1/endpoints",
    "backend/app/core",
    "backend/app/models",
    "backend/app/repositories",
    "backend/app/schemas",
    "backend/app/services",
    "backend/app/workers",
    "backend/app/providers",
    "backend/alembic/versions",
    "backend/tests",
    "frontend/src/components",
    "frontend/src/services",
    "frontend/src/stores",
    "frontend/src/types",
    "frontend/src/utils",
    "frontend/public",
    "docs",
    "logs"
)

foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "  Creado: $dir" -ForegroundColor Gray
    }
}

Write-Success "Estructura de directorios creada"

# ============================================================================
# STEP 3: Crear y activar entorno virtual de Python
# ============================================================================

Write-Step "Configurando entorno virtual de Python..."

Set-Location backend

if (-not (Test-Path "venv")) {
    Write-Host "  Creando entorno virtual..." -ForegroundColor Gray
    python -m venv venv
    
    if ($LASTEXITCODE -ne 0) {
        Write-Error-Custom "Error al crear entorno virtual"
        exit 1
    }
}

Write-Host "  Activando entorno virtual..." -ForegroundColor Gray
.\venv\Scripts\Activate.ps1

if ($LASTEXITCODE -ne 0) {
    Write-Error-Custom "Error al activar entorno virtual"
    Write-Host "  Intenta ejecutar manualmente: .\venv\Scripts\Activate.ps1"
    exit 1
}

Write-Success "Entorno virtual activado"

# ============================================================================
# STEP 4: Instalar dependencias de Python
# ============================================================================

Write-Step "Instalando dependencias de Python..."

Write-Host "  Esto puede tardar varios minutos..." -ForegroundColor Yellow

pip install --upgrade pip | Out-Null
pip install -r requirements.txt

if ($LASTEXITCODE -ne 0) {
    Write-Error-Custom "Error al instalar dependencias de Python"
    exit 1
}

Write-Success "Dependencias de Python instaladas"

# ============================================================================
# STEP 5: Crear archivo .env
# ============================================================================

Write-Step "Configurando variables de entorno..."

if (-not (Test-Path ".env")) {
    Write-Host "  Creando archivo .env..." -ForegroundColor Gray
    
    $envContent = @"
# Application
APP_NAME=Portfolio Tracker API
APP_VERSION=1.0.0
DEBUG=True
ENVIRONMENT=development

# API Configuration
API_V1_PREFIX=/api/v1
HOST=0.0.0.0
PORT=8000

# Database
DATABASE_URL=sqlite+aiosqlite:///./portfolio_tracker.db
DATABASE_ECHO=False

# CORS
CORS_ORIGINS=["http://localhost:5173","http://localhost:3000"]

# Price Fetcher
PRICE_FETCH_INTERVAL_HOURS=1
PRICE_FETCH_ENABLED=True
PRICE_FETCH_ON_STARTUP=True

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json

# Security
SECRET_KEY=$(New-Guid)
ACCESS_TOKEN_EXPIRE_MINUTES=10080

# External APIs (Optional)
# COINGECKO_API_KEY=
# ALPHA_VANTAGE_API_KEY=
"@
    
    $envContent | Out-File -FilePath ".env" -Encoding UTF8
    Write-Success "Archivo .env creado"
} else {
    Write-Success "Archivo .env ya existe"
}

# ============================================================================
# STEP 6: Inicializar base de datos
# ============================================================================

Write-Step "Inicializando base de datos..."

Write-Host "  Creando tablas..." -ForegroundColor Gray

# Crear un script Python temporal para inicializar la DB
$initScript = @"
import asyncio
from app.core.database import init_db

async def main():
    await init_db()
    print("Base de datos inicializada correctamente")

if __name__ == "__main__":
    asyncio.run(main())
"@

$initScript | Out-File -FilePath "init_db.py" -Encoding UTF8
python init_db.py

if ($LASTEXITCODE -eq 0) {
    Write-Success "Base de datos inicializada"
    Remove-Item "init_db.py"
} else {
    Write-Error-Custom "Error al inicializar base de datos"
}

# ============================================================================
# STEP 7: Instalar dependencias del frontend
# ============================================================================

Write-Step "Instalando dependencias del frontend..."

Set-Location ../frontend

if (Test-Path "package.json") {
    Write-Host "  Ejecutando npm install..." -ForegroundColor Gray
    npm install
    
    if ($LASTEXITCODE -ne 0) {
        Write-Error-Custom "Error al instalar dependencias de frontend"
        exit 1
    }
    
    Write-Success "Dependencias de frontend instaladas"
} else {
    Write-Host "  package.json no encontrado - skipping frontend setup" -ForegroundColor Yellow
}

Set-Location ..

# ============================================================================
# STEP 8: Crear scripts de inicio
# ============================================================================

Write-Step "Creando scripts de inicio..."

# Script para iniciar backend
$startBackendScript = @"
# Inicia el backend FastAPI

Write-Host "Iniciando Portfolio Tracker Backend..." -ForegroundColor Cyan

Set-Location backend
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
"@

$startBackendScript | Out-File -FilePath "scripts\start_backend.ps1" -Encoding UTF8

# Script para iniciar frontend
$startFrontendScript = @"
# Inicia el frontend React

Write-Host "Iniciando Portfolio Tracker Frontend..." -ForegroundColor Cyan

Set-Location frontend
npm run dev
"@

$startFrontendScript | Out-File -FilePath "scripts\start_frontend.ps1" -Encoding UTF8

# Script para iniciar ambos
$startAllScript = @"
# Inicia backend y frontend en paralelo

Write-Host "Iniciando Portfolio Tracker (Backend + Frontend)..." -ForegroundColor Cyan
Write-Host ""
Write-Host "Backend API: http://localhost:8000" -ForegroundColor Green
Write-Host "Frontend UI: http://localhost:5173" -ForegroundColor Green
Write-Host "API Docs: http://localhost:8000/docs" -ForegroundColor Green
Write-Host ""
Write-Host "Presiona Ctrl+C para detener ambos servicios" -ForegroundColor Yellow
Write-Host ""

# Iniciar backend en ventana separada
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; .\scripts\start_backend.ps1"

# Esperar 5 segundos para que backend inicie
Start-Sleep -Seconds 5

# Iniciar frontend en ventana separada
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; .\scripts\start_frontend.ps1"

Write-Host "Servicios iniciados en ventanas separadas" -ForegroundColor Green
"@

$startAllScript | Out-File -FilePath "scripts\start_dev.ps1" -Encoding UTF8

Write-Success "Scripts de inicio creados"

# ============================================================================
# FINALIZACIÓN
# ============================================================================

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  ¡Setup Completado!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Próximos pasos:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Iniciar el sistema:" -ForegroundColor White
Write-Host "   .\scripts\start_dev.ps1" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Acceder al dashboard:" -ForegroundColor White
Write-Host "   Frontend: http://localhost:5173" -ForegroundColor Gray
Write-Host "   API Docs: http://localhost:8000/docs" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Crear tu primer portfolio:" -ForegroundColor White
Write-Host "   - Abre el dashboard" -ForegroundColor Gray
Write-Host "   - Click en 'Nuevo Portfolio'" -ForegroundColor Gray
Write-Host "   - Agrega tus holdings" -ForegroundColor Gray
Write-Host ""
Write-Host "Documentación completa en: ./docs/" -ForegroundColor Cyan
Write-Host ""
