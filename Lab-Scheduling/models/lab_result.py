"""
Lab Result Model
SQLAlchemy model for laboratory test results
"""

from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, Text, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import enum


class ResultStatus(enum.Enum):
    PENDING_VERIFICATION = "pending_verification"
    VERIFIED = "verified"
    REJECTED = "rejected"


class LabResult(Base):
    """Lab Result model for storing laboratory test results"""
    
    __tablename__ = "lab_results"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("lab_orders.id"), nullable=False, index=True)
    test_id = Column(Integer, ForeignKey("lab_tests.id"), nullable=False, index=True)
    
    result_value = Column(String(200), nullable=False)
    numeric_value = Column(Float, nullable=True)
    unit = Column(String(50), nullable=True)
    reference_range_min = Column(Float, nullable=True)
    reference_range_max = Column(Float, nullable=True)
    
    status = Column(Enum(ResultStatus), default=ResultStatus.PENDING_VERIFICATION, nullable=False)
    is_abnormal = Column(Boolean, default=False, nullable=False)
    
    test_name = Column(String(200), nullable=True)
    notes = Column(Text, nullable=True)
    
    # Verification tracking
    verified_at = Column(DateTime(timezone=True), nullable=True)
    verified_by = Column(Integer, nullable=True, index=True)
    verification_notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    order = relationship("LabOrder", back_populates="results")
    test = relationship("LabTest", back_populates="results")
    
    def __repr__(self):
        return f"<LabResult(id={self.id}, order_id={self.order_id}, value={self.result_value})>"