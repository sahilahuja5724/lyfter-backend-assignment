import sqlite3
from app.config import DB_PATH

def get_conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id TEXT PRIMARY KEY,
            sender TEXT,
            content TEXT
        )
    """)
    conn.commit()
    conn.close()

def insert_message(msg_id, sender, content):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT OR IGNORE INTO messages VALUES (?, ?, ?)",
        (msg_id, sender, content)
    )
    conn.commit()
    conn.close()

def list_messages(limit, offset):
    conn = get_conn()
    cur = conn.cursor()
    rows = cur.execute(
        "SELECT id, sender, content FROM messages LIMIT ? OFFSET ?",
        (limit, offset)
    ).fetchall()
    conn.close()
    return rows

def count_messages():
    conn = get_conn()
    cur = conn.cursor()
    count = cur.execute("SELECT COUNT(*) FROM messages").fetchone()[0]
    conn.close()
    return count
