from __future__ import annotations

from dataclasses import dataclass
import os
import re

import numpy as np

from grid07_ai.embeddings import get_embedder
from grid07_ai.personas import BOT_PERSONAS, BotPersona


@dataclass(frozen=True)
class RoutedBot:
    bot: BotPersona
    similarity: float


class InMemoryVectorStore:
    def __init__(self) -> None:
        self._vectors: dict[str, np.ndarray] = {}

    def add(self, key: str, vector: list[float]) -> None:
        v = np.asarray(vector, dtype=np.float32)
        # store normalized vectors to make cosine similarity = dot product
        norm = np.linalg.norm(v)
        if norm != 0:
            v = v / norm
        self._vectors[key] = v

    def query(self, vector: list[float], top_k: int | None = None) -> list[tuple[str, float]]:
        q = np.asarray(vector, dtype=np.float32)
        norm = np.linalg.norm(q)
        if norm != 0:
            q = q / norm

        scored: list[tuple[str, float]] = [(k, float(np.dot(q, v))) for k, v in self._vectors.items()]
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored if top_k is None else scored[:top_k]


_STOPWORDS = {
    "i",
    "am",
    "a",
    "an",
    "and",
    "are",
    "as",
    "about",
    "all",
    "after",
    "at",
    "be",
    "by",
    "can",
    "do",
    "for",
    "from",
    "in",
    "is",
    "it",
    "just",
    "me",
    "my",
    "of",
    "on",
    "or",
    "that",
    "the",
    "this",
    "to",
    "will",
    "with",
    "you",
    "your",
}


def _tokenize(text: str) -> list[str]:
    toks = re.findall(r"[a-z0-9]+", (text or "").lower())
    return [t for t in toks if t not in _STOPWORDS]


class _PersonaVocabEmbedder:
    """
    Offline embedder designed specifically for Phase 1.
    Builds a vocabulary from persona texts and embeds as a binary presence vector.
    This makes cosine similarity behave like "topic overlap", and is fully offline.
    """

    def __init__(self, vocab: list[str]) -> None:
        self.vocab = vocab
        self.index = {t: i for i, t in enumerate(vocab)}

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [self.embed_query(t) for t in texts]

    def embed_query(self, text: str) -> list[float]:
        v = np.zeros((len(self.vocab),), dtype=np.float32)
        for tok in set(_tokenize(text)):
            idx = self.index.get(tok)
            if idx is not None:
                v[idx] = 1.0
        # normalize so cosine = dot
        n = np.linalg.norm(v)
        if n != 0:
            v = v / n
        return v.tolist()


def build_persona_store() -> tuple[InMemoryVectorStore, dict[str, BotPersona], str]:
    store = InMemoryVectorStore()

    personas_by_id = {p.bot_id: p for p in BOT_PERSONAS}

    # If an online embedding backend is configured, use it.
    # Otherwise, use the offline persona-vocabulary embedder (no network/downloads).
    if os.getenv("OPENAI_API_KEY"):
        embedder, info = get_embedder()
        vectors = embedder.embed_documents([p.persona_text for p in BOT_PERSONAS])
        backend = info.name
    else:
        keyword_docs = [" ".join(p.interest_keywords) for p in BOT_PERSONAS]
        vocab = sorted(set(tok for doc in keyword_docs for tok in _tokenize(doc)))
        embedder = _PersonaVocabEmbedder(vocab)
        vectors = embedder.embed_documents(keyword_docs)
        backend = f"persona-vocab:{len(vocab)}"

    for p, vec in zip(BOT_PERSONAS, vectors, strict=True):
        store.add(p.bot_id, vec)

    return store, personas_by_id, backend


def route_post_to_bots(post_content: str, threshold: float = 0.85) -> list[RoutedBot]:
    """
    Embed the post and return bots whose persona similarity exceeds threshold.
    """
    store, personas_by_id, backend = build_persona_store()
    # Use same embedding strategy as store.
    if backend.startswith("persona-vocab:"):
        keyword_docs = [" ".join(p.interest_keywords) for p in BOT_PERSONAS]
        vocab = sorted(set(tok for doc in keyword_docs for tok in _tokenize(doc)))
        embedder = _PersonaVocabEmbedder(vocab)
        q = embedder.embed_query(post_content)
    else:
        embedder, _info = get_embedder()
        q = embedder.embed_query(post_content)
    matches = store.query(q)
    routed: list[RoutedBot] = []
    for bot_id, sim in matches:
        if sim > threshold:
            routed.append(RoutedBot(bot=personas_by_id[bot_id], similarity=sim))
    return routed

