from datetime import datetime, date
from typing import Optional
from sqlalchemy import Column, Integer, String, Numeric, Boolean, DateTime, Date, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from enum import Enum
from database import Base

class Medicine(Base):
    __tablename__ = "medicine"

    medicine_id = Column(Integer, primary_key=True, autoincrement=True)
    medicine_name = Column(String(200), nullable=False)
    generic_name = Column(String(200), nullable=False)
    strength = Column(String(50), nullable=False)
    form = Column(String(50), nullable=False)  # Tablet, Capsule, Syrup, Injection
    shelf_location = Column(String(50))
    unit_price = Column(Numeric(10, 2), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    min_quantity = Column(Integer, default=10)
    reorder_level = Column(Integer, default=20)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(Integer, ForeignKey("user.user_id"))
    updated_by = Column(Integer, ForeignKey("user.user_id"))

    # Relationships
    batches = relationship("MedicineBatch", back_populates="medicine")
    prescription_items = relationship("PrescriptionItem", back_populates="medicine")

    def __repr__(self):
        return f"<Medicine {self.medicine_name} - {self.strength}>"

class MedicineBatch(Base):
    __tablename__ = "medicine_batch"

    batch_id = Column(Integer, primary_key=True, autoincrement=True)
    medicine_id = Column(Integer, ForeignKey("medicine.medicine_id"), nullable=False)
    batch_number = Column(String(50), unique=True, nullable=False)
    quantity_in_stock = Column(Integer, nullable=False, default=0)
    manufacture_date = Column(Date, nullable=False)
    expiry_date = Column(Date, nullable=False)
    purchase_price = Column(Numeric(10, 2), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    medicine = relationship("Medicine", back_populates="batches")
    dispense_items = relationship("DispenseItem", back_populates="batch")

    def __repr__(self):
        return f"<Batch {self.batch_number} - Qty: {self.quantity_in_stock}>"

