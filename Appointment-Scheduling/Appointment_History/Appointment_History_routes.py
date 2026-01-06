from fastapi import APIRouter
from Appointment_History.Appointment_History_controller import router as appointment_history_router

router = APIRouter()

router.include_router(appointment_history_router)
