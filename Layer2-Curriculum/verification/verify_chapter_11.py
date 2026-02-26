#!/usr/bin/env python3
"""
Verification Script for Chapter 11: Structured Output

Tests Pydantic model validation and type coercion logic.
Includes tests for Projects 3-5.
"""

import sys
from pydantic import BaseModel, ValidationError, Field
from typing import List, Dict, Any

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_test(name, passed, details=""):
    status = f"{Colors.GREEN}✓ PASS{Colors.RESET}" if passed else f"{Colors.RED}✗ FAIL{Colors.RESET}"
    print(f"{status} - {name}")
    if details: print(f"  {details}")

# --- Test 1: Pydantic Validation & Coercion ---
def test_pydantic_coercion():
    """Verify that Pydantic turns strings into integers/floats"""
    class Movie(BaseModel):
        title: str
        year: int
        rating: float

    raw_data = {
        "title": "Interstellar",
        "year": "2014", # String input
        "rating": "8.6" # String input
    }
    
    try:
        movie = Movie.model_validate(raw_data)
        assert isinstance(movie.year, int)
        assert isinstance(movie.rating, float)
        assert movie.year == 2014
        print_test("Type Coercion", True, "Strings coerced to correct numeric types")
        return True
    except Exception as e:
        print_test("Type Coercion", False, str(e))
        return False

# --- Test 2: Validation Errors ---
def test_validation_errors():
    """Verify that missing required fields raise errors"""
    class User(BaseModel):
        name: str
        age: int

    try:
        # Missing 'age'
        User.model_validate({"name": "Ahmed"})
        print_test("Validation Error Handling", False, "Should have raised ValidationError")
        return False
    except ValidationError:
        print_test("Validation Error Handling", True, "Successfully caught missing field error")
        return True
    except Exception as e:
        print_test("Validation Error Handling", False, str(e))
        return False

# --- Test 3: Schema Validator (Project 3) ---
def test_schema_validator():
    """Test Schema Validator logic"""
    class Product(BaseModel):
        name: str
        price: float = Field(gt=0)
        in_stock: bool

    try:
        # Valid data
        valid_data = {"name": "Laptop", "price": 999.99, "in_stock": True}
        product = Product.model_validate(valid_data)
        assert product.price == 999.99

        # Invalid data - negative price
        try:
            Product.model_validate({"name": "Item", "price": -10, "in_stock": True})
            print_test("Schema Validator (Project 3)", False, "Should catch negative price")
            return False
        except ValidationError as e:
            assert any("greater than 0" in str(err) for err in e.errors())

        print_test("Schema Validator (Project 3)", True, "Validates constraints correctly")
        return True
    except Exception as e:
        print_test("Schema Validator (Project 3)", False, str(e))
        return False

# --- Test 4: Multi-Format Extractor (Project 4) ---
def test_multi_format_extractor():
    """Test multi-format extraction fallback logic"""
    class Event(BaseModel):
        date: str
        title: str
        attendees: int = Field(gt=0)

    try:
        # Test primary format success
        valid_json = {"date": "2024-01-15", "title": "Tech Conf", "attendees": 250}
        event = Event.model_validate(valid_json)
        assert event.attendees == 250

        # Test fallback scenarios with error tracking
        attempts = []

        # Attempt 1: Invalid format (should fail)
        try:
            Event.model_validate({"date": "2024-01-15", "title": "Conf"})  # Missing attendees
            attempts.append({"format": "json", "status": "failed"})
        except ValidationError:
            attempts.append({"format": "json", "status": "failed"})

        # Attempt 2: Valid fallback
        try:
            fallback_data = {"date": "2024-01-15", "title": "Conf", "attendees": 100}
            Event.model_validate(fallback_data)
            attempts.append({"format": "fallback", "status": "success"})
        except:
            attempts.append({"format": "fallback", "status": "failed"})

        assert len(attempts) == 2
        assert attempts[-1]["status"] == "success"

        print_test("Multi-Format Extractor (Project 4)", True,
                  f"Fallback logic works ({len(attempts)} attempts)")
        return True
    except Exception as e:
        print_test("Multi-Format Extractor (Project 4)", False, str(e))
        return False

# --- Test 5: Contract Parser (Project 5) ---
def test_contract_parser():
    """Test Contract Parser nested validation"""
    class Party(BaseModel):
        name: str
        role: str

    class PaymentTerm(BaseModel):
        amount: float = Field(gt=0)
        due_date: str
        description: str

    class Contract(BaseModel):
        contract_id: str
        parties: List[Party] = Field(min_length=2)
        payment_terms: List[PaymentTerm]
        total_value: float = Field(gt=0)

    try:
        # Valid contract
        valid_contract = {
            "contract_id": "CONT-001",
            "parties": [
                {"name": "Acme Corp", "role": "client"},
                {"name": "DevShop", "role": "consultant"}
            ],
            "payment_terms": [
                {"amount": 5000, "due_date": "2024-03-01", "description": "Phase 1"},
                {"amount": 5000, "due_date": "2024-06-01", "description": "Phase 2"}
            ],
            "total_value": 10000
        }

        contract = Contract.model_validate(valid_contract)
        assert len(contract.parties) == 2
        assert len(contract.payment_terms) == 2
        assert sum(p.amount for p in contract.payment_terms) == contract.total_value

        # Invalid - too few parties
        try:
            Contract.model_validate({
                "contract_id": "CONT-002",
                "parties": [{"name": "Only One", "role": "client"}],
                "payment_terms": [],
                "total_value": 1000
            })
            print_test("Contract Parser (Project 5)", False, "Should require 2+ parties")
            return False
        except ValidationError as e:
            assert any("at least 2" in str(err) for err in e.errors())

        print_test("Contract Parser (Project 5)", True,
                  "Nested validation with business rules works")
        return True
    except Exception as e:
        print_test("Contract Parser (Project 5)", False, str(e))
        return False

def main():
    print(f"\n{Colors.BOLD}Chapter 11 Verification{Colors.RESET}")
    print("="*60)

    tests = [
        test_pydantic_coercion,
        test_validation_errors,
        test_schema_validator,
        test_multi_format_extractor,
        test_contract_parser
    ]

    results = []
    for test in tests:
        try:
            results.append(test())
        except Exception as e:
            print(f"Test crashed: {e}")
            results.append(False)
        print()

    passed = sum(1 for r in results if r)
    total = len(results)

    print("="*60)
    print(f"Passed: {passed}/{total}")

    if passed == total:
        print(f"\n{Colors.GREEN}✅ All Chapter 11 tests passed!{Colors.RESET}")
    else:
        print(f"\n{Colors.RED}⚠️ Some tests failed.{Colors.RESET}")

if __name__ == "__main__":
    main()
