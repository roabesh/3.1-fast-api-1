from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from app.models import UserGroup


# ── Advertisement ──────────────────────────────────────────────────────────────

class AdvertisementCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    price: float = Field(..., ge=0)


class AdvertisementUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    price: Optional[float] = Field(None, ge=0)


class AdvertisementResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    price: float
    author: str
    created_at: datetime
    user_id: Optional[int]

    model_config = {"from_attributes": True}


# ── User ───────────────────────────────────────────────────────────────────────

class UserCreate(BaseModel):
    username: str = Field(..., min_length=1, max_length=255)
    password: str = Field(..., min_length=6)
    group: Optional[UserGroup] = UserGroup.USER


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=1, max_length=255)
    password: Optional[str] = Field(None, min_length=6)
    group: Optional[UserGroup] = None


class UserResponse(BaseModel):
    id: int
    username: str
    group: UserGroup

    model_config = {"from_attributes": True}


# ── Auth ───────────────────────────────────────────────────────────────────────

class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    token: str
