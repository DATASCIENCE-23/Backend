"""
Pharmacy Module - Database Models
Represents the entities for medicine management, prescriptions, and dispensing
"""
from datetime import datetime, date
from typing import Optional
from sqlalchemy import Column, Integer, String, Numeric, Boolean, DateTime, Date, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from enum import Enum
from database import Base


class MedicineStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    DISCONTINUED = "discontinued"


class PrescriptionStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    PARTIALLY_COMPLETED = "partially_completed"
    CANCELLED = "cancelled"


class DispenseStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    BILLED = "billed"


# ============ MEDICINE MODELS ============

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


# ============ PRESCRIPTION MODELS ============

class Prescription(Base):
    __tablename__ = "prescription"

    prescription_id = Column(Integer, primary_key=True, autoincrement=True)
    record_id = Column(Integer, ForeignKey("medical_record.record_id"))
    patient_id = Column(Integer, ForeignKey("patient.patient_id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctor.doctor_id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    status = Column(SQLEnum(PrescriptionStatus), default=PrescriptionStatus.PENDING, nullable=False)
    notes = Column(Text)

    # External reference for integration
    external_ref = Column(String(100))  # Reference from doctor module

    # Relationships
    prescription_items = relationship("PrescriptionItem", back_populates="prescription", cascade="all, delete-orphan")
    dispenses = relationship("Dispense", back_populates="prescription")

    def __repr__(self):
        return f"<Prescription {self.prescription_id} - Status: {self.status}>"


class PrescriptionItem(Base):
    __tablename__ = "prescription_item"

    prescription_item_id = Column(Integer, primary_key=True, autoincrement=True)
    prescription_id = Column(Integer, ForeignKey("prescription.prescription_id"), nullable=False)
    medicine_id = Column(Integer, ForeignKey("medicine.medicine_id"), nullable=False)
    prescribed_quantity = Column(Integer, nullable=False)
    dosage = Column(String(100), nullable=False)  # e.g., "500mg"
    frequency = Column(String(100), nullable=False)  # e.g., "Twice daily"
    duration_days = Column(Integer, nullable=False)
    instructions = Column(Text)  # e.g., "Take after meals"

    # Relationships
    prescription = relationship("Prescription", back_populates="prescription_items")
    medicine = relationship("Medicine", back_populates="prescription_items")
    dispense_items = relationship("DispenseItem", back_populates="prescription_item")

    def __repr__(self):
        return f"<PrescriptionItem {self.prescription_item_id} - Medicine: {self.medicine_id}>"


# ============ DISPENSING MODELS ============

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


# ============ PHARMACIST MODEL ============

class Pharmacist(Base):
    __tablename__ = "pharmacist"

    pharmacist_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    employee_code = Column(String(50), unique=True, nullable=False)
    license_number = Column(String(50), unique=True, nullable=False)
    phone_number = Column(String(20))
    email = Column(String(100))
    is_active = Column(Boolean, default=True, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    dispenses = relationship("Dispense", back_populates="pharmacist")

    def __repr__(self):
        return f"<Pharmacist {self.first_name} {self.last_name}>"


# ============ AUDIT LOG FOR PHARMACY ============

class PharmacyAuditLog(Base):
    __tablename__ = "pharmacy_audit_log"

    log_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    entity_name = Column(String(100), nullable=False)  # Medicine, Prescription, Dispense
    entity_id = Column(Integer, nullable=False)
    action_type = Column(String(50), nullable=False)  # CREATE, UPDATE, DELETE, DISPENSE
    action_time = Column(DateTime, default=datetime.utcnow, nullable=False)
    ip_address = Column(String(50))
    details = Column(Text)  # JSON formatted details of the change

    def __repr__(self):
        return f"<AuditLog {self.entity_name}:{self.entity_id} - {self.action_type}>"