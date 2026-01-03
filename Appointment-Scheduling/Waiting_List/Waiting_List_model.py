from sqlalchemy import Column, Integer, Date, Time, Text, DateTime, Enum, ForeignKey
from sqlalchemy.sql import func
from Waiting_List_config import Base
import enum

class WaitingListStatusEnum(enum.Enum):
    ACTIVE = "Active"
    NOTIFIED = "Notified"
    ACCEPTED = "Accepted"
    DECLINED = "Declined"
    EXPIRED = "Expired"
    CANCELLED = "Cancelled"

class WaitingList(Base):
    __tablename__ = "waiting_list"

    waiting_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Foreign Keys
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False, index=True)
    doctor_id = Column(Integer, ForeignKey("doctor.doctor_id"), nullable=False, index=True)
    
    # Preferred Date and Time
    preferred_date = Column(Date, nullable=False, index=True)
    preferred_time_start = Column(Time, nullable=False)
    preferred_time_end = Column(Time, nullable=False)
    
    # Reason for waiting
    reason = Column(Text, nullable=True)
    
    # Status
    status = Column(
        Enum(WaitingListStatusEnum),
        nullable=False,
        default=WaitingListStatusEnum.ACTIVE,
        index=True
    )
    
    # Timestamps
    added_at = Column(DateTime, nullable=False, default=func.now())
    notified_at = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=False)
    
    def __repr__(self):
        return f"<WaitingList(id={self.waiting_id}, patient_id={self.patient_id}, doctor_id={self.doctor_id}, status={self.status})>"