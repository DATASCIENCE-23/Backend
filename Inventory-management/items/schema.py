# items/schemas.py
from pydantic import BaseModel, Field, validator
from typing import Optional

class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(CategoryBase):
    name: Optional[str] = None

class CategoryRead(CategoryBase):
    id: int

    class Config:
        from_attributes = True

# Similar for Supplier and StoreLocation
class SupplierBase(BaseModel):
    name: str
    contact_person: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None

class SupplierCreate(SupplierBase):
    pass

class SupplierRead(SupplierBase):
    id: int

    class Config:
        from_attributes = True

class StoreLocationBase(BaseModel):
    name: str
    location_type: Optional[str] = None

class StoreLocationCreate(StoreLocationBase):
    pass

class StoreLocationRead(StoreLocationBase):
    id: int

    class Config:
        from_attributes = True

class ItemBase(BaseModel):
    code: str = Field(..., max_length=50)
    name: str
    unit: str
    unit_price: float = Field(..., gt=0)
    expiry_applicable: bool = False
    minimum_stock_level: int = Field(..., gt=0)
    category_id: int
    status: Optional[str] = "active"

    @validator("status")
    def valid_status(cls, v):
        if v not in {"active", "inactive"}:
            raise ValueError("Status must be 'active' or 'inactive'")
        return v

class ItemCreate(ItemBase):
    pass

class ItemUpdate(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    unit: Optional[str] = None
    unit_price: Optional[float] = None
    expiry_applicable: Optional[bool] = None
    minimum_stock_level: Optional[int] = None
    category_id: Optional[int] = None
    status: Optional[str] = None

class ItemRead(ItemBase):
    id: int
    category: CategoryRead

    class Config:
        from_attributes = True