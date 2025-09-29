# app/db/database.py
import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Загружаем переменные окружения из .env
load_dotenv()

# Берём готовую строку подключения, если есть
DATABASE_URL = os.getenv("DATABASE_URL")

# Если нет — собираем вручную
if not DATABASE_URL:
    DB_USER = os.getenv("DB_USER", "exp_user")
    DB_PASS = os.getenv("DB_PASS", "exp_pass")
    DB_NAME = os.getenv("DB_NAME", "expense_db")
    DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
    DB_PORT = os.getenv("DB_PORT", "5432")

    DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set and could not be built.")

# Создаём асинхронный движок
engine = create_async_engine(DATABASE_URL, echo=True, future=True)

# Фабрика асинхронных сессий
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)

# Зависимость для FastAPI
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
