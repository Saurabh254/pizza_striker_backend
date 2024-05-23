import datetime
from typing import Type, TypeVar

from nanoid import generate
from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, declarative_mixin, declared_attr, mapped_column

from .db import Base

T = TypeVar("Mix", bound="MyMixin")


@declarative_mixin
class MyMixin:
    id: Mapped[str] = mapped_column(
        String(12),
        default=lambda: generate(size=12),
        primary_key=True,
        unique=True,
        nullable=False,
    )
    created_at = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.datetime.now(datetime.timezone.utc),
        nullable=False,
    )
    updated_at = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.datetime.now(datetime.timezone.utc),
        onupdate=lambda: datetime.datetime.now(datetime.timezone.utc),
        nullable=False,
    )

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    __table_args__ = {"mysql_engine": "InnoDB"}
    __mapper_args__ = {"always_refresh": True}


class BaseModel(MyMixin, Base):
    __abstract__ = True
