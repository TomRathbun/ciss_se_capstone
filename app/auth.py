"""PIN auth + signed session cookies."""

import hashlib
import hmac
import secrets

from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from fastapi import Request
from sqlalchemy.orm import Session

from app.config import SECRET_KEY, SESSION_COOKIE, SESSION_MAX_AGE
from app.models import Candidate

serializer = URLSafeTimedSerializer(SECRET_KEY)


def hash_pin(pin: str) -> str:
    """Salted SHA-256 hash (training app; not for high-security production)."""
    salt = secrets.token_hex(16)
    digest = hashlib.sha256(f"{salt}:{pin}".encode("utf-8")).hexdigest()
    return f"sha256${salt}${digest}"


def verify_pin(pin: str, pin_hash: str) -> bool:
    try:
        algo, salt, digest = pin_hash.split("$", 2)
        if algo != "sha256":
            return False
        check = hashlib.sha256(f"{salt}:{pin}".encode("utf-8")).hexdigest()
        return hmac.compare_digest(check, digest)
    except Exception:
        return False


def create_session_token(candidate_id: int, role: str) -> str:
    return serializer.dumps({"id": candidate_id, "role": role})


def decode_session_token(token: str) -> dict | None:
    try:
        return serializer.loads(token, max_age=SESSION_MAX_AGE)
    except (BadSignature, SignatureExpired):
        return None


def get_current_user(request: Request, db: Session) -> Candidate | None:
    token = request.cookies.get(SESSION_COOKIE)
    if not token:
        return None
    data = decode_session_token(token)
    if not data:
        return None
    return (
        db.query(Candidate)
        .filter(Candidate.id == data["id"], Candidate.is_active == True)  # noqa: E712
        .first()
    )
