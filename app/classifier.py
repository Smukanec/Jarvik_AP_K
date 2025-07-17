# Optional text classifier placeholder

def classify(text: str) -> str:
    """Return one of: traceability, problem, cause, action"""
    # simple heuristic: choose by keywords
    t = text.lower()
    if 'proto' in t:
        return 'traceability'
    if 'řešení' in t or 'solution' in t:
        return 'action'
    if 'příčina' in t or 'cause' in t:
        return 'cause'
    return 'problem'
