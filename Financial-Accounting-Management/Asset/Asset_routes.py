from fastapi import APIRouter
from Asset.Asset_controller import router as asset_controller

router = APIRouter(
    prefix="/assets",
    tags=["Assets"]
)

router.include_router(asset_controller)
