"""
OPTIONAL EXPLORATION — OpenAI vs Anthropic API Comparison
===========================================================
Goal: Send the same prompt to both OpenAI and Anthropic, compare responses.
Time: 30-45 minutes (optional — only if you have time and curiosity)

This is NOT required for Day 1 completion, but it will help you answer the
logbook question: "How would you switch this to Anthropic's Claude API? What would change?"

Prerequisites:
  - You've completed hello.py and chatbot.py
  - You have an Anthropic API key (get one free at console.anthropic.com)
  - Add ANTHROPIC_API_KEY=your-key-here to your .env file
  - Install: pip install anthropic

Key Differences You'll Discover:
  1. Import: OpenAI uses `from openai import OpenAI`, Anthropic uses `from anthropic import Anthropic`
  2. Client init: Both use api_key from environment
  3. System prompt: OpenAI puts it in messages list, Anthropic has a separate `system` parameter
  4. Model names: OpenAI uses "gpt-4o-mini", Anthropic uses "claude-3-5-sonnet-20241022" (or similar)
  5. Response format: Both use choices[0] but field names differ slightly
  6. Streaming: Both support it, but chunk structure differs

Run with: python compare_apis.py
"""

# TODO 1: Imports
#   from openai import OpenAI
#   from anthropic import Anthropic
#   from dotenv import load_dotenv
#   import os


# TODO 2: Load environment variables


# TODO 3: Create both clients
#   openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
#   anthropic_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


# ── TEST PROMPT ───────────────────────────────────────────────────────────────
TEST_PROMPT = "Explain what a Large Language Model is in exactly 2 sentences."
SYSTEM_PROMPT = "You are a helpful AI assistant who explains technical concepts clearly and concisely."


# ── OPENAI CALL ───────────────────────────────────────────────────────────────
def call_openai(prompt: str) -> str:
    """
    TODO 4: Call OpenAI's API (non-streaming for simplicity)

    Steps:
      a) Call openai_client.chat.completions.create() with:
           - model="gpt-4o-mini"
           - messages=[
               {"role": "system", "content": SYSTEM_PROMPT},
               {"role": "user", "content": prompt}
             ]
      b) Extract and return: response.choices[0].message.content
    """
    # your code here
    pass


# ── ANTHROPIC CALL ────────────────────────────────────────────────────────────
def call_anthropic(prompt: str) -> str:
    """
    TODO 5: Call Anthropic's API (non-streaming for simplicity)

    Steps:
      a) Call anthropic_client.messages.create() with:
           - model="claude-3-5-sonnet-20241022"  (or latest model from docs)
           - max_tokens=1024  ← REQUIRED for Anthropic (OpenAI infers this)
           - system=SYSTEM_PROMPT  ← NOTE: separate parameter, not in messages!
           - messages=[
               {"role": "user", "content": prompt}
             ]
      b) Extract and return: response.content[0].text
         NOTE: Anthropic's response structure is different!
         OpenAI: response.choices[0].message.content
         Anthropic: response.content[0].text
    """
    # your code here
    pass


# ── MAIN COMPARISON ───────────────────────────────────────────────────────────
def main():
    """
    TODO 6: Call both APIs and compare results

    Steps:
      a) Print the test prompt
      b) Call call_openai(TEST_PROMPT) and print the result with a label
      c) Call call_anthropic(TEST_PROMPT) and print the result with a label
      d) Print a separator and ask yourself:
           - Which response do you prefer? Why?
           - Are they similar or different in style?
           - Which API was faster? (you can time them with time.time())
    """
    print("=" * 70)
    print("PROMPT:")
    print(TEST_PROMPT)
    print("=" * 70)

    # your code here
    pass


if __name__ == "__main__":
    main()


# ── REFLECTION QUESTIONS ──────────────────────────────────────────────────────
# After running this, answer these in your logbook:
#
# 1. What are the 3 biggest API differences between OpenAI and Anthropic?
#    (Hint: system prompt location, max_tokens requirement, response structure)
#
# 2. If you had to convert chatbot.py to use Claude instead of GPT, what would you change?
#    (Hint: client init, model name, system prompt handling, response extraction)
#
# 3. Which model gave a better response for this specific prompt? Why?
#
# 4. How would you build a "multi-provider chatbot" that can switch between
#    OpenAI and Anthropic based on user preference?
#    (Hint: create a unified interface that abstracts the differences)
#
# 5. Cost comparison: Look up current pricing for gpt-4o-mini vs claude-3-5-sonnet.
#    Which is cheaper per million tokens? By how much?
#    (As of Feb 2025: gpt-4o-mini is ~$0.15/$0.60 per 1M tokens input/output,
#     claude-3-5-sonnet is ~$3/$15 per 1M tokens — 20x more expensive but more capable)

