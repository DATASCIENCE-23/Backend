from fastapi import APIRouter
from Insurance_controller import router as insurance_controller

router = APIRouter(
    prefix="/insurance",
    tags=["Insurance"]
)

router.include_router(insurance_controller)
