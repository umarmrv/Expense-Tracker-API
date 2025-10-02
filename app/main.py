# app/main.py
from fastapi import FastAPI
from app.db.database import engine
from app.db.base import Base
from app.models.user import User
from app.models.category import Category
from app.models.transaction import Transaction
from app.routers import user as user_router  

app = FastAPI(title="Expense Tracker API")

@app.on_event("startup")
async def startup():
    # создаём все таблицы в базе при старте
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# 👇 регистрируем роутер
app.include_router(user_router.router)

@app.get("/")
async def root():
    return {"message": "API работает"}
