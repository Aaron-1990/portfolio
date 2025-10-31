# Portfolio Tracker - Script de Instalacion Automatizada
# Arquitectura: Sistema de instalacion automatizado con validacion de dependencias

<#
.SYNOPSIS
    Script de instalacion automatizada para Portfolio Tracker
    
.DESCRIPTION
    Este script automatiza la configuracion completa del sistema:
    - Valida prerrequisitos (Python 3.11+, Node.js 18+)
    - Configura backend (Python + FastAPI)
    - Configura frontend (React + Vite)
    - Inicializa base de datos
    - Crea archivos de configuracion
    
.NOTES
    Author: Architecture-First Approach
    Version: 1.0
    Requiere: PowerShell 5.1+, Python 3.11+, Node.js 18+
#>

# Configuracion de ErrorActionPreference
$ErrorActionPreference = "Stop"

# Colores y formato
$Host.UI.RawUI.WindowTitle = "Portfolio Tracker - Instalacion"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Portfolio Tracker - Setup Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# [1/6] Verificar prerrequisitos
Write-Host "[1/6] Verificando prerrequisitos..." -ForegroundColor Yellow
Write-Host ""

# Verificar Python
Write-Host "Verificando Python 3.11+..." -ForegroundColor Gray
try {
    $pythonVersion = python --version 2>&1
    # CORRECCION: Usar comillas simples para expresiones regulares
    if ($pythonVersion -match 'v?(3\.(1[1-9]|[2-9]\d))') {
        Write-Host "[OK] Python encontrado: $pythonVersion" -ForegroundColor Green
    } else {
        Write-Host "[ERROR] Se requiere Python 3.11 o superior" -ForegroundColor Red
        Write-Host "  Descargar desde: https://www.python.org/downloads/" -ForegroundColor Yellow
        exit 1
    }
} catch {
    Write-Host "[ERROR] Python no encontrado" -ForegroundColor Red
    Write-Host "  Instalar desde: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

# Verificar Node.js
Write-Host "Verificando Node.js 18+..." -ForegroundColor Gray
try {
    $nodeVersion = node --version 2>&1
    # CORRECCION: Usar comillas simples para expresiones regulares
    if ($nodeVersion -match 'v(1[8-9]|[2-9]\d)') {
        Write-Host "[OK] Node.js encontrado: $nodeVersion" -ForegroundColor Green
    } else {
        Write-Host "[ERROR] Se requiere Node.js 18 o superior" -ForegroundColor Red
        Write-Host "  Descargar desde: https://nodejs.org/" -ForegroundColor Yellow
        exit 1
    }
} catch {
    Write-Host "[ERROR] Node.js no encontrado" -ForegroundColor Red
    Write-Host "  Instalar desde: https://nodejs.org/" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "[2/6] Configurando Backend..." -ForegroundColor Yellow
Write-Host ""

# Navegar al directorio backend
if (-not (Test-Path "backend")) {
    Write-Host "[ERROR] Directorio 'backend' no encontrado" -ForegroundColor Red
    Write-Host "  Asegurate de ejecutar este script desde la raiz del proyecto" -ForegroundColor Yellow
    exit 1
}

Set-Location backend

# Crear entorno virtual Python
Write-Host "Creando entorno virtual Python..." -ForegroundColor Gray
if (Test-Path "venv") {
    Write-Host "  Entorno virtual ya existe, omitiendo..." -ForegroundColor Yellow
} else {
    python -m venv venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] No se pudo crear el entorno virtual" -ForegroundColor Red
        exit 1
    }
    Write-Host "[OK] Entorno virtual creado" -ForegroundColor Green
}

# Activar entorno virtual
Write-Host "Activando entorno virtual..." -ForegroundColor Gray
& .\venv\Scripts\Activate.ps1

# Actualizar pip
Write-Host "Actualizando pip..." -ForegroundColor Gray
python -m pip install --upgrade pip --quiet
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] No se pudo actualizar pip" -ForegroundColor Red
    exit 1
}
Write-Host "[OK] pip actualizado" -ForegroundColor Green

# Instalar dependencias
Write-Host "Instalando dependencias Python..." -ForegroundColor Gray
Write-Host "  Esto puede tomar varios minutos..." -ForegroundColor Yellow
pip install -r requirements.txt --quiet

