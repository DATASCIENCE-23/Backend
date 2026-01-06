from fastapi import APIRouter
from Appointment_Reminder.Appointment_Reminder_controller import router as appointment_reminder_router

router = APIRouter()

router.include_router(appointment_reminder_router)
