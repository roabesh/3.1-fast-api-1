import os
from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, Header
from sqlalchemy.orm import Session

from app.database import get_db

SECRET_KEY = os.getenv("SECRET_KEY", "change_me_in_production")
ALGORITHM = "HS256"
TOKEN_EXPIRE_HOURS = 48

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(hours=TOKEN_EXPIRE_HOURS)
    return jwt.encode(
        {"user_id": user_id, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM
    )


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


def get_current_user(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db),
):
    if not authorization:
        return None
    token = authorization.removeprefix("Bearer ").strip()
    payload = decode_token(token)
    from app.models import User
    user = db.get(User, payload["user_id"])
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


def require_auth(current_user=Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Authentication required")
    return current_user


def require_admin(current_user=Depends(require_auth)):
    from app.models import UserGroup
    if current_user.group != UserGroup.ADMIN:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user
