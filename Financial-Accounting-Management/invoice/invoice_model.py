from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from common_base import Base

class Invoice(Base):
    __tablename__ = "invoices"

    invoice_id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.patient_id"), nullable=False)
    invoice_date = Column(Date, nullable=False)
    total_amount = Column(Float, nullable=False)
    tax_amount = Column(Float, default=0)
    discount_amount = Column(Float, default=0)
    status = Column(String(50), default="UNPAID")

    # Relationships
    patient = relationship("Patient", back_populates="invoices")
    invoice_lines = relationship("InvoiceLine", back_populates="invoice")
    payments = relationship("Payment", back_populates="invoice")
