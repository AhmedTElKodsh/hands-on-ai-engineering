"""
Stage 1 — First Wrench Turn
============================
Goal: send ONE message to the LLM and print the response.
Target time: 15 minutes.

Your job: fill in every TODO. Do NOT copy-paste from tutorials.
Type every character. Muscle memory matters.

► Read 00_concepts.ipynb FIRST — it teaches every SDK call you need here.
  Hints for each TODO are in that notebook (collapsed — open only when stuck).

Run with: python hello.py

NOTE: This script requires Python 3.10 or higher.
"""

import sys

# Python version check — prevents confusing errors on older versions
if sys.version_info < (3, 10):
    print("ERROR: This script requires Python 3.10 or higher.")
    print(f"You are running Python {sys.version_info.major}.{sys.version_info.minor}")
    print("Please upgrade Python and try again.")
    sys.exit(1)

# TODO 1: Import the OpenAI client class from the openai library
# ► Stuck? See 00_concepts.ipynb → Section 0, Hint TODO 1
from openai import ___________

# TODO 2: Import load_dotenv from dotenv, and os from the standard library
# ► Stuck? See 00_concepts.ipynb → Section 0, Hint TODO 2

# TODO 3: Call load_dotenv() so your .env file is loaded into environment variables

# TODO 4: Create an OpenAI client instance
# ► Stuck? See 00_concepts.ipynb → Section 0, Hint TODO 4

# TODO 5: Call the API and store the result in a variable called "response"
#         Use model="gpt-4o-mini" and a user message asking for a hello + Python fact.
# ► Stuck? See 00_concepts.ipynb → Section 3, Hint TODO 5
#
# response = client.chat.completions.create(
#     model=___________,
#     messages=___________,
# )

# TODO 6: Extract the text from response and print it
#         The response object tree: response → .choices → [0] → .message → .content
# ► Stuck? See 00_concepts.ipynb → Section 4, Hint TODO 6

# TODO 7: Print token usage and estimated cost.
#
# Fields: response.usage.prompt_tokens / .completion_tokens / .total_tokens
# Prices: gpt-4o-mini input=$0.15/M tokens, output=$0.60/M tokens
#         (verify at platform.openai.com/docs/pricing — prices change)
#
# ► Stuck? See 00_concepts.ipynb → Section 5, Hint TODO 7

# -----------------------------------------------------------------------
# EXPECTED OUTPUT when this works:
#   Hello! Here's an interesting fact about Python: Python was named after
#   the British comedy series "Monty Python's Flying Circus," not the snake!
#
#   Tokens used — prompt: 21, completion: 34, total: 55
#   Estimated cost: $0.000024
#
#   ──────────────────────────────────────────────────────────────
#   ✓ Your code just communicated with one of the most advanced
#     AI systems ever built. That is the foundation of everything
#     you will build in the next 39 days.
#   ──────────────────────────────────────────────────────────────
# -----------------------------------------------------------------------

# TODO 8: Print the success banner below AFTER printing the response and usage.
#         Copy this exactly — it fires only when your code works.
#
# print("\n" + "─" * 62)
# print("✓ Your code just communicated with one of the most advanced")
# print("  AI systems ever built. That is the foundation of everything")
# print("  you will build in the next 39 days.")
# print("─" * 62 + "\n")

# -----------------------------------------------------------------------
# Once it works, answer these questions in comments below:
#
# Q: What type is response.choices? (hint: print(type(response.choices)))
#
# Q: What other fields does response have besides choices?
#    (hint: print(response.model_dump().keys()))
#
# Q: This request cost roughly $0.000024. How much would 1000 identical
#    requests cost? How many could you run for $1?
# -----------------------------------------------------------------------
