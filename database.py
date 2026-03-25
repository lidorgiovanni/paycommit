import sqlite3
from contextlib import contextmanager

DB_PATH = "commitments.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id          TEXT PRIMARY KEY,
    email       TEXT UNIQUE NOT NULL,
    created_at  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS otp_codes (
    email       TEXT PRIMARY KEY,
    code        TEXT NOT NULL,
    expires_at  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS sessions (
    token       TEXT PRIMARY KEY,
    user_id     TEXT NOT NULL,
    email       TEXT NOT NULL,
    created_at  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS commitments (
    id          TEXT PRIMARY KEY,
    amount      REAL NOT NULL,
    currency    TEXT NOT NULL DEFAULT 'ILS',
    due_date    TEXT NOT NULL,
    creator_id  TEXT NOT NULL,
    recipient_id TEXT NOT NULL,
    description TEXT,
    status      TEXT NOT NULL DEFAULT 'CREATED',
    signature   TEXT,
    created_at  TEXT NOT NULL,
    updated_at  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS audit_log (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    commitment_id   TEXT NOT NULL,
    action          TEXT NOT NULL,
    actor_id        TEXT NOT NULL,
    from_status     TEXT,
    to_status       TEXT,
    timestamp       TEXT NOT NULL
);
"""


def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.executescript(SCHEMA)


@contextmanager
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
