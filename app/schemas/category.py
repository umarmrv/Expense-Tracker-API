# app/schemas/category.py
from datetime import datetime
from pydantic import BaseModel
from app.models.category import CategoryType


class CategoryBase(BaseModel):
    name: str
    type: CategoryType


class CategoryCreate(CategoryBase):
    owner_id: int | None = None   # можно создавать глобальные категории


class CategoryUpdate(BaseModel):
    name: str | None = None
    type: CategoryType | None = None


class CategoryOut(CategoryBase):
    id: int
    owner_id: int | None
    created_at: datetime

    class Config:
        orm_mode = True
