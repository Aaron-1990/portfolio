# Portfolio Tracker - Script de Inicio
$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Portfolio Tracker - Iniciando" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

if (-not (Test-Path "backend") -or -not (Test-Path "frontend")) {
    Write-Host "[ERROR] Ejecuta desde el directorio raiz" -ForegroundColor Red
    Read-Host "Presiona Enter para salir"
    exit 1
}

Write-Host "[1/3] Iniciando Backend..." -ForegroundColor Yellow

$backendCmd = @"
Set-Location '$PWD\backend'
& .\venv\Scripts\Activate.ps1
`$Host.UI.RawUI.WindowTitle = 'Backend - Portfolio Tracker'
Write-Host ''
Write-Host 'Backend iniciado en http://localhost:8000' -ForegroundColor Green
Write-Host 'NO CIERRES ESTA VENTANA' -ForegroundColor Yellow
Write-Host ''
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
"@

$backendProcess = Start-Process powershell -ArgumentList "-NoExit", "-Command", $backendCmd -PassThru -WindowStyle Normal
Write-Host "  [OK] Backend PID: $($backendProcess.Id)" -ForegroundColor Green

Start-Sleep -Seconds 5

Write-Host ""
Write-Host "[2/3] Iniciando Frontend..." -ForegroundColor Yellow

$frontendCmd = @"
Set-Location '$PWD\frontend'
`$Host.UI.RawUI.WindowTitle = 'Frontend - Portfolio Tracker'
Write-Host ''
Write-Host 'Frontend iniciado en http://localhost:5173' -ForegroundColor Green
Write-Host 'NO CIERRES ESTA VENTANA' -ForegroundColor Yellow
Write-Host ''
Start-Sleep -Seconds 3
Start-Process 'http://localhost:5173'
npm run dev
"@

$frontendProcess = Start-Process powershell -ArgumentList "-NoExit", "-Command", $frontendCmd -PassThru -WindowStyle Normal
Write-Host "  [OK] Frontend PID: $($frontendProcess.Id)" -ForegroundColor Green

Write-Host ""
Write-Host "[3/3] Abriendo navegador..." -ForegroundColor Yellow
Start-Sleep -Seconds 8
Start-Process "http://localhost:5173"

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  SISTEMA INICIADO" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Dashboard: http://localhost:5173" -ForegroundColor Cyan
Write-Host "API Docs:  http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""

$pidsFile = Join-Path $PWD "running_processes.txt"
@"
BACKEND_PID=$($backendProcess.Id)
FRONTEND_PID=$($frontendProcess.Id)
"@ | Out-File -FilePath $pidsFile -Encoding UTF8

Read-Host "Presiona Enter para cerrar (los servicios seguiran corriendo)"
