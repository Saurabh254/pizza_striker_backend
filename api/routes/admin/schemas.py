from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class LoginUser(BaseModel):
    phone: str = Field(max_length=10, min_length=10)
    hashed_password: str = Field(max_length=255, min_length=3)


class Admin(BaseModel):
    id: str = Field(min_length=12, max_length=12)
    name: Optional[str] = None
    phone: str = Field(min_length=13, max_length=13)
    created_at: datetime
    updated_at: datetime


class LoginResponse(BaseModel):
    access_token: str
    admin: Admin


class CreateStrike(BaseModel):
    user_id: str
    reason: str


class StrikesResponse(CreateStrike):
    reason: str
    created_at: datetime
    updated_at: datetime
