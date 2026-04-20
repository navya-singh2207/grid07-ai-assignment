from __future__ import annotations

from grid07_ai.llm import generate_defense_reply_text


def generate_defense_reply(
    bot_persona: str,
    parent_post: str,
    comment_history: list[str],
    human_reply: str,
) -> str:
    """
    Phase 3 entrypoint per assignment:
    - Feeds the exact thread context
    - Defends persona against prompt injection
    """
    reply, _info = generate_defense_reply_text(
        bot_persona_text=bot_persona,
        parent_post=parent_post,
        comment_history=comment_history,
        human_reply=human_reply,
    )
    return reply

