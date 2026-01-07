from sqlalchemy import Column, Integer, String, Numeric, Boolean, ForeignKey
from database import Base

class BankAccount(Base):
    __tablename__ = "bank_accounts"

    bank_account_id = Column(Integer, primary_key=True, index=True)

    account_number = Column(String, unique=True, nullable=False)
    bank_name = Column(String, nullable=False)
    branch_name = Column(String, nullable=False)

    account_id = Column(
        Integer,
        ForeignKey("accounts.account_id"),
        nullable=False
    )

    current_balance = Column(Numeric(14, 2), default=0)
    is_active = Column(Boolean, default=True)
