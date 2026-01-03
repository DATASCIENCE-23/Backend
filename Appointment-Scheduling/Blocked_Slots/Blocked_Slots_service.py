from sqlalchemy.orm import Session
from datetime import date, time, datetime, timedelta
from typing import List, Optional, Dict
from Blocked_Slots.Blocked_Slots_model import BlockedSlot
from Repository.Blocked_Slots_repository import BlockedSlotRepository

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

        # Convert string values if needed
        if isinstance(blocked_date, str):
            blocked_date = datetime.strptime(blocked_date, "%Y-%m-%d").date()
        if isinstance(start_time, str):
            start_time = datetime.strptime(start_time, "%H:%M:%S").time()
        if isinstance(end_time, str):
            end_time = datetime.strptime(end_time, "%H:%M:%S").time()

        # Validate blocked date (should not be in the past)
        if blocked_date < date.today():
            raise ValueError("Cannot block slots for past dates")

        # Validate time logic
        if start_time >= end_time:
            raise ValueError("Start time must be before end time")

        # Check for time conflicts with existing blocked slots
        has_conflict = BlockedSlotRepository.check_time_conflict(
            db, doctor_id, blocked_date, start_time, end_time
        )
        
        if has_conflict:
            raise ValueError("This time slot conflicts with an existing blocked slot")

        # Validate reason
        if not reason or len(reason.strip()) == 0:
            raise ValueError("Reason for blocking must be provided")

        # Create blocked slot object
        blocked_slot = BlockedSlot(
            doctor_id=doctor_id,
            blocked_date=blocked_date,
            start_time=start_time,
            end_time=end_time,
            reason=reason.strip(),
            created_at=datetime.now(),
            created_by=created_by
        )

        return BlockedSlotRepository.create(db, blocked_slot)

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
    def get_blocked_slots_by_date(db: Session, blocked_date: date) -> List[BlockedSlot]:
        """Get all blocked slots on a specific date"""
        if isinstance(blocked_date, str):
            blocked_date = datetime.strptime(blocked_date, "%Y-%m-%d").date()
        return BlockedSlotRepository.get_by_date(db, blocked_date)

    @staticmethod
    def get_doctor_blocked_slots_by_date(db: Session, doctor_id: int, blocked_date: date) -> List[BlockedSlot]:
        """Get blocked slots for a doctor on a specific date"""
        if isinstance(blocked_date, str):
            blocked_date = datetime.strptime(blocked_date, "%Y-%m-%d").date()
        return BlockedSlotRepository.get_by_doctor_and_date(db, doctor_id, blocked_date)

    @staticmethod
    def get_blocked_slots_by_date_range(
        db: Session,
        doctor_id: int,
        start_date: date,
        end_date: date
    ) -> List[BlockedSlot]:
        """Get blocked slots for a doctor within a date range"""
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

        if start_date > end_date:
            raise ValueError("start_date must be before or equal to end_date")

        return BlockedSlotRepository.get_by_date_range(db, doctor_id, start_date, end_date)

    @staticmethod
    def get_upcoming_blocked_slots(db: Session, doctor_id: int) -> List[BlockedSlot]:
        """Get upcoming blocked slots for a doctor"""
        today = date.today()
        return BlockedSlotRepository.get_upcoming_blocked_slots(db, doctor_id, today)

    @staticmethod
    def update_blocked_slot(db: Session, blocked_slot_id: int, data: dict) -> BlockedSlot:
        """
        Update an existing blocked slot with validation
        """
        blocked_slot = BlockedSlotRepository.get_by_id(db, blocked_slot_id)
        if not blocked_slot:
            raise ValueError(f"Blocked slot with ID {blocked_slot_id} not found")

        # If updating date or time, validate
        if any(key in data for key in ["blocked_date", "start_time", "end_time"]):
            new_date = data.get("blocked_date", blocked_slot.blocked_date)
            new_start = data.get("start_time", blocked_slot.start_time)
            new_end = data.get("end_time", blocked_slot.end_time)

            # Convert strings if needed
            if isinstance(new_date, str):
                new_date = datetime.strptime(new_date, "%Y-%m-%d").date()
            if isinstance(new_start, str):
                new_start = datetime.strptime(new_start, "%H:%M:%S").time()
            if isinstance(new_end, str):
                new_end = datetime.strptime(new_end, "%H:%M:%S").time()

            # Validate time logic
            if new_start >= new_end:
                raise ValueError("Start time must be before end time")

            # Check for conflicts (excluding current blocked slot)
            has_conflict = BlockedSlotRepository.check_time_conflict(
                db, blocked_slot.doctor_id, new_date, new_start, new_end,
                exclude_blocked_slot_id=blocked_slot_id
            )
            
            if has_conflict:
                raise ValueError("This time slot conflicts with an existing blocked slot")

        # Validate reason if being updated
        if "reason" in data:
            reason = data["reason"]
            if not reason or len(reason.strip()) == 0:
                raise ValueError("Reason for blocking must be provided")
            data["reason"] = reason.strip()

        # Update fields (except created_at and created_by which should not change)
        immutable_fields = ["created_at", "created_by", "blocked_slot_id"]
        for key, value in data.items():
            if key not in immutable_fields and hasattr(blocked_slot, key):
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
    def is_time_slot_blocked(
        db: Session,
        doctor_id: int,
        check_date: date,
        start_time: time,
        end_time: time
    ) -> Dict[str, any]:
        """
        Check if a specific time slot is blocked for a doctor
        Returns detailed information about the blockage
        """
        if isinstance(check_date, str):
            check_date = datetime.strptime(check_date, "%Y-%m-%d").date()
        if isinstance(start_time, str):
            start_time = datetime.strptime(start_time, "%H:%M:%S").time()
        if isinstance(end_time, str):
            end_time = datetime.strptime(end_time, "%H:%M:%S").time()

        is_blocked = BlockedSlotRepository.is_time_blocked(
            db, doctor_id, check_date, start_time, end_time
        )
        
        result = {
            "is_blocked": is_blocked,
            "doctor_id": doctor_id,
            "date": str(check_date),
            "start_time": str(start_time),
            "end_time": str(end_time)
        }

        if is_blocked:
            # Get the conflicting blocked slots
            blocked_slots = BlockedSlotRepository.get_by_doctor_and_date(db, doctor_id, check_date)
            conflicting_slots = []
            
            for slot in blocked_slots:
                # Check if this slot overlaps with the requested time
                if not (end_time <= slot.start_time or start_time >= slot.end_time):
                    conflicting_slots.append({
                        "blocked_slot_id": slot.blocked_slot_id,
                        "start_time": str(slot.start_time),
                        "end_time": str(slot.end_time),
                        "reason": slot.reason
                    })
            
            result["conflicting_slots"] = conflicting_slots

        return result

    @staticmethod
    def block_full_day(
        db: Session,
        doctor_id: int,
        blocked_date: date,
        reason: str,
        created_by: int
    ) -> BlockedSlot:
        """
        Block an entire day for a doctor (00:00:00 to 23:59:59)
        """
        if isinstance(blocked_date, str):
            blocked_date = datetime.strptime(blocked_date, "%Y-%m-%d").date()

        # Check if there are any existing blocked slots on this date
        existing_slots = BlockedSlotRepository.get_by_doctor_and_date(db, doctor_id, blocked_date)
        if existing_slots:
            raise ValueError(f"Cannot block full day. There are already {len(existing_slots)} blocked slot(s) on this date. Please remove them first.")

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
        Block multiple consecutive days for a doctor (e.g., for vacation)
        """
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

        if start_date > end_date:
            raise ValueError("start_date must be before or equal to end_date")

        if start_date < date.today():
            raise ValueError("Cannot block slots for past dates")

        # Calculate number of days
        delta = end_date - start_date
        num_days = delta.days + 1

        if num_days > 365:
            raise ValueError("Cannot block more than 365 days at once")

        blocked_slots = []
        current_date = start_date

        while current_date <= end_date:
            # Check if there are existing blocked slots on this date
            existing_slots = BlockedSlotRepository.get_by_doctor_and_date(db, doctor_id, current_date)
            
            if not existing_slots:
                # Only create if no existing blocks
                data = {
                    "doctor_id": doctor_id,
                    "blocked_date": current_date,
                    "start_time": time(0, 0, 0),
                    "end_time": time(23, 59, 59),
                    "reason": reason,
                    "created_by": created_by
                }
                
                blocked_slot = BlockedSlotService.create_blocked_slot(db, data)
                blocked_slots.append(blocked_slot)
            
            current_date += timedelta(days=1)

        return blocked_slots

    @staticmethod
    def get_blocked_dates_in_range(
        db: Session,
        doctor_id: int,
        start_date: date,
        end_date: date
    ) -> List[str]:
        """
        Get list of dates that have any blocked slots for a doctor within a range
        """
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

        blocked_dates = BlockedSlotRepository.get_blocked_dates_for_doctor(
            db, doctor_id, start_date, end_date
        )
        
        return [str(d) for d in blocked_dates]

    @staticmethod
    def delete_past_blocked_slots(db: Session, days_to_keep: int = 90) -> int:
        """
        Cleanup old blocked slots (maintenance function)
        Keep only the last N days of blocked slots
        """
        cutoff_date = date.today() - timedelta(days=days_to_keep)
        count = BlockedSlotRepository.delete_past_blocked_slots(db, cutoff_date)
        return count

    @staticmethod
    def cancel_blocked_slots_in_range(
        db: Session,
        doctor_id: int,
        start_date: date,
        end_date: date
    ) -> int:
        """
        Remove all blocked slots for a doctor within a date range
        Useful for cancelling vacation plans
        """
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

        if start_date > end_date:
            raise ValueError("start_date must be before or equal to end_date")

        count = BlockedSlotRepository.delete_by_date_range(db, doctor_id, start_date, end_date)
        return count

    @staticmethod
    def get_blocked_slots_summary(db: Session, doctor_id: int) -> Dict:
        """
        Get summary statistics of blocked slots for a doctor
        """
        today = date.today()
        
        total_blocked = BlockedSlotRepository.count_blocked_slots_by_doctor(db, doctor_id)
        upcoming_blocked = BlockedSlotRepository.count_upcoming_blocked_slots(db, doctor_id, today)
        past_blocked = total_blocked - upcoming_blocked

        # Get next upcoming blocked slot
        upcoming_slots = BlockedSlotRepository.get_upcoming_blocked_slots(db, doctor_id, today)
        next_blocked = upcoming_slots[0] if upcoming_slots else None

        return {
            "doctor_id": doctor_id,
            "total_blocked_slots": total_blocked,
            "upcoming_blocked_slots": upcoming_blocked,
            "past_blocked_slots": past_blocked,
            "next_blocked_slot": {
                "blocked_slot_id": next_blocked.blocked_slot_id,
                "date": str(next_blocked.blocked_date),
                "start_time": str(next_blocked.start_time),
                "end_time": str(next_blocked.end_time),
                "reason": next_blocked.reason
            } if next_blocked else None
        }

    @staticmethod
    def get_doctor_availability_for_month(
        db: Session,
        doctor_id: int,
        year: int,
        month: int
    ) -> Dict:
        """
        Get doctor's blocked dates for a specific month
        Useful for calendar views
        """
        from calendar import monthrange
        
        # Get first and last day of month
        first_day = date(year, month, 1)
        last_day_num = monthrange(year, month)[1]
        last_day = date(year, month, last_day_num)

        # Get all blocked dates in this month
        blocked_dates = BlockedSlotRepository.get_blocked_dates_for_doctor(
            db, doctor_id, first_day, last_day
        )

        # Get detailed blocked slots
        blocked_slots = BlockedSlotRepository.get_by_date_range(
            db, doctor_id, first_day, last_day
        )

        # Organize by date
        slots_by_date = {}
        for slot in blocked_slots:
            date_str = str(slot.blocked_date)
            if date_str not in slots_by_date:
                slots_by_date[date_str] = []
            
            slots_by_date[date_str].append({
                "blocked_slot_id": slot.blocked_slot_id,
                "start_time": str(slot.start_time),
                "end_time": str(slot.end_time),
                "reason": slot.reason
            })

        return {
            "doctor_id": doctor_id,
            "year": year,
            "month": month,
            "total_blocked_dates": len(blocked_dates),
            "blocked_dates": [str(d) for d in blocked_dates],
            "slots_by_date": slots_by_date
        }
