from fastapi import APIRouter
from PAYMENT.payment_controller import router as payment_controller

router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)

router.include_router(payment_controller)
