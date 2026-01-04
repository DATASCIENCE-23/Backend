from pydantic import BaseModel, Field

class StockCreate(BaseModel):
    item_id: int
    location_id: int
    quantity_available: int = Field(..., ge=0)

class StockRead(StockCreate):
    id: int

    class Config:
        from_attributes = True
