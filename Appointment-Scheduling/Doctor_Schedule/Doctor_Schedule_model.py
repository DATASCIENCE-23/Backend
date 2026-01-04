from sqlalchemy import Column, Integer, Time, Date, Enum, Boolean
from Doctor_Schedule.Doctor_Schedule_config import Base
import enum


# ============ MATCH DATABASE ENUM VALUES EXACTLY ============

class DayOfWeekEnum(enum.Enum):
    """
    Match database: hms.day_of_week_enum
    Values: 'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun'
    """
    mon = "mon"
    tue = "tue"
    wed = "wed"
    thu = "thu"
    fri = "fri"
    sat = "sat"
    sun = "sun"


class DoctorSchedule(Base):
    """Doctor Schedule model matching hms.doctor_schedule table"""
    __tablename__ = "doctor_schedule"
    __table_args__ = {"schema": "hms"}

    schedule_id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Foreign Key - just integer, DB has the constraint
    doctor_id = Column(Integer, nullable=False, index=True)
    
    # Day of Week
    day_of_week = Column(
        Enum(DayOfWeekEnum, name="day_of_week_enum", create_type=False, schema="hms"),
        nullable=False,
        index=True
    )
    
    # Time Slots
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    
    # Slot Configuration
    slot_duration = Column(Integer, nullable=False)
    max_patients_per_slot = Column(Integer, nullable=False)
    
    # Active Status
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Effective Dates
    effective_from = Column(Date, nullable=False)
    effective_to = Column(Date, nullable=True)
    
    def __repr__(self):
        return f"<DoctorSchedule {self.schedule_id}: Dr.{self.doctor_id} {self.day_of_week.value} {self.start_time}-{self.end_time}>"