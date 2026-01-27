from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"]
)

MESSAGES_RECEIVED = Counter(
    "messages_received_total",
    "Total messages received"
)

def generate_metrics():
    return generate_latest()
