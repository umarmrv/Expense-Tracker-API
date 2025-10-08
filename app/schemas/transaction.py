# app/schemas/transaction.py
from datetime import date, datetime
from pydantic import BaseModel, condecimal
from typing import Optional
from . import UserOut , CategoryOut
from decimal import Decimal



# Базовая схема
class TransactionBase(BaseModel):
    user_id: int
    category_id: int
    amount: condecimal(max_digits=12, decimal_places=2)
    date: date
    note: Optional[str] = None
    currency: str


# Схема для создания
class TransactionCreate(TransactionBase):
    pass


# Схема для обновления
class TransactionUpdate(BaseModel):
    user_id: Optional[int] = None
    category_id: Optional[int] = None
    amount: Optional[condecimal(max_digits=12, decimal_places=2)] = None
    date: Optional[date] = None
    note: Optional[str] = None
    currency: Optional[str] = None


# Схема для ответа
class TransactionOut(BaseModel):
    id: int
    amount: Decimal
    date: date
    note: str | None
    currency: str
    created_at: datetime

    # Только нужные поля из связанных таблиц
    user_email: str
    category_name: str
    category_type: str

    class Config:
        from_attributes = True  # для SQLAlchemy совместимости