from sqlalchemy import Column, DateTime, Integer, String, Numeric, ForeignKey, func
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Invoice(Base):
    __tablename__ = "invoices"

    invoice_id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey("patients.patient_id"), nullable=False)
    issue_datetime = Column(DateTime, nullable=False, server_default=func.now())
    invoice_type = Column(String(50), nullable=False)  # e.g. "Outpatient", "Pharmacy", "Lab"
    subtotal = Column(Numeric(12, 2), nullable=False, default=0)
    tax_amount = Column(Numeric(12, 2), nullable=False, default=0)
    discount_amount = Column(Numeric(12, 2), nullable=False, default=0)
    grand_total = Column(Numeric(12, 2), nullable=False, default=0)
    status = Column(String(50), nullable=False, default="DRAFT")  # DRAFT, ISSUED, PAID, CANCELLED, etc.
    created_by = Column(Integer, ForeignKey("users.user_id"), nullable=False)

    # Relationships
    line_items = relationship("InvoiceLineItem", back_populates="invoice", cascade="all, delete-orphan")


class InvoiceLineItem(Base):
    __tablename__ = "invoice_line_items"

    line_item_id = Column(Integer, primary_key=True, autoincrement=True)
    invoice_id = Column(Integer, ForeignKey("invoices.invoice_id", ondelete="CASCADE"), nullable=False)
    service_id = Column(Integer, ForeignKey("service_master.service_id"), nullable=False)
    description = Column(String(255), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    unit_price = Column(Numeric(12, 2), nullable=False)
    line_subtotal = Column(Numeric(12, 2), nullable=False)
    tax_amount = Column(Numeric(12, 2), nullable=False, default=0)
    line_total = Column(Numeric(12, 2), nullable=False)

    # Relationships
    invoice = relationship("Invoice", back_populates="line_items")
    service = relationship("ServiceMaster")  # optional - if you have ServiceMaster model
