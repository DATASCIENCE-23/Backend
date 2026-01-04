from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from database import Base
from pydantic import BaseModel
from datetime import datetime


class Payment(Base):
    __tablename__ = "payment"

    payment_id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey("invoice.invoice_id"), nullable=False)
    payment_datetime = Column(DateTime, default=func.now())
    amount_paid = Column(Float, nullable=False)
    payment_mode = Column(String(50))
    transaction_ref = Column(String(100))
    bank_account_id = Column(Integer)
    received_by = Column(Integer)
    status = Column(String(30))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


# ---------- Pydantic Schemas ----------

class PaymentCreate(BaseModel):
    invoice_id: int
    amount_paid: float
    payment_mode: str
    transaction_ref: str | None = None
    bank_account_id: int | None = None
    received_by: int
    status: str


class PaymentResponse(PaymentCreate):
    payment_id: int
    payment_datetime: datetime

    class Config:
        orm_mode = True
