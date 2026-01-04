from sqlalchemy import Column, Integer, DateTime, Text, Enum, ForeignKey
from sqlalchemy.sql import func
from Appointment_Reminder_config import Base
import enum

class ReminderTypeEnum(enum.Enum):
    EMAIL = "Email"
    SMS = "SMS"
    PUSH_NOTIFICATION = "Push Notification"
    WHATSAPP = "WhatsApp"

class ReminderStatusEnum(enum.Enum):
    PENDING = "Pending"
    SENT = "Sent"
    FAILED = "Failed"
    CANCELLED = "Cancelled"

class AppointmentReminder(Base):
    __tablename__ = "appointment_reminder"

    reminder_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Foreign Key
    appointment_id = Column(Integer, ForeignKey("appointment.appointment_id"), nullable=False, index=True)
    
    # Reminder Details
    reminder_type = Column(
        Enum(ReminderTypeEnum),
        nullable=False
    )
    
    reminder_time = Column(DateTime, nullable=False, index=True)
    sent_at = Column(DateTime, nullable=True)
    
    status = Column(
        Enum(ReminderStatusEnum),
        nullable=False,
        default=ReminderStatusEnum.PENDING,
        index=True
    )
    
    # Message Content
    message_content = Column(Text, nullable=True)
    
    def __repr__(self):
        return f"<AppointmentReminder(id={self.reminder_id}, appointment_id={self.appointment_id}, type={self.reminder_type}, status={self.status})>"