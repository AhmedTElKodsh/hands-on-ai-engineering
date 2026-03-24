import os
from dotenv import load_dotenv
from openai import OpenAI

# ── IMPLEMENTATION ORDER ──────────────────────────────────────────────────────
# TODO 1: Setup and initialization
# TODO 2: Implement zero-shot sentiment classification
# TODO 3: Implement few-shot entity extraction
# TODO 4: Implement Chain-of-Thought (CoT) reasoning
# TODO 5: Implement System Role styling
# TODO 6: Implement Prompt Chaining
# Build in order. Run after each section before moving to the next.

# ── WHAT BROKEN LOOKS LIKE ────────────────────────────────────────────────────
# If FEW-SHOT fails:
#   The model might copy the example literally instead of using it as a template.
#   Fix: Clearly separate examples using generic delimiters like "---" or "Example 1".

def run_zero_shot(client):
    # TODO 2: Implement zero-shot sentiment classification.
    #
    # WHY: Zero-shot relies purely on the model's pre-training to understand the task
    # without any examples. It's fast and easy for simple tasks.
    #
    # PATTERN: "Classify this movie review as positive or negative: {review}"
    # EXPECTED: Just the word "Positive" or "Negative"
    print("\n--- Zero-Shot Classification ---")
    pass

def run_few_shot(client):
    # TODO 3: Implement few-shot entity extraction.
    #
    # WHY: When the task is complex or requires a specific output format, providing
    # 2-3 examples in the prompt dramatically improves accuracy.
    #
    # PATTERN: 
    # Example 1: "User: John is from NY. Extract: Name: John, City: NY"
    # Example 2: "User: Sarah lives in London. Extract: Name: Sarah, City: London"
    # Target: "User: Mike works in Tokyo. Extract: "
    print("\n--- Few-Shot Extraction ---")
    pass

def run_chain_of_thought(client):
    # TODO 4: Implement Chain-of-Thought (CoT) reasoning.
    #
    # WHY: For math or logic, forcing the model to explain its steps prevents it
    # from jumping to the wrong conclusion.
    #
    # PATTERN: "Solve this math problem. Let's think step by step: {problem}"
    print("\n--- Chain-of-Thought Reasoning ---")
    pass

def run_system_role(client):
    # TODO 5: Implement System Role Persona.
    #
    # WHY: The system prompt dictates the behavior, tone, and constraints of the agent.
    # It acts as the "source code" for the AI's identity.
    #
    # PATTERN: 
    # messages=[{"role": "system", "content": "You are a strict math teacher..."},
    #           {"role": "user", "content": "What is 2+2?"}]
    print("\n--- System Role Persona ---")
    pass

def run_prompt_chaining(client):
    # TODO 6: Implement Prompt Chaining.
    #
    # WHY: Decomposing a complex task into multiple interconnected prompts reduces
    # hallucination and makes debugging easier. Output of Prompt 1 -> Input of Prompt 2.
    #
    # PATTERN:
    # prompt_1 = "Extract the main subject from this text: {text}"
    # subject = client.chat.completions...
    # prompt_2 = f"Write a poem about {subject}"
    print("\n--- Prompt Chaining ---")
    pass

if __name__ == "__main__":
    # TODO 1: Initialize the client and run the patterns
    # load_dotenv()
    # client = OpenAI()
    pass
