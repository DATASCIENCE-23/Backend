from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base


class AuditLog(Base):
    __tablename__ = "audit_log"
    __table_args__ = {"schema": "hms"}   # ✅ ADD THIS

    log_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("hms.users.user_id", ondelete="SET NULL"), nullable=True, index=True)
    entity_name = Column(String(100), nullable=True)  # e.g., "Patient", "MedicalRecord"
    entity_id = Column(Integer, nullable=True)  # ID of the entity affected
    action_time = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False, index=True)
    action_type = Column(String(100), nullable=False)  # e.g., "login", "view_medical_record", "create_report"
    ip_address = Column(String(45), nullable=True)  # Supports IPv4 and IPv6
    details = Column(String, nullable=True)  # Additional details about the action

    # Relationship back to User (optional, for easy querying)
    user = relationship("User", back_populates="audit_logs")


# IMPORTANT: In your User model (User_model.py), add this line:
# audit_logs = relationship("AuditLog", back_populates="user")