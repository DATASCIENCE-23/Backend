from pydantic import BaseModel
from datetime import date
from typing import List, Optional
from decimal import Decimal


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


class POCreate(BaseModel):
    poNum: str
    orderDate: date
    supplierId: int
    totalAmt: Optional[Decimal] = None
    status: Optional[str] = None
    createdBy: Optional[int] = None
    expDeliveryDate: Optional[date] = None


class POUpdate(BaseModel):
    status: Optional[str] = None
    expDeliveryDate: Optional[date] = None
    totalAmt: Optional[Decimal] = None


class POResp(BaseModel):
    purchaseId: int
    poNum: str
    orderDate: date
    supplierId: int
    totalAmt: Optional[Decimal]
    status: Optional[str]
    createdBy: Optional[int]
    expDeliveryDate: Optional[date]
    items: List[POItemResp] = []

    class Config:
        from_attributes = True
