from sqlalchemy.orm import Session
from sqlalchemy import and_, desc
from datetime import datetime
from typing import List, Optional

from Appointment_History.Appointment_History_model import (
    AppointmentHistory,
    ChangeTypeEnum
)


class AppointmentHistoryRepository:
    """Repository layer for Appointment History (DB operations only)"""

    # ================= BASIC GET =================

    @staticmethod
    def get_by_id(
        db: Session,
        history_id: int
    ) -> Optional[AppointmentHistory]:
        return (
            db.query(AppointmentHistory)
            .filter(AppointmentHistory.history_id == history_id)
            .first()
        )

    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 100
    ) -> List[AppointmentHistory]:
        return (
            db.query(AppointmentHistory)
            .offset(skip)
            .limit(limit)
            .all()
        )

    # ================= APPOINTMENT BASED =================

    @staticmethod
    def get_by_appointment_id(
        db: Session,
        appointment_id: int
    ) -> List[AppointmentHistory]:
        return (
            db.query(AppointmentHistory)
            .filter(AppointmentHistory.appointment_id == appointment_id)
            .order_by(desc(AppointmentHistory.changed_at))
            .all()
        )

    @staticmethod
    def get_appointment_timeline(
        db: Session,
        appointment_id: int
    ) -> List[AppointmentHistory]:
        """Chronological timeline"""
        return (
            db.query(AppointmentHistory)
            .filter(AppointmentHistory.appointment_id == appointment_id)
            .order_by(AppointmentHistory.changed_at)
            .all()
        )

    @staticmethod
    def count_by_appointment(
        db: Session,
        appointment_id: int
    ) -> int:
        return (
            db.query(AppointmentHistory)
            .filter(AppointmentHistory.appointment_id == appointment_id)
            .count()
        )

    # ================= FILTERS =================

    @staticmethod
    def get_by_change_type(
        db: Session,
        change_type: ChangeTypeEnum
    ) -> List[AppointmentHistory]:
        return (
            db.query(AppointmentHistory)
            .filter(AppointmentHistory.change_type == change_type)
            .order_by(desc(AppointmentHistory.changed_at))
            .all()
        )

    @staticmethod
    def get_by_changed_by(
        db: Session,
        changed_by: int
    ) -> List[AppointmentHistory]:
        return (
            db.query(AppointmentHistory)
            .filter(AppointmentHistory.changed_by == changed_by)
            .order_by(desc(AppointmentHistory.changed_at))
            .all()
        )

    @staticmethod
    def get_by_date_range(
        db: Session,
        start_date: datetime,
        end_date: datetime
    ) -> List[AppointmentHistory]:
        return (
            db.query(AppointmentHistory)
            .filter(
                and_(
                    AppointmentHistory.changed_at >= start_date,
                    AppointmentHistory.changed_at <= end_date
                )
            )
            .order_by(desc(AppointmentHistory.changed_at))
            .all()
        )

    @staticmethod
    def get_recent_changes(
        db: Session,
        limit: int = 50
    ) -> List[AppointmentHistory]:
        return (
            db.query(AppointmentHistory)
            .order_by(desc(AppointmentHistory.changed_at))
            .limit(limit)
            .all()
        )

    # ================= SPECIALIZED =================

    @staticmethod
    def get_reschedule_history(
        db: Session,
        appointment_id: int
    ) -> List[AppointmentHistory]:
        return (
            db.query(AppointmentHistory)
            .filter(
                and_(
                    AppointmentHistory.appointment_id == appointment_id,
                    AppointmentHistory.change_type == ChangeTypeEnum.RESCHEDULED
                )
            )
            .order_by(AppointmentHistory.changed_at)
            .all()
        )

    @staticmethod
    def get_status_change_history(
        db: Session,
        appointment_id: int
    ) -> List[AppointmentHistory]:
        return (
            db.query(AppointmentHistory)
            .filter(
                and_(
                    AppointmentHistory.appointment_id == appointment_id,
                    AppointmentHistory.change_type.in_(
                        [
                            ChangeTypeEnum.STATUS_CHANGED,
                            ChangeTypeEnum.CONFIRMED,
                            ChangeTypeEnum.CANCELLED,
                            ChangeTypeEnum.COMPLETED,
                            ChangeTypeEnum.NO_SHOW,
                        ]
                    )
                )
            )
            .order_by(AppointmentHistory.changed_at)
            .all()
        )

    # ================= CREATE / DELETE =================

    @staticmethod
    def create(
        db: Session,
        history: AppointmentHistory
    ) -> AppointmentHistory:
        db.add(history)
        db.commit()
        db.refresh(history)
        return history

    @staticmethod
    def delete(
        db: Session,
        history: AppointmentHistory
    ) -> None:
        db.delete(history)
        db.commit()

    @staticmethod
    def delete_old_records(
        db: Session,
        before_date: datetime
    ) -> int:
        records = (
            db.query(AppointmentHistory)
            .filter(AppointmentHistory.changed_at < before_date)
        )

        count = records.count()
        records.delete(synchronize_session=False)
        db.commit()
        return count

    # ================= STATISTICS =================

    @staticmethod
    def get_statistics(db: Session) -> dict:
        stats = {
            "total_records": db.query(AppointmentHistory).count(),
            "by_change_type": {}
        }

        for change_type in ChangeTypeEnum:
            stats["by_change_type"][change_type.name] = (
                db.query(AppointmentHistory)
                .filter(AppointmentHistory.change_type == change_type)
                .count()
            )

        return stats
