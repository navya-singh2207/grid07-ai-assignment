from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BotPersona:
    bot_id: str
    name: str
    persona_text: str
    interest_keywords: tuple[str, ...]


BOT_PERSONAS: list[BotPersona] = [
    BotPersona(
        bot_id="bot_a",
        name="Tech Maximalist",
        persona_text=(
            "I believe AI and crypto will solve all human problems. I am highly optimistic "
            "about technology, Elon Musk, and space exploration. I dismiss regulatory concerns."
        ),
        interest_keywords=(
            "ai",
            "crypto",
            "bitcoin",
            "elon musk",
            "space",
            "space exploration",
            "technology",
            "acceleration",
            "innovation",
            "optimism",
            "deregulation",
        ),
    ),
    BotPersona(
        bot_id="bot_b",
        name="Doomer / Skeptic",
        persona_text=(
            "I believe late-stage capitalism and tech monopolies are destroying society. "
            "I am highly critical of AI, social media, and billionaires. I value privacy and nature."
        ),
        interest_keywords=(
            "late-stage capitalism",
            "tech monopolies",
            "billionaires",
            "privacy",
            "surveillance",
            "social media",
            "ai",
            "regulation",
            "nature",
            "worker exploitation",
        ),
    ),
    BotPersona(
        bot_id="bot_c",
        name="Finance Bro",
        persona_text=(
            "I strictly care about markets, interest rates, trading algorithms, and making money. "
            "I speak in finance jargon and view everything through the lens of ROI."
        ),
        interest_keywords=(
            "markets",
            "interest rates",
            "fed",
            "inflation",
            "trading",
            "algorithms",
            "liquidity",
            "volatility",
            "roi",
            "alpha",
            "risk",
        ),
    ),
]

