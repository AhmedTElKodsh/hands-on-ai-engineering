# Chapter 1: Environment & Project Setup

**Difficulty:** Beginner  
**Time:** 1 hour  
**Prerequisites:** None  
**AITEA Component:** Project structure, development environment

> **Quick Reference:** For a condensed setup guide, see [ENVIRONMENT_SETUP.md](../ENVIRONMENT_SETUP.md)

## Learning Objectives

By the end of this chapter, you will be able to:

1. Set up Conda for Python environment management
2. Install and use UV for fast package management
3. Understand the purpose of `pyproject.toml` for project configuration
4. Set up a proper Python project structure
5. Configure environment variables using `.env` files
6. Verify your development environment is working correctly

## 1.1 Why Conda + UV?

Modern Python development benefits from combining the best tools:

- **Conda**: Manages Python versions and system-level dependencies
- **UV**: Ultra-fast package installer (10-100x faster than pip)
- **No pip needed**: UV replaces pip entirely

**The Problem with pip alone:**

```
Project A needs Python 3.10 + CUDA libraries
Project B needs Python 3.11 + different system deps
💥 Complex system conflicts!
```

**The Conda + UV Solution:**

```
Project A → conda env (Python 3.10) → UV installs packages ⚡
Project B → conda env (Python 3.11) → UV installs packages ⚡
```

### Combined Benefits

- **Conda** handles Python versions and system dependencies
- **UV** handles Python packages with blazing speed
- **Best of both worlds**: Robust environment + fast installation

## 1.2 Installing Conda

If you don't have Conda installed:

**Option 1: Miniconda (Recommended)**

```bash
# Download and install Miniconda
# Windows: https://docs.conda.io/en/latest/miniconda.html
# macOS: brew install miniconda
# Linux: wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
```

**Option 2: Anaconda (Full distribution)**

```bash
# Download from https://www.anaconda.com/products/distribution
```

Verify installation:

```bash
conda --version
# Should show: conda 23.x.x
```

## 1.3 Creating Your Environment

Create a Conda environment with Python 3.11:

```bash
# Create conda environment
conda create -n aitea python=3.11 -y

# Activate it
conda activate aitea
```

You'll see `(aitea)` in your terminal prompt:

```
(aitea) PS D:\projects\aitea>
```

**Why Python 3.11?**

- Excellent performance improvements over 3.10
- Great type hint support for modern Python
- Compatible with all AI/ML libraries we'll use

## 1.4 Installing UV

Install UV inside your Conda environment:

```bash
# Make sure aitea environment is activated
conda activate aitea

# Install UV (only need to do this once per environment)
pip install uv

# Verify UV installation
uv --version
# Should show: uv 0.x.x
```

**Why UV over pip?**

- **Speed**: 10-100x faster than pip
- **Better Dependency Resolution**: Handles conflicts more intelligently
- **Drop-in Replacement**: Same commands as pip (`uv pip install`)
- **Modern**: Built in Rust, actively maintained

### Your Turn: Exercise 1.1

Create your environment and verify it's working:

```python
import sys
print(f"Python executable: {sys.executable}")
print(f"Python version: {sys.version}")
# Should show conda environment path
```

**Expected output:**

```
Python executable: /home/user/miniconda3/envs/aitea/bin/python
Python version: 3.11.x
```

## 1.5 Daily Development Workflow

Here's your daily development workflow:

```bash
# 1. Activate conda environment (do this once per terminal session)
conda activate aitea

# 2. Use UV for all package operations (replaces pip entirely)
uv pip install requests
uv pip install -r requirements.txt
uv pip install -e .

# 3. Run your code
python your_script.py

# 4. Deactivate when done (optional)
conda deactivate
```

**Command Comparison:**

| Task              | Old Way (pip)                     | New Way (UV)                         |
| ----------------- | --------------------------------- | ------------------------------------ |
| Install package   | `pip install requests`            | `uv pip install requests`            |
| Install from file | `pip install -r requirements.txt` | `uv pip install -r requirements.txt` |
| Install editable  | `pip install -e .`                | `uv pip install -e .`                |
| Upgrade package   | `pip install --upgrade requests`  | `uv pip install --upgrade requests`  |

## 1.6 Automated Setup Scripts

**Windows PowerShell (`setup-aitea-env.ps1`):**

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

**macOS/Linux (`setup-aitea-env.sh`):**

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

## 1.7 Project Structure

AITEA follows a standard Python project layout:

```
aitea/
├── .gitignore              # Files to exclude from git
├── pyproject.toml          # Project configuration
├── requirements.txt        # Dependencies
├── setup-aitea-env.ps1     # Windows setup script
├── setup-aitea-env.sh      # macOS/Linux setup script
├── src/
│   ├── __init__.py
│   ├── models/             # Data models
│   ├── services/           # Business logic
│   ├── agents/             # Agent implementations
│   ├── cli/                # Command-line interface
│   └── utils/              # Helper functions
├── tests/
│   ├── conftest.py         # Test fixtures
│   ├── properties/         # Property-based tests
│   └── agents/             # Agent tests
├── examples/               # Example scripts
├── curriculum/             # Learning materials
└── data/                   # Sample data files
```

