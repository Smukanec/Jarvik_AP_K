import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app
from app.parser import parse_text


def test_action_plan_post():
    client = app.test_client()
    response = client.post('/action_plan', json={
        'text': 'Testovací problém s páčkou WI',
        'user': 'test'
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'record' in data
    assert 'id' in data['record']


def test_parse_multi_sentence():
    text = (
        "Traceability: TR01. Problem: Something is wrong. It fails! "
        "Cause: Unknown. Action: Restart system."
    )
    result = parse_text(text)
    assert result['traceability'] == 'TR01'
    assert result['problem'] == 'Something is wrong. It fails!'
    assert result['cause'] == 'Unknown'
    assert result['action'] == 'Restart system'


def test_parse_edge_punctuation():
    text = "Traceability - TR02? Problem - gear stuck! Cause - worn part. Action - replace it."
    result = parse_text(text)
    assert result['traceability'] == 'TR02'
    assert result['problem'] == 'gear stuck!'
    assert result['cause'] == 'worn part'
    assert result['action'] == 'replace it'


def test_duplicate_detection(tmp_path):
    user = 'dup_test'
    mem_dir = tmp_path / 'memory'
    os.makedirs(mem_dir / user)
    # patch memory directory in app.memory for test
    from app import memory as memory_mod
    old_dir = memory_mod.MEMORY_DIR
    memory_mod.MEMORY_DIR = mem_dir

    client = app.test_client()
    text1 = 'Traceability: TR01. Problem: lever stuck. Cause: unknown. Action: fix.'
    text2 = 'Traceability: TR01. Problem: lever stuck. Cause: rust. Action: grease.'

    r1 = client.post('/action_plan', json={'text': text1, 'user': user})
    assert r1.status_code == 200
    r2 = client.post('/action_plan', json={'text': text2, 'user': user})
    assert r2.status_code == 200

    memory = memory_mod.load_memory(user)
    assert len(memory) == 1
    assert memory[0]['cause'] == 'rust'

    # restore original directory
    memory_mod.MEMORY_DIR = old_dir
