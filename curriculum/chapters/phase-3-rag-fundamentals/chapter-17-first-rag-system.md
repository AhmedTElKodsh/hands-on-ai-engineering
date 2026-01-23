# Chapter 17: Your First RAG System — Chatting with Data

<!--
METADATA
Phase: 3 - RAG Fundamentals
Time: 1.5 hours (30 min reading + 60 min hands-on)
Difficulty: ⭐⭐⭐
Type: Implementation
Prerequisites: Chapter 14 (Vector Store), Chapter 8 (Client)
Builds Toward: Advanced RAG (Ch 19), Agents (Ch 26)
Correctness Properties: P19 (Citation Accuracy), P20 (Consistency)
Project Thread: Knowledge Retrieval

NAVIGATION
→ Quick Reference: #quick-reference-card
→ Verification: #verification-required-section
→ What's Next: #whats-next
-->

---

## ☕ Coffee Shop Intro

Let me paint you a picture that everyone who's been through school can relate to. Imagine you're sitting in a university lecture hall on a warm spring afternoon, surrounded by dozens of other students who look just as nervous as you feel. In front of you is a blank blue book, and you're about to take your comprehensive final exam on world history.

This exam covers absolutely everything from ancient Mesopotamian civilizations all the way through modern geopolitics. We're talking about literally thousands of dates, names, events, cause-and-effect relationships, and interconnected threads spanning thousands of years.

**Now, let's consider two dramatically different scenarios:**

**Scenario A: The Closed-Book Nightmare** 😓  
In this scenario, you're not allowed to bring any materials into the exam room. Everything you need to know must be stored entirely in your memory. You've spent the past three weeks cramming information into your brain, making hundreds of flashcards, staying up late drilling yourself. But here's the problem with human memory: when you're under pressure, you'll inevitably forget some details. You might remember the concept, but forget the date. Or you might mix up two similar historical figures. The closed-book exam is hard, stressful, and prone to errors.

**Scenario B: The Open-Book Advantage** 😎  
Now imagine a completely different approach. In this scenario, you're allowed to bring your textbook into the examination room with you. Suddenly, the entire dynamic changes. Instead of spending your time memorizing thousands of facts, you focus on understanding _concepts_ and knowing _how to find_ information. When a question asks about a specific date, you don't guess—you flip to the relevant page and verify it. This creates confidence, accuracy, and depth.

**Here's the fascinating parallel with AI:**

Large Language Models (LLMs) like GPT-4 are, by default, taking a **Closed Book Exam**. They only know what they memorized during their training (the internet data up to their cutoff date). They don't know about _your_ private company emails. They don't know about _your_ specific contracts. And they certainly don't know about the new product specs your team wrote yesterday morning.

If you ask an LLM about these things, it has two bad choices: say "I don't know," or worse, try to guess based on similar things it _has_ seen (Hallucination).

**RAG (Retrieval-Augmented Generation) is the "Open Book" strategy for AI.**

Instead of forcing the massive AI model to memorize your private data (which is expensive and slow), we simply find the relevant "page" of your data and show it to the AI right before it answers the question. We are literally giving the AI "eyes" to read your documents. 👀

**By the end of this chapter**, you will build a complete system that allows an AI to answer accurate questions about documents it has _never seen before_ in its training.

---

## Prerequisites Check

To build a RAG system, we need to combine two tools we've built in previous chapters. Let's make sure they are ready.

✅ **The Brain: LLM Client** (from Chapter 8)
You need your `MultiProviderClient` working, so we can send prompts to the AI.

```python
from shared.infrastructure.llm.client import MultiProviderClient
# Should not crash
client = MultiProviderClient(provider="openai")
```

✅ **The Memory: Vector Store** (from Chapter 14)
You need your ChromaDB wrapper working, so we can search for documents.

```python
from shared.infrastructure.vector_store import VectorStore
# Should initialize without error
store = VectorStore(path="./test_db", collection_name="test")
```

If either of these are missing, pause here and go back to Chapter 14. You can't build a house without bricks! 🧱

