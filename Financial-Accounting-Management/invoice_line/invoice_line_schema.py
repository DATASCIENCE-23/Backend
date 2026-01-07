from pydantic import BaseModel

class InvoiceLineCreate(BaseModel):
    invoice_id: int
    service_name: str
    account_id: int
    quantity: int
    unit_price: float
    line_total: float

class InvoiceLineResponse(InvoiceLineCreate):
    invoice_line_id: int

    class Config:
        orm_mode = True
