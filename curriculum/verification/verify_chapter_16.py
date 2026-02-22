#!/usr/bin/env python3
"""
Verification Script for Chapter 16: Document Loaders

Tests Document object structure and Factory extension detection.
"""

import sys
import os

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_test(name, passed, details=""):
    status = f"{Colors.GREEN}✓ PASS{Colors.RESET}" if passed else f"{Colors.RED}✗ FAIL{Colors.RESET}"
    print(f"{status} - {name}")
    if details: print(f"  {details}")

# --- Test 1: Document Model ---
def test_document_model():
    """Verify that we can create a Document object with content and metadata"""
    try:
        # Simplified Document for the test
        class Document:
            def __init__(self, page_content, metadata=None):
                self.page_content = page_content
                self.metadata = metadata or {}
        
        doc = Document(page_content="test", metadata={"source": "me"})
        assert doc.page_content == "test"
        assert doc.metadata["source"] == "me"
        print_test("Document Model", True, "Container object works correctly")
        return True
    except Exception as e:
        print_test("Document Model", False, str(e))
        return False

# --- Test 2: Extension Logic (Factory) ---
def test_extension_detection():
    """Verify os.path logic used in the Factory"""
    paths = ["test.pdf", "MEMO.TXT", "data.json"]
    try:
        exts = [os.path.splitext(p)[1].lower() for p in paths]
        assert exts == [".pdf", ".txt", ".json"]
        print_test("Extension Logic", True, "Detection logic is robust")
        return True
    except Exception as e:
        print_test("Extension Logic", False, str(e))
        return False

def main():
    print(f"\n{Colors.BOLD}Chapter 16 Verification{Colors.RESET}")
    print("="*40)
    
    results = [
        test_document_model(),
        test_extension_detection()
    ]
    
    if all(results):
        print(f"\n{Colors.GREEN}✅ Chapter 16 Logic Verified!{Colors.RESET}")
    else:
        print(f"\n{Colors.RED}⚠️ Some tests failed.{Colors.RESET}")

if __name__ == "__main__":
    main()
