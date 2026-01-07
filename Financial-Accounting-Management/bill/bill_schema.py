from pydantic import BaseModel
from datetime import date

class BillCreate(BaseModel):
    vendor_id: int
    bill_date: date
    total_amount: float
    tax_amount: float = 0
    status: str

class BillResponse(BillCreate):
    bill_id: int

    class Config:
        orm_mode = True
