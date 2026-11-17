# ControlPlane - Frontend Startup Script
$ErrorActionPreference = "Stop"

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Starting ControlPlane Frontend (React Vite)..." -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

$WorkspaceRoot = Split-Path -Parent $PSScriptRoot
$FrontendDir = Join-Path $WorkspaceRoot "frontend"

Set-Location $FrontendDir

Write-Host "Launching Vite dev server on http://localhost:5173..." -ForegroundColor Green
npm run dev

