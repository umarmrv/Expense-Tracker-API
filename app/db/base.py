from __future__ import annotations


try:
    # Нормальный путь для SQLAlchemy 2.x
    from sqlalchemy.orm import DeclarativeBase, declared_attr
except ImportError:
    # Редкий fallback (если IDE/окружение чудит)
    from sqlalchemy.orm import DeclarativeBase
    from sqlalchemy.ext.declarative import declared_attr


class Base(DeclarativeBase):
    """Общий базовый класс для всех ORM-моделей."""

    @declared_attr.directive
    def __tablename__(cls) -> str:  # type: ignore[override]
        return cls.__name__.lower()
