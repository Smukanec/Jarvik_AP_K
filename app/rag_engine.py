import re
from typing import List, Dict, Optional, Tuple

from .embedder import embed, cosine_similarity


def tokenize(text: str):
    return set(re.findall(r'\b\w+\b', text.lower()))


def jaccard(s1: set, s2: set) -> float:
    if not s1 or not s2:
        return 0.0
    return len(s1 & s2) / len(s1 | s2)


def find_similar(record: Dict, memory: List[Dict]) -> Tuple[Optional[Dict], float]:
    """Return the most similar record from memory and its similarity score.

    Similarity is computed using both Jaccard distance on tokens and cosine
    similarity on text embeddings. The higher of the two scores is used.
    If the best score is below ``0.5`` no record is considered a valid match.
    """

    tokens = tokenize(record.get("problem", ""))
    emb = embed(record.get("problem", ""))
    best = None
    best_score = 0.0

    for r in memory:
        j_score = jaccard(tokens, tokenize(r.get("problem", "")))
        r_emb = r.get("embedding")
        if r_emb is None:
            r_emb = embed(r.get("problem", ""))
            r["embedding"] = r_emb
        e_score = cosine_similarity(emb, r_emb)
        score = max(j_score, e_score)
        if score > best_score:
            best_score = score
            best = r

    if best_score > 0.5:
        return best, best_score
    return None, best_score
