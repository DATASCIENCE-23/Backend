from datetime import datetime, date
from typing import Optional
from sqlalchemy import Column, Integer, String, Numeric, Boolean, DateTime, Date, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from enum import Enum
from database import Base
from .. import  Pharmacist,  MedicineBatch
from .../prescription import Prescription, PrescriptionItem


class DispenseStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    BILLED = "billed"


class Dispense(Base):
    __tablename__ = "dispense"

    dispense_id = Column(Integer, primary_key=True, autoincrement=True)
    prescription_id = Column(Integer, ForeignKey("prescription.prescription_id"), nullable=False)
    pharmacist_id = Column(Integer, ForeignKey("pharmacist.pharmacist_id"), nullable=False)
    dispensed_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False)
    status = Column(SQLEnum(DispenseStatus), default=DispenseStatus.PENDING, nullable=False)
    invoice_id = Column(Integer, ForeignKey("invoice.invoice_id"))

    notes = Column(Text)  # Any special notes or partial dispense reasons

    # Relationships
    prescription = relationship("Prescription", back_populates="dispenses")
    pharmacist = relationship("Pharmacist", back_populates="dispenses")
    dispense_items = relationship("DispenseItem", back_populates="dispense", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Dispense {self.dispense_id} - Amount: {self.total_amount}>"


class DispenseItem(Base):
    __tablename__ = "dispense_item"

    dispense_item_id = Column(Integer, primary_key=True, autoincrement=True)
    dispense_id = Column(Integer, ForeignKey("dispense.dispense_id"), nullable=False)
    prescription_item_id = Column(Integer, ForeignKey("prescription_item.prescription_item_id"), nullable=False)
    batch_id = Column(Integer, ForeignKey("medicine_batch.batch_id"), nullable=False)
    dispensed_quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)
    line_total = Column(Numeric(10, 2), nullable=False)

    # Relationships
    dispense = relationship("Dispense", back_populates="dispense_items")
    prescription_item = relationship("PrescriptionItem", back_populates="dispense_items")
    batch = relationship("MedicineBatch", back_populates="dispense_items")

    def __repr__(self):
        return f"<DispenseItem {self.dispense_item_id} - Qty: {self.dispensed_quantity}>"

