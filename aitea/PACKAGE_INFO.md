# AITEA Package Information

## Overview

The `aitea/pyproject.toml` file defines the AITEA package as a standalone, installable Python package. This modular structure supports both curriculum-based learning and independent package distribution.

## Package Configuration

### Project Metadata

- **Name**: `aitea`
- **Version**: `0.1.0`
- **Description**: AI Time Estimation Agent
- **Python Requirement**: `>=3.10`

### Build System

- **Build Backend**: `setuptools>=61.0`
- Uses modern `pyproject.toml` standard (replaces legacy `setup.py`)

### Core Dependencies

The package requires these core dependencies:

```toml
dependencies = [
    "typer[all]>=0.9.0",    # CLI framework with rich support
    "rich>=13.0.0",          # Terminal formatting
    "pandas>=2.0.0",         # Data processing
    "numpy>=1.24.0",         # Numerical operations
    "pydantic>=2.0.0",       # Data validation
]
```

### Optional Dependencies

#### Development Tools (`dev`)

```bash
uv pip install -e ".[dev]"
```

Includes:

- `pytest>=7.0.0` - Testing framework
- `hypothesis>=6.0.0` - Property-based testing
- `pytest-cov>=4.0.0` - Code coverage
- `mypy>=1.0.0` - Static type checking

#### Agent Frameworks (`agents`)

```bash
uv pip install -e ".[agents]"
```

Includes:

- `crewai>=0.1.0` - Multi-agent orchestration
- `pyautogen>=0.2.0` - Microsoft's agent framework

### CLI Entry Point

The package defines a CLI entry point:

```toml
[project.scripts]
aitea = "src.cli.main:app"
```

After installation, the `aitea` command is available system-wide:

```bash
aitea --help
aitea feature add "User Auth" --team backend --seed-hours 16
aitea estimate "User Auth" "Dashboard"
```

## Installation Methods

### Method 1: From Project Root (Recommended for Curriculum)

```bash
# Install main project with all curriculum materials
uv pip install -e .
```

### Method 2: From aitea/ Directory (Standalone Package)

```bash
# Navigate to package directory
cd aitea

# Install just the aitea package
uv pip install -e .
```

### Method 3: With Optional Dependencies

```bash
# Install with dev tools
uv pip install -e ".[dev]"

# Install with agent frameworks
uv pip install -e ".[agents]"

# Install with all optional dependencies
uv pip install -e ".[dev,agents]"
```

## Package vs Project Structure

### Main Project (Root)

```
aitea-project/
├── pyproject.toml          # Main project config
├── requirements.txt        # All dependencies
├── curriculum/             # Learning materials
├── examples/               # Example scripts
├── src/                    # Source code
└── tests/                  # Test suite
```

### AITEA Package (aitea/)

```
aitea/
├── pyproject.toml          # Package-specific config
├── requirements.txt        # Package dependencies
├── setup-aitea-env.ps1     # Windows setup
├── setup-aitea-env.sh      # Unix setup
├── src/                    # Package source (to be implemented)
└── tests/                  # Package tests (to be implemented)
```

## Benefits of This Structure

### For Learners

- **Progressive learning**: Work through curriculum in main project
- **Clean separation**: Package code separate from learning materials
- **Real-world structure**: Learn professional package organization

### For Distribution

- **Standalone package**: Can be installed independently
- **PyPI ready**: Prepared for package distribution
- **Modular design**: Easy to maintain and version

### For Development

- **Editable installs**: Changes take effect immediately
- **Optional dependencies**: Install only what you need
- **CLI integration**: Command available after installation

## Relationship to Curriculum

The `aitea/` package structure aligns with the curriculum phases:

- **Phase 1-2**: Build core functionality in `src/`
- **Phase 3-4**: Add LLM and agent capabilities
- **Phase 5-6**: Integrate LangChain and LlamaIndex
- **Phase 7+**: Production hardening and deployment

As you progress through the curriculum, you're building a real, installable package.

## Future Distribution

When ready for distribution:

```bash
# Build the package
cd aitea
python -m build

# Upload to PyPI (when ready)
python -m twine upload dist/*

# Users can then install with:
pip install aitea
```

## Development Workflow

### Daily Development

```bash
# 1. Activate environment
conda activate aitea

# 2. Make changes to src/
# ... edit files ...

# 3. Changes take effect immediately (editable install)
python -m pytest tests/

# 4. Run CLI to test
aitea feature list
```

### Adding Dependencies

```bash
# Add to pyproject.toml dependencies list
# Then reinstall
uv pip install -e .
```

### Running Tests

```bash
# Install dev dependencies
uv pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=src --cov-report=html
```

## Documentation Updates

The following documentation has been updated to reflect the package structure:

1. **README.md** (root) - Updated installation section
2. **aitea/README.md** (new) - Package-specific documentation
3. **curriculum/ENVIRONMENT_SETUP.md** - Added package structure notes
4. **curriculum/chapters/CH01_environment_setup.md** - Already covers setup

## Next Steps

1. **Verify installation**: Run `aitea --help` after installing
2. **Follow curriculum**: Work through chapters to build the package
3. **Test as you go**: Run tests after each chapter
4. **Use the CLI**: Practice with the command-line interface

## Questions?

- **Setup issues**: See `curriculum/ENVIRONMENT_SETUP.md`
- **Package structure**: See `aitea/README.md`
- **Curriculum**: See `curriculum/README.md`
- **Main project**: See root `README.md`
