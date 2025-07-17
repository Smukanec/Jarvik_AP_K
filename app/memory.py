from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parent.parent
MEMORY_DIR = BASE_DIR / 'memory'


def get_memory_path(user: str) -> Path:
    user_dir = MEMORY_DIR / user
    user_dir.mkdir(parents=True, exist_ok=True)
    return user_dir / 'action_plan.jsonl'


def load_memory(user: str):
    path = get_memory_path(user)
    records = []
    if path.exists():
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                records.append(json.loads(line))
    return records


def save_record(user: str, record: dict):
    path = get_memory_path(user)
    with open(path, 'a', encoding='utf-8') as f:
        f.write(json.dumps(record, ensure_ascii=False) + '\n')


def save_memory(user: str, records: list):
    """Rewrite the entire memory file with the provided records."""
    path = get_memory_path(user)
    with open(path, 'w', encoding='utf-8') as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False) + '\n')
