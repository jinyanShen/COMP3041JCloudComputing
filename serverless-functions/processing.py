import json
import re

def handler(event, context):
    """
    Processing Function - 核心处理逻辑
    部署：阿里云函数计算 FC
    """
    print(f"Processing event: {event}")

    # 解析输入
    body = {}
    if isinstance(event, dict):
        if 'body' in event:
            body = json.loads(event.get('body', '{}'))
        else:
            body = event

    record_id = body.get('record_id')
    data = body.get('data', {})

    print(f"Processing record {record_id}: {data}")

    # 1. 检查必填字段
    required = ['title', 'description', 'location', 'date', 'organiser']
    for field in required:
        if field not in data or not data[field]:
            result = {
                'status': 'INCOMPLETE',
                'category': None,
                'priority': None,
                'note': f'Missing required field: {field}'
            }
            return {
                'statusCode': 200,
                'body': json.dumps(result)
            }

    # 2. 检查日期格式
    if not re.match(r'\d{4}-\d{2}-\d{2}', data['date']):
        result = {
            'status': 'NEEDS REVISION',
            'category': 'GENERAL',
            'priority': 'NORMAL',
            'note': 'Invalid date format. Use YYYY-MM-DD.'
        }
        return {
            'statusCode': 200,
            'body': json.dumps(result)
        }

    # 3. 检查描述长度
    if len(data['description']) < 40:
        result = {
            'status': 'NEEDS REVISION',
            'category': 'GENERAL',
            'priority': 'NORMAL',
            'note': f'Description must be at least 40 characters. Current: {len(data["description"])}'
        }
        return {
            'statusCode': 200,
            'body': json.dumps(result)
        }

    # 4. 分类逻辑（按优先级：OPPORTUNITY > ACADEMIC > SOCIAL > GENERAL）
    text = (data.get('title', '') + ' ' + data.get('description', '')).lower()

    if any(k in text for k in ['career', 'internship', 'recruitment']):
        cat, pri = 'OPPORTUNITY', 'HIGH'
    elif any(k in text for k in ['workshop', 'seminar', 'lecture']):
        cat, pri = 'ACADEMIC', 'MEDIUM'
    elif any(k in text for k in ['club', 'society', 'social']):
        cat, pri = 'SOCIAL', 'NORMAL'
    else:
        cat, pri = 'GENERAL', 'NORMAL'

    result = {
        'status': 'APPROVED',
        'category': cat,
        'priority': pri,
        'note': 'All checks passed. Event approved.'
    }

    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }