# Agentic Workshop

| Lab | Folder | What it is |
| --- | --- | --- |
| 1 | [`lab1/`](lab1) | Compact agent architectures: single agent, supervisor/worker, peer-to-peer (plain Python, Anthropic Messages API) |
| 2 | [`lab2/`](lab2) | RAG lab starter notebook: classic RAG, document-aware, multimodal, long context, tree navigation, agentic RAG |

## Setup (both labs)

Requires Python 3.10+. One shared virtual environment at the repo root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt   # or lab1/requirements.txt / lab2/requirements.txt for one lab
cp .env.example .env              # then add your key(s)
```

In VS Code, pick `./.venv/bin/python` as the interpreter (and as the notebook kernel for Lab 2).

## Lab 1: Compact agent architectures

| Script | Pattern |
| --- | --- |
| `lab1/pattern1_single_agent.py` | Single agent with tools (calculator + mock config reader) |
| `lab1/pattern2_supervisor.py` | Supervisor delegating to Coder and Security Auditor workers |
| `lab1/pattern3_peertopeer.py` | Peer-to-peer draft/critique refinement loop |

```bash
python lab1/check_setup.py
python lab1/pattern1_single_agent.py
```

`lab1/llm.py` lets you switch between **Anthropic** and **OpenRouter** at runtime. Set `LLM_PROVIDER` in `.env`, or per run:

```bash
LLM_PROVIDER=openrouter python lab1/pattern1_single_agent.py
```

| Variable | Default |
| --- | --- |
| `LLM_PROVIDER` | `anthropic` (or `openrouter`) |
| `ANTHROPIC_API_KEY` / `ANTHROPIC_MODEL` | – / `claude-sonnet-4-6` |
| `OPENROUTER_API_KEY` / `OPENROUTER_MODEL` | – / `anthropic/claude-sonnet-4.6` |

OpenRouter is called through its Anthropic-compatible endpoint, so tool use works unchanged. `text_of()` skips the "thinking" blocks that reasoning models return before their text. In VS Code, the Run and Debug configurations ask which provider to use.

## Lab 2: RAG lab

Open `lab2/RAG_Lab_Starter.ipynb` and run the cells in order. All model calls go through OpenRouter and read `OPENROUTER_API_KEY` from the environment (VS Code loads it from `.env`). The notebook downloads its two documents into `lab2/` on first run; the embedding model runs locally on CPU.
