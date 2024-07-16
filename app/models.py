from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Product(BaseModel):
    id: Optional[str]
    name: str
    description: Optional[str]
    price: float
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime]
