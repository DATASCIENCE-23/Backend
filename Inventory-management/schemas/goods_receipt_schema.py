from pydantic import BaseModel
from datetime import date
from typing import Optional


class GRNCreate(BaseModel):
    purchaseId: int
    grnNum: str
    recvDate: date
    recvBy: Optional[int] = None
    notes: Optional[str] = None


class GRNResp(BaseModel):
    receiptId: int
    purchaseId: int
    grnNum: str
    recvDate: Optional[date]
    recvBy: Optional[int]
    notes: Optional[str]

    class Config:
        from_attributes = True
