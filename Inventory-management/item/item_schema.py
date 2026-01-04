from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

class ItemStatusSchema(str, Enum):
    active = "active"
    inactive = "inactive"

class ItemCreate(BaseModel):
    code: str = Field(..., min_length=1, max_length=50)
    name: str
    unit: str
    unit_price: float = Field(..., gt=0)

    minimum_stock_level: int = Field(..., gt=0)
    expiry_applicable: bool

    category_id: int
    status: Optional[ItemStatusSchema] = ItemStatusSchema.active

class ItemRead(ItemCreate):
    id: int

    class Config:
        from_attributes = True
