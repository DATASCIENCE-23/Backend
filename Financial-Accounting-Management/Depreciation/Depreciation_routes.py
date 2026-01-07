from fastapi import APIRouter
from Depreciation.Depreciation_controller import router as depreciation_controller

router = APIRouter(
    prefix="/depreciations",
    tags=["Depreciations"]
)

router.include_router(depreciation_controller)
