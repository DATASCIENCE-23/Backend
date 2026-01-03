from sqlalchemy.orm import Session
from datetime import date, time, datetime, timedelta
from typing import List, Optional, Dict
from Appointment_History.Appointment_History_model import AppointmentHistory, ChangeTypeEnum
from Repository.Appointment_History_repository import AppointmentHistoryRepository
from Appointment_History_config import get_history_settings

class AppointmentHistoryService:

    @staticmethod
    def create_history_record(db: Session, data: dict) -> AppointmentHistory:
        """Create a new history record"""
        # Extract required fields
        appointment_id = data.get("appointment_id")
        changed_by = data.get("changed_by")
        change_type = data.get("change_type")

        # Validate required fields
        if not all([appointment_id, changed_by, change_type]):
            raise ValueError("Missing required fields: appointment_id, changed_by, change_type")

        # Convert change_type if string
        if isinstance(change_type, str):
            try:
                change_type = ChangeTypeEnum[change_type]
            except KeyError:
                raise ValueError(f"Invalid change_type: {change_type}")

        # Convert date/time strings if needed
        old_date = data.get("old_date")
        new_date = data.get("new_date")
        old_time = data.get("old_time")
        new_time = data.get("new_time")

        if old_date and isinstance(old_date, str):
            old_date = datetime.strptime(old_date, "%Y-%m-%d").date()
        if new_date and isinstance(new_date, str):
            new_date = datetime.strptime(new_date, "%Y-%m-%d").date()
        if old_time and isinstance(old_time, str):
            old_time = datetime.strptime(old_time, "%H:%M:%S").time()
        if new_time and isinstance(new_time, str):
            new_time = datetime.strptime(new_time, "%H:%M:%S").time()

        # Check if appointment has too many history records
        settings = get_history_settings()
        current_count = AppointmentHistoryRepository.count_by_appointment(db, appointment_id)
        if current_count >= settings.MAX_HISTORY_PER_APPOINTMENT:
            raise ValueError(f"Maximum history records ({settings.MAX_HISTORY_PER_APPOINTMENT}) exceeded for this appointment")

        # Create history record
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

    @staticmethod
    def get_history_record(db: Session, history_id: int) -> AppointmentHistory:
        """Get history record by ID"""
        history = AppointmentHistoryRepository.get_by_id(db, history_id)
        if not history:
            raise ValueError(f"History record with ID {history_id} not found")
        return history

    @staticmethod
    def list_history_records(db: Session, skip: int = 0, limit: int = 100) -> List[AppointmentHistory]:
        """List all history records with pagination"""
        return AppointmentHistoryRepository.get_all(db, skip, limit)

    @staticmethod
    def get_appointment_history(db: Session, appointment_id: int) -> List[AppointmentHistory]:
        """Get all history records for an appointment"""
        return AppointmentHistoryRepository.get_by_appointment_id(db, appointment_id)

    @staticmethod
    def get_appointment_timeline(db: Session, appointment_id: int) -> List[AppointmentHistory]:
        """Get chronological timeline for an appointment"""
        return AppointmentHistoryRepository.get_appointment_timeline(db, appointment_id)

    @staticmethod
    def get_by_change_type(db: Session, change_type: str) -> List[AppointmentHistory]:
        """Get history records by change type"""
        try:
            change_type_enum = ChangeTypeEnum[change_type]
        except KeyError:
            raise ValueError(f"Invalid change_type: {change_type}")
        return AppointmentHistoryRepository.get_by_change_type(db, change_type_enum)

    @staticmethod
    def get_by_user(db: Session, user_id: int) -> List[AppointmentHistory]:
        """Get all changes made by a specific user"""
        return AppointmentHistoryRepository.get_by_changed_by(db, user_id)

    @staticmethod
    def get_recent_changes(db: Session, limit: int = 50) -> List[AppointmentHistory]:
        """Get recent history records"""
        return AppointmentHistoryRepository.get_recent_changes(db, limit)

    @staticmethod
    def get_reschedule_history(db: Session, appointment_id: int) -> List[AppointmentHistory]:
        """Get all reschedule records for an appointment"""
        return AppointmentHistoryRepository.get_reschedule_history(db, appointment_id)

    @staticmethod
    def get_status_change_history(db: Session, appointment_id: int) -> List[AppointmentHistory]:
        """Get all status change records"""
        return AppointmentHistoryRepository.get_status_change_history(db, appointment_id)

    @staticmethod
    def get_history_by_date_range(
        db: Session,
        start_date: datetime,
        end_date: datetime
    ) -> List[AppointmentHistory]:
        """Get history records within a date range"""
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")

        if start_date > end_date:
            raise ValueError("start_date must be before end_date")

        return AppointmentHistoryRepository.get_by_date_range(db, start_date, end_date)

    @staticmethod
    def delete_history_record(db: Session, history_id: int) -> None:
        """Delete a history record"""
        history = AppointmentHistoryRepository.get_by_id(db, history_id)
        if not history:
            raise ValueError(f"History record with ID {history_id} not found")
        AppointmentHistoryRepository.delete(db, history)

    @staticmethod
    def cleanup_old_records(db: Session, days_to_keep: int = None) -> int:
        """Cleanup old history records"""
        settings = get_history_settings()
        days = days_to_keep if days_to_keep else settings.RETENTION_DAYS
        cutoff_date = datetime.now() - timedelta(days=days)
        return AppointmentHistoryRepository.delete_old_records(db, cutoff_date)

    @staticmethod
    def get_statistics(db: Session) -> Dict:
        """Get overall history statistics"""
        return AppointmentHistoryRepository.get_statistics(db)

    @staticmethod
    def get_appointment_summary(db: Session, appointment_id: int) -> Dict:
        """Get summary of changes for an appointment"""
        history_records = AppointmentHistoryRepository.get_by_appointment_id(db, appointment_id)
        
        if not history_records:
            return {
                "appointment_id": appointment_id,
                "total_changes": 0,
                "reschedule_count": 0,
                "status_changes": 0,
                "timeline": []
            }

        reschedules = sum(1 for h in history_records if h.change_type == ChangeTypeEnum.RESCHEDULED)
        status_changes = sum(1 for h in history_records if h.change_type in [
            ChangeTypeEnum.STATUS_CHANGED,
            ChangeTypeEnum.CONFIRMED,
            ChangeTypeEnum.CANCELLED,
            ChangeTypeEnum.COMPLETED
        ])

        timeline = sorted(history_records, key=lambda x: x.changed_at)

        return {
            "appointment_id": appointment_id,
            "total_changes": len(history_records),
            "reschedule_count": reschedules,
            "status_changes": status_changes,
            "first_change": timeline[0].changed_at.isoformat() if timeline else None,
            "last_change": timeline[-1].changed_at.isoformat() if timeline else None,
            "timeline": [
                {
                    "history_id": h.history_id,
                    "change_type": h.change_type.name,
                    "changed_at": h.changed_at.isoformat(),
                    "changed_by": h.changed_by
                }
                for h in timeline
            ]
        }

    @staticmethod
    def log_appointment_created(
        db: Session,
        appointment_id: int,
        created_by: int,
        appointment_date: date,
        start_time: time
    ) -> AppointmentHistory:
        """Helper: Log appointment creation"""
        return AppointmentHistoryService.create_history_record(db, {
            "appointment_id": appointment_id,
            "changed_by": created_by,
            "change_type": "CREATED",
            "new_date": appointment_date,
            "new_time": start_time,
            "new_status": "SCHEDULED",
            "change_reason": "Initial appointment booking"
        })

    @staticmethod
    def log_appointment_rescheduled(
        db: Session,
        appointment_id: int,
        changed_by: int,
        old_date: date,
        new_date: date,
        old_time: time,
        new_time: time,
        reason: str = None
    ) -> AppointmentHistory:
        """Helper: Log appointment reschedule"""
        return AppointmentHistoryService.create_history_record(db, {
            "appointment_id": appointment_id,
            "changed_by": changed_by,
            "change_type": "RESCHEDULED",
            "old_date": old_date,
            "new_date": new_date,
            "old_time": old_time,
            "new_time": new_time,
            "change_reason": reason or "Appointment rescheduled"
        })

    @staticmethod
    def log_status_change(
        db: Session,
        appointment_id: int,
        changed_by: int,
        old_status: str,
        new_status: str,
        reason: str = None
    ) -> AppointmentHistory:
        """Helper: Log status change"""
        change_type_map = {
            "CONFIRMED": "CONFIRMED",
            "CANCELLED": "CANCELLED",
            "COMPLETED": "COMPLETED",
            "NO_SHOW": "NO_SHOW"
        }
        
        change_type = change_type_map.get(new_status, "STATUS_CHANGED")
        
        return AppointmentHistoryService.create_history_record(db, {
            "appointment_id": appointment_id,
            "changed_by": changed_by,
            "change_type": change_type,
            "old_status": old_status,
            "new_status": new_status,
            "change_reason": reason or f"Status changed to {new_status}"
        })