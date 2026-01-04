from fastapi import APIRouter
from Appointment.Appointment_controller import router as appointment_controller

router = APIRouter(
    prefix="/appointments",
    tags=["Appointments"]
)

router.include_router(appointment_controller)