if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Error instalando dependencias Python" -ForegroundColor Red
    exit 1
}
Write-Host "[OK] Dependencias Python instaladas" -ForegroundColor Green

# Crear archivo .env si no existe
Write-Host "Configurando variables de entorno..." -ForegroundColor Gray
if (-not (Test-Path ".env")) {
    if (Test-Path ".env.example") {
        Copy-Item ".env.example" ".env"
        Write-Host "[OK] Archivo .env creado desde .env.example" -ForegroundColor Green
        Write-Host "  IMPORTANTE: Edita .env con tus configuraciones si es necesario" -ForegroundColor Yellow
    } else {
        Write-Host "[AVISO] No se encontro .env.example, creando .env basico..." -ForegroundColor Yellow
        @"
# Portfolio Tracker Configuration
DB_PATH=./data/portfolio.db
LOG_LEVEL=INFO
PRICE_UPDATE_INTERVAL=3600
"@ | Out-File -FilePath ".env" -Encoding UTF8
        Write-Host "[OK] Archivo .env creado con configuracion basica" -ForegroundColor Green
    }
} else {
    Write-Host "[OK] Archivo .env ya existe" -ForegroundColor Green
}

# Crear directorio de datos si no existe
Write-Host "Creando directorios necesarios..." -ForegroundColor Gray
if (-not (Test-Path "data")) {
    New-Item -ItemType Directory -Path "data" | Out-Null
    Write-Host "[OK] Directorio 'data' creado" -ForegroundColor Green
} else {
    Write-Host "[OK] Directorio 'data' ya existe" -ForegroundColor Green
}

# Crear directorio de logs si no existe
if (-not (Test-Path "logs")) {
    New-Item -ItemType Directory -Path "logs" | Out-Null
    Write-Host "[OK] Directorio 'logs' creado" -ForegroundColor Green
} else {
    Write-Host "[OK] Directorio 'logs' ya existe" -ForegroundColor Green
}

# Volver al directorio raiz
Set-Location ..

Write-Host ""
Write-Host "[3/6] Configurando Frontend..." -ForegroundColor Yellow
Write-Host ""

# Navegar al directorio frontend
if (-not (Test-Path "frontend")) {
    Write-Host "[ERROR] Directorio 'frontend' no encontrado" -ForegroundColor Red
    exit 1
}

Set-Location frontend

# Instalar dependencias de Node
Write-Host "Instalando dependencias Node.js..." -ForegroundColor Gray
Write-Host "  Esto puede tomar varios minutos..." -ForegroundColor Yellow
npm install --silent

if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Error instalando dependencias Node.js" -ForegroundColor Red
    exit 1
}
Write-Host "[OK] Dependencias Node.js instaladas" -ForegroundColor Green

# Crear archivo .env.local si no existe
Write-Host "Configurando variables de entorno del frontend..." -ForegroundColor Gray
if (-not (Test-Path ".env.local")) {
    if (Test-Path ".env.example") {
        Copy-Item ".env.example" ".env.local"
        Write-Host "[OK] Archivo .env.local creado desde .env.example" -ForegroundColor Green
    } else {
        Write-Host "[AVISO] No se encontro .env.example, creando .env.local basico..." -ForegroundColor Yellow
        @"
VITE_API_URL=http://localhost:8000
"@ | Out-File -FilePath ".env.local" -Encoding UTF8
        Write-Host "[OK] Archivo .env.local creado con configuracion basica" -ForegroundColor Green
    }
} else {
    Write-Host "[OK] Archivo .env.local ya existe" -ForegroundColor Green
}

# Volver al directorio raiz
Set-Location ..

Write-Host ""
Write-Host "[4/6] Inicializando base de datos..." -ForegroundColor Yellow
Write-Host ""

# Activar entorno virtual y ejecutar script de inicializacion
Set-Location backend
& .\venv\Scripts\Activate.ps1

Write-Host "Ejecutando script de inicializacion de base de datos..." -ForegroundColor Gray
python -m app.database.init_db

