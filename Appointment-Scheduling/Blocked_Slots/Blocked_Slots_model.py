from sqlalchemy import Column, Integer, Date, Time, DateTime, Text
from sqlalchemy.sql import func
from Blocked_Slots.Blocked_Slots_config import Base


class BlockedSlot(Base):
    """Blocked Slots model matching hms.blocked_slots table"""
    __tablename__ = "blocked_slots"
    __table_args__ = {"schema": "hms"}

    blocked_slot_id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Foreign Key - just integer, DB has the constraint
    doctor_id = Column(Integer, nullable=False, index=True)
    
    # Date and Time
    blocked_date = Column(Date, nullable=False, index=True)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    
    # Reason for blocking
    reason = Column(Text, nullable=False)
    
    # Audit fields
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    created_by = Column(Integer, nullable=False)
    
    def __repr__(self):
        return f"<BlockedSlot {self.blocked_slot_id}: Dr.{self.doctor_id} on {self.blocked_date} {self.start_time}-{self.end_time}>"