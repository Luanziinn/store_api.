from fastapi import APIRouter, Depends, HTTPException
from app.schemas import ProductCreate, ProductDB
from app.crud import create_product, update_product, get_products_by_price_range
from app.main import get_db
from typing import List

router = APIRouter()

@router.post("/products", response_model=ProductDB)
async def create_product_route(product: ProductCreate, db=Depends(get_db)):
    return await create_product(db, product)

@router.put("/products/{id}", response_model=ProductDB)
async def update_product_route(id: str, product: ProductCreate, db=Depends(get_db)):
    return await update_product(db, id, product)

@router.get("/products", response_model=List[ProductDB])
async def get_products_route(min_price: float = 0, max_price: float = 1000000, db=Depends(get_db)):
    return await get_products_by_price_range(db, min_price, max_price)
