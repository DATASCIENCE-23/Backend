from pydantic import BaseModel, Field
from typing import List

class StockAuditItem(BaseModel):
    item_id: int
    physical_quantity: int = Field(..., ge=0)

class StockAuditCreate(BaseModel):
    location_id: int
    remarks: str
    items: List[StockAuditItem]
