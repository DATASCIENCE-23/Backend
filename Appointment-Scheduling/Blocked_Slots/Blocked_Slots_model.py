from sqlalchemy import Column, Integer, Date, Time, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from Blocked_Slots_config import Base

class BlockedSlot(Base):
    __tablename__ = "blocked_slots"

    blocked_slot_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Foreign Key
    doctor_id = Column(Integer, ForeignKey("doctor.doctor_id"), nullable=False, index=True)
    
    # Blocked Date and Time
    blocked_date = Column(Date, nullable=False, index=True)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    
    # Reason for Blocking
    reason = Column(Text, nullable=False)
    
    # Audit Information
    created_at = Column(DateTime, nullable=False, default=func.now())
    created_by = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    
    def __repr__(self):
        return f"<BlockedSlot(id={self.blocked_slot_id}, doctor_id={self.doctor_id}, date={self.blocked_date}, time={self.start_time}-{self.end_time})>"