if ($LASTEXITCODE -ne 0) {
    Write-Host "[AVISO] Error inicializando base de datos" -ForegroundColor Yellow
    Write-Host "  La base de datos se creara automaticamente al iniciar el servidor" -ForegroundColor Yellow
} else {
    Write-Host "[OK] Base de datos inicializada correctamente" -ForegroundColor Green
}

# Volver al directorio raiz
Set-Location ..

Write-Host ""
Write-Host "[5/6] Creando scripts de inicio rapido..." -ForegroundColor Yellow
Write-Host ""

# Crear script de inicio (START)
$startScript = @'
# Portfolio Tracker - Script de Inicio
# Inicia Backend y Frontend automaticamente

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Portfolio Tracker - Iniciando" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar que estamos en el directorio correcto
if (-not (Test-Path "backend") -or -not (Test-Path "frontend")) {
    Write-Host "[ERROR] Ejecuta este script desde el directorio raiz del proyecto" -ForegroundColor Red
    Read-Host "Presiona Enter para salir"
    exit 1
}

# Iniciar Backend
Write-Host "[1/2] Iniciando Backend..." -ForegroundColor Yellow
Set-Location backend

$backendProcess = Start-Process powershell -ArgumentList "-NoExit", "-Command", "& .\venv\Scripts\Activate.ps1; Write-Host 'Backend iniciado en http://localhost:8000' -ForegroundColor Green; python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000" -PassThru -WindowStyle Normal

Start-Sleep -Seconds 3
Write-Host "[OK] Backend iniciado (PID: $($backendProcess.Id))" -ForegroundColor Green

Set-Location ..

# Iniciar Frontend
Write-Host "[2/2] Iniciando Frontend..." -ForegroundColor Yellow
Set-Location frontend

$frontendProcess = Start-Process powershell -ArgumentList "-NoExit", "-Command", "Write-Host 'Frontend iniciado en http://localhost:5173' -ForegroundColor Green; npm run dev" -PassThru -WindowStyle Normal

Start-Sleep -Seconds 3
Write-Host "[OK] Frontend iniciado (PID: $($frontendProcess.Id))" -ForegroundColor Green

Set-Location ..

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  SISTEMA INICIADO CORRECTAMENTE" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "  * Dashboard: http://localhost:5173" -ForegroundColor Cyan
Write-Host "  * API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "Para detener el sistema:" -ForegroundColor Yellow
Write-Host "  Ejecuta: .\STOP_PORTFOLIO_TRACKER.ps1" -ForegroundColor Yellow
Write-Host "  O cierra las ventanas de PowerShell" -ForegroundColor Yellow
Write-Host ""
Write-Host "Presiona Enter para abrir el navegador..." -ForegroundColor Gray
Read-Host

Start-Process "http://localhost:5173"

Write-Host ""
Write-Host "Sistema en ejecucion. No cierres esta ventana." -ForegroundColor Green
Write-Host "Presiona Ctrl+C para detener" -ForegroundColor Yellow
Write-Host ""

# Mantener script corriendo
try {
    while ($true) {
        Start-Sleep -Seconds 10
        
        # Verificar que los procesos sigan corriendo
        if (-not (Get-Process -Id $backendProcess.Id -ErrorAction SilentlyContinue)) {
            Write-Host "[ERROR] El proceso del backend se detuvo" -ForegroundColor Red
            break
        }
        if (-not (Get-Process -Id $frontendProcess.Id -ErrorAction SilentlyContinue)) {
            Write-Host "[ERROR] El proceso del frontend se detuvo" -ForegroundColor Red
            break
        }
    }
} finally {
    Write-Host "Deteniendo procesos..." -ForegroundColor Yellow
    Stop-Process -Id $backendProcess.Id -ErrorAction SilentlyContinue
    Stop-Process -Id $frontendProcess.Id -ErrorAction SilentlyContinue
}
'@

Write-Host "Creando START_PORTFOLIO_TRACKER.ps1..." -ForegroundColor Gray
$startScript | Out-File -FilePath "START_PORTFOLIO_TRACKER.ps1" -Encoding UTF8
Write-Host "[OK] START_PORTFOLIO_TRACKER.ps1 creado" -ForegroundColor Green

# Crear script de detencion (STOP)
$stopScript = @'
# Portfolio Tracker - Script de Detencion
# Detiene todos los procesos del sistema

