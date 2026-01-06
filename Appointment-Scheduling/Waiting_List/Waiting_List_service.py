from sqlalchemy.orm import Session
from datetime import date, datetime, timedelta
from typing import List, Dict

from Waiting_List.Waiting_List_model import WaitingList, WaitingListStatusEnum
from Waiting_List.Waiting_List_repository import WaitingListRepository
from Waiting_List.Waiting_List_config import get_waiting_list_settings


class WaitingListService:
    """Business logic for Waiting List"""

    # ================= CREATE =================

    @staticmethod
    def create_waiting_entry(db: Session, data: dict) -> WaitingList:
        patient_id = data.get("patient_id")
        doctor_id = data.get("doctor_id")
        preferred_date = data.get("preferred_date")
        preferred_time_start = data.get("preferred_time_start")
        preferred_time_end = data.get("preferred_time_end")

        # ---- Required fields ----
        if not all([patient_id, doctor_id, preferred_date, preferred_time_start, preferred_time_end]):
            raise ValueError(
                "Missing required fields: patient_id, doctor_id, preferred_date, "
                "preferred_time_start, preferred_time_end"
            )

        # ---- Convert date/time ----
        if isinstance(preferred_date, str):
            preferred_date = datetime.strptime(preferred_date, "%Y-%m-%d").date()

        if isinstance(preferred_time_start, str):
            preferred_time_start = datetime.strptime(preferred_time_start, "%H:%M:%S").time()

        if isinstance(preferred_time_end, str):
            preferred_time_end = datetime.strptime(preferred_time_end, "%H:%M:%S").time()

        # ---- Validations ----
        if preferred_date < date.today():
            raise ValueError("Preferred date cannot be in the past")

        if preferred_time_start >= preferred_time_end:
            raise ValueError("Preferred start time must be before end time")

        settings = get_waiting_list_settings()

        # ---- Max active entries per patient ----
        active_count = WaitingListRepository.count_active_by_patient(db, patient_id)
        if active_count >= settings.MAX_ACTIVE_WAITING_ENTRIES_PER_PATIENT:
            raise ValueError(
                f"Patient already has {active_count} active waiting list entries. "
                f"Maximum allowed is {settings.MAX_ACTIVE_WAITING_ENTRIES_PER_PATIENT}"
            )

        # ---- Duplicate check ----
        if WaitingListRepository.check_duplicate_entry(db, patient_id, doctor_id, preferred_date):
            raise ValueError(
                "Patient already has an active waiting list entry for this doctor on this date"
            )

        # ---- Expiry calculation ----
        added_at = datetime.now()
        expiry_days = data.get("expiry_days", settings.DEFAULT_EXPIRY_DAYS)
        expires_at = added_at + timedelta(days=expiry_days)

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

    # ================= READ =================

    @staticmethod
    def get_waiting_entry(db: Session, waiting_id: int) -> WaitingList:
        entry = WaitingListRepository.get_by_id(db, waiting_id)
        if not entry:
            raise ValueError(f"Waiting list entry with ID {waiting_id} not found")
        return entry

    @staticmethod
    def list_waiting_entries(db: Session, skip: int = 0, limit: int = 100) -> List[WaitingList]:
        return WaitingListRepository.get_all(db, skip, limit)

    @staticmethod
    def get_patient_waiting_entries(db: Session, patient_id: int) -> List[WaitingList]:
        return WaitingListRepository.get_by_patient_id(db, patient_id)

    @staticmethod
    def get_doctor_waiting_entries(db: Session, doctor_id: int) -> List[WaitingList]:
        return WaitingListRepository.get_by_doctor_id(db, doctor_id)

    @staticmethod
    def get_active_entries(db: Session, doctor_id: int = None) -> List[WaitingList]:
        return WaitingListRepository.get_active_entries(db, doctor_id)

    # ================= UPDATE =================

    @staticmethod
    def update_waiting_entry(db: Session, waiting_id: int, data: dict) -> WaitingList:
        entry = WaitingListRepository.get_by_id(db, waiting_id)
        if not entry:
            raise ValueError(f"Waiting list entry with ID {waiting_id} not found")

        if entry.status in (
            WaitingListStatusEnum.ACCEPTED,
            WaitingListStatusEnum.DECLINED,
            WaitingListStatusEnum.EXPIRED,
            WaitingListStatusEnum.CANCELLED,
        ):
            raise ValueError(f"Cannot update waiting list entry with status: {entry.status.value}")

        # ---- Validate date/time if updating ----
        if any(k in data for k in ("preferred_date", "preferred_time_start", "preferred_time_end")):
            new_date = data.get("preferred_date", entry.preferred_date)
            new_start = data.get("preferred_time_start", entry.preferred_time_start)
            new_end = data.get("preferred_time_end", entry.preferred_time_end)

            if isinstance(new_date, str):
                new_date = datetime.strptime(new_date, "%Y-%m-%d").date()
            if isinstance(new_start, str):
                new_start = datetime.strptime(new_start, "%H:%M:%S").time()
            if isinstance(new_end, str):
                new_end = datetime.strptime(new_end, "%H:%M:%S").time()

            if new_start >= new_end:
                raise ValueError("Preferred start time must be before end time")

        for key, value in data.items():
            if key == "status" and isinstance(value, str):
                value = WaitingListStatusEnum[value]

            if hasattr(entry, key):
                setattr(entry, key, value)

        return WaitingListRepository.update(db, entry)

    # ================= STATUS TRANSITIONS =================

    @staticmethod
    def notify_patient(db: Session, waiting_id: int) -> WaitingList:
        entry = WaitingListRepository.get_by_id(db, waiting_id)
        if not entry:
            raise ValueError(f"Waiting list entry with ID {waiting_id} not found")

        if entry.status != WaitingListStatusEnum.ACTIVE:
            raise ValueError(
                f"Can only notify active entries. Current status: {entry.status.value}"
            )

        entry.status = WaitingListStatusEnum.NOTIFIED
        entry.notified_at = datetime.now()
        return WaitingListRepository.update(db, entry)

    @staticmethod
    def accept_entry(db: Session, waiting_id: int) -> WaitingList:
        entry = WaitingListRepository.get_by_id(db, waiting_id)
        if not entry:
            raise ValueError(f"Waiting list entry with ID {waiting_id} not found")

        if entry.status != WaitingListStatusEnum.NOTIFIED:
            raise ValueError(
                f"Can only accept notified entries. Current status: {entry.status.value}"
            )

        entry.status = WaitingListStatusEnum.ACCEPTED
        return WaitingListRepository.update(db, entry)

    @staticmethod
    def decline_entry(db: Session, waiting_id: int) -> WaitingList:
        entry = WaitingListRepository.get_by_id(db, waiting_id)
        if not entry:
            raise ValueError(f"Waiting list entry with ID {waiting_id} not found")

        if entry.status != WaitingListStatusEnum.NOTIFIED:
            raise ValueError(
                f"Can only decline notified entries. Current status: {entry.status.value}"
            )

        entry.status = WaitingListStatusEnum.DECLINED
        return WaitingListRepository.update(db, entry)

    @staticmethod
    def cancel_entry(db: Session, waiting_id: int) -> WaitingList:
        entry = WaitingListRepository.get_by_id(db, waiting_id)
        if not entry:
            raise ValueError(f"Waiting list entry with ID {waiting_id} not found")

        if entry.status not in (
            WaitingListStatusEnum.ACTIVE,
            WaitingListStatusEnum.NOTIFIED,
        ):
            raise ValueError(
                f"Can only cancel active or notified entries. Current status: {entry.status.value}"
            )

        entry.status = WaitingListStatusEnum.CANCELLED
        return WaitingListRepository.update(db, entry)

    # ================= MAINTENANCE =================

    @staticmethod
    def expire_old_entries(db: Session) -> int:
        current_time = datetime.now()
        expired_entries = WaitingListRepository.get_expired_entries(db, current_time)

        count = 0
        for entry in expired_entries:
            entry.status = WaitingListStatusEnum.EXPIRED
            WaitingListRepository.update(db, entry)
            count += 1

        return count

    # ================= REPORTING =================

    @staticmethod
    def get_waiting_statistics(db: Session, doctor_id: int) -> Dict:
        stats = WaitingListRepository.get_statistics_by_doctor(db, doctor_id)

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
                    "expires_at": entry.expires_at.isoformat(),
                }
                for entry in next_entries
            ],
        }

    @staticmethod
    def get_priority_entries(
        db: Session,
        doctor_id: int,
        preferred_date: date
    ) -> List[WaitingList]:
        if isinstance(preferred_date, str):
            preferred_date = datetime.strptime(preferred_date, "%Y-%m-%d").date()

        return WaitingListRepository.get_priority_sorted_entries(
            db, doctor_id, preferred_date
        )

    @staticmethod
    def get_notified_entries(db: Session, doctor_id: int = None) -> List[WaitingList]:
        return WaitingListRepository.get_notified_entries(db, doctor_id)

    @staticmethod
    def bulk_cancel_entries(db: Session, waiting_ids: List[int]) -> int:
        if not waiting_ids:
            return 0

        return WaitingListRepository.bulk_update_status(
            db, waiting_ids, WaitingListStatusEnum.CANCELLED
        )

    @staticmethod
    def get_patient_active_count(db: Session, patient_id: int) -> int:
        return WaitingListRepository.count_active_by_patient(db, patient_id)
