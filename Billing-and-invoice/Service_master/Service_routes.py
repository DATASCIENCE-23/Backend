from fastapi import APIRouter
from Service.Service_controller import router as service_controller

router = APIRouter(
    prefix="/services",
    tags=["Services"]
)

router.include_router(service_controller)