import json
import re

def handler(event, context):
   
    body = json.loads(event.get('body', '{}'))
    data = body.get('data', {})


    required = ['title', 'description', 'location', 'date', 'organiser']
    for field in required:
        if field not in data or not data[field]:
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'status': 'INCOMPLETE',
                    'category': None,
                    'priority': None,
                    'note': f'Missing required field: {field}'
                })
            }


    if not re.match(r'\d{4}-\d{2}-\d{2}', data['date']):
        return {
            'statusCode': 200,
            'body': json.dumps({
                'status': 'NEEDS REVISION',
                'category': 'GENERAL',
                'priority': 'NORMAL',
                'note': 'Invalid date format. Use YYYY-MM-DD.'
            })
        }


    if len(data['description']) < 40:
        return {
            'statusCode': 200,
            'body': json.dumps({
                'status': 'NEEDS REVISION',
                'category': 'GENERAL',
                'priority': 'NORMAL',
                'note': f'Description must be at least 40 characters. Current: {len(data["description"])}'
            })
        }


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
        'statusCode': 200,
        'body': json.dumps({
            'status': 'APPROVED',
            'category': cat,
            'priority': pri,
            'note': 'All checks passed. Event approved.'
        })
    }