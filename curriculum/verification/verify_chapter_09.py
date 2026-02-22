#!/usr/bin/env python3
"""
Verification Script for Chapter 9: Prompt Engineering Basics

Tests the Template Logic, Variable Substitution, and JSON Escaping.
Includes tests for Project 3 (Few-Shot Builder), Project 4 (A/B Tester), and Project 5 (Validator).
"""

import sys
import re
from typing import List, Dict

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_test(name, passed, details=""):
    status = f"{Colors.GREEN}✓ PASS{Colors.RESET}" if passed else f"{Colors.RED}✗ FAIL{Colors.RESET}"
    print(f"{status} - {name}")
    if details: print(f"  {details}")

# --- Test 1: Simple Template Substitution ---
def test_template_substitution():
    """Verify that Python's .format() works as expected for prompts"""
    try:
        template = "You are a {persona}. Write about {topic}."
        result = template.format(persona="Pirate", topic="Coffee")
        assert "Pirate" in result
        assert "Coffee" in result
        print_test("Simple Substitution", True, "Variables injected correctly")
        return True
    except Exception as e:
        print_test("Simple Substitution", False, str(e))
        return False

# --- Test 2: JSON Brace Escaping ---
def test_json_escaping():
    """Verify that double braces correctly escape literal braces for JSON templates"""
    try:
        # In a real app, we use double {{ }} to keep literal braces when calling .format()
        template = '{{ "name": "{name}", "role": "AI" }}'
        result = template.format(name="Ahmed")
        assert result == '{ "name": "Ahmed", "role": "AI" }'
        print_test("JSON Escaping", True, "Double braces handled correctly")
        return True
    except Exception as e:
        print_test("JSON Escaping", False, str(e))
        return False

# --- Test 3: Missing Variable Error ---
def test_missing_variable_behavior():
    """Verify that missing variables raise KeyError (standard Python behavior)"""
    try:
        template = "Hello {name}, welcome to {city}."
        # Intentional missing variable 'city'
        try:
            template.format(name="Ahmed")
            print_test("Error Handling", False, "Should have raised KeyError")
            return False
        except KeyError:
            print_test("Error Handling", True, "Successfully caught missing variable error")
            return True
    except Exception as e:
        print_test("Error Handling", False, str(e))
        return False

# --- Test 4: Few-Shot Template Builder (Project 3) ---
def test_few_shot_builder():
    """Test Few-Shot Template Builder logic"""
    try:
        class FewShotBuilder:
            def __init__(self, task_description: str):
                self.task_description = task_description
                self.examples = []

            def add_example(self, input_text: str, expected_output: str):
                """Add an example to the few-shot collection"""
                self.examples.append({
                    "input": input_text,
                    "output": expected_output
                })

            def build_prompt(self, new_input: str) -> str:
                """Generate a complete prompt with all examples + new input"""
                prompt_parts = [self.task_description, ""]

                for i, example in enumerate(self.examples, 1):
                    prompt_parts.append(f"Example {i}: {example['input']} -> {example['output']}")

                prompt_parts.append(f"\nInput: {new_input}")
                prompt_parts.append("Output:")

                return "\n".join(prompt_parts)

        # Test builder
        builder = FewShotBuilder("Classify the sentiment as positive, negative, or neutral.")
        builder.add_example("I love this product!", "positive")
        builder.add_example("This is terrible.", "negative")
        builder.add_example("It's okay.", "neutral")

        prompt = builder.build_prompt("Best purchase ever!")

        # Verify prompt structure
        assert "Classify the sentiment" in prompt, "Task description missing"
        assert "Example 1:" in prompt, "Examples not formatted"
        assert "I love this product!" in prompt, "Example 1 missing"
        assert "This is terrible." in prompt, "Example 2 missing"
        assert "It's okay." in prompt, "Example 3 missing"
        assert "Best purchase ever!" in prompt, "New input missing"
        assert "Output:" in prompt, "Output marker missing"

        # Test with different number of examples
        builder2 = FewShotBuilder("Extract company names")
        builder2.add_example("Apple launched iPhone", "Apple")
        prompt2 = builder2.build_prompt("Google released Gemini")

        assert "Example 1:" in prompt2
        assert "Google released Gemini" in prompt2

        print_test("Few-Shot Builder (Project 3)", True,
                  f"Correctly formats {len(builder.examples)} examples")
        return True
    except Exception as e:
        print_test("Few-Shot Builder (Project 3)", False, str(e))
        return False

