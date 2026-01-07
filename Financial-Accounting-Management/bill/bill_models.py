from sqlalchemy import Column, Integer, Date, Numeric, String, ForeignKey
from database import Base

class Bill(Base):
    __tablename__ = "bills"

    bill_id = Column(Integer, primary_key=True, index=True)
    vendor_id = Column(
        Integer,
        ForeignKey("vendors.vendor_id"),
        nullable=False
    )
    bill_date = Column(Date, nullable=False)
    total_amount = Column(Numeric(12, 2), nullable=False)
    tax_amount = Column(Numeric(12, 2), default=0)
    status = Column(String, nullable=False)
