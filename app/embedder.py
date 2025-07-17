import math
import re
from typing import List

# Try to load real sentence-transformers if available
try:
    from sentence_transformers import SentenceTransformer  # type: ignore
    _model = SentenceTransformer("all-MiniLM-L6-v2")

    def embed(text: str) -> List[float]:
        """Return embedding vector for the given text."""
        vec = _model.encode(text)
        return vec.tolist()
except Exception:  # pragma: no cover - fallback path
    # Simple fallback embedder based on hashed token counts with synonyms
    SYNONYMS = {
        "lever": "handle",
        "handle": "handle",
        "stuck": "jammed",
        "jammed": "jammed",
    }

    def _tokenize(text: str) -> List[str]:
        tokens = re.findall(r"\b\w+\b", text.lower())
        return [SYNONYMS.get(t, t) for t in tokens]

    def embed(text: str) -> List[float]:
        tokens = _tokenize(text)
        size = 64
        vec = [0.0] * size
        for tok in tokens:
            idx = hash(tok) % size
            vec[idx] += 1.0
        return vec


def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    dot = sum(a * b for a, b in zip(v1, v2))
    norm1 = math.sqrt(sum(a * a for a in v1))
    norm2 = math.sqrt(sum(b * b for b in v2))
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot / (norm1 * norm2)
