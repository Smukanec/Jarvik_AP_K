import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app
from app import memory as memory_mod


def test_embedding_similarity(tmp_path):
    user = 'emb_test'
    mem_dir = tmp_path / 'memory'
    os.makedirs(mem_dir / user)
    old_dir = memory_mod.MEMORY_DIR
    memory_mod.MEMORY_DIR = mem_dir

    client = app.test_client()
    text1 = 'Traceability: TR01. Problem: lever stuck. Cause: unknown. Action: fix.'
    text2 = 'Traceability: TR01. Problem: handle jammed. Cause: rust. Action: grease.'

    r1 = client.post('/action_plan', json={'text': text1, 'user': user})
    assert r1.status_code == 200
    r2 = client.post('/action_plan', json={'text': text2, 'user': user})
    assert r2.status_code == 200
    data = json.loads(r2.data)
    assert data['score'] > 0.5

    memory = memory_mod.load_memory(user)
    assert len(memory) == 1

    memory_mod.MEMORY_DIR = old_dir
