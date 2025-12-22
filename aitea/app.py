"""AITEA Application Entry Point

Multi-provider LLM fallback system with automatic provider detection.
Implements Requirement 13: Multi-Provider Fallback Mode.
"""

import os
from typing import List
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(override=True)


def get_available_providers() -> List[str]:
    """
    Detect which LLM providers are configured via API keys.
    
    Returns list of available providers in priority order:
    OpenAI → Cohere → Gemini → Grok → Mistral → HuggingFace → Ollama → MockLLM
    
    Returns:
        List of provider names that have API keys configured
    """
    providers = []
    
    if os.getenv("OPENAI_API_KEY"):
        providers.append("OpenAI")
    if os.getenv("COHERE_API_KEY"):
        providers.append("Cohere")
    if os.getenv("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY2"):
        providers.append("Gemini")
    if os.getenv("GROQ_API_KEY"):
        providers.append("Grok")
    if os.getenv("MISTRAL_API_KEY"):
        providers.append("Mistral")
    if os.getenv("LANGCHAIN_API_KEY") or os.getenv("LANGCHAIN_API_KEY2"):
        providers.append("Langchain")
    if os.getenv("OLLAMA_API_KEY"):
        providers.append("Ollama")
   
    
    return providers

def main():
    """
    Main function to run the application.
    """
    providers = get_available_providers()
    print(f"Available providers: {providers}")


if __name__ == "__main__":
    main()
