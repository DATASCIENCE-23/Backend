from sqlalchemy import Column, Integer, String, Float, ForeignKey
from Tax.database import Base

class Tax(Base):
    __tablename__ = "taxes"

    id = Column(Integer, primary_key=True, index=True)
    tax_name = Column(String(100), nullable=False, unique=True)
    tax_rate = Column(Float, nullable=False)
    account_id = Column(Integer, ForeignKey("accounts.account_id"), nullable=False)
