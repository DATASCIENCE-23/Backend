from pydantic import BaseModel
from datetime import date
from typing import Optional

class ExpenseCreate(BaseModel):
    expense_date: date
    account_id: int
    amount: float
    department_id: int
    reference_id: Optional[int] = None
    description: Optional[str] = None

class ExpenseResponse(ExpenseCreate):
    expense_id: int

    class Config:
        orm_mode = True
