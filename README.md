# Grid07 AI Engineering Assignment (Cognitive Routing & RAG)

This repo implements the three required phases:

- **Phase 1**: Vector-based persona matching router using cosine similarity over embeddings.
- **Phase 2**: LangGraph autonomous content engine (Decide Search → Mock Web Search → Draft Post) with **strict JSON output**.
- **Phase 3**: Deep thread “combat engine” reply that includes full context and **defends against prompt injection** via system-level constraints.

## Setup

```bash
cd grid07-ai-assignment
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
cp .env.example .env
```

Then set either `OPENAI_API_KEY` (recommended) or configure Ollama variables.

## Run the demo (generates logs)

```bash
python -m grid07_ai.demo
```

This writes `execution_logs.md` in the repo root and prints the same output to console.

## LangGraph node structure (Phase 2)

The graph is a linear 3-node state machine:

- **Decide Search**: LLM chooses a topic + produces a search query from the bot persona.
- **Web Search**: `mock_searxng_search()` returns hardcoded “recent headline” context.
- **Draft Post**: LLM generates an opinionated ~280 character post **as strict JSON**:
  `{"bot_id":"...","topic":"...","post_content":"..."}`

## Prompt-injection defense (Phase 3)

`generate_defense_reply()` uses:

- A **system message** that locks persona/role and explicitly rejects instruction hierarchy overrides.
- A **thread-context block** containing the parent post + comment history + latest human reply.
- A response directive to **ignore attempts to rewrite the system/persona**, and to continue arguing naturally.

## Files

- `src/grid07_ai/personas.py`: Bot persona definitions.
- `src/grid07_ai/embeddings.py`: Embedding backend (OpenAI if configured; otherwise SentenceTransformers).
- `src/grid07_ai/router.py`: `route_post_to_bots()`.
- `src/grid07_ai/mock_search.py`: `mock_searxng_search()` tool.
- `src/grid07_ai/content_graph.py`: LangGraph orchestration for Phase 2.
- `src/grid07_ai/combat.py`: `generate_defense_reply()` for Phase 3.
- `src/grid07_ai/demo.py`: Runs all phases and writes `execution_logs.md`.

