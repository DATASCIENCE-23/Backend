from sqlalchemy import Column, Integer, Date, Numeric, String, ForeignKey
from database import Base

class Payment(Base):
    __tablename__ = "payments"

    payment_id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(
        Integer,
        ForeignKey("invoices.invoice_id"),
        nullable=False
    )
    payment_date = Column(Date, nullable=False)
    amount_paid = Column(Numeric(12, 2), nullable=False)
    payment_mode = Column(String, nullable=False)

    bank_account_id = Column(
        Integer,
        ForeignKey("bank_accounts.bank_account_id"),
        nullable=True
    )