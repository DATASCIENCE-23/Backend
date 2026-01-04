from fastapi import APIRouter
from PATIENT.patient_controller import router as patient_controller

router = APIRouter(
    prefix="/patients",
    tags=["Patients"]
)

router.include_router(patient_controller)
