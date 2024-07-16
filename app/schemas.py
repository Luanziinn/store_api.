from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float

class ProductDB(ProductCreate):
    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
