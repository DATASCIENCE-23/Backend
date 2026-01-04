from fastapi import APIRouter
from Doctor_Schedule.Doctor_Schedule_controller import router as doctor_schedule_controller

router = APIRouter(
    prefix="/doctor-schedules",
    tags=["Doctor Schedules"]
)

router.include_router(doctor_schedule_controller)
