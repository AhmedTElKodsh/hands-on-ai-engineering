"""
Stage 3 — Streamlit Chat UI
=============================
Goal: wrap your chatbot in a web interface.

Streamlit concepts you need:
  - st.session_state       — persists data across reruns (like a global variable
                             that survives the page refreshing)
  - st.chat_message(role)  — renders a chat bubble. role = "user" or "assistant"
                             use as a context manager: with st.chat_message("user"):
  - st.chat_input(prompt)  — renders the input box at the bottom of the page.
                             Returns the submitted string, or None if not submitted yet.
  - st.markdown(text)      — renders text inside a chat bubble
  - st.write_stream(gen)   — renders a streaming generator token-by-token
                             (alternative to manual streaming)

STREAMLIT EXECUTION MODEL (CRITICAL TO UNDERSTAND):
═══════════════════════════════════════════════════
Every time the user submits input, Streamlit RERUNS THIS ENTIRE FILE from top to bottom.

Think of it like this:
  User types "Hello" and hits Enter → Python runs app.py from line 1 to the end
  User types "How are you?" → Python runs app.py AGAIN from line 1 to the end
  User types "Goodbye" → Python runs app.py AGAIN from line 1 to the end

This means:
  ❌ BAD:  messages = []  ← This resets to empty list on every rerun! Chat history lost!
  ✅ GOOD: st.session_state.messages  ← This PERSISTS across reruns. Chat history saved!

How session_state works:
  First run:  st.session_state is empty → you initialize it with messages = [system_msg]
  Second run: st.session_state already has messages → you keep using the existing list
  Third run:  st.session_state still has messages → history keeps growing

This is how chat history persists even though the script reruns every time.

Pattern you'll use:
  if "messages" not in st.session_state:
      st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
  # Now st.session_state.messages exists and persists across reruns

Run with: streamlit run app.py
"""

# TODO 1: Imports — streamlit as st, openai, dotenv, os

# TODO 2: Load environment variables and create OpenAI client

# TODO 3: Page config (optional but professional)
#         st.set_page_config(page_title="...", page_icon="🤖")
#         NOTE: Parameter is page_title, not title


# ── SYSTEM PROMPT ─────────────────────────────────────────────────────────────
# TODO 4: Define your SYSTEM_PROMPT (can be the same as chatbot.py or different)
#
# NOTE: Yes, this is duplicated from chatbot.py. You'll learn to avoid this
# pattern later. For now, just copy your system prompt from chatbot.py and paste
# it here.

SYSTEM_PROMPT = ""  # replace with your prompt


# ── SESSION STATE INITIALISATION ─────────────────────────────────────────────
# TODO 5: Initialise st.session_state.messages if it doesn't exist yet.
#
#   Pattern:
#     if "messages" not in st.session_state:
#         st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
#
#   Why: on the FIRST run, session_state is empty. On every subsequent run
#   (after each user input), it already has the conversation history.


# ── RENDER EXISTING MESSAGES ─────────────────────────────────────────────────
# TODO 6: Loop through st.session_state.messages and render each one.
#
#   Skip the system message (role == "system") — users don't need to see it.
#   For each user/assistant message:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])


# ── HANDLE NEW INPUT ──────────────────────────────────────────────────────────
# TODO 7: Get new user input and generate a response.
#
#   Steps:
#   a) prompt = st.chat_input("Ask me anything...")
#      If prompt is None (user hasn't submitted anything), stop here — do nothing.
#
#   b) Append the user message to session_state.messages
#
#   c) Display the user message immediately:
#        with st.chat_message("user"):
#            st.markdown(prompt)
#
#   d) Call the API with streaming and display the response:
#        with st.chat_message("assistant"):
#            response = client.chat.completions.create(
#                model="gpt-4o-mini",
#                messages=st.session_state.messages,
#                stream=True,
#            )
#            # Option A — manual streaming (like chatbot.py):
#            #   full = ""
#            #   placeholder = st.empty()
#            #   for chunk in response:
#            #       delta = chunk.choices[0].delta.content or ""
#            #       full += delta
#            #       placeholder.markdown(full + "▌")   # ▌ = typing cursor
#            #   placeholder.markdown(full)
#            #
#            # Option B — use st.write_stream() (simpler):
#            #   full = st.write_stream(
#            #       chunk.choices[0].delta.content or ""
#            #       for chunk in response
#            #   )
#            #   NOTE: Option B requires Streamlit >= 1.33. If full comes back as None,
#            #   use Option A instead.
#
#   e) Append the assistant reply to session_state.messages:
#        {"role": "assistant", "content": full}


# ── CHECKPOINT: STREAMLIT RERUN MODEL ──────────────────────────────────────────
# Before continuing, explain to yourself (out loud):
#
# 1. Why does `messages = []` break the chat, but `st.session_state.messages`
#    does not? What happens on each rerun?
# 2. Why do you need the `if "messages" not in st.session_state` guard?
#    What would happen if you always reset it to [system_msg]?
# 3. Why must you render ALL existing messages (the for loop in TODO 6)
#    on every rerun — not just the new message?
#
# If you can answer all three, you understand Streamlit's execution model.
# If not, re-read the EXECUTION MODEL section at the top of this file.
# ──────────────────────────────────────────────────────────────────────────────

# ── SIDEBAR (stretch goal) ────────────────────────────────────────────────────
# TODO 8 (optional): Add a sidebar showing conversation stats.
#
#   with st.sidebar:
#       st.header("Session Stats")
#       num_turns = (len(st.session_state.messages) - 1) // 2  # exclude system msg
#       st.metric("Turns", num_turns)
#       if st.button("Clear conversation"):
#           st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
#           st.rerun()


# ── SELF-CHECK ────────────────────────────────────────────────────────────────
# After your UI works, verify:
#
# EXPECTED BEHAVIOR when everything works:
# ───────────────────────────────────────
# 1. You type "Hello" → message appears in chat → AI responds → both messages stay visible
# 2. You type "What did I just say?" → AI responds "You said hello" (memory works!)
# 3. You refresh the page (F5) → chat history disappears (session_state resets)
# 4. Streaming: AI response appears word-by-word, not all at once
# 5. User messages appear on one side, assistant on the other (Streamlit default styling)
#
# EXPECTED BEHAVIOR when session_state is BROKEN:
# ───────────────────────────────────────────────
# 1. You type "Hello" → AI responds
# 2. You type "What did I just say?" → AI responds "I don't have that information"
# 3. Only the LAST message pair is visible (previous messages disappeared)
# → This means you're not using st.session_state correctly
#
# EXPECTED BEHAVIOR when streaming is BROKEN:
# ───────────────────────────────────────────
# 1. You type "Tell me a story" → (long pause) → entire response appears at once
# → This means you're not using stream=True or not displaying chunks progressively
#
# Checklist:
# 1. Chat history persists across multiple messages (reload page to reset)
# 2. Streaming shows tokens appearing progressively in the bubble
# 3. User messages appear on the right, assistant on the left (Streamlit default)
# 4. Sending an empty message does nothing (st.chat_input handles this)
# 5. The typing cursor ▌ disappears when the response is complete
#
# Stretch: Can you figure out how to add a "Copy to clipboard" button
# below each assistant message? (hint: st.button + st.code)
