from sqlalchemy.orm import Session
from datetime import date, time, datetime, timedelta
from typing import List, Dict

from Appointment_History.Appointment_History_model import (
    AppointmentHistory,
    ChangeTypeEnum
)
from Appointment_History.Appointment_History_repository import AppointmentHistoryRepository
from Appointment_History.Appointment_History_config import get_history_settings


class AppointmentHistoryService:
    """Business logic for Appointment History"""

    # ================= CREATE =================

    @staticmethod
    def create_history_record(db: Session, data: dict) -> AppointmentHistory:
        appointment_id = data.get("appointment_id")
        changed_by = data.get("changed_by")
        change_type = data.get("change_type")

        if not all([appointment_id, changed_by, change_type]):
            raise ValueError(
                "Missing required fields: appointment_id, changed_by, change_type"
            )

        # ---- Convert change_type ----
        if isinstance(change_type, str):
            try:
                change_type = ChangeTypeEnum[change_type]
            except KeyError:
                raise ValueError(f"Invalid change_type: {change_type}")

        # ---- Convert date/time ----
        def parse_date(value):
            if value is None:
                return None
            if isinstance(value, date):
                return value
            return datetime.strptime(value, "%Y-%m-%d").date()

        def parse_time(value):
            if value is None:
                return None
            if isinstance(value, time):
                return value
            return datetime.strptime(value, "%H:%M:%S").time()

        old_date = parse_date(data.get("old_date"))
        new_date = parse_date(data.get("new_date"))
        old_time = parse_time(data.get("old_time"))
        new_time = parse_time(data.get("new_time"))

        # ---- Max history per appointment ----
        settings = get_history_settings()
        current_count = AppointmentHistoryRepository.count_by_appointment(
            db, appointment_id
        )
        if current_count >= settings.MAX_HISTORY_PER_APPOINTMENT:
            raise ValueError(
                f"Maximum history records ({settings.MAX_HISTORY_PER_APPOINTMENT}) "
                f"exceeded for this appointment"
            )

        history = AppointmentHistory(
            appointment_id=appointment_id,
            changed_by=changed_by,
            change_type=change_type,
            old_date=old_date,
            new_date=new_date,
            old_time=old_time,
            new_time=new_time,
            old_status=data.get("old_status"),
            new_status=data.get("new_status"),
            change_reason=data.get("change_reason"),
            changed_at=datetime.now()
        )

        return AppointmentHistoryRepository.create(db, history)

    # ================= READ =================

    @staticmethod
    def get_history_record(db: Session, history_id: int) -> AppointmentHistory:
        history = AppointmentHistoryRepository.get_by_id(db, history_id)
        if not history:
            raise ValueError(f"History record with ID {history_id} not found")
        return history

    @staticmethod
    def list_history_records(
        db: Session,
        skip: int = 0,
        limit: int = 100
    ) -> List[AppointmentHistory]:
        return AppointmentHistoryRepository.get_all(db, skip, limit)

    @staticmethod
    def get_appointment_history(
        db: Session,
        appointment_id: int
    ) -> List[AppointmentHistory]:
        return AppointmentHistoryRepository.get_by_appointment_id(db, appointment_id)

    @staticmethod
    def get_appointment_timeline(
        db: Session,
        appointment_id: int
    ) -> List[AppointmentHistory]:
        return AppointmentHistoryRepository.get_appointment_timeline(
            db, appointment_id
        )

    @staticmethod
    def get_by_change_type(
        db: Session,
        change_type: str
    ) -> List[AppointmentHistory]:
        try:
            enum_value = ChangeTypeEnum[change_type]
        except KeyError:
            raise ValueError(f"Invalid change_type: {change_type}")
        return AppointmentHistoryRepository.get_by_change_type(db, enum_value)

    @staticmethod
    def get_by_user(
        db: Session,
        user_id: int
    ) -> List[AppointmentHistory]:
        return AppointmentHistoryRepository.get_by_changed_by(db, user_id)

    @staticmethod
    def get_recent_changes(
        db: Session,
        limit: int = 50
    ) -> List[AppointmentHistory]:
        return AppointmentHistoryRepository.get_recent_changes(db, limit)

    @staticmethod
    def get_reschedule_history(
        db: Session,
        appointment_id: int
    ) -> List[AppointmentHistory]:
        return AppointmentHistoryRepository.get_reschedule_history(
            db, appointment_id
        )

    @staticmethod
    def get_status_change_history(
        db: Session,
        appointment_id: int
    ) -> List[AppointmentHistory]:
        return AppointmentHistoryRepository.get_status_change_history(
            db, appointment_id
        )

    @staticmethod
    def get_history_by_date_range(
        db: Session,
        start_date: datetime,
        end_date: datetime
    ) -> List[AppointmentHistory]:
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")

        if start_date > end_date:
            raise ValueError("start_date must be before end_date")

        return AppointmentHistoryRepository.get_by_date_range(
            db, start_date, end_date
        )

    # ================= DELETE / CLEANUP =================

    @staticmethod
    def delete_history_record(db: Session, history_id: int) -> None:
        history = AppointmentHistoryRepository.get_by_id(db, history_id)
        if not history:
            raise ValueError(f"History record with ID {history_id} not found")
        AppointmentHistoryRepository.delete(db, history)

    @staticmethod
    def cleanup_old_records(
        db: Session,
        days_to_keep: int = None
    ) -> int:
        settings = get_history_settings()
        days = days_to_keep if days_to_keep is not None else settings.RETENTION_DAYS
        cutoff_date = datetime.now() - timedelta(days=days)
        return AppointmentHistoryRepository.delete_old_records(
            db, cutoff_date
        )

    # ================= REPORTING =================

    @staticmethod
    def get_statistics(db: Session) -> Dict:
        return AppointmentHistoryRepository.get_statistics(db)

    @staticmethod
    def get_appointment_summary(
        db: Session,
        appointment_id: int
    ) -> Dict:
        records = AppointmentHistoryRepository.get_by_appointment_id(
            db, appointment_id
        )

        if not records:
            return {
                "appointment_id": appointment_id,
                "total_changes": 0,
                "reschedule_count": 0,
                "status_changes": 0,
                "timeline": []
            }

        reschedules = sum(
            1 for r in records if r.change_type == ChangeTypeEnum.RESCHEDULED
        )

        status_changes = sum(
            1 for r in records if r.change_type in (
                ChangeTypeEnum.STATUS_CHANGED,
                ChangeTypeEnum.CONFIRMED,
                ChangeTypeEnum.CANCELLED,
                ChangeTypeEnum.COMPLETED,
                ChangeTypeEnum.NO_SHOW,
            )
        )

        timeline = sorted(records, key=lambda r: r.changed_at)

        return {
            "appointment_id": appointment_id,
            "total_changes": len(records),
            "reschedule_count": reschedules,
            "status_changes": status_changes,
            "first_change": timeline[0].changed_at.isoformat(),
            "last_change": timeline[-1].changed_at.isoformat(),
            "timeline": [
                {
                    "history_id": r.history_id,
                    "change_type": r.change_type.name,
                    "changed_at": r.changed_at.isoformat(),
                    "changed_by": r.changed_by,
                }
                for r in timeline
            ],
        }

    # ================= HELPER LOGGERS =================

    @staticmethod
    def log_appointment_created(
        db: Session,
        appointment_id: int,
        created_by: int,
        appointment_date: date,
        start_time: time
    ) -> AppointmentHistory:
        return AppointmentHistoryService.create_history_record(
            db,
            {
                "appointment_id": appointment_id,
                "changed_by": created_by,
                "change_type": "CREATED",
                "new_date": appointment_date,
                "new_time": start_time,
                "new_status": "SCHEDULED",
                "change_reason": "Initial appointment booking",
            },
        )

    @staticmethod
    def log_appointment_rescheduled(
        db: Session,
        appointment_id: int,
        changed_by: int,
        old_date: date,
        new_date: date,
        old_time: time,
        new_time: time,
        reason: str = None,
    ) -> AppointmentHistory:
        return AppointmentHistoryService.create_history_record(
            db,
            {
                "appointment_id": appointment_id,
                "changed_by": changed_by,
                "change_type": "RESCHEDULED",
                "old_date": old_date,
                "new_date": new_date,
                "old_time": old_time,
                "new_time": new_time,
                "change_reason": reason or "Appointment rescheduled",
            },
        )

    @staticmethod
    def log_status_change(
        db: Session,
        appointment_id: int,
        changed_by: int,
        old_status: str,
        new_status: str,
        reason: str = None,
    ) -> AppointmentHistory:
        status_to_change_type = {
            "CONFIRMED": "CONFIRMED",
            "CANCELLED": "CANCELLED",
            "COMPLETED": "COMPLETED",
            "NO_SHOW": "NO_SHOW",
        }

        change_type = status_to_change_type.get(
            new_status, "STATUS_CHANGED"
        )

        return AppointmentHistoryService.create_history_record(
            db,
            {
                "appointment_id": appointment_id,
                "changed_by": changed_by,
                "change_type": change_type,
                "old_status": old_status,
                "new_status": new_status,
                "change_reason": reason or f"Status changed to {new_status}",
            },
        )
