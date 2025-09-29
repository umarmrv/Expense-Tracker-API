from __future__ import annotations
from datetime import date, datetime
from typing import TYPE_CHECKING  # 

from sqlalchemy import Date, ForeignKey, Numeric, String, func, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

# 👇 типовые импорты только для анализа, в рантайме не выполняются
if TYPE_CHECKING:
    from .user import User
    from .category import Category


class Transaction(Base):
    """Финансовая операция (доход или расход)."""

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), index=True)
    category_id: Mapped[int] = mapped_column(
        ForeignKey("category.id", ondelete="RESTRICT"), index=True
    )

    amount: Mapped[float] = mapped_column(Numeric(12, 2))  # > 0
    date: Mapped[date] = mapped_column(Date, index=True)
    note: Mapped[str | None]
    currency: Mapped[str] = mapped_column(String(3), default="USD")
    created_at: Mapped[datetime] = mapped_column(default=func.now())

    # связи
    user: Mapped["User"] = relationship(back_populates="transactions")
    category: Mapped["Category"] = relationship(back_populates="transactions")

    __table_args__ = (
        Index("ix_tx_user_date", "user_id", "date"),
        Index("ix_tx_category_date", "category_id", "date"),
    )

    def __repr__(self) -> str:
        return (
            f"Transaction(id={self.id}, user_id={self.user_id}, "
            f"category_id={self.category_id}, amount={self.amount}, date={self.date})"
        )
