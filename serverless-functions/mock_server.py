from flask import Flask, request, jsonify
import json
import re
import requests

app = Flask(__name__)

def process_event(data):
    """The logic for handling events"""
    # 1. Check the required fields
    required = ['title', 'description', 'location', 'date', 'organiser']
    for field in required:
        if field not in data or not data[field]:
            return {
                'status': 'INCOMPLETE',
                'category': None,
                'priority': None,
                'note': f'Missing required field: {field}'
            }

    # 2. Check the date format
    if not re.match(r'\d{4}-\d{2}-\d{2}', data['date']):
        return {
            'status': 'NEEDS REVISION',
            'category': 'GENERAL',
            'priority': 'NORMAL',
            'note': 'Invalid date format. Use YYYY-MM-DD.'
        }

    # 3. Check the length of the description
    if len(data['description']) < 40:
        return {
            'status': 'NEEDS REVISION',
            'category': 'GENERAL',
            'priority': 'NORMAL',
            'note': f'Description must be at least 40 characters. Current: {len(data["description"])}'
        }

    # 4. Secretary
    text = (data.get('title', '') + ' ' + data.get('description', '')).lower()

    if any(k in text for k in ['career', 'internship', 'recruitment']):
        cat, pri = 'OPPORTUNITY', 'HIGH'
    elif any(k in text for k in ['workshop', 'seminar', 'lecture']):
        cat, pri = 'ACADEMIC', 'MEDIUM'
    elif any(k in text for k in ['club', 'society', 'social']):
        cat, pri = 'SOCIAL', 'NORMAL'
    else:
        cat, pri = 'GENERAL', 'NORMAL'

    return {
        'status': 'APPROVED',
        'category': cat,
        'priority': pri,
        'note': 'All checks passed. Event approved.'
    }

@app.route('/process', methods=['POST'])
def process():
    """simulate Processing Function"""
    data = request.json
    result = process_event(data)
    return jsonify(result)

@app.route('/update', methods=['POST'])
def update():
    """simulate Result Update Function"""
    data = request.json
    record_id = data.get('record_id')
    result = data.get('result', {})

    # Call the Data Service to update
    update_url = f"http://localhost:5001/update/{record_id}"
    try:
        response = requests.put(update_url, json=result)
        return jsonify({'status': 'updated', 'message': 'OK'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    print("Mock Serverless Functions running on http://localhost:9000")
    print("  - POST /process - Process event data")
    print("  - POST /update - Update record with result")
    app.run(port=9000, host='0.0.0.0', debug=True)