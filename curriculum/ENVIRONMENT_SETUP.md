# AITEA Environment Setup Guide

> **Quick Reference Guide** - For detailed learning materials, see [Chapter 1: Environment Setup](chapters/CH01_environment_setup.md)

## Overview

AITEA uses a modern Python development setup combining:

- **Conda**: Python version and environment management
- **UV**: Ultra-fast package installation (10-100x faster than pip)
- **pyproject.toml**: Modern Python project configuration

### Why This Combination?

- **Conda** manages Python versions and system-level dependencies
- **UV** handles Python package installation with blazing speed
- **Best of both worlds**: Robust environment isolation + fast package management

## Quick Setup

### Prerequisites

- **Conda**: Install [Miniconda](https://docs.conda.io/en/latest/miniconda.html) (recommended) or [Anaconda](https://www.anaconda.com/products/distribution)
- **Operating System**: Windows, macOS, or Linux

### Automated Setup (Recommended)

**Windows PowerShell:**

```powershell
.\setup-aitea-env.ps1
```

**macOS/Linux:**

```bash
chmod +x setup-aitea-env.sh
./setup-aitea-env.sh
```

### Manual Setup

### 1. Install Conda

**Miniconda (Recommended):**

```bash
# Windows: Download from https://docs.conda.io/en/latest/miniconda.html
# macOS: brew install miniconda
# Linux: wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
```

### 2. Create Environment

```bash
# Create conda environment with Python 3.11
conda create -n aitea python=3.11 -y

# Activate environment
conda activate aitea
```

### 3. Install UV

```bash
# Install UV inside conda environment (only once)
pip install uv

# Verify installation
uv --version
```

### 4. Install Project Dependencies

```bash
# Install from requirements.txt (10-100x faster than pip!)
uv pip install -r requirements.txt

# Install project in editable mode
uv pip install -e .

# Install dev dependencies
uv pip install -e ".[dev]"
```

### Package Structure

The AITEA project includes a modular `aitea/` package with its own `pyproject.toml`:

```bash
# Install the main project (recommended for curriculum)
uv pip install -e .

# Or install just the aitea package
cd aitea
uv pip install -e .
```

The `aitea/` package can be installed independently for distribution or deployment.

## Daily Workflow

```bash
# 1. Activate environment (once per terminal session)
conda activate aitea

# 2. Use UV for all package operations
uv pip install new-package
uv pip install -r requirements.txt

# 3. Run your code
python your_script.py

# 4. Deactivate when done (optional)
conda deactivate
```

## Why This Combination?

### Conda Advantages

- **Python Version Management**: Easy switching between Python versions
- **System Dependencies**: Handles complex libraries (CUDA, MKL, etc.)
- **Cross-Platform**: Consistent behavior across Windows/macOS/Linux
- **Scientific Computing**: Optimized packages for data science/ML

### UV Advantages

- **Speed**: 10-100x faster than pip
- **Better Dependency Resolution**: Handles conflicts more intelligently
- **Drop-in Replacement**: Same commands as pip (`uv pip install`)
- **Modern**: Built in Rust, actively maintained

### Combined Benefits

```bash
# Conda manages the environment
conda create -n project python=3.11

# UV handles package installation
uv pip install -r requirements.txt  # ⚡ Super fast!
```

## Command Comparison

| Task              | Old Way (pip)                     | New Way (UV)                         |
| ----------------- | --------------------------------- | ------------------------------------ |
| Install package   | `pip install requests`            | `uv pip install requests`            |
| Install from file | `pip install -r requirements.txt` | `uv pip install -r requirements.txt` |
| Install editable  | `pip install -e .`                | `uv pip install -e .`                |
| Upgrade package   | `pip install --upgrade requests`  | `uv pip install --upgrade requests`  |

## Environment Scripts

### Windows PowerShell (`setup-env.ps1`)

```powershell
# AITEA Environment Setup Script
Write-Host "🚀 Setting up AITEA development environment..." -ForegroundColor Green

# Create conda environment
conda create -n aitea python=3.11 -y
conda activate aitea

# Install UV
pip install uv

# Install project dependencies
uv pip install -r requirements.txt
uv pip install -e .

Write-Host "✅ Environment ready! Use 'conda activate aitea' to start." -ForegroundColor Green
```

### macOS/Linux (`setup-env.sh`)

```bash
#!/bin/bash
echo "🚀 Setting up AITEA development environment..."

# Create conda environment
conda create -n aitea python=3.11 -y
conda activate aitea

# Install UV
pip install uv

# Install project dependencies
uv pip install -r requirements.txt
uv pip install -e .

echo "✅ Environment ready! Use 'conda activate aitea' to start."
```

## Troubleshooting

### Environment Not Found

```bash
# List all conda environments
conda info --envs

# Create if missing
conda create -n aitea python=3.11 -y
```

### UV Not Found

```bash
# Make sure conda environment is activated
conda activate aitea

# Install UV
pip install uv

# Verify
uv --version
```

### Wrong Python Version

```bash
# Check current Python
python --version

# Check conda environment
echo $CONDA_DEFAULT_ENV  # Linux/macOS
echo %CONDA_DEFAULT_ENV%  # Windows

# Should show 'aitea' and Python 3.11.x
```

### Package Installation Issues

```bash
# Clear UV cache
uv cache clean

# Reinstall dependencies
uv pip install -r requirements.txt --force-reinstall
```

## Verification

Run the verification script to ensure everything is working:

```bash
conda activate aitea
python verify_setup.py
```

**Expected output:**

```
🔍 Verifying AITEA setup...

✅ Python 3.11.x
✅ Conda environment: aitea
✅ Python path: /path/to/miniconda3/envs/aitea
✅ UV installed: uv 0.x.x
✅ pydantic installed
✅ hypothesis installed
✅ typer installed
✅ rich installed
✅ pandas installed
✅ src exists
✅ tests exists
✅ pyproject.toml exists

🎉 All checks passed! Ready for development.
```

## Verification Script

Create `verify_setup.py`:

```python
"""Verify AITEA development environment setup."""

import sys
import os
import subprocess
from pathlib import Path


def check_python_version():
    """Ensure Python 3.10+."""
    version = sys.version_info
    assert version >= (3, 10), f"Need Python 3.10+, got {version.major}.{version.minor}"
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")


def check_conda_env():
    """Ensure running in conda environment."""
    conda_env = os.environ.get('CONDA_DEFAULT_ENV')
    assert conda_env == 'aitea', f"Expected 'aitea' environment, got '{conda_env}'"
    print(f"✅ Conda environment: {conda_env}")
    print(f"✅ Python path: {sys.prefix}")


def check_uv_installed():
    """Ensure UV is available."""
    try:
        result = subprocess.run(['uv', '--version'], capture_output=True, text=True)
        assert result.returncode == 0, "UV not installed or not in PATH"
        print(f"✅ UV installed: {result.stdout.strip()}")
    except FileNotFoundError:
        raise AssertionError("UV not found. Install with: pip install uv")


def check_dependencies():
    """Ensure core dependencies are installed."""
    deps = ["pydantic", "hypothesis", "typer", "rich", "pandas", "chromadb", "pytest_asyncio"]
    for dep in deps:
        __import__(dep)
        print(f"✅ {dep} installed")


def check_project_structure():
    """Ensure project structure exists."""
    required = ["src", "tests", "pyproject.toml"]
    for item in required:
        path = Path(item)
        assert path.exists(), f"Missing: {item}"
        print(f"✅ {item} exists")


if __name__ == "__main__":
    print("🔍 Verifying AITEA setup...\n")

    check_python_version()
    check_conda_env()
    check_uv_installed()
    check_dependencies()
    check_project_structure()

    print("\n🎉 All checks passed! Ready for development.")
```

Run with:

```bash
conda activate aitea
python verify_setup.py
```

## Integration with IDEs

### VS Code

1. Install Python extension
2. Select interpreter: `Ctrl+Shift+P` → "Python: Select Interpreter"
3. Choose: `~/miniconda3/envs/aitea/bin/python`

### PyCharm

1. File → Settings → Project → Python Interpreter
2. Add → Conda Environment → Existing
3. Select: `~/miniconda3/envs/aitea/bin/python`

## Best Practices

1. **Always activate environment first**:

   ```bash
   conda activate aitea
   ```

2. **Use UV for all package operations**:

   ```bash
   uv pip install package-name  # Not pip!
   ```

3. **Keep requirements.txt updated**:

   ```bash
   uv pip freeze > requirements.txt
   ```

4. **Use editable installs for development**:

   ```bash
   uv pip install -e .
   ```

5. **Check environment before running code**:
   ```bash
   echo $CONDA_DEFAULT_ENV  # Should show 'aitea'
   ```

This setup provides the best of both worlds: Conda's robust environment management with UV's lightning-fast package installation.
