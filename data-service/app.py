# Import core Flask modules
# Flask: Initialize the web application
# request: Parse incoming JSON request data
# jsonify: Return standardized JSON format responses
from flask import Flask, request, jsonify
# Import uuid library to generate unique identifiers for records
import uuid

# Initialize Flask application instance
app = Flask(__name__)
# In-memory dictionary as a lightweight database (data will be lost after service restart)
db = {}

# API endpoint: Create a new event record
# HTTP Method: POST
# Function: Receive JSON data, generate a unique ID, and store data in memory
@app.route('/create', methods=['POST'])
def create():
    # Get JSON data from the request body
    data = request.json
    # Generate a unique UUID string as the record ID
    record_id = str(uuid.uuid4())
    # Store the data in the in-memory database with the unique ID as the key
    db[record_id] = data
    # Return the generated unique record ID in JSON format
    return jsonify({'id': record_id})

# API endpoint: Query a record by its unique ID
# HTTP Method: GET
# URL Parameter: record_id - unique identifier of the record
@app.route('/get/<record_id>', methods=['GET'])
def get(record_id):
    # Query the database, return the record if exists, return empty dict if not found
    return jsonify(db.get(record_id, {}))

# API endpoint: Update an existing record by ID
# HTTP Method: PUT
# URL Parameter: record_id - unique identifier of the record
# Request Body: JSON data with fields to update
@app.route('/update/<record_id>', methods=['PUT'])
def update(record_id):
    # Get the update data from the request body
    data = request.json
    # If the record exists, merge and update the data
    if record_id in db:
        db[record_id].update(data)
    # Return a success response status
    return jsonify({'status': 'ok'})

# Main entry: Start the Flask server
if __name__ == '__main__':
    # Run the service on port 5001, accessible from all network addresses
    app.run(port=5001, host='0.0.0.0')