### Why This Structure?

- **`src/`**: Keeps source code separate from tests and config
- **`tests/`**: Mirrors the `src/` structure for easy navigation
- **`pyproject.toml`**: Modern Python packaging standard (replaces `setup.py`)
- **`examples/`**: Demonstrates how to use the system
- **`curriculum/`**: Learning materials for the AITEA curriculum

## 1.8 Understanding pyproject.toml

The `pyproject.toml` file is your project's configuration hub:

```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "aitea"
version = "0.1.0"
description = "AI Time Estimation Agent"
requires-python = ">=3.10"
dependencies = [
    "typer[all]>=0.9.0",
    "rich>=13.0.0",
    "pandas>=2.0.0",
    "numpy>=1.24.0",
    "pydantic>=2.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "hypothesis>=6.0.0",
    "pytest-cov>=4.0.0",
    "mypy>=1.0.0",
]
agents = [
    "crewai>=0.1.0",
    "pyautogen>=0.2.0",
]

[project.scripts]
aitea = "src.cli.main:app"
```

**Key sections:**

- `[project]`: Name, version, and core dependencies
- `[project.optional-dependencies]`: Optional feature groups (dev, agents, etc.)
- `[project.scripts]`: CLI entry points

## 1.9 Installing Dependencies with UV

UV replaces pip with much faster package installation:

```bash
# Make sure conda environment is activated
conda activate aitea

# Install from requirements.txt (10-100x faster than pip!)
uv pip install -r requirements.txt

# Install the project in editable mode
uv pip install -e .

# Install dev dependencies
uv pip install -e ".[dev]"

# Install agent frameworks
uv pip install -e ".[agents]"
```

The `-e` flag means "editable" - changes to your code take effect immediately without reinstalling.

### Your Turn: Exercise 1.2

Install the project and verify the dependencies:

```python
# Check installed packages
import pydantic
import hypothesis
import typer
import rich

print(f"Pydantic version: {pydantic.__version__}")
print(f"Hypothesis version: {hypothesis.__version__}")
print("✅ All dependencies installed with UV!")
```

## 1.10 Environment Variables with .env

API keys and configuration should never be hardcoded. Use `.env` files:

**`.env.example`** (commit this to git):

```env
# Copy to .env and fill in your actual API keys

# ============================================================================
# LLM Provider API Keys (Multi-Provider Fallback)
# ============================================================================
# The system will try providers in this priority order:
# 1. OpenAI → 2. Cohere → 3. Gemini → 4. Grok → 5. Mistral → 6. HuggingFace → 7. Ollama → 8. MockLLM
# Set at least one key to use real LLM providers, or leave all blank to use MockLLM

# OpenAI (GPT-4o, GPT-4o-mini)
OPENAI_API_KEY=your-openai-key-here

# Cohere (Command R+, Command R)
COHERE_API_KEY=your-cohere-key-here

# Google Gemini (Gemini 1.5 Pro, Gemini 1.5 Flash)
GOOGLE_API_KEY=your-google-key-here
# Alternative Gemini key (if you have multiple)
GOOGLE_API_KEY_2=your-second-google-key-here

# xAI Grok
XAI_API_KEY=your-xai-key-here

# Mistral AI
MISTRAL_API_KEY=your-mistral-key-here

# HuggingFace Inference API
HUGGINGFACE_API_KEY=your-huggingface-key-here

# LangChain API Keys
LANGCHAIN_API_KEY=your-langchain-key-here
LANGCHAIN_API_KEY_2=your-second-langchain-key-here

# Ollama (local models - no key needed, just ensure Ollama is running)
# OLLAMA_HOST=http://localhost:11434

# ============================================================================
# AITEA Configuration
# ============================================================================
AITEA_DATA_DIR=./data
AITEA_LOG_LEVEL=INFO

# ============================================================================
# Optional: Observability & Monitoring
# ============================================================================
# LANGSMITH_API_KEY=your-langsmith-key-here
# LANGFUSE_PUBLIC_KEY=your-langfuse-public-key-here
# LANGFUSE_SECRET_KEY=your-langfuse-secret-key-here
```

