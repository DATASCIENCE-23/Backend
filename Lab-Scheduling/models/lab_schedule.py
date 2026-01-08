"""
Lab Schedule Model
SQLAlchemy model for laboratory appointment scheduling
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import enum


class ScheduleStatus(enum.Enum):
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class SampleType(enum.Enum):
    BLOOD = "blood"
    URINE = "urine"
    STOOL = "stool"
    SALIVA = "saliva"
    OTHER = "other"


class LabSchedule(Base):
    """Lab Schedule model for managing laboratory appointments"""
    
    __tablename__ = "lab_schedules"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("lab_orders.id"), nullable=False, index=True)
    technician_id = Column(Integer, ForeignKey("lab_technicians.id"), nullable=False, index=True)
    
    scheduled_datetime = Column(DateTime(timezone=True), nullable=False, index=True)
    
    sample_type = Column(Enum(SampleType), default=SampleType.BLOOD, nullable=False)
    status = Column(Enum(ScheduleStatus), default=ScheduleStatus.SCHEDULED, nullable=False)
    is_home_collection = Column(Boolean, default=False, nullable=False)
    
    notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    order = relationship("LabOrder", back_populates="schedules")
    technician = relationship("LabTechnician", back_populates="schedules")
    
    def __repr__(self):
        return f"<LabSchedule(id={self.id}, order_id={self.order_id}, datetime={self.scheduled_datetime})>"