$ErrorActionPreference = "Continue"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Portfolio Tracker - Deteniendo" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Buscando procesos en ejecucion..." -ForegroundColor Yellow

# Detener procesos de Python (Backend)
$pythonProcesses = Get-Process -Name python -ErrorAction SilentlyContinue | Where-Object {
    $_.CommandLine -like "*uvicorn*" -or $_.CommandLine -like "*fastapi*"
}

if ($pythonProcesses) {
    Write-Host "Deteniendo Backend (Python)..." -ForegroundColor Gray
    $pythonProcesses | Stop-Process -Force
    Write-Host "[OK] Backend detenido" -ForegroundColor Green
} else {
    Write-Host "[INFO] No se encontraron procesos de Backend" -ForegroundColor Yellow
}

# Detener procesos de Node (Frontend)
$nodeProcesses = Get-Process -Name node -ErrorAction SilentlyContinue | Where-Object {
    $_.CommandLine -like "*vite*"
}

if ($nodeProcesses) {
    Write-Host "Deteniendo Frontend (Node)..." -ForegroundColor Gray
    $nodeProcesses | Stop-Process -Force
    Write-Host "[OK] Frontend detenido" -ForegroundColor Green
} else {
    Write-Host "[INFO] No se encontraron procesos de Frontend" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  SISTEMA DETENIDO" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

Read-Host "Presiona Enter para salir"
'@

Write-Host "Creando STOP_PORTFOLIO_TRACKER.ps1..." -ForegroundColor Gray
$stopScript | Out-File -FilePath "STOP_PORTFOLIO_TRACKER.ps1" -Encoding UTF8
Write-Host "[OK] STOP_PORTFOLIO_TRACKER.ps1 creado" -ForegroundColor Green

Write-Host ""
Write-Host "[6/6] Verificando instalacion..." -ForegroundColor Yellow
Write-Host ""

# Verificar estructura de directorios
$requiredDirs = @(
    "backend",
    "backend/venv",
    "backend/data",
    "backend/logs",
    "frontend",
    "frontend/node_modules"
)

$allDirsExist = $true
foreach ($dir in $requiredDirs) {
    if (Test-Path $dir) {
        Write-Host "[OK] $dir" -ForegroundColor Green
    } else {
        Write-Host "[ERROR] $dir - No encontrado" -ForegroundColor Red
        $allDirsExist = $false
    }
}

# Verificar archivos criticos
$requiredFiles = @(
    "backend/.env",
    "frontend/.env.local",
    "START_PORTFOLIO_TRACKER.ps1",
    "STOP_PORTFOLIO_TRACKER.ps1"
)

$allFilesExist = $true
foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "[OK] $file" -ForegroundColor Green
    } else {
        Write-Host "[ERROR] $file - No encontrado" -ForegroundColor Red
        $allFilesExist = $false
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  INSTALACION COMPLETADA" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

if ($allDirsExist -and $allFilesExist) {
    Write-Host "[OK] Todos los componentes instalados correctamente" -ForegroundColor Green
} else {
    Write-Host "[AVISO] Algunos componentes no se instalaron correctamente" -ForegroundColor Yellow
    Write-Host "  Revisa los errores arriba" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "PROXIMOS PASOS:" -ForegroundColor Cyan
Write-Host "  1. Ejecuta: .\START_PORTFOLIO_TRACKER.ps1" -ForegroundColor White
Write-Host "  2. Espera ~10 segundos" -ForegroundColor White
Write-Host "  3. Abre: http://localhost:5173" -ForegroundColor White
Write-Host ""
Write-Host "Para detener el sistema:" -ForegroundColor Cyan
Write-Host "  Ejecuta: .\STOP_PORTFOLIO_TRACKER.ps1" -ForegroundColor White
Write-Host ""
Write-Host "Documentacion completa en:" -ForegroundColor Cyan
Write-Host "  - QUICK_START.md (inicio rapido)" -ForegroundColor White
Write-Host "  - GUIA_ACCESO_DIARIO.md (uso diario)" -ForegroundColor White
Write-Host "  - INSTALLATION_GUIDE.md (guia completa)" -ForegroundColor White
Write-Host ""

Read-Host "Presiona Enter para salir"