#!/usr/bin/env python3
"""
Verification Script for Chapter 23: LangChain Loaders

Tests Metadata Propagation (P31) and Splitter logic.
"""

import sys

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_test(name, passed, details=""):
    status = f"{Colors.GREEN}✓ PASS{Colors.RESET}" if passed else f"{Colors.RED}✗ FAIL{Colors.RESET}"
    print(f"{status} - {name}")
    if details: print(f"  {details}")

# --- Test 1: Metadata Propagation (P31) ---
def test_metadata_propagation():
    """Verify that split_documents preserves parent metadata"""
    try:
        from langchain_core.documents import Document
        from langchain_text_splitters import CharacterTextSplitter
        
        parent_meta = {"source": "manual.pdf", "page": 1}
        parent_doc = Document(page_content="Part A. Part B.", metadata=parent_meta)
        
        splitter = CharacterTextSplitter(chunk_size=5, chunk_overlap=0, separator=".")
        chunks = splitter.split_documents([parent_doc])
        
        # Verify
        assert len(chunks) >= 2
        for c in chunks:
            assert c.metadata == parent_meta
            
        print_test("Metadata Propagation (P31)", True, "Metadata correctly copied to all chunks")
        return True
    except Exception as e:
        print_test("Metadata Propagation (P31)", False, str(e))
        return False

# --- Test 2: Dependency Check ---
def test_langchain_community_installed():
    try:
        import langchain_community
        import langchain_text_splitters
        print_test("Package Install", True, "langchain-community and splitters installed")
        return True
    except ImportError as e:
        print_test("Package Install", False, f"Missing: {e}")
        return False

def main():
    print(f"\n{Colors.BOLD}Chapter 23 Verification{Colors.RESET}")
    print("="*40)
    
    results = [
        test_langchain_community_installed(),
        test_metadata_propagation()
    ]
    
    if all(results):
        print(f"\n{Colors.GREEN}✅ Chapter 23 Logic Verified!{Colors.RESET}")
    else:
        print(f"\n{Colors.RED}⚠️ Some tests failed.{Colors.RESET}")

if __name__ == "__main__":
    main()
