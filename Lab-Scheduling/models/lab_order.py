"""
Lab Order Model
SQLAlchemy model for laboratory test orders
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import enum


class OrderPriority(enum.Enum):
    NORMAL = "normal"
    URGENT = "urgent"
    STAT = "stat"


class OrderStatus(enum.Enum):
    PENDING = "pending"
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class LabOrder(Base):
    """Lab Order model for managing laboratory test orders"""
    
    __tablename__ = "lab_orders"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, nullable=False, index=True)
    doctor_id = Column(Integer, nullable=False, index=True)
    medical_record_id = Column(Integer, nullable=True, index=True)
    
    test_names = Column(String(500), nullable=False)
    priority = Column(Enum(OrderPriority), default=OrderPriority.NORMAL, nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING, nullable=False)
    
    clinical_notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    schedules = relationship("LabSchedule", back_populates="order", cascade="all, delete-orphan")
    results = relationship("LabResult", back_populates="order", cascade="all, delete-orphan")
    reports = relationship("LabReport", back_populates="order", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<LabOrder(id={self.id}, patient_id={self.patient_id}, status={self.status.value})>"