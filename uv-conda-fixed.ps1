$UV_ENVS_DIR = "$env:USERPROFILE\.uv\envs"

function uv-create {
    param($name, $python = "3.11")
    uv venv "$UV_ENVS_DIR\$name" --python $python
    Write-Host "Environment '$name' created. Activate with: uv-activate $name" -ForegroundColor Green
}

function uv-activate {
    param($name)
    if (-not (Test-Path "$UV_ENVS_DIR\$name")) {
        Write-Host "Environment '$name' does not exist. Create it with: uv-create $name" -ForegroundColor Red
        return
    }
    & "$UV_ENVS_DIR\$name\Scripts\Activate.ps1"
}

function uv-list {
    if (Test-Path $UV_ENVS_DIR) {
        $envs = Get-ChildItem $UV_ENVS_DIR | Select-Object Name
        if ($envs) {
            Write-Host "Available UV environments:" -ForegroundColor Cyan
            $envs | ForEach-Object { Write-Host "  - $($_.Name)" }
        } else {
            Write-Host "No environments found. Create one with: uv-create <name>" -ForegroundColor Yellow
        }
    } else {
        Write-Host "No environments directory found. Create one with: uv-create <name>" -ForegroundColor Yellow
    }
}

function uv-remove {
    param($name)
    
    # Check if environment exists
    if (-not (Test-Path "$UV_ENVS_DIR\$name")) {
        Write-Host "Environment '$name' does not exist." -ForegroundColor Red
        return
    }
    
    # Check if this environment is currently active
    if ($env:VIRTUAL_ENV -and $env:VIRTUAL_ENV.Contains($name)) {
        Write-Host "Deactivating environment '$name'..." -ForegroundColor Yellow
        deactivate
    }
    
    # Remove the environment
    try {
        Remove-Item -Recurse -Force "$UV_ENVS_DIR\$name"
        Write-Host "Environment '$name' removed successfully." -ForegroundColor Green
    }
    catch {
        Write-Host "Failed to remove environment '$name': $($_.Exception.Message)" -ForegroundColor Red
    }
}

function uv-info {
    Write-Host "UV Conda-style Environment Manager" -ForegroundColor Cyan
    Write-Host "Available commands:" -ForegroundColor White
    Write-Host "  uv-create <name> [python-version]  - Create new environment" -ForegroundColor Gray
    Write-Host "  uv-activate <name>                 - Activate environment" -ForegroundColor Gray
    Write-Host "  uv-list                            - List all environments" -ForegroundColor Gray
    Write-Host "  uv-remove <name>                   - Remove environment" -ForegroundColor Gray
    Write-Host "  uv-info                            - Show this help" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Environments are stored in: $UV_ENVS_DIR" -ForegroundColor Gray
}

Write-Host "UV Conda-style functions loaded: uv-create, uv-activate, uv-list, uv-remove, uv-info" -ForegroundColor Green