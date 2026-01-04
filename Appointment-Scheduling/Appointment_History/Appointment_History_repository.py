from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc
from datetime import date, time, datetime, timedelta
from typing import List, Optional
from Appointment_History.Appointment_History_model import AppointmentHistory, ChangeTypeEnum

class AppointmentHistoryRepository:

    @staticmethod
    def get_by_id(db: Session, history_id: int) -> Optional[AppointmentHistory]:
        """Get history record by ID"""
        return db.query(AppointmentHistory).filter(AppointmentHistory.history_id == history_id).first()

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[AppointmentHistory]:
        """Get all history records with pagination"""
        return db.query(AppointmentHistory).offset(skip).limit(limit).all()

    @staticmethod
    def get_by_appointment_id(db: Session, appointment_id: int) -> List[AppointmentHistory]:
        """Get all history records for a specific appointment"""
        return db.query(AppointmentHistory).filter(
            AppointmentHistory.appointment_id == appointment_id
        ).order_by(desc(AppointmentHistory.changed_at)).all()

    @staticmethod
    def get_by_change_type(db: Session, change_type: ChangeTypeEnum) -> List[AppointmentHistory]:
        """Get all history records of a specific change type"""
        return db.query(AppointmentHistory).filter(
            AppointmentHistory.change_type == change_type
        ).order_by(desc(AppointmentHistory.changed_at)).all()

    @staticmethod
    def get_by_changed_by(db: Session, changed_by: int) -> List[AppointmentHistory]:
        """Get all history records changed by a specific user"""
        return db.query(AppointmentHistory).filter(
            AppointmentHistory.changed_by == changed_by
        ).order_by(desc(AppointmentHistory.changed_at)).all()

    @staticmethod
    def get_by_date_range(
        db: Session,
        start_date: datetime,
        end_date: datetime
    ) -> List[AppointmentHistory]:
        """Get history records within a date range"""
        return db.query(AppointmentHistory).filter(
            and_(
                AppointmentHistory.changed_at >= start_date,
                AppointmentHistory.changed_at <= end_date
            )
        ).order_by(desc(AppointmentHistory.changed_at)).all()

    @staticmethod
    def get_recent_changes(db: Session, limit: int = 50) -> List[AppointmentHistory]:
        """Get recent history records"""
        return db.query(AppointmentHistory).order_by(
            desc(AppointmentHistory.changed_at)
        ).limit(limit).all()

    @staticmethod
    def get_appointment_timeline(db: Session, appointment_id: int) -> List[AppointmentHistory]:
        """Get complete timeline for an appointment (chronological order)"""
        return db.query(AppointmentHistory).filter(
            AppointmentHistory.appointment_id == appointment_id
        ).order_by(AppointmentHistory.changed_at).all()

    @staticmethod
    def count_by_appointment(db: Session, appointment_id: int) -> int:
        """Count history records for an appointment"""
        return db.query(AppointmentHistory).filter(
            AppointmentHistory.appointment_id == appointment_id
        ).count()

    @staticmethod
    def count_by_change_type(db: Session, change_type: ChangeTypeEnum) -> int:
        """Count history records of a specific type"""
        return db.query(AppointmentHistory).filter(
            AppointmentHistory.change_type == change_type
        ).count()

    @staticmethod
    def get_reschedule_history(db: Session, appointment_id: int) -> List[AppointmentHistory]:
        """Get all reschedule records for an appointment"""
        return db.query(AppointmentHistory).filter(
            and_(
                AppointmentHistory.appointment_id == appointment_id,
                AppointmentHistory.change_type == ChangeTypeEnum.RESCHEDULED
            )
        ).order_by(AppointmentHistory.changed_at).all()

    @staticmethod
    def get_status_change_history(db: Session, appointment_id: int) -> List[AppointmentHistory]:
        """Get all status change records for an appointment"""
        return db.query(AppointmentHistory).filter(
            and_(
                AppointmentHistory.appointment_id == appointment_id,
                AppointmentHistory.change_type.in_([
                    ChangeTypeEnum.STATUS_CHANGED,
                    ChangeTypeEnum.CONFIRMED,
                    ChangeTypeEnum.CANCELLED,
                    ChangeTypeEnum.COMPLETED,
                    ChangeTypeEnum.NO_SHOW
                ])
            )
        ).order_by(AppointmentHistory.changed_at).all()

    @staticmethod
    def create(db: Session, history: AppointmentHistory) -> AppointmentHistory:
        """Create a new history record"""
        db.add(history)
        db.commit()
        db.refresh(history)
        return history

    @staticmethod
    def delete(db: Session, history: AppointmentHistory) -> None:
        """Delete a history record"""
        db.delete(history)
        db.commit()

    @staticmethod
    def delete_old_records(db: Session, before_date: datetime) -> int:
        """Delete history records older than specified date"""
        count = db.query(AppointmentHistory).filter(
            AppointmentHistory.changed_at < before_date
        ).count()
        db.query(AppointmentHistory).filter(
            AppointmentHistory.changed_at < before_date
        ).delete()
        db.commit()
        return count

    @staticmethod
    def get_statistics(db: Session) -> dict:
        """Get overall statistics"""
        total = db.query(AppointmentHistory).count()
        
        stats = {
            "total_records": total,
            "by_change_type": {}
        }
        
        for change_type in ChangeTypeEnum:
            count = db.query(AppointmentHistory).filter(
                AppointmentHistory.change_type == change_type
            ).count()
            stats["by_change_type"][change_type.name] = count
        
        return stats