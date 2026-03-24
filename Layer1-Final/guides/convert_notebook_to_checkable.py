#!/usr/bin/env python3
"""
Convert Jupyter Notebook diagnostic back to checkable Python file.

Usage:
    python convert_notebook_to_checkable.py

This script:
1. Reads DAY-00-DIAGNOSTIC.ipynb
2. Extracts all code cells
3. Removes test/execution code (prints, test calls)
4. Preserves TODO comments and function signatures
5. Outputs DAY-00-DIAGNOSTIC.checkable.py for grading
"""

import json
import re
import sys
from pathlib import Path


def extract_code_from_notebook(notebook_path: str) -> str:
    """Extract and clean code from Jupyter notebook cells."""
    
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)
    
    code_cells = []
    skip_next_test_block = False
    
    for cell in notebook['cells']:
        if cell['cell_type'] != 'code':
            continue
        
        source = cell['source']
        if isinstance(source, list):
            source = ''.join(source)
        
        # Skip import cell (we'll add it manually)
        if 'import pandas as pd' in source and 'print("✓ All libraries imported' in source:
            continue
        
        # Skip self-assessment cell
        if 'Self-Assessment' in source or 'print("=" * 60)' in source:
            continue
        
        # Remove test execution code but keep function definitions
        lines = source.split('\n')
        cleaned_lines = []
        in_test_block = False
        
        for line in lines:
            # Skip print statements that are just for testing
            if line.strip().startswith('print(') and '"""' not in line:
                # Keep print statements in docstrings, skip test prints
                if 'Testing' in line or 'Expected:' in line or 'Match:' in line:
                    continue
                if 'Testing' in ''.join(cleaned_lines[-5:]):
                    continue
            
            # Skip test function calls (not definitions)
            if re.match(r'^\s*(test_|account\.|df_clean =|stats =|result =|electronics =|titles =|post =)', line):
                if 'def test_' not in line:
                    continue
            
            # Skip try/except blocks used for testing
            if line.strip() == 'try:' and 'Testing' in ''.join(cleaned_lines[-3:]):
                in_test_block = True
                continue
            
            if line.strip().startswith('except ') and in_test_block:
                continue
            
            if line.strip() == 'except Exception as e:' and in_test_block:
                continue
            
            if in_test_block and (line.strip().startswith('print(') or line.strip() == ''):
                if 'API Error' in line or 'Unexpected error' in line:
                    continue
                if line.strip() == '':
                    # Check if next meaningful line ends the block
                    pass
            
            # Reset test block flag on function/class definitions
            if line.strip().startswith('def ') or line.strip().startswith('class '):
                in_test_block = False
            
            cleaned_lines.append(line)
        
        # Remove trailing empty lines and test code
        cleaned_source = '\n'.join(cleaned_lines)
        
        # Remove inline test code at end of cells
        cleaned_source = re.sub(
            r'\n# Run the.*?\n.*?(?=\n#|$)',
            '',
            cleaned_source,
            flags=re.DOTALL
        )
        
        cleaned_source = re.sub(
            r'\n# Test the.*?\n.*?(?=\n#|$)',
            '',
            cleaned_source,
            flags=re.DOTALL
        )
        
        cleaned_source = re.sub(
            r'\n# Run tests inline.*?\n.*?(?=\n#|$)',
            '',
            cleaned_source,
            flags=re.DOTALL
        )
        
        if cleaned_source.strip():
            code_cells.append(cleaned_source)
    
    # Assemble the final Python file
    header = '''#!/usr/bin/env python3
"""
Day 00 Python Diagnostic — Student Task File
Converted from Jupyter Notebook for grading

Instructions:
1. Replace ALL TODO comments with your implementation
2. Do NOT use AI assistance during this diagnostic
3. Run the grader: python grade_diagnostic.py
4. Check your results in diagnostic_results/

Scoring: 5 tasks × 1 point each = 5 points total
"""

import pandas as pd
import requests
from typing import List, Dict, Optional, TypedDict
import pytest

'''
    
    return header + '\n\n'.join(code_cells)


def main():
    """Main conversion function."""
    notebook_path = Path(__file__).parent / 'DAY-00-DIAGNOSTIC.ipynb'
    output_path = Path(__file__).parent / 'DAY-00-DIAGNOSTIC.checkable.py'
    
    if not notebook_path.exists():
        print(f"✗ Error: Notebook not found at {notebook_path}")
        sys.exit(1)
    
    print(f"Converting: {notebook_path}")
    
    python_code = extract_code_from_notebook(str(notebook_path))
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(python_code)
    
    print(f"✓ Created checkable file: {output_path}")
    print(f"  Now run: python grade_diagnostic.py {output_path}")


if __name__ == '__main__':
    main()
