import requests
import json
import hmac
import hashlib
import uuid
import time

WEBHOOK_URL = "http://127.0.0.1:8000/webhook"
SECRET = b"supersecret"

TOTAL_MESSAGES = 1000  # try 100, then 1000, then 10000

print(f"🚀 Starting bulk test: {TOTAL_MESSAGES} messages\n")

start = time.time()

for i in range(1, TOTAL_MESSAGES + 1):
    payload = {
        "id": str(uuid.uuid4()),
        "sender": f"user_{i % 10}",
        "content": f"Message number {i}",
    }

    raw_body = json.dumps(payload, separators=(",", ":")).encode()
    signature = hmac.new(SECRET, raw_body, hashlib.sha256).hexdigest()

    r = requests.post(
        WEBHOOK_URL,
        json=payload,
        headers={"x-signature": signature},
        timeout=5,
    )

    if r.status_code != 200:
        print(f"❌ Failed at message {i}: {r.status_code} → {r.text}")
        break

    if i % 100 == 0:
        print(f"✅ Sent {i} messages")

end = time.time()

print(f"\n🎉 Completed in {end - start:.2f} seconds")
