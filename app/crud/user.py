# app/crud/user.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


async def get_user(db: AsyncSession, user_id: int) -> User | None:
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalars().first()


async def get_users(db: AsyncSession, skip: int = 0, limit: int = 10) -> list[User]:
    result = await db.execute(select(User).offset(skip).limit(limit))
    return result.scalars().all()


async def create_user(db: AsyncSession, user_in: UserCreate) -> User:
    new_user = User(email=user_in.email, password_hash=user_in.password)  # ⚠️ пока без хеша
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def update_user(db: AsyncSession, user_id: int, user_in: UserUpdate) -> User | None:
    user = await get_user(db, user_id)
    if not user:
        return None

    if user_in.email is not None:
        user.email = user_in.email
    if user_in.password is not None:
        user.password_hash = user_in.password  # ⚠️ пока без хеша

    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def delete_user(db: AsyncSession, user_id: int) -> bool:
    user = await get_user(db, user_id)
    if not user:
        return False
    await db.delete(user)
    await db.commit()
    return True
