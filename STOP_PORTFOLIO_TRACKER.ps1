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
