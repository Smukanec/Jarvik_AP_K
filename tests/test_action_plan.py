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
    assert 'id' in data
    assert 'problem' in data


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
