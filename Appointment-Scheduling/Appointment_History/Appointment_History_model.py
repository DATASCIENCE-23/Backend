from sqlalchemy import Column, Integer, String, Date, Time, DateTime, Text, Enum, ForeignKey
from sqlalchemy.sql import func
from Appointment_History_config import Base
import enum

class ChangeTypeEnum(enum.Enum):
    CREATED = "Created"
    UPDATED = "Updated"
    RESCHEDULED = "Rescheduled"
    CANCELLED = "Cancelled"
    CONFIRMED = "Confirmed"
    COMPLETED = "Completed"
    NO_SHOW = "No Show"
    STATUS_CHANGED = "Status Changed"

class AppointmentHistory(Base):
    __tablename__ = "appointment_history"

    history_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Foreign Keys
    appointment_id = Column(Integer, ForeignKey("appointment.appointment_id"), nullable=False, index=True)
    changed_by = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    
    # Change Information
    change_type = Column(
        Enum(ChangeTypeEnum),
        nullable=False,
        index=True
    )
    
    # Old Values
    old_date = Column(Date, nullable=True)
    old_time = Column(Time, nullable=True)
    old_status = Column(String(50), nullable=True)
    
    # New Values
    new_date = Column(Date, nullable=True)
    new_time = Column(Time, nullable=True)
    new_status = Column(String(50), nullable=True)
    
    # Change Details
    change_reason = Column(Text, nullable=True)
    changed_at = Column(DateTime, nullable=False, default=func.now(), index=True)
    
    def __repr__(self):
        return f"<AppointmentHistory(id={self.history_id}, appointment_id={self.appointment_id}, type={self.change_type})>"