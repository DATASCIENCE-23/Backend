from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from common_base import Base

class Account(Base):
    __tablename__ = "accounts"

    account_id = Column(Integer, primary_key=True, index=True)
    account_name = Column(String, nullable=False)
    account_type = Column(String, nullable=False)  # e.g., Asset, Liability, Equity, Revenue, Expense
    parent_account_id = Column(Integer, ForeignKey("accounts.account_id"), nullable=True)
    is_active = Column(Boolean, default=True)

    # Relationships
    parent = relationship("Account", remote_side=[account_id], back_populates="children")
    children = relationship("Account", back_populates="parent")
    
    # Used in journal lines, invoice lines, expenses, etc.
    journal_lines = relationship("JournalLine", back_populates="account")
    invoice_lines = relationship("InvoiceLine", back_populates="account")
    bill_lines = relationship("BillLine", back_populates="account")
    expenses = relationship("Expense", back_populates="account")
    budget_lines = relationship("BudgetLine", back_populates="account")
    taxes = relationship("Tax", back_populates="account")