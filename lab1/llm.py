"""Shared client setup: pick Anthropic or OpenRouter at runtime.

Set LLM_PROVIDER in .env (or on the command line) to "anthropic" or "openrouter":

    LLM_PROVIDER=openrouter python pattern1_single_agent.py

OpenRouter exposes an Anthropic-compatible Messages endpoint, so the same
`anthropic` SDK calls (including tool use) work unchanged; only the base URL,
auth header and model name differ.
"""
import os
import sys

import anthropic
from dotenv import load_dotenv

load_dotenv()  # values already in the shell environment take precedence

PROVIDER = os.getenv("LLM_PROVIDER", "anthropic").strip().lower()

if PROVIDER == "anthropic":
    API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-6")
    client = anthropic.Anthropic(api_key=API_KEY or None)
elif PROVIDER == "openrouter":
    API_KEY = os.getenv("OPENROUTER_API_KEY", "")
    MODEL = os.getenv("OPENROUTER_MODEL", "anthropic/claude-sonnet-4.6")
    client = anthropic.Anthropic(
        base_url="https://openrouter.ai/api",
        auth_token=API_KEY or None,  # sent as "Authorization: Bearer <key>"
        api_key=None,
    )
else:
    sys.exit(f"Unknown LLM_PROVIDER '{PROVIDER}'. Use 'anthropic' or 'openrouter'.")

print(f"[llm] provider={PROVIDER} model={MODEL}")


def text_of(response) -> str:
    """Join the text blocks of a response.

    Reasoning models (e.g. many OpenRouter models) return "thinking" blocks
    before the text, so response.content[0] is not always a text block.
    """
    text = "".join(b.text for b in response.content if b.type == "text")
    if not text and response.stop_reason == "max_tokens":
        return "[no text: hit max_tokens while thinking - raise max_tokens]"
    return text
