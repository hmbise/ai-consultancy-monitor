# AI Consultancy Monitor - PowerShell Commands
# Usage: .\dev.ps1 <command>

param(
    [Parameter(Mandatory=$false)]
    [string]$Command = "help",

    [Parameter(Mandatory=$false)]
    [string]$Msg = ""
)

function Show-Help {
    Write-Host "AI Consultancy Monitor - Development Commands" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Commands:" -ForegroundColor Yellow
    Write-Host "  save              - Quick commit with timestamp"
    Write-Host "  commit -Msg '...' - Commit with custom message"
    Write-Host "  dev               - Start API server with reload"
    Write-Host "  worker            - Start Celery worker"
    Write-Host "  test              - Run tests"
    Write-Host "  init-db           - Initialize database schema"
    Write-Host "  docker-up         - Start Redis/Elasticsearch"
    Write-Host "  docker-down       - Stop Docker services"
    Write-Host ""
    Write-Host "Examples:" -ForegroundColor Yellow
    Write-Host '  .\dev.ps1 save'
    Write-Host '  .\dev.ps1 commit -Msg "feat: add new feature"'
    Write-Host '  .\dev.ps1 dev'
}

function Save-Checkpoint {
    git add -A
    $timestamp = Get-Date -Format "yyyy-MM-dd-HH:mm"
    git commit -m "checkpoint: $timestamp" 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Saved at $(Get-Date -Format 'HH:mm')" -ForegroundColor Green
    } else {
        Write-Host "Nothing to commit" -ForegroundColor Yellow
    }
}

function Commit-WithMessage {
    param([string]$Message)
    git add -A
    git commit -m "$Message" 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Committed: $Message" -ForegroundColor Green
    } else {
        Write-Host "Nothing to commit" -ForegroundColor Yellow
    }
}

function Start-DevServer {
    Write-Host "Starting API server..." -ForegroundColor Cyan
    uvicorn src.api.main:app --reload
}

function Start-Worker {
    Write-Host "Starting Celery worker..." -ForegroundColor Cyan
    celery -A src.worker worker -l info
}

function Run-Tests {
    Write-Host "Running tests..." -ForegroundColor Cyan
    pytest -v
}

function Initialize-Database {
    Write-Host "Initializing database..." -ForegroundColor Cyan
    python -c "import asyncio; from src.core.database import init_db; asyncio.run(init_db())"
    Write-Host "✓ Database initialized" -ForegroundColor Green
}

function Start-Docker {
    Write-Host "Starting Docker services..." -ForegroundColor Cyan
    docker-compose up -d redis elasticsearch
}

function Stop-Docker {
    Write-Host "Stopping Docker services..." -ForegroundColor Cyan
    docker-compose down
}

switch ($Command) {
    "save" { Save-Checkpoint }
    "commit" { Commit-WithMessage -Message $Msg }
    "dev" { Start-DevServer }
    "worker" { Start-Worker }
    "test" { Run-Tests }
    "init-db" { Initialize-Database }
    "docker-up" { Start-Docker }
    "docker-down" { Stop-Docker }
    default { Show-Help }
}
