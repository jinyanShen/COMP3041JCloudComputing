# COMP3041JCloudComputing

### Cloud Computing Assignment: Campus Event System (Microservices & Serverless)
A lightweight campus event submission & auto‑review system built with Flask microservices and Alibaba Cloud Serverless Function Compute. It implements a full closed loop: submission → storage → intelligent review → result update → query.
#### 1. Architecture
Frontend → Workflow → Data Service → Cloud/Local Serverless → Result Update


```plaintext
Frontend (5000) → Workflow (5002) → Data (5001)
                        ↓
           Alibaba Cloud / Local Mock (9000)
```
#### 2. Service List


|Service|File|Port|Duty|
|---|---|---|---|
|Frontend Web|app.py |5000|Form & result page|
|Workflow|app.py |5002|Process orchestration & fault tolerance|
|Data Service|app.py |5001|In-memory CRUD|
|Local Mock|mock_server.py |9000|Mock review & update|
|Cloud Function|processing.py |–|Cloud auto-review|
#### 3. Core Features
- Event form with required fields: title, description, location, date, organiser
- UUID-based record management
- Auto validation: required fields, date format (YYYY‑MM‑DD), description ≥40 chars
- Keyword classification & priority
- Status: APPROVED / NEEDS REVISION / INCOMPLETE
- Fault tolerance: cloud failure → fallback to local update
- Visual result query
#### 4. Tech Stack
Python 3, Flask, Requests, Alibaba Cloud Function Compute, in-memory storage, regex
#### 5. Local Run (in order)
- Data Service (5001): python app.py
- Mock Service (9000): python mock_server.py
- Workflow (5002): python app.py
- Frontend (5000): python app.py
- Open: http://localhost:5000
#### 6. Key APIs

- Data: `POST /create`; `GET /get/<id>`; `PUT /update/<id>`
- Workflow: `POST /submit`; `GET /health`
- Frontend: `GET /`; `POST /`; `GET /result/<id>`
#### 7. Classification Rules

|Keywords|Category|Priority|
|---|---|---|
|Career/Internship|OPPORTUNITY|HIGH|
|Workshop/Seminar|ACADEMIC|MEDIUM|
|Club/Social|SOCIAL|NORMAL|
|Others|GENERAL|NORMAL|
#### 8. Highlights
- Microservice decoupling

- Real Serverless practice

- Fault tolerance & degradation

- Full automation

- Simple web UI
#### 9. Notes
- In-memory storage: data lost after restart

- Cloud deployment: update CLOUD_PROCESSING_URL

- Local test: use mock_server only