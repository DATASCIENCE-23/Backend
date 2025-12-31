from pydantic import BaseModel, Field
from datetime import date
from typing import Optional
from decimal import Decimal


class POItemCreate(BaseModel):
    itemId: int
    orderedQty: int = Field(gt=0)
    unitPrice: Decimal = Field(gt=0)
    expiryDate: Optional[date] = None


class POItemResp(BaseModel):
    poItemId: int
    purchaseId: int
    itemId: int
    orderedQty: Optional[int]
    receivedQty: Optional[int]
    unitPrice: Optional[Decimal]
    lineTotal: Optional[Decimal]
    expiryDate: Optional[date]

    class Config:
        from_attributes = True
