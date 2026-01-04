from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from datetime import datetime
from typing import List, Optional
from Appointment_Reminder.Appointment_Reminder_model import AppointmentReminder, ReminderTypeEnum, ReminderStatusEnum

class AppointmentReminderRepository:

    @staticmethod
    def get_by_id(db: Session, reminder_id: int) -> Optional[AppointmentReminder]:
        return db.query(AppointmentReminder).filter(AppointmentReminder.reminder_id == reminder_id).first()

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[AppointmentReminder]:
        return db.query(AppointmentReminder).offset(skip).limit(limit).all()

    @staticmethod
    def get_by_appointment_id(db: Session, appointment_id: int) -> List[AppointmentReminder]:
        return db.query(AppointmentReminder).filter(
            AppointmentReminder.appointment_id == appointment_id
        ).order_by(AppointmentReminder.reminder_time).all()

    @staticmethod
    def get_by_status(db: Session, status: ReminderStatusEnum) -> List[AppointmentReminder]:
        return db.query(AppointmentReminder).filter(
            AppointmentReminder.status == status
        ).order_by(AppointmentReminder.reminder_time).all()

    @staticmethod
    def get_pending_reminders(db: Session) -> List[AppointmentReminder]:
        return db.query(AppointmentReminder).filter(
            AppointmentReminder.status == ReminderStatusEnum.PENDING
        ).order_by(AppointmentReminder.reminder_time).all()

    @staticmethod
    def get_due_reminders(db: Session, current_time: datetime) -> List[AppointmentReminder]:
        return db.query(AppointmentReminder).filter(
            and_(
                AppointmentReminder.status == ReminderStatusEnum.PENDING,
                AppointmentReminder.reminder_time <= current_time
            )
        ).order_by(AppointmentReminder.reminder_time).all()

    @staticmethod
    def get_failed_reminders(db: Session) -> List[AppointmentReminder]:
        return db.query(AppointmentReminder).filter(
            AppointmentReminder.status == ReminderStatusEnum.FAILED
        ).order_by(AppointmentReminder.reminder_time.desc()).all()

    @staticmethod
    def get_by_reminder_type(db: Session, reminder_type: ReminderTypeEnum) -> List[AppointmentReminder]:
        return db.query(AppointmentReminder).filter(
            AppointmentReminder.reminder_type == reminder_type
        ).all()

    @staticmethod
    def count_by_appointment(db: Session, appointment_id: int) -> int:
        return db.query(AppointmentReminder).filter(
            AppointmentReminder.appointment_id == appointment_id
        ).count()

    @staticmethod
    def count_by_status(db: Session, status: ReminderStatusEnum) -> int:
        return db.query(AppointmentReminder).filter(
            AppointmentReminder.status == status
        ).count()

    @staticmethod
    def get_reminders_by_time_range(
        db: Session,
        start_time: datetime,
        end_time: datetime
    ) -> List[AppointmentReminder]:
        return db.query(AppointmentReminder).filter(
            and_(
                AppointmentReminder.reminder_time >= start_time,
                AppointmentReminder.reminder_time <= end_time
            )
        ).order_by(AppointmentReminder.reminder_time).all()

    @staticmethod
    def create(db: Session, reminder: AppointmentReminder) -> AppointmentReminder:
        db.add(reminder)
        db.commit()
        db.refresh(reminder)
        return reminder

    @staticmethod
    def update(db: Session, reminder: AppointmentReminder) -> AppointmentReminder:
        db.commit()
        db.refresh(reminder)
        return reminder

    @staticmethod
    def delete(db: Session, reminder: AppointmentReminder) -> None:
        db.delete(reminder)
        db.commit()

    @staticmethod
    def bulk_update_status(
        db: Session,
        reminder_ids: List[int],
        new_status: ReminderStatusEnum
    ) -> int:
        count = db.query(AppointmentReminder).filter(
            AppointmentReminder.reminder_id.in_(reminder_ids)
        ).update(
            {AppointmentReminder.status: new_status},
            synchronize_session=False
        )
        db.commit()
        return count