from datetime import datetime, date
from typing import Optional
from sqlalchemy import Column, Integer, String, Numeric, Boolean, DateTime, Date, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from enum import Enum
from ..database import Base

class PharmacyAuditLog(Base):
    __tablename__ = "pharmacy_audit_log"

    log_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    entity_name = Column(String(100), nullable=False)  # Medicine, Prescription, Dispense
    entity_id = Column(Integer, nullable=False)
    action_type = Column(String(50), nullable=False)  # CREATE, UPDATE, DELETE, DISPENSE
    action_time = Column(DateTime, default=datetime.utcnow, nullable=False)
    ip_address = Column(String(50))
    details = Column(Text)  # JSON formatted details of the change

    def __repr__(self):
        return f"<AuditLog {self.entity_name}:{self.entity_id} - {self.action_type}>"