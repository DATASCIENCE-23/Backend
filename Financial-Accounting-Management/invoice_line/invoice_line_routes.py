from fastapi import APIRouter
from INVOICE_LINE.invoice_line_controller import router as invoice_line_controller

router = APIRouter(
    prefix="/invoice-lines",
    tags=["Invoice Lines"]
)

router.include_router(invoice_line_controller)
