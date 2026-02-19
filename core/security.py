# core/security.py
import hashlib
import base64
import bcrypt
from datetime import datetime, timedelta
from jose import jwt, JWTError
import os

SECRET_KEY = os.getenv("SECRET_KEY", "change-this-in-production")
REFRESH_SECRET_KEY = os.getenv("REFRESH_SECRET_KEY", "refresh-secret-change-this")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24       # 24 hours
REFRESH_TOKEN_EXPIRE_DAYS = 7               # 7 days

def _normalize_password(password: str) -> str:
    digest = hashlib.sha256(password.encode("utf-8")).digest()
    return base64.b64encode(digest).decode("utf-8")

def hash_password(password: str) -> str:
    normalized = _normalize_password(password)
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(normalized.encode("utf-8"), salt).decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    normalized = _normalize_password(plain_password)
    return bcrypt.checkpw(normalized.encode("utf-8"), hashed_password.encode("utf-8"))

def create_access_token(data: dict) -> str:
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload["type"] = "access"
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict) -> str:
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    payload["type"] = "refresh"
    return jwt.encode(payload, REFRESH_SECRET_KEY, algorithm=ALGORITHM)

def decode_refresh_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "refresh":
            raise JWTError("Not a refresh token")
        return payload
    except JWTError:
        raise

