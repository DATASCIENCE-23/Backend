from pydantic import BaseModel
from typing import Optional

class AccountCreate(BaseModel):
    account_name: str
    account_type: str
    parent_account_id: Optional[int] = None

class AccountUpdate(BaseModel):
    account_name: Optional[str]
    account_type: Optional[str]
    parent_account_id: Optional[int]
    is_active: Optional[bool]

class AccountResponse(BaseModel):
    account_id: int
    account_name: str
    account_type: str
    parent_account_id: Optional[int]
    is_active: bool

    class Config:
        orm_mode = True
