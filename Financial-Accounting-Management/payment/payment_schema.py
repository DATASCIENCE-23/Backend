from pydantic import BaseModel
from datetime import date
from typing import Optional

class PaymentCreate(BaseModel):
    invoice_id: int
    payment_date: date
    amount_paid: float
    payment_mode: str
    bank_account_id: Optional[int] = None

class PaymentResponse(PaymentCreate):
    payment_id: int

    class Config:
        orm_mode = True
