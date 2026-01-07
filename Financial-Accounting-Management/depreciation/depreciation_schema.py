from pydantic import BaseModel
from datetime import date
from typing import Optional

class DepreciationCreate(BaseModel):
    asset_id: int
    depreciation_date: date
    amount: float
    journal_id: Optional[int] = None

class DepreciationResponse(DepreciationCreate):
    depreciation_id: int

    class Config:
        orm_mode = True
