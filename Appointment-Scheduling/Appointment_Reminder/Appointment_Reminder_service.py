from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List, Optional, Dict
from Appointment_Reminder.Appointment_Reminder_model import AppointmentReminder, ReminderTypeEnum, ReminderStatusEnum
from Appointment_Reminder_repository import AppointmentReminderRepository
from Appointment_Reminder_config import get_reminder_settings

class AppointmentReminderService:

    @staticmethod
    def create_reminder(db: Session, data: dict) -> AppointmentReminder:
        appointment_id = data.get("appointment_id")
        reminder_type = data.get("reminder_type")
        reminder_time = data.get("reminder_time")

        if not all([appointment_id, reminder_type, reminder_time]):
            raise ValueError("Missing required fields: appointment_id, reminder_type, reminder_time")

        if isinstance(reminder_type, str):
            try:
                reminder_type = ReminderTypeEnum[reminder_type]
            except KeyError:
                raise ValueError(f"Invalid reminder_type: {reminder_type}")

        if isinstance(reminder_time, str):
            reminder_time = datetime.strptime(reminder_time, "%Y-%m-%d %H:%M:%S")

        if reminder_time < datetime.now():
            raise ValueError("Reminder time cannot be in the past")

        settings = get_reminder_settings()
        current_count = AppointmentReminderRepository.count_by_appointment(db, appointment_id)
        if current_count >= settings.MAX_REMINDERS_PER_APPOINTMENT:
            raise ValueError(f"Maximum reminders ({settings.MAX_REMINDERS_PER_APPOINTMENT}) exceeded for this appointment")

        reminder = AppointmentReminder(
            appointment_id=appointment_id,
            reminder_type=reminder_type,
            reminder_time=reminder_time,
            status=ReminderStatusEnum.PENDING,
            message_content=data.get("message_content")
        )

        return AppointmentReminderRepository.create(db, reminder)

    @staticmethod
    def get_reminder(db: Session, reminder_id: int) -> AppointmentReminder:
        reminder = AppointmentReminderRepository.get_by_id(db, reminder_id)
        if not reminder:
            raise ValueError(f"Reminder with ID {reminder_id} not found")
        return reminder

    @staticmethod
    def list_reminders(db: Session, skip: int = 0, limit: int = 100) -> List[AppointmentReminder]:
        return AppointmentReminderRepository.get_all(db, skip, limit)

    @staticmethod
    def get_appointment_reminders(db: Session, appointment_id: int) -> List[AppointmentReminder]:
        return AppointmentReminderRepository.get_by_appointment_id(db, appointment_id)

    @staticmethod
    def get_pending_reminders(db: Session) -> List[AppointmentReminder]:
        return AppointmentReminderRepository.get_pending_reminders(db)

    @staticmethod
    def get_due_reminders(db: Session) -> List[AppointmentReminder]:
        current_time = datetime.now()
        return AppointmentReminderRepository.get_due_reminders(db, current_time)

    @staticmethod
    def get_failed_reminders(db: Session) -> List[AppointmentReminder]:
        return AppointmentReminderRepository.get_failed_reminders(db)

    @staticmethod
    def mark_as_sent(db: Session, reminder_id: int) -> AppointmentReminder:
        reminder = AppointmentReminderRepository.get_by_id(db, reminder_id)
        if not reminder:
            raise ValueError(f"Reminder with ID {reminder_id} not found")

        if reminder.status != ReminderStatusEnum.PENDING:
            raise ValueError(f"Can only mark pending reminders as sent. Current status: {reminder.status.value}")

        reminder.status = ReminderStatusEnum.SENT
        reminder.sent_at = datetime.now()

        return AppointmentReminderRepository.update(db, reminder)

    @staticmethod
    def mark_as_failed(db: Session, reminder_id: int, reason: str = None) -> AppointmentReminder:
        reminder = AppointmentReminderRepository.get_by_id(db, reminder_id)
        if not reminder:
            raise ValueError(f"Reminder with ID {reminder_id} not found")

        reminder.status = ReminderStatusEnum.FAILED
        if reason:
            reminder.message_content = f"{reminder.message_content}\nFailed: {reason}"

        return AppointmentReminderRepository.update(db, reminder)

    @staticmethod
    def cancel_reminder(db: Session, reminder_id: int) -> AppointmentReminder:
        reminder = AppointmentReminderRepository.get_by_id(db, reminder_id)
        if not reminder:
            raise ValueError(f"Reminder with ID {reminder_id} not found")

        if reminder.status not in [ReminderStatusEnum.PENDING]:
            raise ValueError(f"Can only cancel pending reminders. Current status: {reminder.status.value}")

        reminder.status = ReminderStatusEnum.CANCELLED

        return AppointmentReminderRepository.update(db, reminder)

    @staticmethod
    def update_reminder(db: Session, reminder_id: int, data: dict) -> AppointmentReminder:
        reminder = AppointmentReminderRepository.get_by_id(db, reminder_id)
        if not reminder:
            raise ValueError(f"Reminder with ID {reminder_id} not found")

        if reminder.status != ReminderStatusEnum.PENDING:
            raise ValueError(f"Can only update pending reminders. Current status: {reminder.status.value}")

        for key, value in data.items():
            if key == "reminder_type" and isinstance(value, str):
                value = ReminderTypeEnum[value]
            elif key == "status" and isinstance(value, str):
                value = ReminderStatusEnum[value]
            elif key == "reminder_time" and isinstance(value, str):
                value = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
            
            if hasattr(reminder, key):
                setattr(reminder, key, value)

        return AppointmentReminderRepository.update(db, reminder)

    @staticmethod
    def delete_reminder(db: Session, reminder_id: int) -> None:
        reminder = AppointmentReminderRepository.get_by_id(db, reminder_id)
        if not reminder:
            raise ValueError(f"Reminder with ID {reminder_id} not found")

        AppointmentReminderRepository.delete(db, reminder)

    @staticmethod
    def cancel_appointment_reminders(db: Session, appointment_id: int) -> int:
        reminders = AppointmentReminderRepository.get_by_appointment_id(db, appointment_id)
        
        cancelled_count = 0
        for reminder in reminders:
            if reminder.status == ReminderStatusEnum.PENDING:
                reminder.status = ReminderStatusEnum.CANCELLED
                AppointmentReminderRepository.update(db, reminder)
                cancelled_count += 1
        
        return cancelled_count

    @staticmethod
    def process_due_reminders(db: Session) -> Dict:
        due_reminders = AppointmentReminderService.get_due_reminders(db)
        
        sent = 0
        failed = 0
        
        for reminder in due_reminders:
            try:
                # Simulate sending reminder (replace with actual sending logic)
                AppointmentReminderService.mark_as_sent(db, reminder.reminder_id)
                sent += 1
            except Exception as e:
                AppointmentReminderService.mark_as_failed(db, reminder.reminder_id, str(e))
                failed += 1
        
        return {
            "total_processed": len(due_reminders),
            "sent": sent,
            "failed": failed
        }

    @staticmethod
    def get_reminder_statistics(db: Session) -> Dict:
        total = AppointmentReminderRepository.count_by_status(db, None) if hasattr(AppointmentReminderRepository, 'count_all') else 0
        pending = AppointmentReminderRepository.count_by_status(db, ReminderStatusEnum.PENDING)
        sent = AppointmentReminderRepository.count_by_status(db, ReminderStatusEnum.SENT)
        failed = AppointmentReminderRepository.count_by_status(db, ReminderStatusEnum.FAILED)
        cancelled = AppointmentReminderRepository.count_by_status(db, ReminderStatusEnum.CANCELLED)

        return {
            "total_reminders": total,
            "pending": pending,
            "sent": sent,
            "failed": failed,
            "cancelled": cancelled
        }
