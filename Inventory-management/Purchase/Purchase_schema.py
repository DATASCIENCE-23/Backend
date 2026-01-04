from pydantic import BaseModel, Field
from datetime import date
from typing import Optional, List
from decimal import Decimal


# Test Cases Documentation
"""
TEST CASES:

1. Test purchase without supplier → fail
   POST /api/po
   {
     "poNum": "PO-001",
     "orderDate": "2025-01-01",
     "supplierId": 999,  # Non-existent supplier
     "createdBy": 1
   }
   Expected: 400 Bad Request - "Supplier 999 does not exist"

2. Test stock increases correctly
   1. Create PO with status "pending"
   2. Add item to PO
   3. Update PO status to "approved"
   4. Check hms.stock table - quantity_available should increase
   Expected: Stock updated with ordered quantity

3. Test duplicate line item handling
   POST /api/po/1/items
   {
     "itemId": 5,
     "orderedQty": 10,
     "unitPrice": 100.00
   }
   POST /api/po/1/items (same itemId)
   Expected: 400 Bad Request - "Item 5 already in PO"
"""


# GRN Schemas
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


# Purchase Order Item Schemas
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


# Purchase Order Schemas
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
