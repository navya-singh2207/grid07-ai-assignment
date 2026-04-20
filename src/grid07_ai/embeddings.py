from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Protocol

import numpy as np
from dotenv import load_dotenv


class Embedder(Protocol):
    def embed_documents(self, texts: list[str]) -> list[list[float]]: ...

    def embed_query(self, text: str) -> list[float]: ...


@dataclass(frozen=True)
class EmbeddingBackendInfo:
    name: str


def get_embedder() -> tuple[Embedder, EmbeddingBackendInfo]:
    """
    Returns an embedder with a consistent interface.

    Preference order:
    1) OpenAI embeddings when OPENAI_API_KEY is set
    2) Fully-offline hashing embedder otherwise (no downloads)
    """

    load_dotenv()

    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key:
        from langchain_openai import OpenAIEmbeddings

        model = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
        return OpenAIEmbeddings(model=model), EmbeddingBackendInfo(name=f"openai:{model}")

    dim = int(os.getenv("HASH_EMBED_DIM", "384"))

    def _tokenize(text: str) -> list[str]:
        return [t for t in "".join(ch.lower() if ch.isalnum() else " " for ch in text).split() if t]

    class _HashingEmbedder:
        def embed_documents(self, texts: list[str]) -> list[list[float]]:
            return [self.embed_query(t) for t in texts]

        def embed_query(self, text: str) -> list[float]:
            v = np.zeros((dim,), dtype=np.float32)
            for tok in _tokenize(text):
                # deterministic hashed bag-of-words (non-negative counts)
                h = hash(tok)
                idx = h % dim
                v[idx] += 1.0
            norm = np.linalg.norm(v)
            if norm != 0:
                v = v / norm
            return v.tolist()

    return _HashingEmbedder(), EmbeddingBackendInfo(name=f"hashing:{dim}")


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    a = a.astype(np.float32)
    b = b.astype(np.float32)
    denom = (np.linalg.norm(a) * np.linalg.norm(b))
    if denom == 0:
        return 0.0
    return float(np.dot(a, b) / denom)

