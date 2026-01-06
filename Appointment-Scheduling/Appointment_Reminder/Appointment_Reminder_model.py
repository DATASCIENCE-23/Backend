from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    Text,
    Enum,
    ForeignKey
)
from sqlalchemy.sql import func
from Appointment_Reminder.Appointment_Reminder_config import Base
import enum


# ================= ENUMS =================

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


# ================= MODEL =================

class AppointmentReminder(Base):
    __tablename__ = "appointment_reminder"
    __table_args__ = {"schema": "hms"}

    reminder_id = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True
    )

    appointment_id = Column(
        Integer,
        ForeignKey("hms.appointment.appointment_id"),
        nullable=False,
        index=True
    )

    reminder_type = Column(
        Enum(
            ReminderTypeEnum,
            name="reminder_type_enum",
            create_type=False
        ),
        nullable=False
    )

    reminder_time = Column(
        DateTime,
        nullable=False,
        index=True
    )

    sent_at = Column(DateTime)

    status = Column(
        Enum(
            ReminderStatusEnum,
            name="reminder_status_enum",
            create_type=False
        ),
        nullable=False,
        default=ReminderStatusEnum.PENDING,
        index=True
    )

    message_content = Column(Text)

    created_at = Column(
        DateTime,
        nullable=False,
        default=func.now()
    )

    def __repr__(self):
        return (
            f"<AppointmentReminder("
            f"reminder_id={self.reminder_id}, "
            f"appointment_id={self.appointment_id}, "
            f"type={self.reminder_type}, "
            f"status={self.status}"
            f")>"
        )
