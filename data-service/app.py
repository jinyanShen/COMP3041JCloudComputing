from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)
db = {}

@app.route('/create', methods=['POST'])
def create():
    data = request.json
    record_id = str(uuid.uuid4())
    db[record_id] = data
    return jsonify({'id': record_id})

@app.route('/get/<record_id>', methods=['GET'])
def get(record_id):
    return jsonify(db.get(record_id, {}))

@app.route('/update/<record_id>', methods=['PUT'])
def update(record_id):
    data = request.json
    if record_id in db:
        db[record_id].update(data)
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(port=5001, host='0.0.0.0')