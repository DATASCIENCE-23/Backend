from fastapi import APIRouter
from Appointment_History.Appointment_History_controller import router as appointment_history_controller

router = APIRouter(
    prefix="/appointment-history",
    tags=["Appointment History"]
)

router.include_router(appointment_history_controller)