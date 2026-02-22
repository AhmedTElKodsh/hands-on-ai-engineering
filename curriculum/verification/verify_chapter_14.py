#!/usr/bin/env python3
"""
Verification Script for Chapter 14: Vector Stores with Chroma

Tests Persistent Client creation and Metadata Filtering logic.
"""

import os
import shutil
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

# --- Test 1: Persistence Logic ---
def test_persistence_init():
    """Verify PersistentClient creates a directory"""
    try:
        import chromadb
        path = "./verify_chroma_db"
        if os.path.exists(path): shutil.rmtree(path)
        
        client = chromadb.PersistentClient(path=path)
        assert os.path.exists(path)
        print_test("Persistence Init", True, "Chroma directory created on disk")
        
        # Cleanup (Try but don't fail if Windows locks it)
        try:
            shutil.rmtree(path)
        except:
            pass
        return True
    except Exception as e:
        print_test("Persistence Init", False, str(e))
        return False

# --- Test 2: Collection CRUD & Filtering ---
def test_collection_logic():
    """Verify we can add data and filter by metadata"""
    try:
        import chromadb
        client = chromadb.Client() # In-memory for speed
        collection = client.create_collection("test")
        
        collection.add(
            documents=["Doc A", "Doc B"],
            metadatas=[{"type": "X"}, {"type": "Y"}],
            ids=["1", "2"]
        )
        
        # Test Query with Filter
        res = collection.query(
            query_texts=["A doc"],
            where={"type": "X"},
            n_results=1
        )
        
        assert res["ids"][0][0] == "1"
        assert res["metadatas"][0][0]["type"] == "X"
        
        print_test("Metadata Filtering", True, "Query respected the 'where' clause")
        return True
    except Exception as e:
        print_test("Metadata Filtering", False, str(e))
        return False

def main():
    print(f"\n{Colors.BOLD}Chapter 14 Verification{Colors.RESET}")
    print("="*40)
    
    results = [
        test_persistence_init(),
        test_collection_logic()
    ]
    
    if all(results):
        print(f"\n{Colors.GREEN}✅ Chapter 14 Logic Verified!{Colors.RESET}")
    else:
        print(f"\n{Colors.RED}⚠️ Some tests failed.{Colors.RESET}")

if __name__ == "__main__":
    main()
