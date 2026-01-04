from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from datetime import date, time, datetime
from typing import List, Optional
from Blocked_Slots.Blocked_Slots_model import BlockedSlot

class BlockedSlotRepository:

    @staticmethod
    def get_by_id(db: Session, blocked_slot_id: int) -> Optional[BlockedSlot]:
        """Get blocked slot by ID"""
        return db.query(BlockedSlot).filter(BlockedSlot.blocked_slot_id == blocked_slot_id).first()

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[BlockedSlot]:
        """Get all blocked slots with pagination"""
        return db.query(BlockedSlot).offset(skip).limit(limit).all()

    @staticmethod
    def get_by_doctor_id(db: Session, doctor_id: int) -> List[BlockedSlot]:
        """Get all blocked slots for a specific doctor"""
        return db.query(BlockedSlot).filter(BlockedSlot.doctor_id == doctor_id).all()

    @staticmethod
    def get_by_date(db: Session, blocked_date: date) -> List[BlockedSlot]:
        """Get all blocked slots on a specific date"""
        return db.query(BlockedSlot).filter(BlockedSlot.blocked_date == blocked_date).all()

    @staticmethod
    def get_by_doctor_and_date(db: Session, doctor_id: int, blocked_date: date) -> List[BlockedSlot]:
        """Get blocked slots for a doctor on a specific date"""
        return db.query(BlockedSlot).filter(
            and_(
                BlockedSlot.doctor_id == doctor_id,
                BlockedSlot.blocked_date == blocked_date
            )
        ).all()

    @staticmethod
    def get_upcoming_blocked_slots(db: Session, doctor_id: int, from_date: date) -> List[BlockedSlot]:
        """Get upcoming blocked slots for a doctor"""
        return db.query(BlockedSlot).filter(
            and_(
                BlockedSlot.doctor_id == doctor_id,
                BlockedSlot.blocked_date >= from_date
            )
        ).order_by(BlockedSlot.blocked_date, BlockedSlot.start_time).all()

    @staticmethod
    def get_past_blocked_slots(db: Session, doctor_id: int, before_date: date) -> List[BlockedSlot]:
        """Get past blocked slots for a doctor"""
        return db.query(BlockedSlot).filter(
            and_(
                BlockedSlot.doctor_id == doctor_id,
                BlockedSlot.blocked_date < before_date
            )
        ).order_by(BlockedSlot.blocked_date.desc(), BlockedSlot.start_time.desc()).all()

    @staticmethod
    def get_by_date_range(
        db: Session, 
        doctor_id: int, 
        start_date: date, 
        end_date: date
    ) -> List[BlockedSlot]:
        """Get blocked slots within a date range"""
        return db.query(BlockedSlot).filter(
            and_(
                BlockedSlot.doctor_id == doctor_id,
                BlockedSlot.blocked_date >= start_date,
                BlockedSlot.blocked_date <= end_date
            )
        ).order_by(BlockedSlot.blocked_date, BlockedSlot.start_time).all()

    @staticmethod
    def check_time_conflict(
        db: Session,
        doctor_id: int,
        blocked_date: date,
        start_time: time,
        end_time: time,
        exclude_blocked_slot_id: Optional[int] = None
    ) -> List[BlockedSlot]:
        """
        Check if there's a time conflict for a doctor on a specific date
        Returns list of conflicting blocked slots
        """
        query = db.query(BlockedSlot).filter(
            and_(
                BlockedSlot.doctor_id == doctor_id,
                BlockedSlot.blocked_date == blocked_date,
                # Time overlap check
                or_(
                    and_(
                        BlockedSlot.start_time <= start_time,
                        BlockedSlot.end_time > start_time
                    ),
                    and_(
                        BlockedSlot.start_time < end_time,
                        BlockedSlot.end_time >= end_time
                    ),
                    and_(
                        BlockedSlot.start_time >= start_time,
                        BlockedSlot.end_time <= end_time
                    )
                )
            )
        )
        
        # Exclude current blocked slot when checking for updates
        if exclude_blocked_slot_id:
            query = query.filter(BlockedSlot.blocked_slot_id != exclude_blocked_slot_id)
        
        return query.all()

    @staticmethod
    def get_blocked_dates(db: Session, doctor_id: int) -> List[date]:
        """Get list of dates that have blocked slots for a doctor"""
        results = db.query(BlockedSlot.blocked_date).filter(
            BlockedSlot.doctor_id == doctor_id
        ).distinct().order_by(BlockedSlot.blocked_date).all()
        
        return [result[0] for result in results]

    @staticmethod
    def create(db: Session, blocked_slot: BlockedSlot) -> BlockedSlot:
        """Create a new blocked slot"""
        db.add(blocked_slot)
        db.commit()
        db.refresh(blocked_slot)
        return blocked_slot

    @staticmethod
    def update(db: Session, blocked_slot: BlockedSlot) -> BlockedSlot:
        """Update an existing blocked slot"""
        db.commit()
        db.refresh(blocked_slot)
        return blocked_slot

    @staticmethod
    def delete(db: Session, blocked_slot: BlockedSlot) -> None:
        """Delete a blocked slot"""
        db.delete(blocked_slot)
        db.commit()

    @staticmethod
    def delete_by_date_range(
        db: Session, 
        doctor_id: int, 
        start_date: date, 
        end_date: date
    ) -> int:
        """Delete blocked slots within a date range. Returns count of deleted slots."""
        count = db.query(BlockedSlot).filter(
            and_(
                BlockedSlot.doctor_id == doctor_id,
                BlockedSlot.blocked_date >= start_date,
                BlockedSlot.blocked_date <= end_date
            )
        ).delete()
        db.commit()
        return count

    @staticmethod
    def count_by_doctor(db: Session, doctor_id: int) -> int:
        """Count total blocked slots for a doctor"""
        return db.query(BlockedSlot).filter(
            BlockedSlot.doctor_id == doctor_id
        ).count()

    @staticmethod
    def count_upcoming(db: Session, doctor_id: int, from_date: date) -> int:
        """Count upcoming blocked slots for a doctor"""
        return db.query(BlockedSlot).filter(
            and_(
                BlockedSlot.doctor_id == doctor_id,
                BlockedSlot.blocked_date >= from_date
            )
        ).count()