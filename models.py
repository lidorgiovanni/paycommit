from enum import Enum
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, field_validator
import hashlib


class CommitmentStatus(str, Enum):
    CREATED = "CREATED"
    SIGNED = "SIGNED"
    SENT = "SENT"
    ACCEPTED = "ACCEPTED"
    REDEEMED = "REDEEMED"
    CANCELED = "CANCELED"
    REJECTED = "REJECTED"


VALID_TRANSITIONS = {
    CommitmentStatus.CREATED:  [CommitmentStatus.SIGNED, CommitmentStatus.CANCELED],
    CommitmentStatus.SIGNED:   [CommitmentStatus.SENT, CommitmentStatus.CANCELED],
    CommitmentStatus.SENT:     [CommitmentStatus.ACCEPTED, CommitmentStatus.REJECTED],
    CommitmentStatus.ACCEPTED: [CommitmentStatus.REDEEMED, CommitmentStatus.CANCELED],
    CommitmentStatus.REDEEMED: [],
    CommitmentStatus.CANCELED: [],
    CommitmentStatus.REJECTED: [],
}


def can_transition(current: CommitmentStatus, next_status: CommitmentStatus) -> bool:
    return next_status in VALID_TRANSITIONS.get(current, [])


def generate_signature(amount: float, due_date: str, creator_id: str, timestamp: str) -> str:
    raw = f"{amount}{due_date}{creator_id}{timestamp}"
    return hashlib.sha256(raw.encode()).hexdigest()


# --- Pydantic Schemas ---

class CommitmentCreate(BaseModel):
    amount: float
    currency: str = "ILS"
    due_date: str  # YYYY-MM-DD
    creator_id: str
    recipient_id: str
    description: Optional[str] = None

    @field_validator("amount")
    @classmethod
    def amount_positive(cls, v):
        if v <= 0:
            raise ValueError("amount must be positive")
        return v


class CommitmentOut(BaseModel):
    id: str
    amount: float
    currency: str
    due_date: str
    creator_id: str
    recipient_id: str
    description: Optional[str]
    status: CommitmentStatus
    signature: Optional[str]
    created_at: str
    updated_at: str
