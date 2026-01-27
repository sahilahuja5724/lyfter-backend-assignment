from fastapi import FastAPI, Request, Header, HTTPException
from fastapi.responses import JSONResponse, PlainTextResponse
import hmac
import hashlib

from app.config import WEBHOOK_SECRET
from app.storage import init_db, insert_message, list_messages
from app.metrics import REQUEST_COUNT, MESSAGES_RECEIVED, generate_metrics

app = FastAPI()


@app.on_event("startup")
def startup():
    init_db()


@app.get("/health/live")
def live():
    return {"status": "alive"}


@app.get("/health/ready")
def ready():
    return {"status": "ready"}


@app.post("/webhook")
async def webhook(request: Request, x_signature: str = Header(None)):
    raw_body = await request.body()

    expected = hmac.new(
        WEBHOOK_SECRET.encode(),
        raw_body,
        hashlib.sha256
    ).hexdigest()

    if not x_signature or not hmac.compare_digest(x_signature, expected):
        raise HTTPException(status_code=401, detail={"signature_ok": False})

    data = await request.json()
    insert_message(data["id"], data["sender"], data["content"])
    MESSAGES_RECEIVED.inc()

    return {"signature_ok": True}


@app.get("/messages")
def get_messages(limit: int = 10, offset: int = 0):
    return list_messages(limit, offset)


@app.get("/metrics")
def metrics():
    return PlainTextResponse(generate_metrics())
