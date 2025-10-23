# Very small wrapper. Replace `call_llm` body with your provider code.
import os
import httpx
from typing import Dict

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")  # just a flag

async def call_llm(prompt: str, max_tokens: int = 400) -> Dict:
    """
    Replace this with actual OpenAI / other provider integration.
    For local testing, return a deterministic canned response.
    """
    # Example placeholder synchronous
    # In production, use httpx.AsyncClient and provider's API.
    # Return dict { "text": "...", "raw": {...} }
    # For now return canned:
    return {
        "text": "LLM placeholder: Based on the ticket this needs an AI code patch. Proposed change: update function X to handle Y.",
        "raw": {}
    }
