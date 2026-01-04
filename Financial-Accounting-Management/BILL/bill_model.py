from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from common_base import Base

class Bill(Base):
    __tablename__ = "bills"
    
    bill_id = Column(Integer, primary_key=True, index=True)
    vendor_id = Column(Integer, ForeignKey("vendors.vendor_id"), nullable=False)
    bill_date = Column(Date, nullable=False)
    total_amount = Column(Float, nullable=False)
    tax_amount = Column(Float, default=0.0)
    status = Column(String, default="Pending")  # Pending, Paid, Partially Paid
    
    # Relationships
    vendor = relationship("Vendor", back_populates="bills")
    bill_lines = relationship("BillLine", back_populates="bill", cascade="all, delete-orphan")
    journal_entry = relationship("JournalEntry", uselist=False, back_populates="bill")