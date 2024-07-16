from motor.motor_asyncio import AsyncIOMotorClient
from app.schemas import ProductCreate, ProductDB
from bson import ObjectId
from datetime import datetime
from pymongo.errors import PyMongoError
from fastapi import HTTPException

async def create_product(db, product: ProductCreate):
    product = product.dict()
    product["created_at"] = product["updated_at"] = datetime.utcnow()
    try:
        result = await db["products"].insert_one(product)
        product["id"] = str(result.inserted_id)
        return ProductDB(**product)
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=str(e))

async def update_product(db, id: str, product: ProductCreate):
    update_data = product.dict()
    update_data["updated_at"] = datetime.utcnow()
    result = await db["products"].update_one({"_id": ObjectId(id)}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return await get_product_by_id(db, id)

async def get_product_by_id(db, id: str):
    product = await db["products"].find_one({"_id": ObjectId(id)})
    if product:
        return ProductDB(**product)
    raise HTTPException(status_code=404, detail="Product not found")

async def get_products_by_price_range(db, min_price: float, max_price: float):
    cursor = db["products"].find({"price": {"$gt": min_price, "$lt": max_price}})
    products = await cursor.to_list(length=100)
    return [ProductDB(**product) for product in products]
