from fastapi import APIRouter
from Appointment_Reminder.Appointment_Reminder_controller import router as appointment_reminder_controller

router = APIRouter(
    prefix="/appointment-reminders",
    tags=["Appointment Reminders"]
)

router.include_router(appointment_reminder_controller)