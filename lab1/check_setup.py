# Setup & API primer (0:00-0:15): verifies Python, packages, API key, and model access.
import sys

import anthropic

from llm import API_KEY, MODEL, PROVIDER, client, text_of

print(f"Python {sys.version.split()[0]}  |  anthropic SDK {anthropic.__version__}")

if not API_KEY or API_KEY.endswith("your-key-here"):
    var = "OPENROUTER_API_KEY" if PROVIDER == "openrouter" else "ANTHROPIC_API_KEY"
    sys.exit(f"{var} is not set. Put your real key in .env and run again.")

res = client.messages.create(
    model=MODEL,
    max_tokens=1024,
    messages=[{"role": "user", "content": "Reply with exactly: API connection OK"}],
)
print(f"{PROVIDER} / {MODEL} says: {text_of(res)}")