# --- Test 5: A/B Prompt Tester Logic (Project 4) ---
def test_ab_tester_logic():
    """Test A/B Prompt Tester tracking logic (without actual API calls)"""
    try:
        class ABTester:
            def __init__(self):
                self.results = {}

            def record_test(self, name: str, prompt_length: int,
                          tokens_used: int, response: str):
                """Record test results (simulated)"""
                self.results[name] = {
                    "prompt_length": prompt_length,
                    "tokens_used": tokens_used,
                    "response_length": len(response),
                    "cost": (tokens_used / 1000) * 0.002  # $0.002 per 1k tokens
                }

            def get_cheapest(self) -> str:
                """Return name of most cost-effective test"""
                if not self.results:
                    return None
                return min(self.results, key=lambda k: self.results[k]["cost"])

            def get_comparison(self) -> Dict:
                """Return comparison summary"""
                if not self.results:
                    return {}

                total_costs = [r["cost"] for r in self.results.values()]
                return {
                    "tests_run": len(self.results),
                    "cheapest": self.get_cheapest(),
                    "most_expensive": max(self.results, key=lambda k: self.results[k]["cost"]),
                    "total_cost": sum(total_costs),
                    "avg_cost": sum(total_costs) / len(total_costs)
                }

        # Simulate 3 different prompt tests
        tester = ABTester()

        # Prompt A: Simple (uses fewer tokens)
        tester.record_test("Simple", 50, 100, "Apple, Microsoft, Google")

        # Prompt B: Few-Shot (uses more tokens)
        tester.record_test("Few-Shot", 200, 250, '["Apple", "Microsoft", "Google"]')

        # Prompt C: Constrained (medium tokens)
        tester.record_test("Constrained", 150, 180, '{"companies": ["Apple", "Microsoft"]}')

        # Verify tracking
        assert len(tester.results) == 3, "Should track all 3 tests"
        assert "Simple" in tester.results, "Simple test missing"
        assert tester.results["Simple"]["tokens_used"] == 100
        assert tester.results["Few-Shot"]["tokens_used"] == 250

        # Verify cost calculation
        simple_cost = tester.results["Simple"]["cost"]
        expected_cost = (100 / 1000) * 0.002  # 0.0002
        assert abs(simple_cost - expected_cost) < 0.00001, "Cost calculation incorrect"

        # Verify comparison
        comparison = tester.get_comparison()
        assert comparison["tests_run"] == 3
        assert comparison["cheapest"] == "Simple", "Should identify cheapest prompt"
        assert comparison["most_expensive"] == "Few-Shot", "Should identify most expensive"

        print_test("A/B Tester Logic (Project 4)", True,
                  f"Tracked 3 prompts, identified cheapest: {comparison['cheapest']}")
        return True
    except Exception as e:
        print_test("A/B Tester Logic (Project 4)", False, str(e))
        return False

