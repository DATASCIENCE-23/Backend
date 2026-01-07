from pydantic import BaseModel
from typing import Optional

class BankAccountCreate(BaseModel):
    account_number: str
    bank_name: str
    branch_name: str
    account_id: int
    current_balance: float = 0

class BankAccountResponse(BankAccountCreate):
    bank_account_id: int
    is_active: bool

    class Config:
        orm_mode = True
