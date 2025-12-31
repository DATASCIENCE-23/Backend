from pydantic import BaseModel, Field
from datetime import date
from typing import Optional, List
from decimal import Decimal


# -----------------------------
# GRN Schemas
# -----------------------------
class GRNCreate(BaseModel):
    purchaseId: int
    grnNum: str
    recvDate: date
    recvBy: Optional[int] = None
    notes: Optional[str] = None


class GRNResp(BaseModel):
    receiptId: int
    purchaseId: int
    grnNum: str
    recvDate: Optional[date]
    recvBy: Optional[int]
    notes: Optional[str]

    class Config:
        from_attributes = True


# -----------------------------
# Purchase Order Item Schemas
# -----------------------------
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


# -----------------------------
# Purchase Order Schemas
# -----------------------------
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
