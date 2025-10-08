# app/crud/transaction.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionUpdate, TransactionOut


async def get_transaction(db: AsyncSession, transaction_id: int) -> TransactionOut | None:
    result = await db.execute(
        select(Transaction)
        .options(selectinload(Transaction.user), selectinload(Transaction.category))
        .where(Transaction.id == transaction_id)
    )
    tx = result.scalars().first()
    if not tx:
        return None

    return TransactionOut(
        id=tx.id,
        amount=tx.amount,
        date=tx.date,
        note=tx.note,
        currency=tx.currency,
        created_at=tx.created_at,
        user_email=tx.user.email if tx.user else None,
        category_name=tx.category.name if tx.category else None,
        category_type=tx.category.type if tx.category else None,
    )


async def get_transactions(db: AsyncSession, skip: int = 0, limit: int = 10) -> list[TransactionOut]:
    result = await db.execute(
        select(Transaction)
        .options(selectinload(Transaction.user), selectinload(Transaction.category))
        .offset(skip)
        .limit(limit)
    )
    transactions = result.scalars().all()

    return [
        TransactionOut(
            id=tx.id,
            amount=tx.amount,
            date=tx.date,
            note=tx.note,
            currency=tx.currency,
            created_at=tx.created_at,
            user_email=tx.user.email if tx.user else None,
            category_name=tx.category.name if tx.category else None,
            category_type=tx.category.type if tx.category else None,
        )
        for tx in transactions
    ]


async def create_transaction(db: AsyncSession, tx_in: TransactionCreate) -> TransactionOut:
    tx = Transaction(**tx_in.dict())
    db.add(tx)
    await db.commit()
    await db.refresh(tx)

    # предзагружаем связи
    result = await db.execute(
        select(Transaction)
        .options(selectinload(Transaction.user), selectinload(Transaction.category))
        .where(Transaction.id == tx.id)
    )
    tx = result.scalars().first()

    return TransactionOut(
        id=tx.id,
        amount=tx.amount,
        date=tx.date,
        note=tx.note,
        currency=tx.currency,
        created_at=tx.created_at,
        user_email=tx.user.email,
        category_name=tx.category.name,
        category_type=tx.category.type,
    )


async def update_transaction(db: AsyncSession, transaction_id: int, tx_in: TransactionUpdate) -> TransactionOut | None:
    result = await db.execute(
        select(Transaction)
        .options(selectinload(Transaction.user), selectinload(Transaction.category))
        .where(Transaction.id == transaction_id)
    )
    tx = result.scalars().first()
    if not tx:
        return None

    for field, value in tx_in.dict(exclude_unset=True).items():
        setattr(tx, field, value)

    db.add(tx)
    await db.commit()
    await db.refresh(tx)

    # заново подгружаем связи
    result = await db.execute(
        select(Transaction)
        .options(selectinload(Transaction.user), selectinload(Transaction.category))
        .where(Transaction.id == tx.id)
    )
    tx = result.scalars().first()

    return TransactionOut(
        id=tx.id,
        amount=tx.amount,
        date=tx.date,
        note=tx.note,
        currency=tx.currency,
        created_at=tx.created_at,
        user_email=tx.user.email,
        category_name=tx.category.name,
        category_type=tx.category.type,
    )


async def delete_transaction(db: AsyncSession, transaction_id: int) -> bool:
    result = await db.execute(select(Transaction).where(Transaction.id == transaction_id))
    tx = result.scalars().first()
    if not tx:
        return False
    await db.delete(tx)
    await db.commit()
    return True
