#!/usr/bin/env python3
"""
Verification Script for Chapter 6D: File Handling & Path Management

Tests all code examples and concepts from the chapter to ensure they work correctly.
Run this after completing Chapter 6D to verify all examples are functional.

Usage:
    python verify_chapter_06D.py
"""

import os
import sys
import tempfile
import csv
import json
from pathlib import Path
from typing import List, Dict


class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def print_test(name: str, passed: bool, details: str = ""):
    """Print test result with color coding"""
    status = f"{Colors.GREEN}✓ PASS{Colors.RESET}" if passed else f"{Colors.RED}✗ FAIL{Colors.RESET}"
    print(f"{status} - {name}")
    if details:
        print(f"  {details}")


def test_basic_file_reading():
    """Test basic file reading with context manager"""
    test_name = "Basic File Reading (with open)"
    
    try:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            test_file = f.name
            f.write("Hello, World!\nThis is a test file.")
        
        # Test reading
        with open(test_file, 'r') as f:
            content = f.read()
        
        # Verify
        assert "Hello, World!" in content
        assert "test file" in content
        
        # Cleanup
        os.unlink(test_file)
        
        print_test(test_name, True, "Successfully read file content")
        return True
    except Exception as e:
        print_test(test_name, False, f"Error: {str(e)}")
        return False


def test_file_writing():
    """Test file writing with context manager"""
    test_name = "File Writing (with open)"
    
    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            test_file = f.name
        
        # Write content
        test_content = "Testing file write operations\nLine 2\nLine 3"
        with open(test_file, 'w') as f:
            f.write(test_content)
        
        # Read back and verify
        with open(test_file, 'r') as f:
            content = f.read()
        
        assert content == test_content
        
        # Cleanup
        os.unlink(test_file)
        
        print_test(test_name, True, "Successfully wrote and verified file content")
        return True
    except Exception as e:
        print_test(test_name, False, f"Error: {str(e)}")
        return False


def test_csv_operations():
    """Test CSV file reading and writing"""
    test_name = "CSV File Operations"
    
    try:
        # Create temporary CSV file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv', newline='') as f:
            test_file = f.name
            writer = csv.writer(f)
            writer.writerow(['Name', 'Age', 'City'])
            writer.writerow(['Alice', '30', 'New York'])
            writer.writerow(['Bob', '25', 'San Francisco'])
        
        # Read CSV
        with open(test_file, 'r', newline='') as f:
            reader = csv.reader(f)
            rows = list(reader)
        
        # Verify
        assert len(rows) == 3
        assert rows[0] == ['Name', 'Age', 'City']
        assert rows[1][0] == 'Alice'
        
        # Cleanup
        os.unlink(test_file)
        
        print_test(test_name, True, "Successfully read and wrote CSV data")
        return True
    except Exception as e:
        print_test(test_name, False, f"Error: {str(e)}")
        return False


def test_json_operations():
    """Test JSON file reading and writing"""
    test_name = "JSON File Operations"
    
    try:
        # Create temporary JSON file
        test_data = {
            "name": "Test User",
            "age": 30,
            "skills": ["Python", "AI", "ML"],
            "active": True
        }
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            test_file = f.name
            json.dump(test_data, f, indent=2)
        
        # Read JSON
        with open(test_file, 'r') as f:
            loaded_data = json.load(f)
        
        # Verify
        assert loaded_data == test_data
        assert loaded_data['name'] == "Test User"
        assert len(loaded_data['skills']) == 3
        
        # Cleanup
        os.unlink(test_file)
        
        print_test(test_name, True, "Successfully read and wrote JSON data")
        return True
    except Exception as e:
        print_test(test_name, False, f"Error: {str(e)}")
        return False


def test_pathlib_operations():
    """Test pathlib for cross-platform path management"""
    test_name = "Pathlib Operations"
    
    try:
        # Create temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            base_path = Path(temp_dir)
            
            # Create file using pathlib
            test_file = base_path / "test.txt"
            test_file.write_text("Testing pathlib")
            
            # Verify file exists
            assert test_file.exists()
            assert test_file.is_file()
            
            # Read content
            content = test_file.read_text()
            assert content == "Testing pathlib"
            
            # Test path operations
            assert test_file.name == "test.txt"
            assert test_file.suffix == ".txt"
            assert test_file.parent == base_path
        
        print_test(test_name, True, "Successfully used pathlib for file operations")
        return True
    except Exception as e:
        print_test(test_name, False, f"Error: {str(e)}")
        return False


