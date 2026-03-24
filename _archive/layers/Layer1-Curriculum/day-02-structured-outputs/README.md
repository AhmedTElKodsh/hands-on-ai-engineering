# Day 2 — Structured Outputs & Prompt Engineering

**Mini-Project 2 | ~5 hours | Difficulty: ⭐⭐**

## The Mechanic's Analogy

Yesterday you started the car. Today you learn to steer precisely. Vague prompts are like vague directions — "go somewhere nice" versus "take I-95 North to Exit 12." Prompt engineering is the skill of giving AI exactly the directions it needs. Structured outputs are like getting parts delivered in exactly the right bins instead of a giant pile.

## Prime the Pump: What You Need to Know

Before you touch code, understand this:

**Prompts are programs.** The system message is your "source code" — it defines behavior, constraints, and output format.
**Temperature acts as a creativity dial.** (0 = deterministic, 1 = creative).
**Structured Output (JSON/Function Calling)** gives you guaranteed, machine-readable data instead of conversational text.

Check out [DeepLearning.AI — ChatGPT Prompt Engineering](https://www.deeplearning.ai/short-courses/chatgpt-prompt-engineering-for-developers/). Spend some time there before you build.

## First Wrench Turn: Extract Structured Data (15 min)

Open `01_extractor.py`. We are going to take messy, unstructured text (a restaurant review) and use the LLM to output clean, structured JSON.

Run it: `python 01_extractor.py`

## Tighten the Bolts: Prompt Engineering Toolkit

Now build a toolkit demonstrating different prompting patterns. Open `02_prompt_patterns.py` and implement:

1. **Zero-shot**: Classify reviews without examples.
2. **Few-shot**: Extract entities by giving the model 3 examples in the prompt to guide the format.
3. **Chain-of-thought**: Force the model to explain its reasoning step-by-step ("Let's think step by step").
4. **System role**: Create a persona (strict teacher, friendly coach) using the system message.
5. **Prompt chaining**: Decompose complex tasks where the output of prompt 1 feeds into prompt 2.

Then explore these advanced techniques:

- **`03_temperature_test.py`**: Test the identical prompt with Temperature 0.0 vs 1.0.
- **`04_token_counter.py`**: Use `tiktoken` to count tokens BEFORE you call the API to estimate cost.
- **`05_pydantic_validation.py`**: Use function calling (Structured Outputs) with Pydantic to strictly type the LLM response.

## Road Test Checklist

- [ ] `01_extractor.py` produces valid JSON for 5 different reviews.
- [ ] Each prompt pattern script runs and demonstrates its concept.
- [ ] Temperature test shows measurable difference between 0.0 and 1.0.
- [ ] Token counter accurately counts tokens and estimates cost.
- [ ] At least one script uses Pydantic to validate LLM output.

## Spaced Review (answer out loud before checking)

From Day 1:

- What are the three message roles in the chat API? What does each one do?
- Why does a 10-turn conversation cost more than a 1-turn conversation?

## Logbook Prompts

> Which prompt pattern surprised you the most? Why?
> What happens when the LLM returns malformed JSON? How did you handle it?
> Why would you choose function calling (Pydantic) over just JSON mode?

### What You'd Say in an Interview

> "I built an extraction pipeline using OpenAI's structured outputs. I used JSON mode (`response_format={"type": "json_object"}`) to ensure machine-readable parsing, paired with a few-shot prompt to enforce schema adherence. For strict validation, I implemented Pydantic models with function calling, which guarantees type safety before the data enters the rest of the application. To optimize costs during prompt engineering, I used `tiktoken` to measure token usage before execution."

### What's Next

You've now learned how to steer the model accurately. Tomorrow (Day 3), we switch gears to Embeddings — the mathematical foundation underlying semantic search and RAG.
