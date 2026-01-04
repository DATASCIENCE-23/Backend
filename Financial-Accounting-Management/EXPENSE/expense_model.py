from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from common_base import Base

class Expense(Base):
    __tablename__ = "expenses"

    expense_id = Column(Integer, primary_key=True, index=True)
    expense_date = Column(Date, nullable=False)
    account_id = Column(Integer, ForeignKey("accounts.account_id"), nullable=False)
    amount = Column(Float, nullable=False)
    department = Column(String, nullable=True)
    reference_id = Column(Integer, nullable=True)  # Can link to bill_id or other ref
    description = Column(String, nullable=True)

    # Relationships
    account = relationship("Account", back_populates="expenses")