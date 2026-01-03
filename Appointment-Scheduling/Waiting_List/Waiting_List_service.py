from sqlalchemy.orm import Session
from datetime import date, time, datetime, timedelta
from typing import List, Optional, Dict
from Waiting_List.Waiting_List_model import WaitingList, WaitingListStatusEnum
from Repository.Waiting_List_repository import WaitingListRepository
from Waiting_List_config import get_waiting_list_settings

class WaitingListService:

    @staticmethod
    def create_waiting_entry(db: Session, data: dict) -> WaitingList:
        """
        Create a new waiting list entry with validation
        """
        # Extract required fields
        patient_id = data.get("patient_id")
        doctor_id = data.get("doctor_id")
        preferred_date = data.get("preferred_date")
        preferred_time_start = data.get("preferred_time_start")
        preferred_time_end = data.get("preferred_time_end")

        # Validate required fields
        if not all([patient_id, doctor_id, preferred_date, preferred_time_start, preferred_time_end]):
            raise ValueError("Missing required fields: patient_id, doctor_id, preferred_date, preferred_time_start, preferred_time_end")

        # Convert string values if needed
        if isinstance(preferred_date, str):
            preferred_date = datetime.strptime(preferred_date, "%Y-%m-%d").date()
        if isinstance(preferred_time_start, str):
            preferred_time_start = datetime.strptime(preferred_time_start, "%H:%M:%S").time()
        if isinstance(preferred_time_end, str):
            preferred_time_end = datetime.strptime(preferred_time_end, "%H:%M:%S").time()

        # Validate preferred date
        if preferred_date < date.today():
            raise ValueError("Preferred date cannot be in the past")

        # Validate time logic
        if preferred_time_start >= preferred_time_end:
            raise ValueError("Preferred start time must be before end time")

        # Check if patient already has too many active entries
        settings = get_waiting_list_settings()
        active_count = WaitingListRepository.count_active_by_patient(db, patient_id)
        if active_count >= settings.MAX_ACTIVE_WAITING_ENTRIES_PER_PATIENT:
            raise ValueError(f"Patient already has {active_count} active waiting list entries. Maximum allowed is {settings.MAX_ACTIVE_WAITING_ENTRIES_PER_PATIENT}")

        # Check for duplicate entry
        has_duplicate = WaitingListRepository.check_duplicate_entry(
            db, patient_id, doctor_id, preferred_date
        )
        if has_duplicate:
            raise ValueError("Patient already has an active waiting list entry for this doctor on this date")

        # Calculate expiry date
        added_at = datetime.now()
        expiry_days = data.get("expiry_days", settings.DEFAULT_EXPIRY_DAYS)
        expires_at = added_at + timedelta(days=expiry_days)

        # Create waiting list entry
        waiting_entry = WaitingList(
            patient_id=patient_id,
            doctor_id=doctor_id,
            preferred_date=preferred_date,
            preferred_time_start=preferred_time_start,
            preferred_time_end=preferred_time_end,
            reason=data.get("reason"),
            status=WaitingListStatusEnum.ACTIVE,
            added_at=added_at,
            expires_at=expires_at
        )

        return WaitingListRepository.create(db, waiting_entry)

    @staticmethod
    def get_waiting_entry(db: Session, waiting_id: int) -> WaitingList:
        """Get waiting list entry by ID"""
        waiting_entry = WaitingListRepository.get_by_id(db, waiting_id)
        if not waiting_entry:
            raise ValueError(f"Waiting list entry with ID {waiting_id} not found")
        return waiting_entry

    @staticmethod
    def list_waiting_entries(db: Session, skip: int = 0, limit: int = 100) -> List[WaitingList]:
        """List all waiting list entries with pagination"""
        return WaitingListRepository.get_all(db, skip, limit)

    @staticmethod
    def get_patient_waiting_entries(db: Session, patient_id: int) -> List[WaitingList]:
        """Get all waiting list entries for a patient"""
        return WaitingListRepository.get_by_patient_id(db, patient_id)

    @staticmethod
    def get_doctor_waiting_entries(db: Session, doctor_id: int) -> List[WaitingList]:
        """Get all waiting list entries for a doctor"""
        return WaitingListRepository.get_by_doctor_id(db, doctor_id)

    @staticmethod
    def get_active_entries(db: Session, doctor_id: int = None) -> List[WaitingList]:
        """Get all active waiting list entries"""
        return WaitingListRepository.get_active_entries(db, doctor_id)

    @staticmethod
    def get_entries_by_date(db: Session, doctor_id: int, preferred_date: date) -> List[WaitingList]:
        """Get waiting list entries for a doctor on a specific date"""
        if isinstance(preferred_date, str):
            preferred_date = datetime.strptime(preferred_date, "%Y-%m-%d").date()
        return WaitingListRepository.get_by_preferred_date(db, doctor_id, preferred_date)

    @staticmethod
    def get_entries_by_date_range(
        db: Session,
        doctor_id: int,
        start_date: date,
        end_date: date
    ) -> List[WaitingList]:
        """Get waiting list entries within a date range"""
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

        if start_date > end_date:
            raise ValueError("start_date must be before or equal to end_date")

        return WaitingListRepository.get_by_date_range(db, doctor_id, start_date, end_date)

    @staticmethod
    def update_waiting_entry(db: Session, waiting_id: int, data: dict) -> WaitingList:
        """
        Update an existing waiting list entry
        """
        waiting_entry = WaitingListRepository.get_by_id(db, waiting_id)
        if not waiting_entry:
            raise ValueError(f"Waiting list entry with ID {waiting_id} not found")

        # Don't allow updates to completed/expired entries
        if waiting_entry.status in [WaitingListStatusEnum.ACCEPTED, WaitingListStatusEnum.DECLINED, WaitingListStatusEnum.EXPIRED]:
            raise ValueError(f"Cannot update waiting list entry with status: {waiting_entry.status.value}")

        # If updating preferred date or time, validate
        if any(key in data for key in ["preferred_date", "preferred_time_start", "preferred_time_end"]):
            new_date = data.get("preferred_date", waiting_entry.preferred_date)
            new_start = data.get("preferred_time_start", waiting_entry.preferred_time_start)
            new_end = data.get("preferred_time_end", waiting_entry.preferred_time_end)

            # Convert strings if needed
            if isinstance(new_date, str):
                new_date = datetime.strptime(new_date, "%Y-%m-%d").date()
            if isinstance(new_start, str):
                new_start = datetime.strptime(new_start, "%H:%M:%S").time()
            if isinstance(new_end, str):
                new_end = datetime.strptime(new_end, "%H:%M:%S").time()

            # Validate time logic
            if new_start >= new_end:
                raise ValueError("Preferred start time must be before end time")

        # Update fields
        for key, value in data.items():
            if key == "status" and isinstance(value, str):
                value = WaitingListStatusEnum[value]
            
            if hasattr(waiting_entry, key):
                setattr(waiting_entry, key, value)

        return WaitingListRepository.update(db, waiting_entry)

    @staticmethod
    def notify_patient(db: Session, waiting_id: int) -> WaitingList:
        """
        Mark waiting list entry as notified
        """
        waiting_entry = WaitingListRepository.get_by_id(db, waiting_id)
        if not waiting_entry:
            raise ValueError(f"Waiting list entry with ID {waiting_id} not found")

        if waiting_entry.status != WaitingListStatusEnum.ACTIVE:
            raise ValueError(f"Can only notify active entries. Current status: {waiting_entry.status.value}")

        waiting_entry.status = WaitingListStatusEnum.NOTIFIED
        waiting_entry.notified_at = datetime.now()

        return WaitingListRepository.update(db, waiting_entry)

    @staticmethod
    def accept_entry(db: Session, waiting_id: int) -> WaitingList:
        """
        Mark waiting list entry as accepted
        """
        waiting_entry = WaitingListRepository.get_by_id(db, waiting_id)
        if not waiting_entry:
            raise ValueError(f"Waiting list entry with ID {waiting_id} not found")

        if waiting_entry.status != WaitingListStatusEnum.NOTIFIED:
            raise ValueError(f"Can only accept notified entries. Current status: {waiting_entry.status.value}")

        waiting_entry.status = WaitingListStatusEnum.ACCEPTED

        return WaitingListRepository.update(db, waiting_entry)

    @staticmethod
    def decline_entry(db: Session, waiting_id: int) -> WaitingList:
        """
        Mark waiting list entry as declined
        """
        waiting_entry = WaitingListRepository.get_by_id(db, waiting_id)
        if not waiting_entry:
            raise ValueError(f"Waiting list entry with ID {waiting_id} not found")

        if waiting_entry.status != WaitingListStatusEnum.NOTIFIED:
            raise ValueError(f"Can only decline notified entries. Current status: {waiting_entry.status.value}")

        waiting_entry.status = WaitingListStatusEnum.DECLINED

        return WaitingListRepository.update(db, waiting_entry)

    @staticmethod
    def cancel_entry(db: Session, waiting_id: int) -> WaitingList:
        """
        Cancel an active waiting list entry
        """
        waiting_entry = WaitingListRepository.get_by_id(db, waiting_id)
        if not waiting_entry:
            raise ValueError(f"Waiting list entry with ID {waiting_id} not found")

        if waiting_entry.status not in [WaitingListStatusEnum.ACTIVE, WaitingListStatusEnum.NOTIFIED]:
            raise ValueError(f"Can only cancel active or notified entries. Current status: {waiting_entry.status.value}")

        waiting_entry.status = WaitingListStatusEnum.CANCELLED

        return WaitingListRepository.update(db, waiting_entry)

    @staticmethod
    def delete_waiting_entry(db: Session, waiting_id: int) -> None:
        """
        Delete a waiting list entry (hard delete)
        """
        waiting_entry = WaitingListRepository.get_by_id(db, waiting_id)
        if not waiting_entry:
            raise ValueError(f"Waiting list entry with ID {waiting_id} not found")

        WaitingListRepository.delete(db, waiting_entry)

    @staticmethod
    def expire_old_entries(db: Session) -> int:
        """
        Mark expired waiting list entries as EXPIRED
        Returns count of expired entries
        """
        current_time = datetime.now()
        expired_entries = WaitingListRepository.get_expired_entries(db, current_time)
        
        count = 0
        for entry in expired_entries:
            entry.status = WaitingListStatusEnum.EXPIRED
            WaitingListRepository.update(db, entry)
            count += 1
        
        return count

    @staticmethod
    def get_waiting_statistics(db: Session, doctor_id: int) -> Dict:
        """
        Get waiting list statistics for a doctor
        """
        stats = WaitingListRepository.get_statistics_by_doctor(db, doctor_id)
        
        # Get next few entries
        active_entries = WaitingListRepository.get_active_entries(db, doctor_id)
        next_entries = active_entries[:5] if active_entries else []
        
        return {
            "doctor_id": doctor_id,
            "statistics": stats,
            "next_entries": [
                {
                    "waiting_id": entry.waiting_id,
                    "patient_id": entry.patient_id,
                    "preferred_date": str(entry.preferred_date),
                    "added_at": entry.added_at.isoformat(),
                    "expires_at": entry.expires_at.isoformat()
                }
                for entry in next_entries
            ]
        }

    @staticmethod
    def get_priority_entries(
        db: Session,
        doctor_id: int,
        preferred_date: date
    ) -> List[WaitingList]:
        """
        Get waiting list entries sorted by priority for a specific date
        """
        if isinstance(preferred_date, str):
            preferred_date = datetime.strptime(preferred_date, "%Y-%m-%d").date()
        
        return WaitingListRepository.get_priority_sorted_entries(db, doctor_id, preferred_date)

    @staticmethod
    def get_notified_entries(db: Session, doctor_id: int = None) -> List[WaitingList]:
        """Get all notified waiting list entries"""
        return WaitingListRepository.get_notified_entries(db, doctor_id)

    @staticmethod
    def bulk_cancel_entries(db: Session, waiting_ids: List[int]) -> int:
        """
        Cancel multiple waiting list entries at once
        """
        if not waiting_ids:
            return 0
        
        count = WaitingListRepository.bulk_update_status(
            db, waiting_ids, WaitingListStatusEnum.CANCELLED
        )
        return count

    @staticmethod
    def get_patient_active_count(db: Session, patient_id: int) -> int:
        """Get count of active waiting list entries for a patient"""
        return WaitingListRepository.count_active_by_patient(db, patient_id)