from pydantic import BaseModel, Field

class StockTransferCreate(BaseModel):
    item_id: int
    from_location_id: int
    to_location_id: int
    quantity: int = Field(..., gt=0)
