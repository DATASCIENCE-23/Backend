from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from database import Base

class Account(Base):
    __tablename__ = "accounts"

    account_id = Column(Integer, primary_key=True, index=True)
    account_name = Column(String, nullable=False)
    account_type = Column(String, nullable=False)
    parent_account_id = Column(
        Integer,
        ForeignKey("accounts.account_id"),
        nullable=True
    )
    is_active = Column(Boolean, default=True)
