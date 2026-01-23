"""
Chapter 17: Simple RAG System Implementation

This is a working implementation of the first RAG system from Chapter 17.
Students implement this by following the hints in the scaffolded chapter.
"""

from shared.infrastructure.vector_store import VectorStore
from shared.infrastructure.llm.client import MultiProviderClient
import os


def ingest_knowledge_base(store: VectorStore, knowledge_base: list[str]) -> None:
    """
    Ingest documents into the vector store.
    
    This function takes a list of text documents and adds them to the vector store
    with unique IDs and metadata for tracking.
    """
    for i, text in enumerate(knowledge_base):
        store.add_document(
            doc_id=str(i),
            text=text,
            metadata={"source": "internal_memo.txt"}
        )
    print("✅ Knowledge ingested successfully.")


def ask_rag(
    question: str,
    store: VectorStore,
    client: MultiProviderClient,
    limit: int = 2
) -> str:
    """
    Answer a question using RAG (Retrieval-Augmented Generation).
    
    This is the core RAG function that:
    1. Retrieves relevant context from the vector store
    2. Augments the prompt with that context
    3. Generates an answer using the LLM
    """
    print(f"\n❓ User asks: {question}")
    
    # Step A: Retrieve
    results = store.search(question, limit=limit)
    context_text = "\n".join(results)
    print(f"🔎 System found these clues:\n{context_text}")
    
    # Step B: Augment
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
    
    # Step C: Generate
    answer = client.generate(prompt)
    print(f"🤖 AI answers: {answer}")
    return answer


# Main execution
if __name__ == "__main__":
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY environment variable not set")
        print("Please set your OpenAI API key to run this example.")
        exit(1)
    
    # 1. Setup our Tools
    print("🔧 Setting up RAG system...")
    client = MultiProviderClient(provider="openai")
    store = VectorStore(path="./rag_test_db", collection_name="rag_demo")
    
    # 2. Ingest Data (The "Study" Phase)
    print("📚 Ingesting Secret Knowledge...")
    knowledge_base = [
        "Project Alpha is a confidential initiative to build a floating bridge.",
        "The lead engineer for Project Alpha is Sarah Jones.",
        "The budget for Project Alpha is $500 million.",
        "The deadline for Project Alpha is December 2026."
    ]
    
    ingest_knowledge_base(store, knowledge_base)
    
    # 3. Test the RAG system
    print("\n" + "="*50)
    print("Testing RAG System")
    print("="*50)
    
    ask_rag("What is Project Alpha building?", store, client)
    ask_rag("Who is in charge of Alpha?", store, client)
    ask_rag("Who is the CEO of Google?", store, client)  # Should fail gracefully
    
    print("\n✅ RAG system test complete!")
