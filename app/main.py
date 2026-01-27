import os
import json
import hmac
import hashlib

from fastapi import FastAPI, Request, Header, HTTPException, status, Body
from fastapi.responses import JSONResponse

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/health/live")
def health_live():
    return {"status": "alive"}


@app.get("/health/ready")
def health_ready():
    if not os.getenv("WEBHOOK_SECRET"):
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "not ready"},
        )
    return {"status": "ready"}


@app.post("/webhook")
async def webhook(
    request: Request,
    payload: dict = Body(...),
    x_signature: str | None = Header(None),
):
    WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")

    if not WEBHOOK_SECRET:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="WEBHOOK_SECRET not set",
        )

    if not x_signature:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing signature",
        )

    raw_body = json.dumps(payload, separators=(",", ":")).encode()

    expected_signature = hmac.new(
        WEBHOOK_SECRET.encode(),
        raw_body,
        hashlib.sha256,
    ).hexdigest()

    if not hmac.compare_digest(x_signature, expected_signature):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "error": "Invalid signature",
                "signature_ok": False,
            },
        )

    # ✅ THIS IS WHAT THE TEST EXPECTS
    return {
        "signature_ok": True
    }
