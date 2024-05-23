from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class LoginUser(BaseModel):
    phone: str = Field(max_length=10, min_length=10)
    hashed_password: str = Field(max_length=255, min_length=3)


class SlimUser(BaseModel):
    id: str = Field(min_length=12, max_length=12)
    name: Optional[str] = None
    profile_photo: Optional[str] = None
    phone: str = Field(min_length=13, max_length=13)
    created_at: datetime
    strike_count: int
    updated_at: datetime


class FullUser(SlimUser):
    hashed_password: str


class LoginResponse(BaseModel):
    access_token: str
    user: FullUser


class StrikesResponse(BaseModel):
    id: str = Field(min_length=12, max_length=12)
    reason: str
    user: SlimUser
