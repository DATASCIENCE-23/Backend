from fastapi import APIRouter
from .Patient_controller import router as patient_controller

router = APIRouter(
    prefix="/patients",
    tags=["Patients"]
)

router.include_router(patient_controller)
