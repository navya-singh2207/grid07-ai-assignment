from __future__ import annotations

from dataclasses import dataclass
from typing import TypedDict

from langgraph.graph import StateGraph, END

from grid07_ai.llm import DraftedPost, draft_post_strict_json
from grid07_ai.mock_search import mock_searxng_search
from grid07_ai.personas import BotPersona


class ContentState(TypedDict, total=False):
    bot_id: str
    persona_text: str
    topic: str
    search_query: str
    search_results: list[str]
    drafted: DraftedPost
    llm_backend: str


@dataclass(frozen=True)
class DecideSearchResult:
    topic: str
    search_query: str


def _decide_search(persona: BotPersona) -> DecideSearchResult:
    """
    Deterministic decide-search step.
    (Kept deterministic so the pipeline runs even without external LLM access.)
    """
    p = persona.persona_text.lower()
    if "finance" in p or "markets" in p or "interest rates" in p or "roi" in p:
        return DecideSearchResult(topic="markets", search_query="interest rates inflation AI trading")
    if "crypto" in p:
        return DecideSearchResult(topic="crypto", search_query="crypto ETF approvals bitcoin AI")
    if "privacy" in p or "monopolies" in p:
        return DecideSearchResult(topic="privacy", search_query="AI monopoly privacy regulation")
    return DecideSearchResult(topic="AI", search_query="OpenAI new model agents software jobs")


def build_content_graph():
    g = StateGraph(ContentState)

    def node_decide_search(state: ContentState) -> ContentState:
        persona_text = state["persona_text"]
        bot_id = state["bot_id"]
        # We only have persona text in state here, so choose based on that.
        # The outer call will pass persona text from a BotPersona.
        fake_persona = BotPersona(bot_id=bot_id, name="bot", persona_text=persona_text, interest_keywords=())
        res = _decide_search(fake_persona)
        return {"topic": res.topic, "search_query": res.search_query}

    def node_web_search(state: ContentState) -> ContentState:
        results = mock_searxng_search.invoke({"query": state["search_query"]})
        return {"search_results": results}

    def node_draft_post(state: ContentState) -> ContentState:
        drafted, info = draft_post_strict_json(
            bot_id=state["bot_id"],
            persona_text=state["persona_text"],
            search_results=state.get("search_results", []),
        )
        return {"drafted": drafted, "llm_backend": info.name}

    g.add_node("decide_search", node_decide_search)
    g.add_node("web_search", node_web_search)
    g.add_node("draft_post", node_draft_post)

    g.set_entry_point("decide_search")
    g.add_edge("decide_search", "web_search")
    g.add_edge("web_search", "draft_post")
    g.add_edge("draft_post", END)

    return g.compile()


def generate_bot_post_json(persona: BotPersona) -> tuple[dict, str]:
    """
    Runs Phase 2 and returns:
    - strict JSON dict: {"bot_id": "...", "topic": "...", "post_content": "..."}
    - backend name (for logs)
    """
    app = build_content_graph()
    out = app.invoke({"bot_id": persona.bot_id, "persona_text": persona.persona_text})
    drafted: DraftedPost = out["drafted"]
    payload = drafted.model_dump()
    return payload, out.get("llm_backend", "unknown")

