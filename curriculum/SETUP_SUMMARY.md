# AITEA Environment Setup Summary

## What Changed

The AITEA curriculum now uses a modern Python development setup:

- **Before**: Python venv + pip
- **After**: Conda + UV (10-100x faster package installation)

## Quick Setup Commands

### Windows

```powershell
# Run the setup script
.\setup-aitea-env.ps1

# Or manually:
conda create -n aitea python=3.11 -y
conda activate aitea
pip install uv
uv pip install -r requirements.txt
uv pip install -e .
```

### macOS/Linux

```bash
# Run the setup script
./setup-aitea-env.sh

# Or manually:
conda create -n aitea python=3.11 -y
conda activate aitea
pip install uv
uv pip install -r requirements.txt
uv pip install -e .
```

## Daily Workflow

```bash
# 1. Activate environment (once per terminal session)
conda activate aitea

# 2. Use UV for package operations (replaces pip)
uv pip install new-package

# 3. Run your code
python your_script.py
```

## Why This Change?

### Conda Benefits

- **Python Version Management**: Easy switching between Python versions
- **System Dependencies**: Handles complex libraries (CUDA, MKL, etc.)
- **Cross-Platform Consistency**: Same behavior on Windows/macOS/Linux
- **Scientific Computing**: Optimized packages for AI/ML development

### UV Benefits

- **Speed**: 10-100x faster than pip
- **Better Dependency Resolution**: Handles conflicts intelligently
- **Drop-in Replacement**: Same commands as pip (`uv pip install`)
- **Modern**: Built in Rust, actively maintained

## Files Updated

1. **`curriculum/chapters/CH01_environment_setup.md`**

   - Updated to use Conda + UV approach
   - Added setup scripts and verification
   - Updated exercises and debugging scenarios

2. **`curriculum/README.md`**

   - Updated quick start instructions
   - Added reference to environment setup guide

3. **`.kiro/specs/curriculum/requirements.md`**

   - Updated Requirement 1.1 to reflect Conda + UV

4. **New Files Created:**
   - `curriculum/ENVIRONMENT_SETUP.md` - Comprehensive setup guide
   - `setup-aitea-env.ps1` - Windows PowerShell setup script
   - `setup-aitea-env.sh` - macOS/Linux setup script
   - `curriculum/SETUP_SUMMARY.md` - This summary

## Verification

Run the verification script to ensure everything is working:

```bash
conda activate aitea
python verify_setup.py
```

Expected output:

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

## Migration Guide

If you have an existing setup with venv + pip:

1. **Deactivate old environment:**

   ```bash
   deactivate  # If using venv
   ```

2. **Install Conda** (if not already installed)

3. **Run setup script:**

   ```bash
   # Windows
   .\setup-aitea-env.ps1

   # macOS/Linux
   ./setup-aitea-env.sh
   ```

4. **Update your workflow:**
   - Replace `pip install` with `uv pip install`
   - Use `conda activate aitea` instead of venv activation

## Troubleshooting

### Common Issues

**"conda: command not found"**

- Install Miniconda or Anaconda
- Restart terminal after installation

**"uv: command not found"**

- Make sure conda environment is activated: `conda activate aitea`
- Install UV: `pip install uv`

**"Wrong Python version"**

- Check environment: `echo $CONDA_DEFAULT_ENV` (should show 'aitea')
- Check Python: `python --version` (should show 3.11.x)

**Package installation fails**

- Try clearing UV cache: `uv cache clean`
- Reinstall: `uv pip install -r requirements.txt --force-reinstall`

## Benefits for Learners

1. **Faster Development**: UV's speed means less waiting for package installs
2. **Better Reliability**: Conda's environment isolation prevents conflicts
3. **Industry Standard**: Learn tools used in professional AI/ML development
4. **Future-Proof**: Modern toolchain that will remain relevant

## Next Steps

1. Complete Chapter 1 with the new setup
2. Verify all exercises work with Conda + UV
3. Continue with the curriculum as normal

The rest of the curriculum remains unchanged - only the environment setup has been modernized!
