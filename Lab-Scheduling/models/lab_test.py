"""
Lab Test Model
SQLAlchemy model for laboratory test definitions
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, Numeric, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import enum


class SampleType(enum.Enum):
    BLOOD = "blood"
    URINE = "urine"
    STOOL = "stool"
    SALIVA = "saliva"
    OTHER = "other"


class LabTest(Base):
    """Lab Test model for defining available laboratory tests"""
    
    __tablename__ = "lab_tests"
    
    id = Column(Integer, primary_key=True, index=True)
    
    name = Column(String(100), nullable=False, index=True)
    code = Column(String(20), unique=True, nullable=False, index=True)
    category = Column(String(50), nullable=True, index=True)
    
    description = Column(Text, nullable=True)
    sample_type = Column(Enum(SampleType), default=SampleType.BLOOD, nullable=False)
    
    # Test configuration
    duration_minutes = Column(Integer, default=30, nullable=False)
    requires_fasting = Column(Boolean, default=False, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Cost information
    price = Column(Numeric(10, 2), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    results = relationship("LabResult", back_populates="test")
    
    def __repr__(self):
        return f"<LabTest(id={self.id}, name={self.name}, code={self.code})>"