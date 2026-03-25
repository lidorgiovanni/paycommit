import uuid
import os
from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from database import init_db, get_db
from models import (
    CommitmentCreate, CommitmentOut, CommitmentStatus,
    can_transition, generate_signature
)
from auth import generate_otp, save_otp, verify_otp, get_or_create_user, send_otp_email

SMTP_CONFIG = {
    "host": os.getenv("SMTP_HOST", "smtp.gmail.com"),
    "port": int(os.getenv("SMTP_PORT", 587)),
    "user": os.getenv("SMTP_USER", ""),
    "password": os.getenv("SMTP_PASSWORD", ""),
}
DEV_MODE = not SMTP_CONFIG["user"]  # אם אין SMTP — מצב פיתוח, OTP מוצג בתגובה

app = FastAPI(title="Payment Commitments API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"], allow_credentials=True)


@app.on_event("startup")
def startup():
    init_db()


def _row_to_dict(row) -> dict:
    return dict(row)


def _log(conn, commitment_id: str, action: str, actor_id: str,
         from_status: str = None, to_status: str = None):
    conn.execute(
        "INSERT INTO audit_log (commitment_id, action, actor_id, from_status, to_status, timestamp) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (commitment_id, action, actor_id, from_status, to_status,
         datetime.now(timezone.utc).isoformat())
    )


# ── AUTH ─────────────────────────────────────────────────────────────────────

class OTPRequest(BaseModel):
    email: str

class OTPVerify(BaseModel):
    email: str
    otp: str

@app.post("/auth/request-otp")
def request_otp(body: OTPRequest):
    otp = generate_otp()
    save_otp(body.email, otp)
    if DEV_MODE:
        return {"message": "DEV MODE — קוד OTP", "otp": otp, "email": body.email}
    try:
        send_otp_email(body.email, otp, SMTP_CONFIG)
        return {"message": "קוד נשלח למייל"}
    except Exception as e:
        raise HTTPException(500, f"שגיאה בשליחת מייל: {e}")

@app.post("/auth/verify-otp")
def verify_otp_endpoint(body: OTPVerify):
    if not verify_otp(body.email, body.otp):
        raise HTTPException(401, "קוד שגוי או פג תוקף")
    user = get_or_create_user(body.email)
    token = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()
    with get_db() as conn:
        conn.execute(
            "INSERT INTO sessions (token, user_id, email, created_at) VALUES (?,?,?,?)",
            (token, user["id"], body.email, now)
        )
    return {"token": token, "user": user}

@app.get("/auth/me")
def get_me(authorization: str = Header(None)):
    return _get_session(authorization)

@app.post("/auth/logout")
def logout(authorization: str = Header(None)):
    token = _extract_token(authorization)
    with get_db() as conn:
        conn.execute("DELETE FROM sessions WHERE token=?", (token,))
    return {"message": "התנתקת בהצלחה"}

# ── CREATE ──────────────────────────────────────────────────────────────────

@app.post("/commitments", response_model=CommitmentOut, status_code=201)
def create_commitment(data: CommitmentCreate):
    now = datetime.now(timezone.utc).isoformat()
    cid = str(uuid.uuid4())
    with get_db() as conn:
        conn.execute(
            "INSERT INTO commitments VALUES (?,?,?,?,?,?,?,?,?,?,?)",
            (cid, data.amount, data.currency, data.due_date,
             data.creator_id, data.recipient_id, data.description,
             CommitmentStatus.CREATED, None, now, now)
        )
        _log(conn, cid, "CREATE", data.creator_id, to_status=CommitmentStatus.CREATED)
    return _get_or_404(cid)


# ── GET ──────────────────────────────────────────────────────────────────────

@app.get("/commitments/{cid}", response_model=CommitmentOut)
def get_commitment(cid: str):
    return _get_or_404(cid)


@app.get("/commitments")
def list_commitments(user_id: str = None, status: CommitmentStatus = None):
    query = "SELECT * FROM commitments WHERE 1=1"
    params = []
    if user_id:
        query += " AND (creator_id=? OR recipient_id=?)"
        params += [user_id, user_id]
    if status:
        query += " AND status=?"
        params.append(status)
    with get_db() as conn:
        rows = conn.execute(query, params).fetchall()
    return [_row_to_dict(r) for r in rows]


# ── SIGN ─────────────────────────────────────────────────────────────────────

@app.post("/commitments/{cid}/sign", response_model=CommitmentOut)
def sign_commitment(cid: str, actor_id: str):
    c = _get_or_404(cid)
    _assert_transition(c, CommitmentStatus.SIGNED)
    if c["creator_id"] != actor_id:
        raise HTTPException(403, "Only creator can sign")
    sig = generate_signature(c["amount"], c["due_date"], c["creator_id"], c["created_at"])
    _update_status(cid, CommitmentStatus.SIGNED, actor_id, "SIGN", signature=sig)
    return _get_or_404(cid)


