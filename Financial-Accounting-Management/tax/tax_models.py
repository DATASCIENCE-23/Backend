from sqlalchemy import Column, Integer, String, Numeric, Boolean, ForeignKey
from database import Base

class Tax(Base):
    __tablename__ = "taxes"

    tax_id = Column(Integer, primary_key=True, index=True)
    tax_name = Column(String, nullable=False)
    tax_rate = Column(Numeric(5, 2), nullable=False)

    account_id = Column(
        Integer,
        ForeignKey("accounts.account_id"),
        nullable=False
    )

    is_active = Column(Boolean, default=True)
