from fastapi import APIRouter
from BILL.bill_controller import router as bill_controller

router = APIRouter(
    prefix="/bills",
    tags=["Bills"]
)

router.include_router(bill_controller)