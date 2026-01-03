from fastapi import APIRouter
from .admission_controller import router as admission_controller

router = APIRouter(
    prefix="/admissions",
    tags=["Admissions"]
)

router.include_router(admission_controller)