# --- Test 6: Prompt Validator (Project 5) ---
def test_prompt_validator():
    """Test Prompt Validator logic"""
    try:
        class PromptValidator:
            def __init__(self):
                self.issues = []

            def validate(self, prompt: str) -> Dict:
                """Run all validation checks and return report"""
                self.issues = []

                # Check 1: Too vague (no specific instructions)
                if not self._has_clear_instruction(prompt):
                    self.issues.append({
                        "severity": "high",
                        "issue": "No clear instruction found",
                        "suggestion": "Add explicit instruction verb"
                    })

                # Check 2: Missing format specification
                if not self._has_format_spec(prompt):
                    self.issues.append({
                        "severity": "medium",
                        "issue": "No output format specified",
                        "suggestion": "Specify format: JSON, bullet points, etc."
                    })

                # Check 3: Prompt too long (>3000 chars)
                if len(prompt) > 3000:
                    self.issues.append({
                        "severity": "medium",
                        "issue": "Prompt exceeds 3000 characters",
                        "suggestion": "Consider splitting into multiple prompts"
                    })

                # Check 4: Contains ambiguous terms
                ambiguous = ["good", "some", "a bit", "maybe", "probably"]
                if any(term in prompt.lower() for term in ambiguous):
                    self.issues.append({
                        "severity": "low",
                        "issue": "Contains ambiguous terms",
                        "suggestion": "Use specific, measurable language"
                    })

                return {
                    "is_valid": len([i for i in self.issues if i["severity"] == "high"]) == 0,
                    "issues": self.issues,
                    "score": self._calculate_score()
                }

            def _has_clear_instruction(self, prompt: str) -> bool:
                """Check if prompt contains action verbs"""
                action_verbs = ["extract", "summarize", "classify", "generate", "rewrite",
                              "identify", "list", "compare", "explain", "translate"]
                prompt_lower = prompt.lower()
                return any(verb in prompt_lower for verb in action_verbs)

            def _has_format_spec(self, prompt: str) -> bool:
                """Check if output format is specified"""
                format_keywords = ["json", "format:", "return as", "output:",
                                 "bullet points", "numbered list", "table"]
                prompt_lower = prompt.lower()
                return any(keyword in prompt_lower for keyword in format_keywords)

            def _calculate_score(self) -> int:
                """Calculate quality score (0-100)"""
                base_score = 100
                for issue in self.issues:
                    if issue["severity"] == "high":
                        base_score -= 30
                    elif issue["severity"] == "medium":
                        base_score -= 15
                    else:
                        base_score -= 5
                return max(0, base_score)

        validator = PromptValidator()

        # Test 1: Bad prompt (vague, no format)
        bad_prompt = "Tell me about the text"
        result_bad = validator.validate(bad_prompt)

        assert not result_bad["is_valid"], "Bad prompt should be invalid"
        assert result_bad["score"] < 70, "Bad prompt should have low score"
        assert len(result_bad["issues"]) >= 2, "Should identify multiple issues"

        # Test 2: Good prompt (clear instruction, format specified)
        good_prompt = """
        Extract all dates and amounts from the invoice text.
        Return the result as JSON with structure:
        {"dates": [...], "amounts": [...]}
        """
        result_good = validator.validate(good_prompt)

        assert result_good["is_valid"], "Good prompt should be valid"
        assert result_good["score"] >= 80, f"Good prompt should have high score (got {result_good['score']})"

        # Test 3: Medium prompt (has instruction but ambiguous language)
        medium_prompt = "Extract some good dates from the text maybe"
        result_medium = validator.validate(medium_prompt)

        assert result_medium["is_valid"], "Should be valid (no high severity issues)"
        issues_severities = [i["severity"] for i in result_medium["issues"]]
        assert "low" in issues_severities or "medium" in issues_severities

        print_test("Prompt Validator (Project 5)", True,
                  f"Bad: {result_bad['score']}, Good: {result_good['score']}, Medium: {result_medium['score']}")
        return True
    except Exception as e:
        print_test("Prompt Validator (Project 5)", False, str(e))
        return False

def main():
    print(f"\n{Colors.BOLD}Chapter 9 Verification{Colors.RESET}")
    print("="*60)

    tests = [
        test_template_substitution,
        test_json_escaping,
        test_missing_variable_behavior,
        test_few_shot_builder,
        test_ab_tester_logic,
        test_prompt_validator
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
        print(f"\n{Colors.GREEN}✅ All Chapter 9 tests passed!{Colors.RESET}")
    else:
        print(f"\n{Colors.RED}⚠️ Some tests failed.{Colors.RESET}")

if __name__ == "__main__":
    main()
