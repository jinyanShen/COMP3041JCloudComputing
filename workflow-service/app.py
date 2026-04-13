from flask import Flask, request, jsonify
import requests
import uuid
import json

app = Flask(__name__)
DATA_SERVICE_URL = "http://localhost:5001"
SERVERLESS_URL = "http://localhost:9000"

@app.route('/submit', methods=['POST'])
def submit():
    form_data = request.json

    print(f"Received submission: {form_data}")

    # 1. 创建记录
    response = requests.post(f"{DATA_SERVICE_URL}/create", json=form_data)
    record_id = response.json()['id']
    print(f"Created record: {record_id}")

    # 2. 调用 Serverless Process 函数
    try:
        print(f"Calling serverless process at {SERVERLESS_URL}/process")
        process_resp = requests.post(f"{SERVERLESS_URL}/process", json=form_data, timeout=10)
        print(f"Process response status: {process_resp.status_code}")
        print(f"Process response body: {process_resp.text}")

        if process_resp.status_code == 200:
            result = process_resp.json()
            print(f"Processing result: {result}")

            # 3. 调用 Serverless Update 函数
            update_resp = requests.post(f"{SERVERLESS_URL}/update", json={
                'record_id': record_id,
                'result': result
            }, timeout=10)
            print(f"Update response: {update_resp.status_code}")
        else:
            print(f"Process failed with status: {process_resp.status_code}")

    except Exception as e:
        print(f"Error: {e}")
        # 如果 serverless 失败，设置一个默认结果
        default_result = {
            'status': 'INCOMPLETE',
            'category': 'GENERAL',
            'priority': 'NORMAL',
            'note': 'Processing failed. Please try again.'
        }
        requests.put(f"{DATA_SERVICE_URL}/update/{record_id}", json=default_result)

    return jsonify({'record_id': record_id, 'status': 'submitted'})

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    print("Workflow Service running on http://localhost:5002")
    app.run(port=5002, host='0.0.0.0', debug=True)