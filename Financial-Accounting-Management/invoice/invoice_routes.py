from fastapi import APIRouter
from INVOICE.invoice_controller import router as invoice_controller

router = APIRouter(
    prefix="/invoices",
    tags=["Invoices"]
)

router.include_router(invoice_controller)
