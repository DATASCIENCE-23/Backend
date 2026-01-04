from pydantic import BaseModel, Field
from typing import List

class PurchaseItem(BaseModel):
    item_id: int
    quantity: int = Field(..., gt=0)
    purchase_price: float = Field(..., gt=0)

class PurchaseCreate(BaseModel):
    supplier_id: int
    invoice_number: str
    items: List[PurchaseItem]
