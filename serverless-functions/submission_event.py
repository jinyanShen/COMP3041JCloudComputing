import json
import requests

def handler(event, context):
    """
    Submission Event Function
    作用：接收 Workflow Service 的请求，触发 Processing Function
    部署：阿里云函数计算 FC
    """
    print(f"Received event: {event}")

    # 解析 Workflow Service 发来的数据
    body = {}
    if isinstance(event, dict):
        if 'body' in event:
            body = json.loads(event.get('body', '{}'))
        else:
            body = event

    record_id = body.get('record_id')
    submission_data = body.get('data', {})

    print(f"Processing submission {record_id}")

    # 调用 Processing Function
    # 注意：部署到阿里云后，需要改成 Processing Function 的 HTTP 触发器地址
    # 本地测试时用 localhost:9000
    processing_url = 'http://localhost:9000/process'  # 本地测试

    try:
        response = requests.post(
            processing_url,
            json={'record_id': record_id, 'data': submission_data},
            timeout=30
        )
        result = response.json()

        # 调用 Result Update Function
        update_url = 'http://localhost:9000/update'  # 本地测试
        requests.post(
            update_url,
            json={'record_id': record_id, 'result': result},
            timeout=30
        )

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Processing completed', 'record_id': record_id})
        }
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Processing failed', 'error': str(e)})
        }