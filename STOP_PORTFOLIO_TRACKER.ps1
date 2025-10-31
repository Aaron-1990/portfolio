# Portfolio Tracker - Script de Detencion
$ErrorActionPreference = "Continue"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Portfolio Tracker - Deteniendo" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$processesKilled = 0
$pidsFile = Join-Path $PWD "running_processes.txt"

if (Test-Path $pidsFile) {
    $content = Get-Content $pidsFile
    foreach ($line in $content) {
        if ($line -match "BACKEND_PID=(\d+)") {
            try {
                Stop-Process -Id $matches[1] -Force
                Write-Host "[OK] Backend detenido" -ForegroundColor Green
                $processesKilled++
            } catch {}
        }
        if ($line -match "FRONTEND_PID=(\d+)") {
            try {
                Stop-Process -Id $matches[1] -Force
                Write-Host "[OK] Frontend detenido" -ForegroundColor Green
                $processesKilled++
            } catch {}
        }
    }
    Remove-Item $pidsFile -ErrorAction SilentlyContinue
}

Get-Process -Name python -ErrorAction SilentlyContinue | Where-Object {
    $_.CommandLine -like "*uvicorn*"
} | ForEach-Object {
    Stop-Process -Id $_.Id -Force
    Write-Host "[OK] Python detenido" -ForegroundColor Green
    $processesKilled++
}

Get-Process -Name node -ErrorAction SilentlyContinue | Where-Object {
    $_.CommandLine -like "*vite*"
} | ForEach-Object {
    Stop-Process -Id $_.Id -Force
    Write-Host "[OK] Node detenido" -ForegroundColor Green
    $processesKilled++
}

Write-Host ""
if ($processesKilled -eq 0) {
    Write-Host "No se encontraron procesos corriendo" -ForegroundColor Yellow
} else {
    Write-Host "Sistema detenido ($processesKilled procesos)" -ForegroundColor Green
}
Write-Host ""

Read-Host "Presiona Enter para salir"
