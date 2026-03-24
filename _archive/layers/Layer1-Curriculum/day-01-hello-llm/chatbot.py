"""
Stage 2 — CLI Chatbot
======================
Goal: a proper multi-turn chatbot that runs in the terminal.

Features to build (in this order):
  1. Conversation loop  — keep chatting until user types "quit"
  2. Message history    — AI remembers what was said earlier
  3. System prompt      — give your bot a personality
  4. Streaming          — print tokens as they arrive, not all at once

IMPORTANT — How to approach this file:
  This file uses "productive failure" for the conversation memory concept.
  That means: you'll be given a GOAL first, asked to TRY it yourself, and
  you WILL probably get it wrong. That's the point. The failure teaches you
  more than the explanation. Read the CHALLENGE section in main() BEFORE
  reading the CONCEPT section.

  Streaming (TODO 5) has detailed scaffolding because the chunk API is
  genuinely non-obvious and you'd waste time on API trivia, not learning.

Run with: python chatbot.py
"""

# TODO 1: Imports — you'll need: OpenAI client, dotenv loader, os, sys

# TODO 2: Load environment variables


# TODO 3: Create the OpenAI client


# ── SYSTEM PROMPT ────────────────────────────────────────────────────────────
# TODO 4: Define a SYSTEM_PROMPT string that gives your chatbot a personality.
#         Keep it focused. Example: "You are a concise coding assistant.
#         You explain things simply and always give short examples."
#         Make it your own — this is YOUR chatbot.
#
# NOTE: This prompt is duplicated in app.py. Yes, this is duplication, and we'll
# fix it later. For now, just copy it when you get to Stage 3.

SYSTEM_PROMPT = ""  # replace with your prompt


# ── HELPER: stream one assistant response ────────────────────────────────────
def stream_response(messages: list) -> tuple[str, dict]:
    """
    Send messages to the API with streaming enabled.
    Print each token chunk as it arrives.
    Return the full assembled response string AND usage statistics.

    NOTE: Type hint changed from list[dict] to list for Python 3.9 compatibility.
    If you're on Python 3.10+, you can use list[dict] instead.

    STREAMING CONCEPT (understand this before coding):
    ─────────────────────────────────────────────────
    When stream=True, the API returns chunks one at a time instead of waiting
    for the complete response. Think of it like a faucet dripping water drops
    vs filling a bucket then pouring it all at once.

    Each chunk is a partial response object. Most chunks have delta.content
    (the new text token), but some chunks are metadata-only (no content).
    You MUST check if delta.content is not None before using it.

    Pattern you'll implement:
      for chunk in response:
          if chunk.choices[0].delta.content is not None:
              text = chunk.choices[0].delta.content
              print(text, end="", flush=True)  # end="" prevents newlines, flush=True shows immediately
              full_response += text

    TOKEN COUNTING (new in this version):
    ────────────────────────────────────
    When streaming, usage statistics come in the LAST chunk. You need to check
    for chunk.usage and save it. This tells you how many tokens were used.

    TODO 5: Implement this function using the Dead Code Scaffold below.
    Uncomment the scaffold, fill in the blanks, then implement steps b–f.

    STEP a) — Complete the API call by filling in each ___________:

      response = client.chat.completions.create(
          model=___________,
          # WHY model: selects the AI model. "gpt-4o-mini" = cheap + fast = perfect for learning.

          messages=___________,
          # WHY messages: the full conversation history so far. The API is stateless —
          # sending the whole list is how the AI "remembers" previous turns.
          # This is the messages parameter passed into THIS function.

          stream=___________,
          # WHY stream=True: instead of waiting for the full response, the API sends
          # tokens one at a time as they're generated. Like a faucet dripping, not a bucket pour.
          # Set this to the boolean value that enables streaming.

          stream_options=___________,
          # WHY stream_options: by default, streaming doesn't include token usage stats.
          # This option tells the API to include usage in the final chunk.
          # Value: {"include_usage": True}
      )

    STEP b) Create an empty string: full_response = ""
    STEP c) Create: usage_stats = None
    STEP d) Iterate over the stream — each item is a chunk:
            - Access delta content: chunk.choices[0].delta.content
            - If it's not None: print it (end="", flush=True) and append to full_response
              WHY end="": prevents a newline after each token (they all flow on one line)
              WHY flush=True: forces the terminal to display immediately, not buffer
            - Check: if chunk.usage is not None → save it: usage_stats = chunk.usage
              WHY: usage only appears in the LAST chunk, all others have None
    STEP e) After the loop: print("") — adds a clean newline after streaming finishes
    STEP f) Return the tuple: return (full_response, usage_stats)
    """
    # your code here
    pass


