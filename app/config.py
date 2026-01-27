import os

WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "supersecret")
DB_PATH = os.getenv("DB_PATH", "app.db")
