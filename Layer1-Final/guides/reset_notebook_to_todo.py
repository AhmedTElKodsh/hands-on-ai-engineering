#!/usr/bin/env python3
"""
Reset Jupyter Notebook diagnostic back to TODO state.

Usage:
    python reset_notebook_to_todo.py

This script:
1. Reads DAY-00-DIAGNOSTIC.ipynb
2. Replaces all implemented code with TODO placeholders
3. Preserves function signatures, docstrings, and structure
4. Saves as DAY-00-DIAGNOSTIC.ipynb (backup created automatically)

WARNING: This will overwrite your work! Backup is created automatically.
"""

import json
import re
import sys
from pathlib import Path
from datetime import datetime


def reset_code_cell(source: str) -> str:
    """Reset a code cell back to TODO state."""
    
    lines = source.split('\n')
    reset_lines = []
    in_function_body = False
    in_class_body = False
    indent_level = 0
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # Keep imports as-is
        if stripped.startswith('import ') or stripped.startswith('from '):
            reset_lines.append(line)
            continue
        
        # Keep function/class definitions and docstrings
        if stripped.startswith('def ') or stripped.startswith('class '):
            reset_lines.append(line)
            in_function_body = stripped.startswith('def ')
            in_class_body = stripped.startswith('class ')
            indent_level = len(line) - len(line.lstrip())
            continue
        
        # Keep docstrings
        if '"""' in stripped or "'''" in stripped:
            reset_lines.append(line)
            continue
        
        # Keep comments that start with # (but not test comments)
        if stripped.startswith('#') and not stripped.startswith('# Test') and not stripped.startswith('# Run'):
            reset_lines.append(line)
            continue
        
        # Keep return statements in skeleton form
        if stripped.startswith('return {') or stripped.startswith('return ['):
            # Replace with pass + TODO
            current_indent = len(line) - len(line.lstrip())
            reset_lines.append(' ' * current_indent + '# TODO: Implement return value')
            reset_lines.append(' ' * current_indent + 'pass')
            continue
        
        # Replace implementation lines with TODO + pass
        if stripped and not stripped.startswith('pass'):
            # Check if this is inside a function/class body
            current_indent = len(line) - len(line.lstrip())
            
            # Skip if it's just closing braces
            if stripped in [']', '}', ')']:
                reset_lines.append(line)
                continue
            
            # Skip test execution code entirely
            if any(x in stripped for x in ['print(', 'assert', 'try:', 'except', 'if __name__']):
                continue
            
            # Replace actual implementation with TODO
            if in_function_body or in_class_body:
                # Only add TODO once per function/block
                if not any('TODO' in l for l in reset_lines[-3:]):
                    reset_lines.append(' ' * current_indent + '# TODO: Implement this section')
                    reset_lines.append(' ' * current_indent + 'pass')
        else:
            reset_lines.append(line)
    
    return '\n'.join(reset_lines)


def reset_notebook_to_todo(notebook_path: str, output_path: str = None) -> bool:
    """Reset notebook to TODO state."""
    
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)
    
    # Create backup
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = Path(notebook_path).parent / f'DAY-00-DIAGNOSTIC.backup.{timestamp}.ipynb'
    
    with open(backup_path, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=1)
    
    print(f"✓ Backup created: {backup_path}")
    
    # Reset each code cell
    for cell in notebook['cells']:
        if cell['cell_type'] != 'code':
            continue
        
        source = cell['source']
        if isinstance(source, list):
            source = ''.join(source)
        
        # Skip import cell
        if 'import pandas as pd' in source and 'import requests' in source:
            continue
        
        # Reset the cell
        reset_source = reset_code_cell(source)
        cell['source'] = reset_source.split('\n')
        cell['source'] = [line + '\n' if i < len(reset_source.split('\n')) - 1 else line 
                          for i, line in enumerate(cell['source'])]
    
    # Save reset notebook
    output = output_path or notebook_path
    with open(output, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=1)
    
    print(f"✓ Notebook reset to TODO state: {output}")
    return True


def main():
    """Main reset function."""
    notebook_path = Path(__file__).parent / 'DAY-00-DIAGNOSTIC.ipynb'
    
    if not notebook_path.exists():
        print(f"✗ Error: Notebook not found at {notebook_path}")
        sys.exit(1)
    
    print(f"Resetting: {notebook_path}")
    print("⚠ WARNING: This will remove all your implemented code!")
    print("  A backup will be created automatically.")
    print()
    
    # Ask for confirmation
    response = input("Continue? (yes/no): ").strip().lower()
    if response not in ['yes', 'y']:
        print("Cancelled.")
        sys.exit(0)
    
    reset_notebook_to_todo(str(notebook_path))
    print()
    print("✓ Notebook reset complete!")
    print("  You can now start fresh with the TODO placeholders.")


if __name__ == '__main__':
    main()
