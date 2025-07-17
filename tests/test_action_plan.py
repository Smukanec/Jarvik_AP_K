import json
from app.main import app


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
