import os, hmac, hashlib, secrets
from passlib.context import CryptContext
from fastapi import Header, HTTPException, status, Depends
from sqlalchemy.orm import Session
from .database import get_db
from .models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
BACKEND_SECRET = os.getenv("BACKEND_SECRET", "dev-secret-change-me")

def hash_api_key(api_key: str):
    return pwd_context.hash(api_key)

def verify_api_key(api_key: str, api_key_hash: str):
    return pwd_context.verify(api_key, api_key_hash)

def generate_api_key(username: str) -> str:
    # Make a stable random key tied to secret
    rand = secrets.token_hex(16)
    msg = f"{username}:{rand}".encode()
    sig = hmac.new(BACKEND_SECRET.encode(), msg, hashlib.sha256).hexdigest()
    return f"brc_{rand}{sig[:16]}"

def require_api_key(x_api_key: str = Header(..., alias="X-API-Key"), db: Session = Depends(get_db)) -> User:
    user = db.query(User).filter(User.username != None).all()  # fetch all then check
    # simple lookup: iterate to find matching hash
    for u in user:
        if verify_api_key(x_api_key, u.api_key_hash):
            return u
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")
