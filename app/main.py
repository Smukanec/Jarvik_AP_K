from flask import Flask, request, jsonify, send_from_directory
from pathlib import Path
import json
from .memory import load_memory, save_record
from .rag_engine import find_similar

app = Flask(__name__, static_folder='../static')

@app.route('/action_plan', methods=['POST'])
def action_plan():
    data = request.get_json(force=True)
    text = data.get('text', '')
    user = data.get('user', 'default')
    memory = load_memory(user)

    # simple parse: split into sentences for demo
    parts = text.split('.')
    record = {
        'id': f"AP-{len(memory)+1:03d}",
        'traceability': parts[0].strip() if parts else '',
        'problem': parts[1].strip() if len(parts) > 1 else '',
        'cause': parts[2].strip() if len(parts) > 2 else '',
        'action': parts[3].strip() if len(parts) > 3 else '',
        'responsible': '',
        'date': '',
        'effectiveness': '',
        'closed': False
    }

    similar = find_similar(record, memory)
    if similar is not None:
        # For simplicity, just append new record
        pass
    save_record(user, record)
    memory.append(record)
    return jsonify({'record': record, 'similar': similar})

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('../static', path)

if __name__ == '__main__':
    app.run(debug=True)
