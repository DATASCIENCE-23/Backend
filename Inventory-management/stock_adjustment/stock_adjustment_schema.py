from pydantic import BaseModel, Field
from enum import Enum

class AdjustmentType(str, Enum):
    ADD = "ADD"
    SUBTRACT = "SUBTRACT"

class StockAdjustmentCreate(BaseModel):
    item_id: int
    location_id: int
    adjustment_type: AdjustmentType
    quantity_changed: int = Field(..., gt=0)
    reason: str
