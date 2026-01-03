from sqlalchemy import Column, Integer, String, Date, Time, DateTime, Text, Enum, Numeric, ForeignKey
from sqlalchemy.sql import func
from Appointment_config import Base
import enum

class AppointmentTypeEnum(enum.Enum):
    CONSULTATION = "Consultation"
    FOLLOWUP = "Follow-up"
    EMERGENCY = "Emergency"
    ROUTINE_CHECKUP = "Routine Checkup"

class AppointmentStatusEnum(enum.Enum):
    SCHEDULED = "Scheduled"
    CONFIRMED = "Confirmed"
    CANCELLED = "Cancelled"
    COMPLETED = "Completed"
    NO_SHOW = "No Show"
    RESCHEDULED = "Rescheduled"

class Appointment(Base):
    __tablename__ = "appointment"

    appointment_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Foreign Keys
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False, index=True)
    doctor_id = Column(Integer, ForeignKey("doctor.doctor_id"), nullable=False, index=True)
    
    # Appointment Date and Time
    appointment_date = Column(Date, nullable=False, index=True)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    
    # Appointment Details
    appointment_type = Column(
        Enum(AppointmentTypeEnum),
        nullable=False,
        default=AppointmentTypeEnum.CONSULTATION
    )
    
    status = Column(
        Enum(AppointmentStatusEnum),
        nullable=False,
        default=AppointmentStatusEnum.SCHEDULED
    )
    
    reason_for_visit = Column(Text, nullable=True)
    symptoms = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    
    # Consultation Fee
    consultation_fee = Column(Numeric(10, 2), nullable=True)
    
    # Booking Information
    booking_date = Column(DateTime, nullable=False, default=func.now())
    
    # Cancellation Information
    cancellation_reason = Column(Text, nullable=True)
    cancelled_at = Column(DateTime, nullable=True)
    cancelled_by = Column(Integer, ForeignKey("user.user_id"), nullable=True)
    
    def __repr__(self):
        return f"<Appointment(id={self.appointment_id}, patient_id={self.patient_id}, doctor_id={self.doctor_id}, date={self.appointment_date}, status={self.status})>"
