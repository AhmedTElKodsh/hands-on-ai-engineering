#!/bin/bash
# AITEA Environment Setup Script for macOS/Linux
# This script sets up the complete AITEA development environment using Conda + UV

echo "🚀 Setting up AITEA development environment..."
echo "Using Conda for environment management + UV for fast package installation"

# Check if conda is installed
if ! command -v conda &> /dev/null; then
    echo "❌ Conda not found. Please install Miniconda or Anaconda first."
    echo "macOS: brew install miniconda"
    echo "Linux: wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh"
    exit 1
fi

CONDA_VERSION=$(conda --version)
echo "✅ Found: $CONDA_VERSION"

# Create conda environment
echo ""
echo "📦 Creating conda environment 'aitea' with Python 3.11..."
conda create -n aitea python=3.11 -y

if [ $? -ne 0 ]; then
    echo "❌ Failed to create conda environment"
    exit 1
fi

# Activate environment
echo "🔄 Activating environment..."
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate aitea

# Install UV
echo "⚡ Installing UV (ultra-fast package installer)..."
pip install uv

if [ $? -ne 0 ]; then
    echo "❌ Failed to install UV"
    exit 1
fi

# Verify UV installation
UV_VERSION=$(uv --version)
echo "✅ Installed: $UV_VERSION"

# Install project dependencies
if [ -f "requirements.txt" ]; then
    echo "📋 Installing dependencies from requirements.txt..."
    uv pip install -r requirements.txt
    
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install dependencies"
        exit 1
    fi
else
    echo "⚠️  requirements.txt not found, skipping dependency installation"
fi

# Install project in editable mode
if [ -f "pyproject.toml" ]; then
    echo "🔧 Installing project in editable mode..."
    uv pip install -e .
    
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install project"
        exit 1
    fi
else
    echo "⚠️  pyproject.toml not found, skipping project installation"
fi

# Success message
echo ""
echo "🎉 AITEA environment setup complete!"
echo ""
echo "To start developing:"
echo "  1. conda activate aitea"
echo "  2. python your_script.py"
echo ""
echo "To install new packages:"
echo "  uv pip install package-name"
echo ""
echo "To verify setup:"
echo "  python verify_setup.py"
echo ""
echo "📚 See ENVIRONMENT_SETUP.md for detailed documentation"