# ── CHECKPOINT: STREAMING ──────────────────────────────────────────────────────
# Before moving to main(), explain to yourself (out loud):
#
# 1. Why does delta.content need a None check? What are those None chunks for?
# 2. What would the user experience be if you removed flush=True?
# 3. Why do you need to accumulate full_response inside the loop — can't you
#    just get the full text from the response object after the loop?
# 4. Why does usage only appear in the LAST chunk?
#
# If any answer is fuzzy, re-read the STREAMING CONCEPT docstring above.
# ───────────────────────────────────────────────────────────────────────────────


# ── MAIN LOOP ─────────────────────────────────────────────────────────────────
def main():
    """
    TODO 6: Build the conversation loop.

    ── CHALLENGE: Build it yourself BEFORE reading the step-by-step ────────────
    Your goal: build a working conversation loop where the AI remembers your
    name after 3 turns, streams responses, and tracks token usage.

    You already know the pieces:
      - The API call pattern (from hello.py)
      - How stream_response() works (you just built it above)
      - That the API is stateless (you saw this in the concepts notebook)
      - How to get user input with input()
      - How to loop with while True

    The challenge is NOT "discover statelessness" — you already know about it.
    The challenge is: can you ASSEMBLE all the pieces into a working program
    without step-by-step instructions? Structure the code yourself. Decide
    what to initialize, what order to do things in, how to handle the loop.

    Build it now. Don't read past this section. Test with:
      1. Tell it: "My name is Ahmed"
      2. Ask: "What's 2+2?"
      3. Ask: "What's my name?"

    If step 3 fails, diagnose WHY — then read the CONCEPT section below.
    If it works, read the CONCEPT section anyway to confirm your mental model.
    Then compare your structure to the step-by-step in "NOW BUILD IT PROPERLY".
    Where did your approach differ? Which is better?
    ──────────────────────────────────────────────────────────────────────────


    ── CONCEPT: Why It Broke (read AFTER attempting the challenge) ────────────
    The API is STATELESS. That word is worth sitting with. The server does not
    store anything between your calls. Every time you call it, it starts fresh.

    If you only sent the LAST message ("What's my name?"), the API has no idea
    you ever told it your name. It received one message with zero context.

    The fix: you keep the ENTIRE conversation in a Python list and re-send it
    every time. This is the "messages" list.

    After each turn, your messages list evolves like this:

    Turn 0 (initialization):
      [
        {"role": "system", "content": SYSTEM_PROMPT}
      ]

    Turn 1 (user says "Hello"):
      [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "Hello"}              ← append BEFORE calling API
      ]
      API responds: "Hi! How can I help?"
      [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi! How can I help?"}  ← append AFTER response
      ]

    Turn 2 (user says "What's 2+2?"):
      [system, user: Hello, assistant: Hi!, user: What's 2+2?]  ← append user
      API responds → append assistant: "2+2 equals 4."

    The list grows by 2 every turn. Cost grows proportionally.
    This is why long conversations cost more — you pay for the full history each call.
    ──────────────────────────────────────────────────────────────────────────


    ── NOW BUILD IT PROPERLY ─────────────────────────────────────────────────
    Steps (now that you understand WHY):

      a) Initialise the messages list with the system message:
           [{"role": "system", "content": SYSTEM_PROMPT}]

      b) Print a welcome banner (anything you like)

      c) Create a variable to track total tokens used: total_tokens = 0

      d) Loop forever:
           - Prompt the user for input: input("You: ").strip()
           - If input is empty, continue (skip blank lines)
           - If input is "quit" or "exit", break the loop (we'll print stats after)
           - Append the user message to messages:
               {"role": "user", "content": user_input}
           - Print "Assistant: " (end="", flush=True) — no newline yet,
             streaming will follow immediately
           - Call stream_response(messages) and unpack BOTH return values:
               assistant_reply, usage_stats = stream_response(messages)
           - Append the assistant reply to messages:
               {"role": "assistant", "content": assistant_reply}
           - TODO 7: Track token usage
               If usage_stats is not None:
                   total_tokens += usage_stats.total_tokens
                   # Optional: print token count for this turn
                   # print(f"\n[Tokens this turn: {usage_stats.total_tokens}]")

      e) After the loop breaks (user typed "quit"), print session statistics:
           - Total turns (hint: (len(messages) - 1) // 2, excluding system message)
           - Total tokens used
           - Estimated cost (gpt-4o-mini pricing as of Feb 2025: $0.15 per 1M input tokens, $0.60 per 1M output tokens)
             For simplicity, use average: $0.375 per 1M tokens, or $0.000000375 per token
             cost = total_tokens * 0.000000375
           - Print: f"Session stats: {num_turns} turns, {total_tokens} tokens, ~${cost:.4f}"

      f) Add a try/except KeyboardInterrupt around the loop so Ctrl+C
         exits cleanly and still prints stats
    """
    # your code here
    pass