# ── SEND ──────────────────────────────────────────────────────────────────────

@app.post("/commitments/{cid}/send", response_model=CommitmentOut)
def send_commitment(cid: str, actor_id: str):
    c = _get_or_404(cid)
    _assert_transition(c, CommitmentStatus.SENT)
    if c["creator_id"] != actor_id:
        raise HTTPException(403, "Only creator can send")
    _update_status(cid, CommitmentStatus.SENT, actor_id, "SEND")
    return _get_or_404(cid)


# ── ACCEPT / REJECT ───────────────────────────────────────────────────────────

@app.post("/commitments/{cid}/accept", response_model=CommitmentOut)
def accept_commitment(cid: str, actor_id: str):
    c = _get_or_404(cid)
    _assert_transition(c, CommitmentStatus.ACCEPTED)
    if c["recipient_id"] != actor_id:
        raise HTTPException(403, "Only recipient can accept")
    _update_status(cid, CommitmentStatus.ACCEPTED, actor_id, "ACCEPT")
    return _get_or_404(cid)


@app.post("/commitments/{cid}/reject", response_model=CommitmentOut)
def reject_commitment(cid: str, actor_id: str):
    c = _get_or_404(cid)
    _assert_transition(c, CommitmentStatus.REJECTED)
    if c["recipient_id"] != actor_id:
        raise HTTPException(403, "Only recipient can reject")
    _update_status(cid, CommitmentStatus.REJECTED, actor_id, "REJECT")
    return _get_or_404(cid)


# ── REDEEM ────────────────────────────────────────────────────────────────────

@app.post("/commitments/{cid}/redeem", response_model=CommitmentOut)
def redeem_commitment(cid: str, actor_id: str):
    c = _get_or_404(cid)
    _assert_transition(c, CommitmentStatus.REDEEMED)
    _update_status(cid, CommitmentStatus.REDEEMED, actor_id, "REDEEM")
    return _get_or_404(cid)


# ── CANCEL ────────────────────────────────────────────────────────────────────

@app.post("/commitments/{cid}/cancel", response_model=CommitmentOut)
def cancel_commitment(cid: str, actor_id: str):
    c = _get_or_404(cid)
    _assert_transition(c, CommitmentStatus.CANCELED)
    _update_status(cid, CommitmentStatus.CANCELED, actor_id, "CANCEL")
    return _get_or_404(cid)


# ── AUDIT ─────────────────────────────────────────────────────────────────────

@app.get("/commitments/{cid}/audit")
def get_audit(cid: str):
    _get_or_404(cid)
    with get_db() as conn:
        rows = conn.execute(
            "SELECT * FROM audit_log WHERE commitment_id=? ORDER BY timestamp",
            (cid,)
        ).fetchall()
    return [_row_to_dict(r) for r in rows]


# ── AUTH HELPERS ─────────────────────────────────────────────────────────────

def _extract_token(authorization: str) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(401, "נדרש אימות")
    return authorization.split(" ", 1)[1]

def _get_session(authorization: str) -> dict:
    token = _extract_token(authorization)
    with get_db() as conn:
        row = conn.execute("SELECT * FROM sessions WHERE token=?", (token,)).fetchone()
    if not row:
        raise HTTPException(401, "Session לא תקף")
    return dict(row)

# ── HELPERS ───────────────────────────────────────────────────────────────────

def _get_or_404(cid: str) -> dict:
    with get_db() as conn:
        row = conn.execute("SELECT * FROM commitments WHERE id=?", (cid,)).fetchone()
    if not row:
        raise HTTPException(404, f"Commitment {cid} not found")
    return _row_to_dict(row)


def _assert_transition(c: dict, target: CommitmentStatus):
    current = CommitmentStatus(c["status"])
    if not can_transition(current, target):
        raise HTTPException(409, f"Cannot transition from {current} to {target}")


def _update_status(cid: str, new_status: CommitmentStatus, actor_id: str,
                   action: str, signature: str = None):
    now = datetime.now(timezone.utc).isoformat()
    with get_db() as conn:
        old = conn.execute("SELECT status FROM commitments WHERE id=?", (cid,)).fetchone()
        if signature:
            conn.execute(
                "UPDATE commitments SET status=?, signature=?, updated_at=? WHERE id=?",
                (new_status, signature, now, cid)
            )
        else:
            conn.execute(
                "UPDATE commitments SET status=?, updated_at=? WHERE id=?",
                (new_status, now, cid)
            )
        _log(conn, cid, action, actor_id, old["status"], new_status)
