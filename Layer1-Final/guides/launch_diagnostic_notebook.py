#!/usr/bin/env python3
"""
Launch DAY-00-DIAGNOSTIC notebook in Jupyter Notebook (classic).

Usage:
    python launch_diagnostic_notebook.py
    
Or simply:
    ./launch_diagnostic_notebook.py  (on Linux/Mac)

This script:
1. Checks if Jupyter Notebook is installed
2. Opens DAY-00-DIAGNOSTIC.ipynb in your default browser
3. Starts Jupyter Notebook server in the background
"""

import subprocess
import sys
import os
from pathlib import Path


def check_jupyter_notebook_installed() -> bool:
    """Check if Jupyter Notebook is installed."""
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'jupyter', 'notebook', '--version'],
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def install_jupyter_notebook():
    """Install Jupyter Notebook if not present."""
    print("Jupyter Notebook not found. Installing...")
    try:
        subprocess.run(
            [sys.executable, '-m', 'pip', 'install', 'notebook', '--upgrade'],
            check=True
        )
        print("✓ Jupyter Notebook installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install Jupyter Notebook: {e}")
        print("\nPlease install manually:")
        print("  pip install notebook")
        return False


def launch_notebook(notebook_path: Path):
    """Launch Jupyter Notebook with the notebook."""
    
    if not notebook_path.exists():
        print(f"✗ Error: Notebook not found at {notebook_path}")
        print("\nCreating fresh notebook from template...")
        
        # Create from Python file if notebook doesn't exist
        python_file = notebook_path.with_suffix('.py')
        if python_file.exists():
            try:
                subprocess.run(
                    [sys.executable, '-m', 'jupyter', 'nbconvert', 
                     '--to', 'notebook', 
                     '--output', str(notebook_path.name),
                     str(python_file)],
                    check=True,
                    cwd=notebook_path.parent
                )
                print(f"✓ Created notebook from {python_file.name}")
            except subprocess.CalledProcessError:
                print(f"✗ Failed to create notebook")
                return
        else:
            print(f"✗ Also cannot find {python_file.name}")
            return
    
    print(f"Launching Jupyter Notebook with: {notebook_path.name}")
    print(f"Directory: {notebook_path.parent}")
    print("\nJupyter Notebook will open in your default browser.")
    print("Press Ctrl+C to stop the server.\n")
    
    # Launch Jupyter Notebook in the notebook's directory
    try:
        subprocess.run(
            [sys.executable, '-m', 'jupyter', 'notebook', str(notebook_path)],
            cwd=notebook_path.parent,
            check=True
        )
    except KeyboardInterrupt:
        print("\n✓ Jupyter Notebook server stopped")
    except FileNotFoundError:
        print("✗ Jupyter Notebook command not found")
        print("\nTry installing:")
        print("  pip install notebook")


def main():
    """Main function."""
    # Get the notebook path (same directory as this script)
    script_dir = Path(__file__).parent
    notebook_path = script_dir / 'DAY-00-DIAGNOSTIC.ipynb'
    
    print("=" * 60)
    print("Day 00 Python Diagnostic - Jupyter Notebook Launcher")
    print("=" * 60)
    print()
    
    # Check if Jupyter Notebook is installed
    if not check_jupyter_notebook_installed():
        print("⚠ Jupyter Notebook is not installed")
        response = input("Install Jupyter Notebook now? (yes/no): ").strip().lower()
        
        if response in ['yes', 'y']:
            if not install_jupyter_notebook():
                sys.exit(1)
        else:
            print("Cancelled. Please install Jupyter Notebook manually:")
            print("  pip install notebook")
            sys.exit(0)
    
    # Launch the notebook
    launch_notebook(notebook_path)


if __name__ == '__main__':
    main()
