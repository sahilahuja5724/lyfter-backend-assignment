
 Secure Webhook Ingestion Service

 Overview

This project implements a **secure, production-oriented webhook ingestion service** using **FastAPI**.
It is designed to receive webhook events at scale, verify request authenticity using **HMAC-SHA256**, persist validated messages, and expose **Prometheus-compatible metrics** for observability.

The architecture and implementation follow **real-world backend engineering practices**, including request validation, security, persistence, health checks, and monitoring.

---

 Features

 Secure Webhook Verification

* HMAC-SHA256 signature verification using a shared secret
* Prevents tampered or spoofed webhook requests
* Unauthorized requests return **HTTP 401**

 Message Ingestion & Storage

* Accepts JSON webhook payloads
* Persists verified messages in **SQLite**
* Efficient handling of high-volume requests

 Observability & Metrics

* Prometheus metrics exposed at `/metrics`
* Tracks:

  * Total webhook requests
  * Successfully received messages

 Health Checks

* Liveness and readiness endpoints for service monitoring

 Load & Integration Testing

* Bulk message sender script included
* Swagger UI available for interactive API testing

---
 Tech Stack

| Component | Technology        |
| --------- | ----------------- |
| Language  | Python 3.12       |
| Framework | FastAPI           |
| Server    | Uvicorn           |
| Database  | SQLite            |
| Metrics   | Prometheus Client |
| Security  | HMAC-SHA256       |

---

 Project Structure

```
lyfter-backend-assignment/
│
├── app/
│   ├── main.py          # FastAPI application entry point
│   ├── config.py        # Environment configuration
│   ├── storage.py       # Database logic
│   ├── metrics.py       # Prometheus metrics
│   ├── models.py        # Data models
│   └── logging_utils.py # Logging helpers
│
├── bulk_test.py         # Load testing script
├── app.db               # SQLite database (git-ignored)
├── .gitignore
└── README.md
```

---

 Setup & Installation
 Clone the Repository

```bash
git clone https://github.com/<your-username>/lyfter-backend-assignment.git
cd lyfter-backend-assignment
```
 Create & Activate Virtual Environment

```bash
python -m venv venv
```

**Windows**

```powershell
venv\Scripts\Activate.ps1
```

 venv/bin/activate
```
 Install Dependencies

```bash
pip install -r requirements.txt
```

---

 Running the Application

```bash
uvicorn app.main:app --reload
```

The server will start at:

```
http://127.0.0.1:8000
```

---

API Documentation (Swagger)

Swagger UI is available at:

```
http://127.0.0.1:8000/docs
```

This allows:

* Interactive request testing
* Viewing request/response schemas
* Manual webhook validation

---
 Webhook Usage

### Endpoint

```
POST /webhook
```

### Required Headers

| Header        | Description                      |
| ------------- | -------------------------------- |
| `x-signature` | HMAC-SHA256 of the raw JSON body |

### Sample Payload

```json
{
  "id": "1",
  "sender": "alice",
  "content": "hello"
}
```

### Signature Generation (Windows / VS Code)

```powershell
$body = '{"id":"1","sender":"alice","content":"hello"}'
python - <<EOF
import hmac, hashlib
print(hmac.new(b"supersecret", $body.encode(), hashlib.sha256).hexdigest())
EOF
```

Use the generated value as the `x-signature` header.

---

 Metrics Endpoint

Prometheus metrics are exposed at:

```
GET /metrics
```

This endpoint can be scraped directly by Prometheus or visualized via Grafana.


## 🚀 Load Testing

A bulk message sender is included:

```bash
python bulk_test.py
```

This simulates high-volume webhook delivery and validates system stability under load.

---

 AI Tool Usage Disclosure

AI-assisted tools such as **GitHub Copilot** and **ChatGPT** were used **to a limited extent** during development, primarily for:

* Code structure suggestions
* Debugging assistance
* Documentation refinement

All architectural decisions, implementation logic, testing, and final validation were **performed and verified manually**.
The final solution reflects the author’s understanding of backend system design and secure API development.



