import re
from typing import List, Dict, Optional


def tokenize(text: str):
    return set(re.findall(r'\b\w+\b', text.lower()))


def jaccard(s1: set, s2: set) -> float:
    if not s1 or not s2:
        return 0.0
    return len(s1 & s2) / len(s1 | s2)


def find_similar(record: Dict, memory: List[Dict]) -> Optional[Dict]:
    tokens = tokenize(record.get('problem', ''))
    best = None
    best_score = 0.0
    for r in memory:
        score = jaccard(tokens, tokenize(r.get('problem', '')))
        if score > best_score:
            best_score = score
            best = r
    if best_score > 0.5:
        return best
    return None
