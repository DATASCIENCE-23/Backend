from sqlalchemy.orm import Session
from datetime import date, time, datetime, timedelta
from typing import List, Optional, Dict
from Blocked_Slots.Blocked_Slots_model import BlockedSlot
from Blocked_Slots.Blocked_Slots_repository import BlockedSlotRepository

class BlockedSlotService:

    @staticmethod
    def create_blocked_slot(db: Session, data: dict) -> BlockedSlot:
        """
        Create a new blocked slot with validation
        """
        # Extract required fields
        doctor_id = data.get("doctor_id")
        blocked_date = data.get("blocked_date")
        start_time = data.get("start_time")
        end_time = data.get("end_time")
        reason = data.get("reason")
        created_by = data.get("created_by")

        # Validate required fields
        if not all([doctor_id, blocked_date, start_time, end_time, reason, created_by]):
            raise ValueError("Missing required fields: doctor_id, blocked_date, start_time, end_time, reason, created_by")

        # Convert string dates/times if needed
        if isinstance(blocked_date, str):
            blocked_date = datetime.strptime(blocked_date, "%Y-%m-%d").date()
        if isinstance(start_time, str):
            start_time = datetime.strptime(start_time, "%H:%M:%S").time()
        if isinstance(end_time, str):
            end_time = datetime.strptime(end_time, "%H:%M:%S").time()

        # Validate date (should not be in the past)
        if blocked_date < date.today():
            raise ValueError("Cannot block dates in the past")

        # Validate time logic
        if start_time >= end_time:
            raise ValueError("Start time must be before end time")

        # Check for time conflicts
        conflicts = BlockedSlotRepository.check_time_conflict(
            db, doctor_id, blocked_date, start_time, end_time
        )
        
        if conflicts:
            conflict_times = [f"{c.start_time}-{c.end_time}" for c in conflicts]
            raise ValueError(f"Time slot conflicts with existing blocked slots: {', '.join(conflict_times)}")

        # Create blocked slot object
        blocked_slot = BlockedSlot(
            doctor_id=doctor_id,
            blocked_date=blocked_date,
            start_time=start_time,
            end_time=end_time,
            reason=reason,
            created_by=created_by,
            created_at=datetime.now()
        )

        return BlockedSlotRepository.create(db, blocked_slot)

    @staticmethod
    def block_full_day(db: Session, doctor_id: int, blocked_date: date, reason: str, created_by: int) -> BlockedSlot:
        """
        Block an entire day for a doctor (00:00 to 23:59)
        """
        data = {
            "doctor_id": doctor_id,
            "blocked_date": blocked_date,
            "start_time": time(0, 0, 0),
            "end_time": time(23, 59, 59),
            "reason": reason,
            "created_by": created_by
        }
        return BlockedSlotService.create_blocked_slot(db, data)

    @staticmethod
    def block_multiple_days(
        db: Session, 
        doctor_id: int, 
        start_date: date, 
        end_date: date, 
        reason: str, 
        created_by: int
    ) -> List[BlockedSlot]:
        """
        Block multiple consecutive days for a doctor (e.g., vacation)
        """
        if start_date > end_date:
            raise ValueError("Start date must be before or equal to end date")
        
        days_to_block = (end_date - start_date).days + 1
        if days_to_block > 365:
            raise ValueError("Cannot block more than 365 days at once")

        blocked_slots = []
        current_date = start_date
        
        while current_date <= end_date:
            try:
                blocked_slot = BlockedSlotService.block_full_day(
                    db, doctor_id, current_date, reason, created_by
                )
                blocked_slots.append(blocked_slot)
            except ValueError as e:
                # Skip if already blocked or other validation error
                print(f"Skipping {current_date}: {str(e)}")
            
            current_date += timedelta(days=1)
        
        return blocked_slots

    @staticmethod
    def get_blocked_slot(db: Session, blocked_slot_id: int) -> BlockedSlot:
        """Get blocked slot by ID"""
        blocked_slot = BlockedSlotRepository.get_by_id(db, blocked_slot_id)
        if not blocked_slot:
            raise ValueError(f"Blocked slot with ID {blocked_slot_id} not found")
        return blocked_slot

    @staticmethod
    def list_blocked_slots(db: Session, skip: int = 0, limit: int = 100) -> List[BlockedSlot]:
        """List all blocked slots with pagination"""
        return BlockedSlotRepository.get_all(db, skip, limit)

    @staticmethod
    def get_doctor_blocked_slots(db: Session, doctor_id: int) -> List[BlockedSlot]:
        """Get all blocked slots for a doctor"""
        return BlockedSlotRepository.get_by_doctor_id(db, doctor_id)

    @staticmethod
    def get_upcoming_blocked_slots(db: Session, doctor_id: int) -> List[BlockedSlot]:
        """Get upcoming blocked slots for a doctor"""
        return BlockedSlotRepository.get_upcoming_blocked_slots(db, doctor_id, date.today())

    @staticmethod
    def get_blocked_slots_by_date(db: Session, doctor_id: int, blocked_date: date) -> List[BlockedSlot]:
        """Get blocked slots for a doctor on a specific date"""
        return BlockedSlotRepository.get_by_doctor_and_date(db, doctor_id, blocked_date)

    @staticmethod
    def get_blocked_slots_in_range(
        db: Session, 
        doctor_id: int, 
        start_date: date, 
        end_date: date
    ) -> List[BlockedSlot]:
        """Get blocked slots within a date range"""
        return BlockedSlotRepository.get_by_date_range(db, doctor_id, start_date, end_date)

    @staticmethod
    def is_time_slot_blocked(
        db: Session, 
        doctor_id: int, 
        check_date: date, 
        start_time: time, 
        end_time: time
    ) -> Dict:
        """
        Check if a time slot is blocked
        Returns dict with is_blocked flag and list of conflicting slots
        """
        conflicts = BlockedSlotRepository.check_time_conflict(
            db, doctor_id, check_date, start_time, end_time
        )
        
        return {
            "is_blocked": len(conflicts) > 0,
            "conflicting_slots": conflicts,
            "reasons": [c.reason for c in conflicts] if conflicts else []
        }

    @staticmethod
    def update_blocked_slot(db: Session, blocked_slot_id: int, data: dict) -> BlockedSlot:
        """
        Update an existing blocked slot with validation
        """
        blocked_slot = BlockedSlotRepository.get_by_id(db, blocked_slot_id)
        if not blocked_slot:
            raise ValueError(f"Blocked slot with ID {blocked_slot_id} not found")

        # If updating date or time, check for conflicts
        if any(key in data for key in ["blocked_date", "start_time", "end_time"]):
            new_date = data.get("blocked_date", blocked_slot.blocked_date)
            new_start = data.get("start_time", blocked_slot.start_time)
            new_end = data.get("end_time", blocked_slot.end_time)

            # Convert if needed
            if isinstance(new_date, str):
                new_date = datetime.strptime(new_date, "%Y-%m-%d").date()
            if isinstance(new_start, str):
                new_start = datetime.strptime(new_start, "%H:%M:%S").time()
            if isinstance(new_end, str):
                new_end = datetime.strptime(new_end, "%H:%M:%S").time()

            # Validate time logic
            if new_start >= new_end:
                raise ValueError("Start time must be before end time")

            # Check for conflicts (excluding current slot)
            conflicts = BlockedSlotRepository.check_time_conflict(
                db, blocked_slot.doctor_id, new_date, new_start, new_end,
                exclude_blocked_slot_id=blocked_slot_id
            )
            
            if conflicts:
                raise ValueError("Updated time slot conflicts with existing blocked slots")

        # Update fields
        for key, value in data.items():
            if hasattr(blocked_slot, key):
                setattr(blocked_slot, key, value)

        return BlockedSlotRepository.update(db, blocked_slot)

    @staticmethod
    def delete_blocked_slot(db: Session, blocked_slot_id: int) -> None:
        """Delete a blocked slot"""
        blocked_slot = BlockedSlotRepository.get_by_id(db, blocked_slot_id)
        if not blocked_slot:
            raise ValueError(f"Blocked slot with ID {blocked_slot_id} not found")
        
        BlockedSlotRepository.delete(db, blocked_slot)

    @staticmethod
    def cancel_blocked_slots_in_range(
        db: Session, 
        doctor_id: int, 
        start_date: date, 
        end_date: date
    ) -> int:
        """Cancel (delete) all blocked slots in a date range. Returns count of deleted slots."""
        return BlockedSlotRepository.delete_by_date_range(db, doctor_id, start_date, end_date)

    @staticmethod
    def get_blocked_slots_summary(db: Session, doctor_id: int) -> Dict:
        """Get summary of blocked slots for a doctor"""
        today = date.today()
        
        total = BlockedSlotRepository.count_by_doctor(db, doctor_id)
        upcoming = BlockedSlotRepository.count_upcoming(db, doctor_id, today)
        past = total - upcoming
        
        blocked_dates = BlockedSlotRepository.get_blocked_dates(db, doctor_id)
        upcoming_dates = [d for d in blocked_dates if d >= today]
        
        return {
            "doctor_id": doctor_id,
            "total_blocked_slots": total,
            "upcoming_blocked_slots": upcoming,
            "past_blocked_slots": past,
            "total_blocked_dates": len(blocked_dates),
            "upcoming_blocked_dates": len(upcoming_dates),
            "next_blocked_date": upcoming_dates[0] if upcoming_dates else None
        }

    @staticmethod
    def get_doctor_availability_for_month(
        db: Session, 
        doctor_id: int, 
        year: int, 
        month: int
    ) -> Dict:
        """
        Get doctor's availability for a specific month showing blocked dates
        """
        from calendar import monthrange
        
        # Get first and last day of month
        first_day = date(year, month, 1)
        last_day = date(year, month, monthrange(year, month)[1])
        
        # Get blocked slots in this month
        blocked_slots = BlockedSlotRepository.get_by_date_range(
            db, doctor_id, first_day, last_day
        )
        
        # Group by date
        blocked_by_date = {}
        for slot in blocked_slots:
            if slot.blocked_date not in blocked_by_date:
                blocked_by_date[slot.blocked_date] = []
            blocked_by_date[slot.blocked_date].append({
                "start_time": str(slot.start_time),
                "end_time": str(slot.end_time),
                "reason": slot.reason
            })
        
        return {
            "doctor_id": doctor_id,
            "year": year,
            "month": month,
            "blocked_dates": sorted(blocked_by_date.keys()),
            "blocked_slots_by_date": blocked_by_date,
            "total_blocked_slots": len(blocked_slots)
        }