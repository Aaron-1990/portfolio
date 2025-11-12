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