---

## The Story: The "Hallucination" Problem

### The Problem: Confidently Wrong

Let's imagine you are building a chatbot for a construction company, "BuildCo."

You ask your basic ChatGPT bot: _"Who is the lead engineer on the Downtown Bridge Project?"_

ChatGPT confidently replies: _"The lead engineer is John Smith."_

**The problem?** Billions of people are named John Smith. The AI has absolutely no idea who works at your company. It just picked a statistically likely name to complete the sentence. It **hallucinated**. It lied to you, with total confidence.

### The Solution: Grounding

We need to **Ground** the AI in reality. We need to force it to look at the facts before speaking.

Here is the 3-step RAG Dance:

1.  **Retrieve**: When the user asks "Who is the lead engineer?", our system quickly searches our database and finds a document that says: _"Staff Assignment: The lead engineer for Downtown Bridge is Sarah Jones."_
2.  **Augment**: We modify the user's prompt. instead of just sending the question, we send:
    > "Here is a fact: The lead engineer is Sarah Jones. Based on this fact, who is the lead engineer?"
3.  **Generate**: The AI reads the fact and generates the answer: _"The lead engineer is Sarah Jones."_

It can't hallucinate if the answer is right in front of its face. It's not "remembering"; it's **reading**.

---

## Part 1: The RAG Architecture 🏗️

The workflow is a circle. It helps to visualize it before we code it.

**Phase A: Ingestion (Preparation)**
_This happens once, before anyone asks a question._

1.  **Load**: We take your PDF/Text file.
2.  **Chunk**: We cut it into small pieces (like slicing a pizza 🍕) because the AI can't read a whole library at once.
3.  **Embed & Save**: We turn those text chunks into number vectors (Chapter 13) and save them in our Vector Database.

**Phase B: The Query Loop (Runtime)**
_This happens every time a user asks a question._

1.  **Search**: User asks a question → We search the Vector DB for the top 3 most relevant chunks.
2.  **Synthesis**: We paste those chunks into a "System Prompt" and send it to the LLM.
3.  **Answer**: The user gets the result.

---

## Part 2: Building the Pipeline 🛠️

Let's assemble the pieces. We're going to simulate the entire process in one file to see how the data flows.

### 🔬 Try This! (Hands-On Practice #1)

**Context**: We are going to build a mini-RAG system for "BuildCo" that knows about a secret project called "Project Alpha." The public AI models know nothing about this project.

**Goal**: Ask the AI about Project Alpha and get a correct answer.

**Create `simple_rag.py`**:

```python
from shared.infrastructure.llm.client import MultiProviderClient
from shared.infrastructure.vector_store import VectorStore
import os

# 1. Setup our Tools
# We initialize the client to talk to OpenAI
client = MultiProviderClient(provider="openai")
# We initialize a temporary vector store for this demo
store = VectorStore(path="./rag_test_db", collection_name="rag_demo")

# 2. Ingest Data (The "Study" Phase)
# In a real app, we'd load this from PDFs. Here, we'll hardcode some "Secret Knowledge".
print("📚 Ingesting Secret Knowledge...")

knowledge_base = [
    "Project Alpha is a confidential initiative to build a floating bridge.",
    "The lead engineer for Project Alpha is Sarah Jones.",
    "The budget for Project Alpha is $500 million.",
    "The deadline for Project Alpha is December 2026."
]

# We verify the store is empty first, then add our docs
for i, text in enumerate(knowledge_base):
    # We assign a simple ID (0, 1, 2...) to each doc
    store.add_document(doc_id=str(i), text=text, metadata={"source": "internal_memo.txt"})

print("✅ Knowledge ingested successfully.")

# 3. The RAG Function (The "Open Book Exam" Logic)
def ask_rag(question):
    print(f"\n❓ User asks: {question}")

    # Step A: Retrieve (Look up the answer in the textbook)
    # We search for the 2 most relevant sentences
    results = store.search(question, limit=2)

    # We join them together into one block of text
    context_text = "\n".join(results)
    print(f"🔎 System found these clues:\n{context_text}")

    # Step B: Augment (Write the exam prompt)
    # This is the magic. We tell the AI: "Here is the answer key. Read it."
    prompt = f"""
    You are a helpful assistant for BuildCo.
    Answer the user's question using ONLY the context provided below.
    If the answer is not in the context, say "I don't know."

    ---
    Context (Secret Knowledge):
    {context_text}
    ---

    Question: {question}
    """

    # Step C: Generate (Take the test)
    answer = client.generate(prompt)
    print(f"🤖 AI answers: {answer}")
    return answer

# 4. Test it!
ask_rag("What is Project Alpha building?")
ask_rag("Who is in charge of Alpha?")
ask_rag("Who is the CEO of Google?") # Should fail gracefully
```

