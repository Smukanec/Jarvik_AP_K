from flask import Flask, request, jsonify, send_from_directory
from pathlib import Path
import json
from .memory import load_memory, save_record, save_memory
from .rag_engine import find_similar
from .parser import parse_text

app = Flask(__name__, static_folder='../static')

SIMILARITY_THRESHOLD = 0.8

@app.route('/action_plan', methods=['POST'])
def action_plan():
    data = request.get_json(force=True)
    text = data.get('text', '')
    user = data.get('user', 'default')
    memory = load_memory(user)

    # parse using the dedicated parser
    sections = parse_text(text)
    record = {
        'id': f"AP-{len(memory)+1:03d}",
        'traceability': sections.get('traceability', ''),
        'problem': sections.get('problem', ''),
        'cause': sections.get('cause', ''),
        'action': sections.get('action', ''),
        'responsible': '',
        'date': '',
        'effectiveness': '',
        'closed': False
    }

    similar, score = find_similar(record, memory)
    if similar is not None and score >= SIMILARITY_THRESHOLD:
        # Update existing record instead of creating a new one
        record['id'] = similar['id']
        similar.update(record)
        save_memory(user, memory)
        record = similar
    else:
        save_record(user, record)
        memory.append(record)

    return jsonify({'record': record, 'similar': similar, 'score': score})

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('../static', path)

if __name__ == '__main__':
    app.run(debug=True)
