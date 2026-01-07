from pydantic import BaseModel
from datetime import date

class InvoiceCreate(BaseModel):
    patient_id: int
    invoice_date: date
    total_amount: float
    tax_amount: float = 0
    discount_amount: float = 0
    status: str

class InvoiceResponse(InvoiceCreate):
    invoice_id: int

    class Config:
        orm_mode = True
