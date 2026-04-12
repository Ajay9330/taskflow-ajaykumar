from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from ..config import settings
from typing import Optional
import bcrypt
import hashlib

ALGORITHM = "HS256"

def hash_password(password: str) -> str:
    # Pre-hash with SHA-256 to handle any password length reliably
    pw_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
    # Cost >= 12 as per Requirement 76
    return bcrypt.hashpw(pw_hash.encode("utf-8"), bcrypt.gensalt(rounds=12)).decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Pre-hash for comparison
    pw_hash = hashlib.sha256(plain_password.encode("utf-8")).hexdigest()
    return bcrypt.checkpw(pw_hash.encode("utf-8"), hashed_password.encode("utf-8"))

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(hours=settings.JWT_EXPIRY_HOURS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
