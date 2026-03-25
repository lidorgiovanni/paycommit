import random
import string
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timezone, timedelta
from database import get_db

OTP_EXPIRY_MINUTES = 10

# ── שמירה וניהול OTP ──────────────────────────────────────────────────────────

def _ensure_tables():
    from database import init_db
    init_db()

def generate_otp() -> str:
    return ''.join(random.choices(string.digits, k=6))

def save_otp(email: str, otp: str):
    expires = (datetime.now(timezone.utc) + timedelta(minutes=OTP_EXPIRY_MINUTES)).isoformat()
    with get_db() as conn:
        conn.execute("DELETE FROM otp_codes WHERE email=?", (email,))
        conn.execute("INSERT INTO otp_codes (email, code, expires_at) VALUES (?,?,?)", (email, otp, expires))

def verify_otp(email: str, otp: str) -> bool:
    with get_db() as conn:
        row = conn.execute(
            "SELECT code, expires_at FROM otp_codes WHERE email=?", (email,)
        ).fetchone()
        if not row:
            return False
        if row["code"] != otp:
            return False
        if datetime.fromisoformat(row["expires_at"]) < datetime.now(timezone.utc):
            return False
        conn.execute("DELETE FROM otp_codes WHERE email=?", (email,))
        return True

def get_or_create_user(email: str) -> dict:
    with get_db() as conn:
        row = conn.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
        if row:
            return dict(row)
        import uuid
        uid = str(uuid.uuid4())
        now = datetime.now(timezone.utc).isoformat()
        conn.execute("INSERT INTO users (id, email, created_at) VALUES (?,?,?)", (uid, email, now))
        return {"id": uid, "email": email, "created_at": now}

# ── שליחת מייל ───────────────────────────────────────────────────────────────

def send_otp_email(email: str, otp: str, smtp_config: dict):
    """
    smtp_config = {
        "host": "smtp.gmail.com",
        "port": 587,
        "user": "your@gmail.com",
        "password": "app_password"
    }
    """
    body = f"""
שלום,

קוד האימות שלך ל-PayCommit הוא:

  {otp}

הקוד תקף ל-{OTP_EXPIRY_MINUTES} דקות.

אם לא ביקשת קוד זה, התעלם מהודעה זו.
"""
    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = f"קוד אימות PayCommit: {otp}"
    msg["From"] = smtp_config["user"]
    msg["To"] = email

    with smtplib.SMTP(smtp_config["host"], smtp_config["port"]) as server:
        server.starttls()
        server.login(smtp_config["user"], smtp_config["password"])
        server.sendmail(smtp_config["user"], email, msg.as_string())
