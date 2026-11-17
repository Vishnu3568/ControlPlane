# ControlPlane - Database Backup Script
$ErrorActionPreference = "Stop"

$WorkspaceRoot = Split-Path -Parent $PSScriptRoot
Set-Location $WorkspaceRoot

$DbPath = Join-Path $WorkspaceRoot "data\database\founder.db"
$BackupDir = Join-Path $WorkspaceRoot "data\backups"

if (-not (Test-Path $DbPath)) {
    Write-Host "Database file not found at $DbPath." -ForegroundColor Red
    exit 1
}

if (-not (Test-Path $BackupDir)) {
    New-Item -ItemType Directory -Path $BackupDir -Force | Out-Null
}

$Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$BackupFile = Join-Path $BackupDir "controlplane_backup_$Timestamp.db"

Write-Host "Creating backup of founder.db..." -ForegroundColor Cyan
Copy-Item -Path $DbPath -Destination $BackupFile -Force

Write-Host "Backup created successfully at:" -ForegroundColor Green
Write-Host "  $BackupFile" -ForegroundColor Yellow

$FileSize = (Get-Item $BackupFile).Length / 1KB
Write-Host "Size: $([math]::Round($FileSize, 2)) KB" -ForegroundColor Cyan

