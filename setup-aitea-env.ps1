# AITEA Environment Setup Script for Windows PowerShell
# This script sets up the complete AITEA development environment using Conda + UV

Write-Host "🚀 Setting up AITEA development environment..." -ForegroundColor Green
Write-Host "Using Conda for environment management + UV for fast package installation" -ForegroundColor Cyan

# Check if conda is installed
try {
    $condaVersion = conda --version 2>$null
    Write-Host "✅ Found: $condaVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Conda not found. Please install Miniconda or Anaconda first." -ForegroundColor Red
    Write-Host "Download from: https://docs.conda.io/en/latest/miniconda.html" -ForegroundColor Yellow
    exit 1
}

# Create conda environment
Write-Host "`n📦 Creating conda environment 'aitea' with Python 3.11..." -ForegroundColor Cyan
conda create -n aitea python=3.11 -y

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to create conda environment" -ForegroundColor Red
    exit 1
}

# Activate environment
Write-Host "🔄 Activating environment..." -ForegroundColor Cyan
conda activate aitea

# Install UV
Write-Host "⚡ Installing UV (ultra-fast package installer)..." -ForegroundColor Cyan
pip install uv

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to install UV" -ForegroundColor Red
    exit 1
}

# Verify UV installation
$uvVersion = uv --version
Write-Host "✅ Installed: $uvVersion" -ForegroundColor Green

# Install project dependencies
if (Test-Path "requirements.txt") {
    Write-Host "📋 Installing dependencies from requirements.txt..." -ForegroundColor Cyan
    uv pip install -r requirements.txt
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to install dependencies" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "⚠️  requirements.txt not found, skipping dependency installation" -ForegroundColor Yellow
}

# Install project in editable mode
if (Test-Path "pyproject.toml") {
    Write-Host "🔧 Installing project in editable mode..." -ForegroundColor Cyan
    uv pip install -e .
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to install project" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "⚠️  pyproject.toml not found, skipping project installation" -ForegroundColor Yellow
}

# Success message
Write-Host "`n🎉 AITEA environment setup complete!" -ForegroundColor Green
Write-Host "`nTo start developing:" -ForegroundColor Cyan
Write-Host "  1. conda activate aitea" -ForegroundColor White
Write-Host "  2. python your_script.py" -ForegroundColor White
Write-Host "`nTo install new packages:" -ForegroundColor Cyan
Write-Host "  uv pip install package-name" -ForegroundColor White
Write-Host "`nTo verify setup:" -ForegroundColor Cyan
Write-Host "  python verify_setup.py" -ForegroundColor White

Write-Host "`n📚 See ENVIRONMENT_SETUP.md for detailed documentation" -ForegroundColor Yellow