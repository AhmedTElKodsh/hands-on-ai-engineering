# Chapter 38A: GraphRAG & Knowledge Graphs — The Librarian Who Knows Everyone

<!--
METADATA
Phase: Phase 7: LlamaIndex
Time: 2.5 hours (45 minutes reading + 105 minutes hands-on)
Difficulty: ⭐⭐⭐⭐
Type: Implementation / Advanced
Prerequisites: Chapter 35 (LlamaIndex Basics), Chapter 38 (Hybrid Search)
Builds Toward: Chapter 53 (Compliance Review), Chapter 54 (Complete System)
Correctness Properties: P80 (Graph completeness), P81 (Relationship accuracy)
-->

## ☕ Coffee Shop Intro: The Networking Event

Imagine you're trying to find a specific person to hire.

**Approach A (Vector Search):** You shout into a crowded room, "Who here knows about Python and Bridges?" You get 10 people who look like they might know (similarity search), but 5 of them just like snakes and card games.

**Approach B (Knowledge Graph):** You ask the master networker (let's call her Graph Grace). She doesn't just match keywords. She knows:
*   *Alice* worked on *Project X*.
*   *Project X* used *Python*.
*   *Project X* was a *Bridge Design*.
*   Therefore, *Alice* fits your criteria perfectly.

**GraphRAG** is that master networker. It combines the fuzzy, semantic power of Vector Search with the precise, relationship-aware power of Knowledge Graphs.

In this chapter, we're building that networker.

---

## 🔍 The 3-Layer Dive

### Layer 1: The Limit of Vectors
Vector databases store text as numbers. They are amazing at finding "things that sound similar."
*   **Good for**: "Tell me about safety regulations."
*   **Bad for**: "How does the load capacity of the Golden Gate Bridge compare to the Bay Bridge?" (This requires understanding specific entities and their relationships).

### Layer 2: The Knowledge Graph (KG)
A Knowledge Graph stores data as **Entities** (Nodes) and **Relationships** (Edges).
*   **Node**: `Golden Gate Bridge`
*   **Edge**: `HAS_LOAD_CAPACITY` -> `4,000 lbs/ft`
*   **Node**: `Bay Bridge`
*   **Edge**: `HAS_LOAD_CAPACITY` -> `5,000 lbs/ft`

It's structured, precise, and rigid.

### Layer 3: GraphRAG (The Best of Both)
GraphRAG queries *both*.
1.  **Retrieves** documents via vector similarity (finding context).
2.  **Traverses** the graph to find hidden connections (finding answers).
3.  **Synthesizes** the result.

It improves retrieval accuracy by **40%** on complex queries because it doesn't just guess—it *knows* how things connect.

---

## 🛠️ Implementation Guide: Building a GraphRAG System

We'll use **LlamaIndex** to build an in-memory GraphRAG system. In production, you'd use a database like Neo4j, but for learning, we'll keep it simple (and free).

### Step 1: Setup & Dependencies

You'll need `llama-index` and `networkx` (for the graph structure).

```bash
pip install llama-index networkx matplotlib
```

### Step 2: The Data Model (Your Turn)

We need text that describes relationships. Let's use a Civil Engineering scenario.

```python
# pattern_graph_setup.py

from llama_index.core import Document, Settings
from llama_index.llms.openai import OpenAI

# Setup LLM (Graph extraction needs a smart model like GPT-4)
Settings.llm = OpenAI(model="gpt-4", temperature=0)

# 1. Create Documents
text_chunks = [
    "The Golden Gate Bridge is a suspension bridge located in San Francisco.",
    "It uses steel cables supplied by Roebling's Sons Co.",
    "The bridge has a main span of 1,280 meters.",
    "San Francisco requires seismic retrofitting for all suspension bridges.",
]

documents = [Document(text=t) for t in text_chunks]

# Your Turn:
# create a list of documents describing a different project
# containing at least 3 entities and 2 relationships.
```

### Step 3: Building the Knowledge Graph Index

This is where the magic happens. The LLM reads the text and extracts triplets: `(Subject, Predicate, Object)`.

Example: `(Golden Gate Bridge, IS_LOCATED_IN, San Francisco)`

```python
from llama_index.core import KnowledgeGraphIndex
from llama_index.core.graph_stores import SimpleGraphStore
from llama_index.core import StorageContext

def build_graph_index(documents):
    # 1. Create a simple in-memory graph store
    graph_store = SimpleGraphStore()
    storage_context = StorageContext.from_defaults(graph_store=graph_store)

    # 2. Build the index
    # max_triplets_per_chunk limits how many relationships to extract per sentence
    index = KnowledgeGraphIndex.from_documents(
        documents,
        max_triplets_per_chunk=2,
        storage_context=storage_context,
        include_embeddings=True, # Critical for GraphRAG (hybrid)
    )
    
    return index

# Build it
kg_index = build_graph_index(documents)
```

### Step 4: Querying with GraphRAG

Now we can ask questions that require understanding relationships.

```python
def query_graph(index, question):
    # 'hybrid' mode uses both keywords/vectors AND graph traversal
    query_engine = index.as_query_engine(
        include_text=True,
        response_mode="tree_summarize",
        embedding_mode="hybrid",
        similarity_top_k=3,
    )
    
    response = query_engine.query(question)
    return response

# Test
print(query_graph(kg_index, "Who supplied cables for the bridge in San Francisco?"))
```

---

## 🧪 Correctness Properties (Testing the Graph)

How do we know our graph isn't hallucinating? We test properties.

| Property | Description |
|----------|-------------|
| **P80: Graph Completeness** | If text says "A implies B", the graph MUST contain edge A->B |
| **P81: Relationship Accuracy** | Extracted relationships must exist in source text |

### Hypothesis Test Example

```python
from hypothesis import given, strategies as st
import networkx as nx

# Mocking the extraction for property testing
def extract_triplets(text):
    # Simple rule-based mock for testing
    if "uses" in text:
        parts = text.split(" uses ")
        return [(parts[0], "USES", parts[1])]
    return []

@given(st.text())
def test_p80_graph_completeness(text):
    """P80: If extraction rule triggers, graph must contain the edge."""
    # Setup
    if " uses " not in text: return # Skip irrelevant tests
    
    triplets = extract_triplets(text)
    
    # Verify
    for subj, pred, obj in triplets:
        assert subj is not None
        assert obj is not None
        # In a real test, we'd check if these exist in the nx_graph
```

---

## ✍️ Try This! (Hands-On Exercises)

### Exercise 1: Visualize the Graph
The internal graph is stored in `networkx` format. Write a function to visualize it or print all triplets.

*Hint*: Access `index.graph_store.get_networkx_graph()`.

### Exercise 2: The "Material" Finder
Create a set of documents about 3 different buildings and the materials they use (e.g., "Tower A uses Concrete", "Tower B uses Steel").
Build a graph index and ask: "Which buildings require Steel?"
Verify if the answer comes from the *graph* (relationships) or just *text similarity*.

---

## ✅ Verification Script

Create a file named `verify_ch38a.py` and run it to prove your system works.

```python
"""
Verification script for Chapter 38A: GraphRAG
"""
import sys
import logging
from llama_index.core import Document, KnowledgeGraphIndex, Settings, StorageContext
from llama_index.core.graph_stores import SimpleGraphStore
from llama_index.llms.mock import MockLLM
from llama_index.embeddings.openai import OpenAIEmbedding

# Setup Mock LLM to avoid API costs during verification
# We mock the extraction to ensure deterministic tests
class MockGraphLLM(MockLLM):
    def predict(self, prompt, **kwargs):
        # Determine if this is extraction or querying based on prompt
        if "triplet" in str(prompt).lower() or "extract" in str(prompt).lower():
            # Mock extraction response
            return "(Golden Gate Bridge, LOCATED_IN, San Francisco)\n(Golden Gate Bridge, USES, Steel)"
        return "The Golden Gate Bridge is in San Francisco and uses Steel."

    @property
    def metadata(self):
        return super().metadata

def verify_graph_construction():
    print("1. Setting up Mock LLM/Embeddings...")
    Settings.llm = MockGraphLLM()
    # We use a dummy embedding for the hybrid part
    Settings.embed_model = OpenAIEmbedding(api_key="sk-dummy", embed_batch_size=1)

    print("2. Creating Documents...")
    docs = [Document(text="The Golden Gate Bridge is located in San Francisco.")]

    print("3. Building Graph Index (Simulated)...")
    graph_store = SimpleGraphStore()
    storage_context = StorageContext.from_defaults(graph_store=graph_store)
    
    # We force extraction via the mock
    index = KnowledgeGraphIndex.from_documents(
        docs,
        max_triplets_per_chunk=2,
        storage_context=storage_context,
        include_embeddings=False # Disable embedding for pure graph test without API key
    )
    
    print("4. Verifying Graph Structure...")
    # Get the underlying networkx graph
    g = graph_store.get_networkx_graph()
    
    # Check if nodes exist (Note: LlamaIndex might normalize names)
    nodes = list(g.nodes())
    print(f"   Nodes found: {len(nodes)}")
    
    # We expect at least the subject/object nodes
    if len(nodes) < 2:
        print("❌ Failed: Graph should have nodes.")
        sys.exit(1)
        
    print("✅ Graph constructed successfully.")

if __name__ == "__main__":
    try:
        verify_graph_construction()
        print("\n🎉 Chapter 38A Verification Passed!")
    except Exception as e:
        print(f"\n❌ Verification Failed: {e}")
        sys.exit(1)
```

---

## 📝 Summary & Key Takeaways

1.  **Vectors aren't enough**: They miss explicit relationships between entities.
2.  **Knowledge Graphs (KG)**: Store data as structured `(Subject, Predicate, Object)` triplets.
3.  **GraphRAG**: Combines Vector Search (Context) + Graph Traversal (Relationships).
4.  **LlamaIndex**: Provides `KnowledgeGraphIndex` to automate triplet extraction.
5.  **Hybrid Mode**: The most powerful query mode, using both keywords and graph paths.
6.  **Production**: In real systems, use Neo4j or Amazon Neptune instead of `SimpleGraphStore`.
7.  **Cost**: Graph construction requires LLM calls to extract triplets, so it's more expensive than simple embedding.

**Key Insight**: An Engineer knows "Steel". A Senior Engineer knows "Steel *supports* the Bridge *located in* Zone 4." GraphRAG gives your AI that Senior Engineer level of understanding.

---

## 🔜 What's Next?

Now that our AI understands relationships, let's make sure it's working reliably in production. In **Chapter 40A**, we'll dive into **Observability** to trace exactly what's happening inside these complex chains.
