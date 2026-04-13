from flask import Flask, request, render_template_string, jsonify
import requests

app = Flask(__name__)
WORKFLOW_URL = "http://localhost:5002"
DATA_URL = "http://localhost:5001"

HTML_FORM = '''
<!DOCTYPE html>
<html>
<head>
    <title>Campus Buzz - Submit Event</title>
    <style>
        body { font-family: Arial; margin: 50px; }
        input, textarea { margin: 10px 0; padding: 8px; width: 300px; }
        button { padding: 10px 20px; background: #007bff; color: white; border: none; cursor: pointer; }
    </style>
</head>
<body>
    <h1>Submit Campus Event</h1>
    <form method="post">
        Title: <input name="title" required><br>
        Description: <textarea name="description" rows="4" required></textarea><br>
        Location: <input name="location" required><br>
        Date (YYYY-MM-DD): <input name="date" placeholder="2024-12-31" required><br>
        Organiser: <input name="organiser" required><br>
        <button type="submit">Submit</button>
    </form>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        resp = requests.post(f"{WORKFLOW_URL}/submit", json=request.form)
        record_id = resp.json()['record_id']
        return f'''
        <h2>Submission Received!</h2>
        <p>Your event has been submitted.</p>
        <a href="/result/{record_id}">Click here to view result</a>
        <br><br>
        <a href="/">Submit another event</a>
        '''
    return HTML_FORM

@app.route('/result/<record_id>')
def result(record_id):
    response = requests.get(f"{DATA_URL}/get/{record_id}")
    data = response.json()

    if not data:
        return "<h2>Event not found</h2><a href='/'>Go back</a>"

    return f'''
    <h2>Event Processing Result</h2>
    <p><strong>Status:</strong> {data.get('status', 'Pending')}</p>
    <p><strong>Category:</strong> {data.get('category', 'Not assigned')}</p>
    <p><strong>Priority:</strong> {data.get('priority', 'Not assigned')}</p>
    <p><strong>Note:</strong> {data.get('note', 'Processing...')}</p>
    <br>
    <a href="/">Submit another event</a>
    '''

if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0')