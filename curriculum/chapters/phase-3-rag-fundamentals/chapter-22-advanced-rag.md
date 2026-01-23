# Chapter 22: Advanced RAG Patterns — The Power Tools

<!--
METADATA
Phase: Phase 3: RAG Fundamentals
Time: 2.0 hours (45 min reading + 75 min hands-on)
Difficulty: ⭐⭐⭐
Type: Implementation
Prerequisites: Chapter 19 (Retrieval)
Builds Toward: LlamaIndex (Ch 35), Production System (Ch 54)
Correctness Properties: P29 (Parent-Child Integrity), P30 (Merge Boundary)
-->

## ☕ Coffee Shop Intro: The Architect's Blueprint

**Imagine this**: You use Google Maps to find a coffee shop.
You zoom in all the way. You see a pixel that says "Door". Great precision!
But... you have no idea what street you're on. You lost the **Context**.

**RAG has this problem.**
Small chunks are easy to find (high precision).
But small chunks (100 words) often lack the information needed to answer the question ("See Appendix A for details" - wait, where is Appendix A?).

**Advanced RAG Patterns** fix this.
We search with the microscope (Small Chunks), but we deliver the whole map (Parent Documents).
It's the best of both worlds: Precision searching, Contextual answering. 🗺️

---

## 🔍 The 3-Layer Dive

### Layer 1: Naive RAG (What we did before)
Chunk → Embed → Retrieve → Answer.
*   **Pro**: Simple.
*   **Con**: Losing context. "He said yes" (Who is He?).

### Layer 2: Advanced Retrieval (Parent/Child)
Chunk → Embed → Retrieve Chunk → **Look up Parent** → Answer with Parent.
*   **Pro**: Full context.
*   **Con**: More storage (need to store relationships).

### Layer 3: Production Maintenance (Incremental)
Docs change. Re-embedding 10,000 PDFs every night is slow and expensive.
*   **Solution**: Incremental Indexing. Only embed what changed.

---

## 🛠️ Implementation Guide: Pattern by Pattern

We need advanced retrievers from LangChain.

```bash
pip install langchain langchain-community chromadb
```

### Part 1: Parent Document Retriever (Context Restoration)

Let's build the hierarchy: Search small, Retrieve big.

#### 🔬 Try This! (Hands-On Practice #1)

**Create `parent_retriever.py`**:

```python
from langchain.retrievers import ParentDocumentRetriever
from langchain.storage import InMemoryStore
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()

# 1. Setup
# We need two stores: 
# - VectorStore (for searching small chunks)
# - DocStore (for holding big chunks)
vectorstore = Chroma(collection_name="split_parents", embedding_function=OpenAIEmbeddings())
docstore = InMemoryStore()

# 2. Splitters
# Children: Small, specific (for search)
child_splitter = RecursiveCharacterTextSplitter(chunk_size=100)
# Parents: Large, contextual (for answer)
parent_splitter = RecursiveCharacterTextSplitter(chunk_size=500)

# 3. The Retriever
retriever = ParentDocumentRetriever(
    vectorstore=vectorstore,
    docstore=docstore,
    child_splitter=child_splitter,
    parent_splitter=parent_splitter,
)

# 4. Add Data
long_text = "The code to unlock the safe is 1234. " * 20 + "The safe contains gold."
doc = Document(page_content=long_text, metadata={"title": "Secret"})

print("Adding document...")
retriever.add_documents([doc], ids=None)

# 5. Search
# Search for a specific detail
query = "contains gold"
results = retriever.invoke(query)

print(f"\nQuery: {query}")
print(f"Retrieved {len(results)} doc(s).")
print(f"Content Length: {len(results[0].page_content)}") # Should be ~500 (Parent)
print(f"Snippet: {results[0].page_content[:50]}...")
```

**Run it**. You'll see the retriever returns the *whole* 500-char parent chunk, even though the query matched a tiny end fragment.

### Part 2: Hypothetical Document Embeddings (HyDE)

Q: "How do I fix a null pointer?"
Doc: "Check for uninitialized variables."

Vector similarity might fail here.
**HyDE Strategy**: Ask LLM to **hallucinate** an answer, then search for that.

#### 🔬 Try This! (Hands-On Practice #2)

**Create `hyde.py`**:

```python
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chains import HydeRetrievalChain, LLMChain
from langchain.prompts import ChatPromptTemplate
from langchain_chroma import Chroma

# 1. Setup Vector Store
vectorstore = Chroma(embedding_function=OpenAIEmbeddings())
vectorstore.add_texts(["To resolve NullPointer, check variable initialization."])

# 2. HyDE Generator
llm = ChatOpenAI(model="gpt-4o-mini")
prompt = ChatPromptTemplate.from_template(
    "Write a scientific paragraph answering the question: {question}"
)
llm_chain = LLMChain(llm=llm, prompt=prompt)

# 3. Search
query = "How do I fix a null pointer?"

# MANUAL HyDE Logic (Concept):
hypothetical = llm_chain.invoke(query)["text"]
print(f"👻 Hallucination: {hypothetical[:60]}...")

results = vectorstore.similarity_search(hypothetical, k=1)
print(f"✅ Found: {results[0].page_content}")
```

