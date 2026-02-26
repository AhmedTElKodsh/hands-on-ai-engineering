# Day 1 — Hello LLM: Your First AI Conversation

**Mini-Project 1 | ~4 hours | Difficulty: ⭐**

## The Mechanic's Analogy

You're about to start a car for the first time.

You don't need to understand the combustion cycle, the transmission, or the fuel injection system. You need to know: key goes in ignition, turn it, press the gas pedal. The car moves. That's the loop.

Today you're learning the equivalent for Large Language Models. You'll send text in, get text back. You'll see it work. Then we'll add one piece at a time: conversation memory, streaming responses, a web interface.

By the end of today, you'll have a working chatbot. Not a toy — a real tool you can use and modify.

## Prime the Pump: What You Need to Know

Before you write any code, understand this:

**LLMs are next-token predictors.** You give them a sequence of text (a "prompt"), and they predict what comes next, one token at a time. A token is roughly a word or part of a word.

**The API is stateless.** The model doesn't remember your last conversation. Every time you call it, you send the ENTIRE conversation history. This is why "memory" costs money — you're paying to re-send everything every time.

**Three message roles matter:**

- `system` — sets the AI's behavior/personality (goes first, once)
- `user` — your input
- `assistant` — the AI's response

That's it. Everything you build today is just managing a list of these messages and sending them to the API.

## What You're Building

By end of day you'll have **three things running**:

1. `hello.py` — 5-line proof-of-life: your code talks to an LLM
2. `chatbot.py` — CLI chatbot with conversation history, system prompt, and streaming
3. `app.py` — Streamlit web UI wrapping your chatbot

## Project Structure

```
day-01-hello-llm/
├── README.md           ← you are here
├── .env.example        ← copy to .env and fill in your key
├── .gitignore          ← already set up — never commit .env
├── requirements.txt    ← pinned dependencies
├── hello.py            ← Stage 1: first wrench turn
├── chatbot.py          ← Stage 2: CLI chatbot (with token counting!)
├── app.py              ← Stage 3: Streamlit UI
└── compare_apis.py     ← Optional: OpenAI vs Anthropic comparison
```

## Setup (Do This First — 15 min)

### Step 1: Get Your OpenAI API Key

1. Go to [platform.openai.com](https://platform.openai.com)
2. Sign up or log in
3. Add billing information (required — you'll need a credit card, but Day 1 costs < $0.10)
4. Navigate to **API Keys** in the left sidebar
5. Click **Create new secret key**
6. Copy the key immediately (you won't see it again)

### Step 2: Set Up Your Environment

#### Modern Approach with `uv` (Recommended)

We'll use `uv` — a modern Python package manager that's 10-100x faster than `pip` with better dependency resolution. It's built in Rust and designed for the current Python ecosystem.

**Why `uv`?**

- 10-100x faster dependency resolution and installation
- Better conflict detection and resolution
- Modern design for current Python workflows
- Single binary installation (no Python required)

```bash
# 1. Verify your Python version (must be 3.10 or higher)
python --version

# 2. Install uv (one-time setup)
# Windows (PowerShell):
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Mac/Linux:
curl -LsSf https://astral.sh/uv/install.sh | sh

# 3. Create environment and install dependencies
uv venv
uv pip install -r requirements.txt

# 4. Activate the virtual environment
# Windows:
.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate

# 5. Copy .env.example to .env and add your OpenAI API key
cp .env.example .env
# Edit .env and replace "your-key-here" with your actual key from Step 1

# 6. Verify setup
python -c "import openai; print('openai OK')"
python -c "import streamlit; print('streamlit OK')"
```

---

#### Traditional Approach (For Reference)

The older `venv + pip` workflow still works but is significantly slower:

```bash
# 1. Verify your Python version (must be 3.10 or higher)
python --version

# 2. Create and activate virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Copy .env.example to .env and add your OpenAI API key
cp .env.example .env
# Edit .env and replace "your-key-here" with your actual key from Step 1

# 5. Verify setup
python -c "import openai; print('openai OK')"
python -c "import streamlit; print('streamlit OK')"
```

Use this if you're in an environment where `uv` isn't available or if you need compatibility with legacy tooling.

### Common Setup Errors

**`AuthenticationError: Invalid API key`**
→ Check your `.env` file. Make sure you copied the full key and removed `your-key-here`.

**`RateLimitError: You exceeded your current quota`**
→ You've hit your free tier limit. Add billing at platform.openai.com/account/billing.

**`ImportError: No module named 'openai'`**
→ Your virtual environment isn't activated, or installation failed.

- With `uv`: Make sure `.venv\Scripts\activate` (Windows) or `source .venv/bin/activate` (Mac/Linux) ran successfully
- Try: `uv pip install --upgrade pip` then re-run `uv pip install -r requirements.txt`
- With traditional: Try `pip install --upgrade pip` then re-run `pip install -r requirements.txt`

**`TypeError: 'type' object is not subscriptable` (on `list[dict]`)**
→ You're using Python 3.8 or older. Upgrade to Python 3.10+.

**`uv: command not found`**
→ `uv` isn't installed or not in your PATH. Re-run the installation command or use the traditional `venv + pip` approach above.

## Build Order

**Stage 1 — hello.py** (aim for 15 minutes)
Get a response from the LLM. That's it. A few lines. Run it.

**Stage 2 — chatbot.py** (60–90 minutes)
Build the CLI chatbot. See the TODOs inside the file.
Run it: `python chatbot.py`

**Stage 3 — app.py** (60–90 minutes)
Wrap your chatbot in Streamlit.
Run it: `streamlit run app.py`

**Optional — compare_apis.py** (30–45 minutes, if time allows)
Compare OpenAI and Anthropic APIs side-by-side. This is NOT required for Day 1 completion, but it will help you understand API differences and answer the logbook question about switching to Claude. Only do this if you've completed all three stages above and have extra time.

## Road Test

Work through this checklist before marking Day 1 complete:

- [ ] `hello.py` runs and prints an AI response
- [ ] `chatbot.py` loop runs, AI remembers context across turns
- [ ] Ask "What did I just ask you?" — AI answers correctly
- [ ] Streaming in chatbot.py prints tokens as they arrive (not all at once)
- [ ] Type "quit" in chatbot.py — see session stats with token count and cost
- [ ] Streamlit UI shows full chat history with user/assistant bubbles
- [ ] `.env` is NOT in git (`git status` should not show it)
- [ ] Optional: `compare_apis.py` runs and shows responses from both OpenAI and Anthropic

## Git Checkpoint

Before you close your laptop, commit your work:

```bash
git init
git add .
git commit -m "Day 1: Hello LLM — chatbot with streaming and Streamlit UI"
```

Your commit history IS your portfolio. Make it count.

## Preview: Tomorrow's Spaced Review

Day 2 will start with questions about today's work. Make sure you can answer:

- What are the three message roles in the chat API and what does each do?
- Why does conversation "memory" cost money?
- What's the difference between streaming and non-streaming responses?

## Logbook (fill in after finishing)

> What surprised you about the API response format?

> What happens when the messages list gets very long?

> How would you switch this to Anthropic's Claude API? What would change?
> (Hint: If you completed the optional compare_apis.py exercise, you already know the answer!)
