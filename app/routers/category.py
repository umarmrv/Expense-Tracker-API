# app/routers/category.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app import crud
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryOut

router = APIRouter(prefix="/categories", tags=["categories"])


@router.post("/", response_model=CategoryOut)
async def create_category(category_in: CategoryCreate, db: AsyncSession = Depends(get_db)):
    return await crud.category.create_category(db, category_in)


@router.get("/{category_id}", response_model=CategoryOut)
async def read_category(category_id: int, db: AsyncSession = Depends(get_db)):
    category = await crud.category.get_category(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.get("/", response_model=list[CategoryOut])
async def read_categories(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    return await crud.category.get_categories(db, skip, limit)


@router.put("/{category_id}", response_model=CategoryOut)
async def update_category(category_id: int, category_in: CategoryUpdate, db: AsyncSession = Depends(get_db)):
    category = await crud.category.update_category(db, category_id, category_in)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.delete("/{category_id}")
async def delete_category(category_id: int, db: AsyncSession = Depends(get_db)):
    ok = await crud.category.delete_category(db, category_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"status": "deleted"}
