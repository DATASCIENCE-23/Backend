from sqlalchemy import Column, Integer, String, Date, Time, Enum, Boolean, ForeignKey
from sqlalchemy.sql import func
from Doctor_Schedule_config import Base
import enum

class DayOfWeekEnum(enum.Enum):
    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY = "Thursday"
    FRIDAY = "Friday"
    SATURDAY = "Saturday"
    SUNDAY = "Sunday"

class DoctorSchedule(Base):
    __tablename__ = "doctor_schedule"

    schedule_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Foreign Key
    doctor_id = Column(Integer, ForeignKey("doctor.doctor_id"), nullable=False, index=True)
    
    # Day of Week
    day_of_week = Column(
        Enum(DayOfWeekEnum),
        nullable=False,
        index=True
    )
    
    # Time Slots
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    
    # Slot Configuration
    slot_duration = Column(Integer, nullable=False, comment="Duration in minutes")
    max_patients_per_slot = Column(Integer, nullable=False, default=1)
    
    # Active Status
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Effective Dates
    effective_from = Column(Date, nullable=False)
    effective_to = Column(Date, nullable=True)
    
    def __repr__(self):
        return f"<DoctorSchedule(id={self.schedule_id}, doctor_id={self.doctor_id}, day={self.day_of_week}, time={self.start_time}-{self.end_time})>"
