from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from common_base import Base

class Payment(Base):
    __tablename__ = "payments"

    payment_id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey("invoices.invoice_id"), nullable=False)
    payment_date = Column(Date, nullable=False)
    amount_paid = Column(Float, nullable=False)
    payment_mode = Column(String(50))
    bank_account_id = Column(Integer)

    # Relationships
    invoice = relationship("Invoice", back_populates="payments")