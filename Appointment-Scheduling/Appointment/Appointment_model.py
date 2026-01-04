from sqlalchemy import Column, Integer, String, Date, Time, DateTime, Text, Enum, Numeric
from sqlalchemy.sql import func
from Appointment.Appointment_config import Base
import enum


# ============ MATCH DATABASE ENUM VALUES EXACTLY ============

class AppointmentTypeEnum(enum.Enum):
    """
    Match database: hms.appointment_type_enum
    Values: 'opd', 'follow_up', 'emergency'
    """
    opd = "opd"
    follow_up = "follow_up"
    emergency = "emergency"


class AppointmentStatusEnum(enum.Enum):
    """
    Match database: hms.appointment_status_enum
    Values: 'scheduled', 'completed', 'cancelled', 'no_show'
    """
    scheduled = "scheduled"
    completed = "completed"
    cancelled = "cancelled"
    no_show = "no_show"


class Appointment(Base):
    __tablename__ = "appointment"
    __table_args__ = {"schema": "hms"}

    appointment_id = Column(Integer, primary_key=True, autoincrement=True)

    # Foreign Keys - Just define as Integer, DB already has the constraints
    patient_id = Column(Integer, nullable=False, index=True)
    doctor_id = Column(Integer, nullable=False, index=True)

    appointment_date = Column(Date, nullable=False, index=True)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)

    appointment_type = Column(
        Enum(AppointmentTypeEnum, name="appointment_type_enum", create_type=False, schema="hms"),
        nullable=False,
        default=AppointmentTypeEnum.opd
    )

    status = Column(
        Enum(AppointmentStatusEnum, name="appointment_status_enum", create_type=False, schema="hms"),
        nullable=False,
        default=AppointmentStatusEnum.scheduled
    )

    reason_for_visit = Column(Text)
    symptoms = Column(Text)
    notes = Column(Text)

    consultation_fee = Column(Numeric(10, 2))

    booking_date = Column(DateTime, nullable=False, server_default=func.now())

    def __repr__(self):
        return f"<Appointment {self.appointment_id} - {self.status.value}>"