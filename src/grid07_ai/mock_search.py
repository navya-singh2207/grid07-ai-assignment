from __future__ import annotations

from langchain_core.tools import tool


@tool
def mock_searxng_search(query: str) -> list[str]:
    """
    Hardcoded "recent news headlines" keyed off simple keywords.
    Returns a list of headlines (strings).
    """
    q = (query or "").lower()

    headlines: list[str] = []
    if any(k in q for k in ["crypto", "bitcoin", "eth", "ethereum", "etf"]):
        headlines.extend(
            [
                "Bitcoin hits new all-time high amid regulatory ETF approvals",
                "Crypto exchanges report surge in spot volumes as volatility returns",
            ]
        )
    if any(k in q for k in ["ai", "openai", "model", "llm", "agents"]):
        headlines.extend(
            [
                "OpenAI unveils a new model focused on reasoning and tool use",
                "Software teams debate AI coding assistants as copilots, not replacements",
            ]
        )
    if any(k in q for k in ["ev", "electric vehicle", "battery", "tesla"]):
        headlines.extend(
            [
                "Study finds EV battery degradation slower than expected under modern thermal management",
                "Automakers expand battery warranties as long-term data improves",
            ]
        )
    if any(k in q for k in ["rates", "inflation", "fed", "interest"]):
        headlines.extend(
            [
                "Markets reprice rate-cut expectations after sticky inflation print",
                "Bond yields jump as investors digest central bank commentary",
            ]
        )

    if not headlines:
        headlines = [
            "Analysts weigh near-term macro uncertainty as tech earnings approach",
            "Regulators consider new rules for data privacy and AI transparency",
        ]

    return headlines[:5]