# ── CHECKPOINT: MEMORY ─────────────────────────────────────────────────────────
# Before moving to the SELF-CHECK tests, explain to yourself (out loud):
#
# 1. Why does the messages list grow by 2 every turn?
# 2. What would happen if you appended the user message but NOT the assistant reply?
# 3. What would happen if you appended the assistant reply BEFORE calling the API?
# 4. On turn 10, roughly how many messages are in the list? How does this affect cost?
#
# If you attempted the CHALLENGE section and experienced the failure yourself,
# these questions should be easy. If you skipped the challenge and went straight
# to the concept — go back and try it. The failure is the lesson.
# ───────────────────────────────────────────────────────────────────────────────


if __name__ == "__main__":
    main()


# ── SELF-CHECK ────────────────────────────────────────────────────────────────
# After your chatbot works, test these scenarios and note results in your logbook:
#
# EXPECTED OUTPUT when everything works:
# ─────────────────────────────────────
#   You: Tell me a joke
#   Assistant: Why did the chicken cross the road? To get to the other side!
#   (Words appear progressively: "Why" ... "did" ... "the" ... "chicken" ...)
#
#   You: What did I just ask you?
#   Assistant: You asked me to tell you a joke.
#   (This proves memory is working — the AI remembers the previous turn)
#
#   You: quit
#   Session stats: 2 turns, 156 tokens, ~$0.0001
#   (This proves token counting is working)
#
# EXPECTED OUTPUT when streaming is BROKEN:
# ─────────────────────────────────────────
#   You: Tell me a joke
#   Assistant: (long pause of 2-3 seconds, then all text appears at once)
#   Why did the chicken cross the road? To get to the other side!
#   (If you see this, you're not printing inside the chunk loop)
#
# EXPECTED OUTPUT when memory is BROKEN:
# ──────────────────────────────────────
#   You: My name is Ahmed
#   Assistant: Nice to meet you, Ahmed!
#   You: What's my name?
#   Assistant: I don't have that information.
#   (If you see this, you're not appending messages correctly)
#
# EXPECTED OUTPUT when token counting is BROKEN:
# ──────────────────────────────────────────────
#   You: quit
#   Session stats: 2 turns, 0 tokens, ~$0.0000
#   (If total_tokens is 0, you're not capturing usage_stats from the last chunk)
#
# Test 1 — Memory check
#   You:       "My name is Ahmed and I'm learning AI engineering."
#   You:       "What's my name and what am I studying?"
#   Expected:  AI recalls both facts correctly.
#   If it fails: check that you're appending BOTH user AND assistant turns to messages
#
# Test 2 — Streaming check
#   Ask a long question like "Explain recursion in 5 sentences."
#   Expected:  Words appear progressively, not all at once.
#   If it fails: check that you're printing inside the chunk loop, not after
#
# Test 3 — Personality check
#   Ask something off-topic for your system prompt persona.
#   Does the bot stay in character?
#
# Test 4 — Long conversation cost observation
#   Chat for 10 turns. Note the token count after each turn (if you print it).
#   Observation: Token count grows with each turn because you're re-sending the entire history.
#   After 10 turns, type "quit" and see the total cost.
#   Question: If you had a 100-turn conversation, how much would it cost?
#   (Hint: token count grows linearly, so cost grows linearly too)
