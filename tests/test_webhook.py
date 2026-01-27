import hmac
import hashlib
import json
import os

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_webhook_valid_signature(monkeypatch):
    # Set secret for test
    monkeypatch.setenv("WEBHOOK_SECRET", "supersecret")

    payload = {"event": "test"}

    raw_body = json.dumps(payload, separators=(",", ":")).encode()

    signature = hmac.new(
        b"supersecret",
        raw_body,
        hashlib.sha256,
    ).hexdigest()

    response = client.post(
        "/webhook",
        json=payload,
        headers={"x-signature": signature},
    )

    assert response.status_code == 200
    assert response.json()["signature_ok"] is True
