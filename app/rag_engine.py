import re
from typing import List, Dict, Optional, Tuple


def tokenize(text: str):
    return set(re.findall(r'\b\w+\b', text.lower()))


def jaccard(s1: set, s2: set) -> float:
    if not s1 or not s2:
        return 0.0
    return len(s1 & s2) / len(s1 | s2)


def find_similar(record: Dict, memory: List[Dict]) -> Tuple[Optional[Dict], float]:
    """Return the most similar record from memory and its similarity score.

    The similarity is computed using Jaccard distance on tokenized problem
    descriptions. If the best score is below ``0.5`` no record is considered a
    valid match and ``None`` is returned for the record.
    """

    tokens = tokenize(record.get('problem', ''))
    best = None
    best_score = 0.0

    for r in memory:
        score = jaccard(tokens, tokenize(r.get('problem', '')))
        if score > best_score:
            best_score = score
            best = r

    if best_score > 0.5:
        return best, best_score
    return None, best_score
