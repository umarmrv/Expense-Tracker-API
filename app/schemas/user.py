# app/schemas/user.py
from datetime import datetime
from pydantic import BaseModel, EmailStr


# Базовая схема (общие поля)
class UserBase(BaseModel):
    email: EmailStr


# Схема для создания пользователя
class UserCreate(UserBase):
    password: str


# Схема для обновления (пароль необязателен)
class UserUpdate(BaseModel):
    email: EmailStr | None = None
    password: str | None = None


# Схема для ответа (то, что отдаём наружу)
class UserOut(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
