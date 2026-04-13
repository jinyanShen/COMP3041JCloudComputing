import json
import requests

def handler(event, context):
    """
    Result Update Function
    作用：将 Processing Function 的结果更新到 Data Service
    部署：阿里云函数计算 FC
    """
    print(f"Update event: {event}")

    # 解析输入
    body = {}
    if isinstance(event, dict):
        if 'body' in event:
            body = json.loads(event.get('body', '{}'))
        else:
            body = event

    record_id = body.get('record_id')
    result = body.get('result', {})

    print(f"Updating record {record_id} with result: {result}")

    # 调用 Data Service 更新
    # 注意：部署到阿里云后，需要改成 Data Service 的内网地址
    data_service_url = 'http://localhost:5001'  # 本地测试

    try:
        response = requests.put(
            f"{data_service_url}/update/{record_id}",
            json=result,
            timeout=10
        )

        if response.status_code == 200:
            return {
                'statusCode': 200,
                'body': json.dumps({'message': 'Record updated successfully', 'record_id': record_id})
            }
        else:
            return {
                'statusCode': 500,
                'body': json.dumps({'message': 'Update failed', 'status': response.status_code})
            }
    except Exception as e:
        print(f"Error updating record: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Update failed', 'error': str(e)})
        }