**Run this code.**

You should see something amazing. When you ask "Who is in charge?", the Vector Store finds the sentence "The lead engineer is Sarah Jones", passes it to the AI, and the AI answers correctly.

When you ask "Who is the CEO of Google?", the Vector Store searches for "Google CEO" in your tiny database, finds _nothing relevant about Google_, passes irrelevant info about bridges to the AI, and the AI (following instructions) says "I don't know." **This is exactly what we want.** We want a bot that only knows what we tell it.

---

## Part 3: Citations (Showing Your Work) 📝

In the business world, trust is everything. If an AI gives an answer, the user (a lawyer, a doctor, an engineer) will immediately ask: **"Where did you get that info?"**

A "Black Box" answer isn't good enough. We need **Citations**.

Because we stored `metadata={"source": "internal_memo.txt"}` in our Vector Store, we can retrieve that alongside the text.

### 🔬 Try This! (Hands-On Practice #2)

Let's modify our search to see _where_ the information came from.

**First**: We need to update our `VectorStore` class in `shared/infrastructure/vector_store.py` to allow returning metadata. (If you haven't already).

**Second**: Create `rag_citations.py` to test it.

```python
from shared.infrastructure.vector_store import VectorStore

# Connect to the same DB we just made
store = VectorStore(path="./rag_test_db", collection_name="rag_demo")

def search_with_sources(query):
    print(f"Searching for: {query}")

    # Note: You might need to add a 'search_with_metadata' method to your
    # VectorStore class if it doesn't exist yet!
    # It works just like search() but returns the 'metadatas' list too.
    results = store.search_with_metadata(query, limit=1)

    for doc, metadata in results:
        print(f"Found Fact: {doc}")
        print(f"Source Document: {metadata['source']}")
        print("-" * 20)

search_with_sources("Sarah Jones")
```

**Why this matters**:
In a real application, you could have thousands of documents. When the AI says "The beam thickness must be 50mm," your app can display: "Source: Structural_Safety_Guidelines_v2.pdf, Page 45." That makes the AI **auditable**.

---

## Part 4: The "I Don't Know" Guardrail 🛡️

The most dangerous thing an AI can do is guess. In RAG, we want to treat "I don't know" as a **success state**.

If we don't have the document, the AI _must_ stay silent.

**The Prompt Pattern:**

This simple instruction prevents 90% of hallucinations:

```text
Answer using ONLY the provided context.
If the answer is not in the context, say "I don't know".
DO NOT make things up.
```

### 🔬 Try This! (Hands-On Practice #3)

Let's witness the difference between a "Raw" LLM and a "Grounded" LLM.

**Create `hallucination_test.py`**:

```python
from shared.infrastructure.llm.client import MultiProviderClient

client = MultiProviderClient()

# A "fact" that is definitely false in the real world
context = "In this hypothetical world, the sky is neon green."

# 1. Prompt WITHOUT guardrails (The Standard LLM behavior)
# It relies on its training data (where the sky is blue)
bad_prompt = f"Context: {context}. What color is the sky?"
print("Bad Prompt Answer:", client.generate(bad_prompt))
# It might say "Blue" because it ignores our context, or gets confused.

# 2. Prompt WITH guardrails (The RAG behavior)
good_prompt = f"""
Context: {context}
Question: What color is the sky?
Answer using ONLY the context. If not mentioned, say "Unknown".
"""
print("Good Prompt Answer:", client.generate(good_prompt))
```

**Expected Result**:
The good prompt will confidently say "Neon Green." It has overridden its "world model" (training data) with your "local facts" (context). This proves you are in control.

---

## Common Mistakes to Avoid 🚫

### Mistake #1: Stuffing Too Much Context

**The Mistake**: "I'll just paste the whole Employee Handbook into the prompt!"
**Why it fails**:

1.  **Cost**: You pay per token. Reading a 50-page book for every "Hi" is expensive.
2.  **The "Middle Child" Problem**: AI models are good at remembering the beginning and end of a text, but often forget details buried in the middle.
    **The Fix**: Only retrieve the top 3-5 most relevant chunks. Less is more.

### Mistake #2: Bad Chunking (cutting the pizza wrong)

**The Mistake**: Cutting chunks in the middle of sentences.
**Why it fails**: If the chunk is `"...profit was $-"` and the next chunk is `"5 million."`, the AI sees two meaningless fragments.
**The Fix**: Use valid sentence splitters or paragraph splitters (we'll cover `RecursiveCharacterTextSplitter` later).

---

## Quick Reference Card 🃏

Here is the "Golden Prompt" for RAG. Copy-paste this into your projects.

```python
RAG_PROMPT_TEMPLATE = """
You are a knowledgeable assistant. Use the following pieces of context to answer the user's question.
If the answer is not present in the context, state "I do not have enough information to answer."

---
CONTEXT:
{context_str}
---

QUESTION:
{query_str}

ANSWER:
"""
```

---

## Verification (REQUIRED SECTION) 🧪

We need to mathematically prove **P20 (Consistency)**: The AI uses the provided context, not its training data.

**Create `verify_rag.py`**:

```python
"""
Verification script for Chapter 17.
Property P20: Consistency with Context.
"""
from shared.infrastructure.llm.client import MultiProviderClient
import sys

print("🧪 Running RAG Verification...\n")

client = MultiProviderClient(provider="openai")

# 1. Counter-Factual Context test
# We tell the AI something clearly false (The moon is cheese).
# If it answers "Rock", it's using training data (Fail).
# If it answers "Cheese", it's using our RAG context (Pass).
fake_fact = "Scientific discovery 2026: The moon is actually made of aged cheddar cheese."
question = "What is the moon made of?"

prompt = f"""
Context: {fake_fact}
Question: {question}
Answer using ONLY the context provided.
"""

# 2. Generate
answer = client.generate(prompt)
print(f"AI Answer: {answer}")

# 3. Verify P20
if "cheese" in answer.lower():
    print("✅ P20 Passed: AI grounded in context (overrode training data).")
else:
    print("❌ Failed: AI hallucinated or ignored context.")
    sys.exit(1)

print("\n🎉 Chapter 17 Complete! You have built a thinking, reading machine.")
```

**Run it:** `python verify_rag.py`

---

## Summary

We've just unlocked a superpower. Before this chapter, your AI was a brilliant but isolated genius. Now, it's a genius _with access to your library_.

**What we accomplished:**

1.  ✅ **Understood the RAG Flow**: Ingest -> Retrieve -> Augment -> Generate.
2.  ✅ **Implemented Grounding**: We forced the AI to read facts before speaking.
3.  ✅ **Added Citations**: We learned how to track where facts come from.
4.  ✅ **Built Guardrails**: We taught the AI to say "I don't know" instead of lying.

**Key Takeaway**: You don't train the model to teach it new facts. You just hand it the facts at runtime. This is cheaper, faster, and more accurate than training.

**What's Next?**
We've been building all these steps by hand—writing Python loops to combine strings. As our applications get more complex (chats, agents, tools), this "plumbing" code gets messy.

In **Chapter 18**, we will introduce **LangChain**, a framework specifically designed to handle this plumbing for us elegantly.

See you in the next chapter! 🚀
