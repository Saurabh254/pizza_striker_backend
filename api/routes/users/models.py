from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.database.base_model import BaseModel


class Users(BaseModel):
    name: Mapped[str] = mapped_column(String(255))
    profile_photo: Mapped[str] = mapped_column(String)
    phone: Mapped[str] = mapped_column(String, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    strike_count: Mapped[int] = mapped_column(Integer, default=0)
    strikes = relationship("UserStrikes", back_populates="user", lazy=True)


class UserStrikes(BaseModel):
    user_id: Mapped[str] = mapped_column(
        String(12), ForeignKey("users.id"), nullable=False
    )
    reason: Mapped[str] = mapped_column(String, default=None)
    user = relationship("Users", back_populates="strikes")
