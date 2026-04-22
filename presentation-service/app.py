# Import core Flask modules
# Flask: Initialize web application
# request: Handle HTTP request data (form/JSON)
# render_template_string: Render HTML from a string
# jsonify: Return JSON-formatted responses
from flask import Flask, request, render_template_string, jsonify
# Import requests to call external microservice APIs
import requests

# Initialize Flask application instance
app = Flask(__name__)
# URL of the workflow orchestration service (port 5002)
WORKFLOW_URL = "http://localhost:5002"
# URL of the data storage service (port 5001)
DATA_URL = "http://localhost:5001"

# HTML template for the event submission form with inline CSS styling
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
    <!-- Form submits data via POST method to the same endpoint -->
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

# Root route: Serve form (GET) and handle form submission (POST)
@app.route('/', methods=['GET', 'POST'])
def index():
    # Handle form submission
    if request.method == 'POST':
        # Forward form data to the workflow service API
        resp = requests.post(f"{WORKFLOW_URL}/submit", json=request.form)
        # Get the unique record ID returned by the workflow service
        record_id = resp.json()['record_id']
        # Return success page with link to view processing result
        return f'''
        <h2>Submission Received!</h2>
        <p>Your event has been submitted.</p>
        <a href="/result/{record_id}">Click here to view result</a>
        <br><br>
        <a href="/">Submit another event</a>
        '''
    # Serve the event submission form for GET requests
    return HTML_FORM

# Route to display event processing result by record ID
@app.route('/result/<record_id>')
def result(record_id):
    # Fetch event data and review result from the data service
    response = requests.get(f"{DATA_URL}/get/{record_id}")
    # Parse JSON response to Python dictionary
    data = response.json()

    # Handle case where record is not found
    if not data:
        return "<h2>Event not found</h2><a href='/'>Go back</a>"

    # Display processing status, category, priority and notes
    return f'''
    <h2>Event Processing Result</h2>
    <p><strong>Status:</strong> {data.get('status', 'Pending')}</p>
    <p><strong>Category:</strong> {data.get('category', 'Not assigned')}</p>
    <p><strong>Priority:</strong> {data.get('priority', 'Not assigned')}</p>
    <p><strong>Note:</strong> {data.get('note', 'Processing...')}</p>
    <br>
    <a href="/">Submit another event</a>
    '''

# Run the Flask web server when the script is executed directly
if __name__ == '__main__':
    # Start app on port 5000, accessible from all network interfaces
    app.run(port=5000, host='0.0.0.0')