**`.env`** (don't commit this - add to .gitignore):

```env
# Your actual API keys go here
OPENAI_API_KEY=sk-abc123...
COHERE_API_KEY=co-xyz789...
GOOGLE_API_KEY=AIza...
# ... etc
```

**Loading environment variables:**

```python
import os
from pathlib import Path

# Option 1: Direct access
api_key = os.getenv("OPENAI_API_KEY")

# Option 2: With default
data_dir = os.getenv("AITEA_DATA_DIR", "./data")

# Option 3: Using python-dotenv (recommended)
from dotenv import load_dotenv
load_dotenv()  # Loads .env file automatically

# Check which providers are available
def get_available_providers():
    """Return list of configured LLM providers."""
    providers = []
    if os.getenv("OPENAI_API_KEY"):
        providers.append("OpenAI")
    if os.getenv("COHERE_API_KEY"):
        providers.append("Cohere")
    if os.getenv("GOOGLE_API_KEY"):
        providers.append("Gemini")
    if os.getenv("XAI_API_KEY"):
        providers.append("Grok")
    if os.getenv("MISTRAL_API_KEY"):
        providers.append("Mistral")
    if os.getenv("HUGGINGFACE_API_KEY"):
        providers.append("HuggingFace")

    if not providers:
        providers.append("MockLLM (no API keys set)")

    return providers

# Usage
print(f"Available LLM providers: {', '.join(get_available_providers())}")
```

**Multi-Provider Fallback Behavior:**

The system automatically tries providers in priority order:

1. **OpenAI** - Tried first if `OPENAI_API_KEY` is set
2. **Cohere** - Tried if OpenAI fails or key not set
3. **Gemini** - Tried if previous providers fail
4. **Grok** - Tried if previous providers fail
5. **Mistral** - Tried if previous providers fail
6. **HuggingFace** - Tried if previous providers fail
7. **Ollama** - Tried if running locally
8. **MockLLM** - Final fallback (always available)

**Example: Setting up your first API key**

```bash
# 1. Copy the example file
cp .env.example .env

# 2. Edit .env and add your OpenAI key
# OPENAI_API_KEY=sk-your-actual-key-here

# 3. Verify it's loaded
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('OpenAI key set:', bool(os.getenv('OPENAI_API_KEY')))"
```

**Security Best Practices:**

- ✅ **DO**: Use `.env` files for local development
- ✅ **DO**: Add `.env` to `.gitignore`
- ✅ **DO**: Commit `.env.example` with placeholder values
- ✅ **DO**: Use environment variables in production (not `.env` files)
- ❌ **DON'T**: Commit actual API keys to git
- ❌ **DON'T**: Share your `.env` file
- ❌ **DON'T**: Hardcode API keys in source code

## 1.11 Debugging Scenario

**The Bug:** A colleague's code isn't finding the installed packages.

```python
# They run this and get ModuleNotFoundError
import pandas as pd
```

**The Problem:** They forgot to activate the conda environment!

**The Fix:**

```bash
# Always activate conda environment before running Python
conda activate aitea

# Then run your code
python your_script.py
```

**Pro tip:** Check which Python and environment you're using:

```bash
# Check Python location
which python  # macOS/Linux
where python  # Windows

# Check conda environment
conda info --envs
echo $CONDA_DEFAULT_ENV  # macOS/Linux
echo %CONDA_DEFAULT_ENV%  # Windows
```

## 1.12 Quick Check Questions

1. What command creates a conda environment named `aitea` with Python 3.11?
2. Why use UV instead of pip for package installation?
3. What does the `-e` flag do in `uv pip install -e .`?
4. Where should you put your source code in a standard Python project?
5. What file has replaced `setup.py` in modern Python projects?
6. How do you check which conda environment is currently active?

<details>
<summary>Answers</summary>

1. `conda create -n aitea python=3.11 -y`
2. UV is 10-100x faster than pip and provides better dependency resolution
3. Installs in "editable" mode - code changes take effect immediately
4. In the `src/` directory
5. `pyproject.toml`
6. `echo $CONDA_DEFAULT_ENV` (Linux/macOS) or `echo %CONDA_DEFAULT_ENV%` (Windows)

</details>

## 1.13 Mini-Project: Verify Your Setup

Create a file `verify_setup.py` that checks everything is working:

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
    deps = ["pydantic", "hypothesis", "typer", "rich", "pandas"]
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

    print("\n🎉 All checks passed! Ready for Chapter 2.")
```

**Acceptance Criteria:**

- [ ] All checks pass without errors
- [ ] Conda environment `aitea` is activated
- [ ] UV is installed and working
- [ ] All dependencies are installed via UV
- [ ] Project structure is correct

**Run the verification:**

```bash
conda activate aitea
python verify_setup.py
```

## 1.14 AITEA Integration

This chapter establishes the foundation for the entire AITEA project:

- **Requirement 1.1**: Working Python environment with Conda + UV
- **Component**: Project structure and configuration

**Verification:**

```bash
# Activate environment
conda activate aitea

# Run the verification script
python verify_setup.py

# Run the test suite
python -m pytest tests/ -v
```

## What's Next

In Chapter 2, we'll create our first Python code: enumerations with type hints. You'll learn:

- How to define enums for type-safe constants
- Why type hints make code more reliable
- How to use mypy for static type checking

**Before proceeding:**

- Ensure all setup checks pass
- Familiarize yourself with the project structure
- Review the `pyproject.toml` file
- Try running the example scripts in `examples/`
