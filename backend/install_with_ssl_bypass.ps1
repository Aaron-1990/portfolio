# Portfolio Tracker - Instalacion con Bypass SSL
# Script robusto para entornos corporativos

$ErrorActionPreference = "Continue"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Instalacion con Bypass SSL" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar que estamos en backend
if (-not (Test-Path "venv")) {
    Write-Host "[ERROR] Ejecuta este script desde backend/ con venv creado" -ForegroundColor Red
    exit 1
}

# Activar entorno virtual
Write-Host "Activando entorno virtual..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

Write-Host ""
Write-Host "[1/4] Configurando pip..." -ForegroundColor Yellow

# Configurar pip globalmente para esta sesion
$env:PIP_TRUSTED_HOST = "pypi.org files.pythonhosted.org pypi.python.org"
$env:PIP_NO_CACHE_DIR = "1"

# Actualizar pip
python -m pip install --upgrade pip `
    --trusted-host pypi.org `
    --trusted-host files.pythonhosted.org `
    --trusted-host pypi.python.org `
    --no-cache-dir

Write-Host ""
Write-Host "[2/4] Detectando version de Python..." -ForegroundColor Yellow
$pythonVersion = python --version
Write-Host "  $pythonVersion" -ForegroundColor Gray

if ($pythonVersion -match "3\.13") {
    Write-Host ""
    Write-Host "  [AVISO] Python 3.13 detectado" -ForegroundColor Yellow
    Write-Host "  Algunos paquetes pueden no tener wheels pre-compilados" -ForegroundColor Yellow
    Write-Host "  RECOMENDACION: Considera usar Python 3.11 o 3.12" -ForegroundColor Yellow
    Write-Host ""
    $response = Read-Host "Continuar de todos modos? (s/n)"
    if ($response -ne "s") {
        Write-Host "Instalacion cancelada" -ForegroundColor Red
        exit 0
    }
}

Write-Host ""
Write-Host "[3/4] Instalando dependencias criticas..." -ForegroundColor Yellow

# Funcion helper para instalar paquetes
function Install-Package {
    param(
        [string]$PackageName,
        [bool]$Critical = $true
    )
    
    Write-Host "  Instalando $PackageName..." -ForegroundColor Gray
    
    $output = python -m pip install $PackageName `
        --trusted-host pypi.org `
        --trusted-host files.pythonhosted.org `
        --trusted-host pypi.python.org `
        --no-cache-dir `
        2>&1
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "    [OK] $PackageName" -ForegroundColor Green
        return $true
    } else {
        if ($Critical) {
            Write-Host "    [FALLO] $PackageName" -ForegroundColor Red
        } else {
            Write-Host "    [SKIP] $PackageName (opcional)" -ForegroundColor Yellow
        }
        return $false
    }
}

# Instalar Core Framework
Write-Host ""
Write-Host "Core Framework:" -ForegroundColor Cyan
Install-Package "fastapi==0.104.1" -Critical $true
Install-Package "uvicorn[standard]==0.24.0" -Critical $true
Install-Package "python-multipart==0.0.6" -Critical $true

# Instalar Database
Write-Host ""
Write-Host "Database & ORM:" -ForegroundColor Cyan
Install-Package "sqlalchemy==2.0.23" -Critical $true
Install-Package "alembic==1.12.1" -Critical $true
Install-Package "aiosqlite==0.19.0" -Critical $true

# Instalar Pydantic (puede fallar con Python 3.13)
Write-Host ""
Write-Host "Data Validation:" -ForegroundColor Cyan
$pydanticSuccess = Install-Package "pydantic==2.5.0" -Critical $true

if (-not $pydanticSuccess) {
    Write-Host ""
    Write-Host "  [AVISO] Pydantic 2.x fallo (requiere Rust)" -ForegroundColor Yellow
    Write-Host "  Intentando con Pydantic 1.x (compatible)..." -ForegroundColor Yellow
    $pydanticSuccess = Install-Package "pydantic==1.10.13" -Critical $true
    
    if ($pydanticSuccess) {
        Write-Host "    [OK] Pydantic 1.x instalado (compatible con FastAPI)" -ForegroundColor Green
        Install-Package "pydantic-settings==2.1.0" -Critical $false
    } else {
        Write-Host ""
        Write-Host "  [ERROR CRITICO] No se pudo instalar Pydantic" -ForegroundColor Red
        Write-Host "  SOLUCION: Instala Python 3.11 o 3.12" -ForegroundColor Yellow
        Read-Host "Presiona Enter para salir"
        exit 1
    }
} else {
    Install-Package "pydantic-settings==2.1.0" -Critical $true
}

# Instalar HTTP Clients
Write-Host ""
Write-Host "HTTP Clients:" -ForegroundColor Cyan
Install-Package "httpx==0.25.1" -Critical $true
Install-Package "requests==2.31.0" -Critical $true
Install-Package "yfinance==0.2.32" -Critical $true

# Instalar Utilities
Write-Host ""
Write-Host "Utilities:" -ForegroundColor Cyan
Install-Package "python-dotenv==1.0.0" -Critical $true
Install-Package "apscheduler==3.10.4" -Critical $true
Install-Package "python-json-logger==2.0.7" -Critical $true

Write-Host ""
Write-Host "[4/4] Verificando instalacion..." -ForegroundColor Yellow

# Test imports
$testScript = @"
import sys
try:
    import fastapi
    import uvicorn
    import sqlalchemy
    import pydantic
    print('[OK] Todas las dependencias criticas funcionan correctamente')
    sys.exit(0)
except ImportError as e:
    print(f'[ERROR] Falta dependencia: {e}')
    sys.exit(1)
"@

$testResult = python -c $testScript
Write-Host "  $testResult" -ForegroundColor Green

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "  INSTALACION EXITOSA" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Puedes continuar con el setup del frontend" -ForegroundColor Cyan
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "  INSTALACION FALLIDA" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "SOLUCION RECOMENDADA:" -ForegroundColor Yellow
    Write-Host "  1. Desinstala Python 3.13" -ForegroundColor White
    Write-Host "  2. Instala Python 3.11.9 desde:" -ForegroundColor White
    Write-Host "     https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe" -ForegroundColor Cyan
    Write-Host "  3. Elimina el venv y recrealo" -ForegroundColor White
    Write-Host "  4. Ejecuta este script de nuevo" -ForegroundColor White
    Write-Host ""
}

Read-Host "Presiona Enter para salir"
