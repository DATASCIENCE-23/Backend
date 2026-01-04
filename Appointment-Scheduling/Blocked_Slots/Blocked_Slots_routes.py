from fastapi import APIRouter
from Blocked_Slots.Blocked_Slots_controller import router as blocked_slots_controller

router = APIRouter(
    prefix="/blocked-slots",
    tags=["Blocked Slots"]
)

router.include_router(blocked_slots_controller)