### Part 3: Production RAG - Incremental Updates (NEW)

**The Problem**: In production, documents change. New drawings are added, old specs are revised.
**The Trap**: Re-indexing everything daily is wasteful.
**The Fix**: **Hash-Based Change Detection**.

We calculate a "fingerprint" (Hash) for each document. If the hash hasn't changed, we skip it.

#### 🔬 Try This! (Hands-On Practice #3)

**Create `incremental_rag.py`**:

```python
import hashlib
from langchain_core.documents import Document

class IncrementalIndexer:
    def __init__(self):
        # In production, this dict should be in a database (Redis/SQL)
        self.doc_hashes = {} 

    def _compute_hash(self, content: str) -> str:
        return hashlib.sha256(content.encode()).hexdigest()

    def index_documents(self, documents):
        new_or_changed = []
        
        for doc in documents:
            doc_id = doc.metadata.get("id")
            current_hash = self._compute_hash(doc.page_content)
            
            # Check if existing and identical
            if doc_id in self.doc_hashes and self.doc_hashes[doc_id] == current_hash:
                print(f"⏩ Skipping {doc_id} (Unchanged)")
                continue
                
            # It's new or changed
            print(f"📥 Indexing {doc_id} (New/Changed)")
            self.doc_hashes[doc_id] = current_hash
            new_or_changed.append(doc)
            
        # In real usage, here you would call vectorstore.add_documents(new_or_changed)
        return len(new_or_changed)

# Test it
indexer = IncrementalIndexer()

docs_v1 = [
    Document(page_content="Bridge A spec v1", metadata={"id": "doc1"}),
    Document(page_content="Bridge B spec v1", metadata={"id": "doc2"}),
]

print("--- Day 1 ---")
indexer.index_documents(docs_v1)

docs_v2 = [
    Document(page_content="Bridge A spec v1", metadata={"id": "doc1"}), # Unchanged
    Document(page_content="Bridge B spec v2", metadata={"id": "doc2"}), # Changed
]

print("\n--- Day 2 ---")
indexer.index_documents(docs_v2)
```

**Run it**. You should see it skip Doc1 on Day 2.

---

## 🧪 Correctness Properties (Testing Integrity)

| Property | Description |
|----------|-------------|
| **P29: Parent-Child Integrity** | Child fragment search MUST return Parent content. |
| **P30: Change Detection** | Unchanged content MUST NOT trigger re-indexing. |

### Hypothesis Test Example

```python
from hypothesis import given, strategies as st
import hashlib

def get_hash(s):
    return hashlib.sha256(s.encode()).hexdigest()

@given(st.text())
def test_p30_stable_hash(content):
    """P30: Hash function must be deterministic."""
    h1 = get_hash(content)
    h2 = get_hash(content)
    assert h1 == h2
```

---

## ✅ Verification Script

Create `verify_ch22.py`.

```python
"""
Verification script for Chapter 22.
"""
from langchain.retrievers import ParentDocumentRetriever
from langchain.storage import InMemoryStore
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
import sys

print("🧪 Running Advanced RAG Verification...\n")

# Setup
vectorstore = Chroma(collection_name="verify_parents", embedding_function=OpenAIEmbeddings())
docstore = InMemoryStore()
retriever = ParentDocumentRetriever(
    vectorstore=vectorstore,
    docstore=docstore,
    child_splitter=RecursiveCharacterTextSplitter(chunk_size=20),
    parent_splitter=RecursiveCharacterTextSplitter(chunk_size=100)
)

# Verify P29 (Parent-Child)
parent_content = "This is a unique parent document identifier code 9999."
doc = Document(page_content=parent_content)
retriever.add_documents([doc])

query = "identifier code"
results = retriever.invoke(query)

if len(results) > 0 and results[0].page_content == parent_content:
    print("✅ P29 Passed: Retrieved full parent.")
else:
    print(f"❌ Failed: Expected parent, got {results}")
    sys.exit(1)

print("\n🎉 Chapter 22 Verification Passed!")
```

---

## 📝 Summary & Key Takeaways

1.  **Parent Document Retriever**: Solves the context problem. Search precise (child), answer broad (parent).
2.  **HyDE**: Improves recall for vague queries by searching for *hypothetical answers*.
3.  **Incremental Indexing**: Essential for production. Use **Hashing** to detect changes.
4.  **Decoupling**: The searchable vector index doesn't have to be the same as the returned content.
5.  **Cost**: Incremental updates save massive amounts of compute and API cost over time.
6.  **Storage**: Parent retrieval requires a persistent Document Store (DocStore), separate from the Vector Store.
7.  **Latency**: HyDE adds latency (extra LLM call). Use carefully.

**Key Insight**: Advanced RAG isn't just about better models. It's about better **Architecture**. Putting the right data in the right shape (Parents, Children, Hashes) for the right step.

---

## 🔜 What's Next?

We've mastered retrieval. But what about the tools to build this? In **Phase 4**, we dive deep into **LangChain Core** to understand exactly how the sausage is made.