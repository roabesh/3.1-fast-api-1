from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class AdvertisementCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    price: float = Field(..., ge=0)
    author: str = Field(..., min_length=1, max_length=255)


class AdvertisementUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    price: Optional[float] = Field(None, ge=0)
    author: Optional[str] = Field(None, min_length=1, max_length=255)


class AdvertisementResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    price: float
    author: str
    created_at: datetime

    model_config = {"from_attributes": True}
