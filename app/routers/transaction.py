# app/routers/transaction.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app import crud
from app.schemas.transaction import TransactionCreate, TransactionUpdate, TransactionOut

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.post("/", response_model=TransactionOut)
async def create_transaction(tx_in: TransactionCreate, db: AsyncSession = Depends(get_db)):
    return await crud.transaction.create_transaction(db, tx_in)


@router.get("/{transaction_id}", response_model=TransactionOut)
async def read_transaction(transaction_id: int, db: AsyncSession = Depends(get_db)):
    tx = await crud.transaction.get_transaction(db, transaction_id)
    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return tx


@router.get("/", response_model=list[TransactionOut])
async def read_transactions(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    return await crud.transaction.get_transactions(db, skip, limit)


@router.put("/{transaction_id}", response_model=TransactionOut)
async def update_transaction(transaction_id: int, tx_in: TransactionUpdate, db: AsyncSession = Depends(get_db)):
    tx = await crud.transaction.update_transaction(db, transaction_id, tx_in)
    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return tx


@router.delete("/{transaction_id}")
async def delete_transaction(transaction_id: int, db: AsyncSession = Depends(get_db)):
    ok = await crud.transaction.delete_transaction(db, transaction_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return {"status": "deleted"}
