import re

LABEL_RE = re.compile(r'(traceability|problem|cause|action)\s*[:\-]\s*', re.IGNORECASE)


def parse_text(text: str) -> dict:
    """Parse raw input text into structured sections.

    The function first looks for explicit labels like ``Traceability:``,
    ``Problem:``, etc. When no labels are found, it falls back to
    sentence-based splitting using regex to recognise sentence boundaries.
    """
    sections = {"traceability": "", "problem": "", "cause": "", "action": ""}

    matches = list(LABEL_RE.finditer(text))
    if matches:
        for idx, match in enumerate(matches):
            label = match.group(1).lower()
            start = match.end()
            end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
            part = text[start:end].strip()
            sections[label] = part.rstrip(" .;!-?")
        return sections

    # fallback: split by sentence boundaries
    sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', text) if s.strip()]
    keys = ["traceability", "problem", "cause", "action"]
    for key, sentence in zip(keys, sentences):
        sections[key] = sentence.rstrip(" .;!?")
    return sections
