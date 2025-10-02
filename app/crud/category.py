# app/crud/category.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate


# Получить категорию по id
async def get_category(db: AsyncSession, category_id: int) -> Category | None:
    result = await db.execute(select(Category).where(Category.id == category_id))
    return result.scalars().first()


# Получить список категорий (с пагинацией)
async def get_categories(db: AsyncSession, skip: int = 0, limit: int = 10) -> list[Category]:
    result = await db.execute(select(Category).offset(skip).limit(limit))
    return result.scalars().all()


# Создать категорию
async def create_category(db: AsyncSession, category_in: CategoryCreate) -> Category:
    new_category = Category(
        name=category_in.name,
        type=category_in.type,
        owner_id=category_in.owner_id,
    )
    db.add(new_category)
    await db.commit()
    await db.refresh(new_category)
    return new_category


# Обновить категорию
async def update_category(db: AsyncSession, category_id: int, category_in: CategoryUpdate) -> Category | None:
    category = await get_category(db, category_id)
    if not category:
        return None

    if category_in.name is not None:
        category.name = category_in.name
    if category_in.type is not None:
        category.type = category_in.type

    db.add(category)
    await db.commit()
    await db.refresh(category)
    return category


# Удалить категорию
async def delete_category(db: AsyncSession, category_id: int) -> bool:
    category = await get_category(db, category_id)
    if not category:
        return False
    await db.delete(category)
    await db.commit()
    return True
