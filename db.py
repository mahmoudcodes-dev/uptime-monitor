import sqlite3, os

DB_PATH = os.getenv("DB_PATH", "monitors.db")

def conn():
    c = sqlite3.connect(DB_PATH)
    c.row_factory = sqlite3.Row
    return c

def init():
    with conn() as c:
        c.execute("""CREATE TABLE IF NOT EXISTS monitors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL UNIQUE,
            status TEXT NOT NULL DEFAULT 'unknown',
            status_code INTEGER,
            latency_ms INTEGER,
            last_checked TEXT
        )""")

def add(url):
    with conn() as c:
        cur = c.execute("INSERT INTO monitors (url) VALUES (?)", (url,))
        return cur.lastrowid

def all_monitors():
    with conn() as c:
        return [dict(r) for r in c.execute("SELECT * FROM monitors ORDER BY id")]

def remove(monitor_id):
    with conn() as c:
        return c.execute("DELETE FROM monitors WHERE id = ?", (monitor_id,)).rowcount

def update(monitor_id, status, status_code, latency_ms):
    with conn() as c:
        c.execute(
            "UPDATE monitors SET status=?, status_code=?, latency_ms=?, "
            "last_checked=datetime('now') WHERE id=?",
            (status, status_code, latency_ms, monitor_id),
        )
