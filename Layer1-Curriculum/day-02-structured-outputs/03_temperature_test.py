import os
from dotenv import load_dotenv
from openai import OpenAI

# ── IMPLEMENTATION ORDER ──────────────────────────────────────────────────────
# TODO 1: Initialize the OpenAI client
# TODO 2: Create a function that runs the same prompt at a specific temperature
# TODO 3: Test with temperature 0.0
# TODO 4: Test with temperature 1.0
# Build in order. Run after each section before moving to the next.

# ── WHAT BROKEN LOOKS LIKE ────────────────────────────────────────────────────
# If TEMPERATURE behaves weirdly:
#   Error: Unpredictable output formatting despite strict prompt.
#   Diagnosis: High temperature (1.0) overrides formatting hints for creative choices.
#   Fix: Lower the temperature to 0.0 or 0.2 for strict JSON or formatting tasks.

def test_temperature(client, temp):
    # TODO 2: Write a creative prompt (e.g., "Write a haiku about a robot mechanic")
    # and pass the temperature parameter to the API call.
    #
    # WHY: Temperature dictates how greedy the next-token prediction is.
    # 0.0 = always picks the most likely next token (deterministic, great for code).
    # 1.0 = occasionally picks less likely tokens (creative, great for poetry).
    
    # PATTERN: client.chat.completions.create(..., temperature=temp)
    pass

if __name__ == "__main__":
    # Test your temperatures here!
    pass
