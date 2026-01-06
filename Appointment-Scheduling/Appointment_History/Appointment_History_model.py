from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    Time,
    DateTime,
    Text,
    Enum,
    ForeignKey
)
from sqlalchemy.sql import func
from Appointment_History.Appointment_History_config import Base
import enum


# ================= ENUM =================

class ChangeTypeEnum(enum.Enum):
    CREATED = "Created"
    UPDATED = "Updated"
    RESCHEDULED = "Rescheduled"
    CANCELLED = "Cancelled"
    CONFIRMED = "Confirmed"
    COMPLETED = "Completed"
    NO_SHOW = "No Show"
    STATUS_CHANGED = "Status Changed"


# ================= MODEL =================

class AppointmentHistory(Base):
    __tablename__ = "appointment_history"
    __table_args__ = {"schema": "hms"}  # IMPORTANT

    history_id = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True
    )

    # -------- Foreign Keys --------
    appointment_id = Column(
        Integer,
        ForeignKey("appointment.appointment_id"),
        nullable=False,
        index=True
    )

    changed_by = Column(
        Integer,
        ForeignKey("users.user_id"),
        nullable=False
    )

    # -------- Change Type --------
    change_type = Column(
        Enum(
            ChangeTypeEnum,
            name="change_type_enum",
            create_type=False
        ),
        nullable=False,
        index=True
    )

    # -------- Old Values --------
    old_date = Column(Date)
    old_time = Column(Time)
    old_status = Column(String(50))

    # -------- New Values --------
    new_date = Column(Date)
    new_time = Column(Time)
    new_status = Column(String(50))

    # -------- Details --------
    change_reason = Column(Text)

    changed_at = Column(
        DateTime,
        nullable=False,
        default=func.now(),
        index=True
    )

    def __repr__(self):
        return (
            f"<AppointmentHistory("
            f"history_id={self.history_id}, "
            f"appointment_id={self.appointment_id}, "
            f"change_type={self.change_type}"
            f")>"
        )
