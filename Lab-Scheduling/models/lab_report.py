"""
Lab Report Model
SQLAlchemy model for laboratory reports
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import enum


class ReportStatus(enum.Enum):
    DRAFT = "draft"
    PENDING_FINALIZATION = "pending_finalization"
    FINALIZED = "finalized"


class LabReport(Base):
    """Lab Report model for comprehensive laboratory reports"""
    
    __tablename__ = "lab_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("lab_orders.id"), nullable=False, index=True)
    
    summary = Column(Text, nullable=True)
    findings = Column(Text, nullable=True)
    recommendations = Column(Text, nullable=True)
    
    status = Column(Enum(ReportStatus), default=ReportStatus.DRAFT, nullable=False)
    
    # Finalization tracking
    finalized_at = Column(DateTime(timezone=True), nullable=True)
    finalized_by = Column(Integer, nullable=True, index=True)
    
    # EMR Integration
    emr_integrated = Column(Boolean, default=False, nullable=False)
    emr_integration_date = Column(DateTime(timezone=True), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    order = relationship("LabOrder", back_populates="reports")
    
    def __repr__(self):
        return f"<LabReport(id={self.id}, order_id={self.order_id}, status={self.status.value})>"