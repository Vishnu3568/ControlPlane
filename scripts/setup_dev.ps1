# ControlPlane - Environment Bootstrap Script
$ErrorActionPreference = "Stop"

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Bootstrapping ControlPlane Workstation..." -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

$WorkspaceRoot = Split-Path -Parent $PSScriptRoot
Set-Location $WorkspaceRoot

# 1. Python Virtual Environment
if (-not (Test-Path ".venv")) {
    Write-Host "[1/4] Creating Python virtual environment (.venv)..." -ForegroundColor Yellow
    python -m venv .venv
} else {
    Write-Host "[1/4] Python virtual environment already exists." -ForegroundColor Green
}

# 2. Python Dependencies
Write-Host "[2/4] Installing backend dependencies..." -ForegroundColor Yellow
& .\.venv\Scripts\pip install -r backend\requirements.txt

# 3. Database Migrations
Write-Host "[3/4] Applying database migrations (Alembic)..." -ForegroundColor Yellow
& .\.venv\Scripts\python -m alembic -c backend\alembic.ini upgrade head

# 4. Frontend Dependencies
Write-Host "[4/4] Installing frontend dependencies..." -ForegroundColor Yellow
Set-Location (Join-Path $WorkspaceRoot "frontend")
npm install
Set-Location $WorkspaceRoot

Write-Host ""
Write-Host "FOUNDER OS environment is ready!" -ForegroundColor Green
Write-Host "Start backend:  powershell scripts/run_backend.ps1" -ForegroundColor Cyan
Write-Host "Start frontend: powershell scripts/run_frontend.ps1" -ForegroundColor Cyan

