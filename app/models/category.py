from __future__ import annotations
from datetime import datetime
from enum import Enum as PyEnum
from typing import TYPE_CHECKING  # 

from sqlalchemy import CheckConstraint, Enum, ForeignKey, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

# 👇 типовые импорты только для анализа, в рантайме не выполняются
if TYPE_CHECKING:
    from .user import User
    from .transaction import Transaction

from app.db.base import Base


class CategoryType(str, PyEnum):
    income = "income"
    expense = "expense"


class Category(Base):
    """Категории доходов/расходов. owner_id = NULL → глобальная категория."""

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), index=True)
    type: Mapped[CategoryType] = mapped_column(Enum(CategoryType, name="category_type"))
    owner_id: Mapped[int | None] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    created_at: Mapped[datetime] = mapped_column(default=func.now())

    # связи
    owner: Mapped["User | None"] = relationship(back_populates="categories")
    transactions: Mapped[list["Transaction"]] = relationship(back_populates="category")

    __table_args__ = (
        UniqueConstraint("owner_id", "name", "type", name="uq_category_owner_name_type"),
        CheckConstraint("name <> ''", name="ck_category_name_not_empty"),
    )

    def __repr__(self) -> str:
        return f"Category(id={self.id}, name={self.name}, type={self.type}, owner={self.owner_id})"
