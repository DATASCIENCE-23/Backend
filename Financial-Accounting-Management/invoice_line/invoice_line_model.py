from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from common_base import Base

class InvoiceLine(Base):
    __tablename__ = "invoice_lines"

    invoice_line_id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey("invoices.invoice_id"), nullable=False)
    service_name = Column(String(100), nullable=False)
    account_id = Column(Integer)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    line_total = Column(Float, nullable=False)

    # Relationships
    invoice = relationship("Invoice", back_populates="invoice_lines")