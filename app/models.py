from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy import String, Text, Float, DateTime, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
import enum


class UserGroup(str, enum.Enum):
    USER = "user"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    group: Mapped[UserGroup] = mapped_column(
        SAEnum(UserGroup), default=UserGroup.USER, nullable=False
    )

    advertisements: Mapped[List["Advertisement"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )


class Advertisement(Base):
    __tablename__ = "advertisements"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    author: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    user_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    user: Mapped[Optional["User"]] = relationship(back_populates="advertisements")
