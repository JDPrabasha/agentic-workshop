# Agentic Workshop – Lab 3.1: Compact Agent Architectures

Three multi-agent patterns built with plain Python and the Anthropic Messages API (no frameworks):

| Script | Pattern |
| --- | --- |
| `pattern1_single_agent.py` | Single agent with tools (calculator + mock config reader) |
| `pattern2_supervisor.py` | Supervisor delegating to Coder and Security Auditor workers |
| `pattern3_peertopeer.py` | Peer-to-peer draft/critique refinement loop |

`llm.py` lets you switch between **Anthropic** and **OpenRouter** at runtime.

## Setup

Requires Python 3.10+.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then add your key(s)
```

## Run

```bash
python check_setup.py
python pattern1_single_agent.py
```

## Switching provider

Set `LLM_PROVIDER` in `.env`, or per run:

```bash
LLM_PROVIDER=openrouter python pattern1_single_agent.py
```

| Variable | Default |
| --- | --- |
| `LLM_PROVIDER` | `anthropic` (or `openrouter`) |
| `ANTHROPIC_API_KEY` / `ANTHROPIC_MODEL` | – / `claude-sonnet-4-6` |
| `OPENROUTER_API_KEY` / `OPENROUTER_MODEL` | – / `anthropic/claude-sonnet-4.6` |

OpenRouter is called through its Anthropic-compatible endpoint, so tool use works unchanged. `text_of()` in `llm.py` skips the "thinking" blocks that reasoning models return before their text.

In VS Code, the Run and Debug configurations ask which provider to use.