def test_error_handling():
    """Test error handling for missing files"""
    test_name = "Error Handling (Missing Files)"
    
    try:
        # Try to read non-existent file
        try:
            with open("nonexistent_file_12345.txt", 'r') as f:
                content = f.read()
            # Should not reach here
            print_test(test_name, False, "Expected FileNotFoundError was not raised")
            return False
        except FileNotFoundError:
            # Expected behavior
            pass
        
        # Try with pathlib
        try:
            p = Path("nonexistent_file_12345.txt")
            content = p.read_text()
            # Should not reach here
            print_test(test_name, False, "Expected FileNotFoundError was not raised")
            return False
        except FileNotFoundError:
            # Expected behavior
            pass
        
        print_test(test_name, True, "Correctly handled missing file errors")
        return True
    except Exception as e:
        print_test(test_name, False, f"Unexpected error: {str(e)}")
        return False


def test_directory_operations():
    """Test directory creation and listing"""
    test_name = "Directory Operations"
    
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            base_path = Path(temp_dir)
            
            # Create subdirectory
            sub_dir = base_path / "subdir"
            sub_dir.mkdir()
            
            # Create files
            (sub_dir / "file1.txt").write_text("File 1")
            (sub_dir / "file2.txt").write_text("File 2")
            (sub_dir / "data.json").write_text('{"key": "value"}')
            
            # List directory
            files = list(sub_dir.iterdir())
            assert len(files) == 3
            
            # Filter by extension
            txt_files = list(sub_dir.glob("*.txt"))
            assert len(txt_files) == 2
            
            # Check directory exists
            assert sub_dir.exists()
            assert sub_dir.is_dir()
        
        print_test(test_name, True, "Successfully performed directory operations")
        return True
    except Exception as e:
        print_test(test_name, False, f"Error: {str(e)}")
        return False


def test_file_iteration():
    """Test reading files line by line"""
    test_name = "File Iteration (Line by Line)"
    
    try:
        # Create test file with multiple lines
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            test_file = f.name
            f.write("Line 1\nLine 2\nLine 3\nLine 4\nLine 5")
        
        # Read line by line
        lines = []
        with open(test_file, 'r') as f:
            for line in f:
                lines.append(line.strip())
        
        # Verify
        assert len(lines) == 5
        assert lines[0] == "Line 1"
        assert lines[4] == "Line 5"
        
        # Cleanup
        os.unlink(test_file)
        
        print_test(test_name, True, "Successfully iterated through file lines")
        return True
    except Exception as e:
        print_test(test_name, False, f"Error: {str(e)}")
        return False


def main():
    """Run all verification tests"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}Chapter 6D Verification Tests{Colors.RESET}")
    print("=" * 60)
    print()
    
    tests = [
        test_basic_file_reading,
        test_file_writing,
        test_csv_operations,
        test_json_operations,
        test_pathlib_operations,
        test_error_handling,
        test_directory_operations,
        test_file_iteration,
    ]
    
    results = []
    for test in tests:
        results.append(test())
        print()
    
    # Summary
    passed = sum(results)
    total = len(results)
    
    print("=" * 60)
    print(f"\n{Colors.BOLD}Summary:{Colors.RESET}")
    print(f"  Passed: {Colors.GREEN}{passed}{Colors.RESET}/{total}")
    print(f"  Failed: {Colors.RED}{total - passed}{Colors.RESET}/{total}")
    
    if passed == total:
        print(f"\n{Colors.GREEN}{Colors.BOLD}✓ All tests passed!{Colors.RESET}")
        print(f"Chapter 6D examples are working correctly.\n")
        return 0
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}✗ Some tests failed{Colors.RESET}")
        print(f"Please review the failed tests above.\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
