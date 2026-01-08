"""
Lab Technician Model
SQLAlchemy model for laboratory technicians
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class LabTechnician(Base):
    """Lab Technician model for managing laboratory staff"""
    
    __tablename__ = "lab_technicians"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    
    license_number = Column(String(50), unique=True, nullable=False, index=True)
    specialization = Column(String(100), nullable=True)
    
    phone_number = Column(String(20), nullable=True)
    email = Column(String(100), unique=True, nullable=True, index=True)
    
    is_active = Column(Boolean, default=True, nullable=False)
    notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    schedules = relationship("LabSchedule", back_populates="technician")
    
    def __repr__(self):
        return f"<LabTechnician(id={self.id}, user_id={self.user_id}, license={self.license_number})>"