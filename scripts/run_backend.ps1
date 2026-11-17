# ControlPlane - Backend Startup Script
$ErrorActionPreference = "Stop"

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Starting ControlPlane Backend (FastAPI)..." -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

$WorkspaceRoot = Split-Path -Parent $PSScriptRoot
Set-Location $WorkspaceRoot

$VenvPython = Join-Path $WorkspaceRoot ".venv\Scripts\python.exe"

if (-not (Test-Path $VenvPython)) {
    Write-Host "Virtual environment not found at $VenvPython. Please run scripts/setup_dev.ps1 first." -ForegroundColor Red
    exit 1
}

Write-Host "Running Alembic Migrations to ensure schema is up-to-date..." -ForegroundColor Yellow
& $VenvPython -m alembic -c backend\alembic.ini upgrade head

Write-Host "Launching Uvicorn server on http://127.0.0.1:8000..." -ForegroundColor Green
& $VenvPython -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload

