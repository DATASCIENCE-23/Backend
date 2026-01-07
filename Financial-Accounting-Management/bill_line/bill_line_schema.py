from pydantic import BaseModel
from typing import Optional

class BillLineCreate(BaseModel):
    bill_id: int
    expense_account_id: int
    description: Optional[str]
    amount: float

class BillLineResponse(BillLineCreate):
    bill_line_id: int

    class Config:
        orm_mode = True
