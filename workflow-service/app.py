from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

DATA_SERVICE_URL = "http://localhost:5001"

# mock address
MOCK_URL = "http://localhost:9000"

# cloud processing
CLOUD_PROCESSING_URL = "https://cloudcomputing-ifgmaptzqs.cn-hangzhou.fcapp.run"


@app.route('/submit', methods=['POST'])
def submit():
    form_data = request.json or {}

    for key in form_data:
        if isinstance(form_data[key], str):
            form_data[key] = form_data[key].strip()

    print(f"[Workflow] Received submission: {form_data}")

    try:
        response = requests.post(f"{DATA_SERVICE_URL}/create", json=form_data, timeout=5)
        response.raise_for_status()
        record_id = response.json().get('id')
    except Exception as e:
        print(f"[Workflow] Data service error: {e}")
        return jsonify({'error': 'Failed to create record'}), 500

    print(f"[Workflow] Created record: {record_id}")


    try:
        print(f"[Workflow] Calling cloud function: {CLOUD_PROCESSING_URL}")

        process_resp = requests.post(
            CLOUD_PROCESSING_URL,
            data=json.dumps(form_data),  
            headers={'Content-Type': 'application/json'},
            timeout=10
        )

        print(f"[Workflow] Process status: {process_resp.status_code}")
        print(f"[Workflow] Process raw response: {process_resp.text}")

        if process_resp.status_code == 200:
            try:
                response_data = process_resp.json()

                # 解析阿里云返回结构
                if isinstance(response_data, dict) and 'body' in response_data:
                    result = json.loads(response_data['body'])
                else:
                    result = response_data

            except Exception as e:
                print(f"[Workflow] Parse error: {e}")
                result = {
                    'status': 'INCOMPLETE',
                    'category': 'GENERAL',
                    'priority': 'NORMAL',
                    'note': 'Invalid response from processing service'
                }

            print(f"[Workflow] Processing result: {result}")

   
            try:
                update_resp = requests.post(
                    f"{MOCK_URL}/update",
                    json={
                        'record_id': record_id,
                        'result': result
                    },
                    timeout=5
                )
                print(f"[Workflow] Update response: {update_resp.status_code}")

            except Exception as e:
                print(f"[Workflow] Update failed: {e}")

                # fallback：直接更新 Data Service
                requests.put(
                    f"{DATA_SERVICE_URL}/update/{record_id}",
                    json=result,
                    timeout=5
                )

        else:
            print(f"[Workflow] Processing failed with status: {process_resp.status_code}")

            default_result = {
                'status': 'INCOMPLETE',
                'category': 'GENERAL',
                'priority': 'NORMAL',
                'note': 'Cloud processing failed. Please try again.'
            }

            requests.put(
                f"{DATA_SERVICE_URL}/update/{record_id}",
                json=default_result,
                timeout=5
            )

    except Exception as e:
        print(f"[Workflow] Error calling cloud function: {e}")

        default_result = {
            'status': 'INCOMPLETE',
            'category': 'GENERAL',
            'priority': 'NORMAL',
            'note': 'Processing failed. Please try again.'
        }

        requests.put(
            f"{DATA_SERVICE_URL}/update/{record_id}",
            json=default_result,
            timeout=5
        )

    return jsonify({
        'record_id': record_id,
        'status': 'submitted'
    })


@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'})


if __name__ == '__main__':
    print("Workflow Service running on http://localhost:5002")
    app.run(host='0.0.0.0', port=5002, debug=True)