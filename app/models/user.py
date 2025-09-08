from __future__ import annotations
from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
# 👇 типовые импорты только для анализа, в рантайме не выполняются
if TYPE_CHECKING:
    from .category import Category
    from .transaction import Transaction

class User(Base):
    """Пользователь приложения."""

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(default=func.now())

    # связи
    transactions: Mapped[list["Transaction"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    categories: Mapped[list["Category"]] = relationship(
        back_populates="owner", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"User(id={self.id}, email={self.email})"
