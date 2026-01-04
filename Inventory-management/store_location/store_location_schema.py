from pydantic import BaseModel
from typing import Optional

class StoreLocationCreate(BaseModel):
    name: str
    location_type: Optional[str] = None

class StoreLocationRead(StoreLocationCreate):
    id: int

    class Config:
        from_attributes = True
