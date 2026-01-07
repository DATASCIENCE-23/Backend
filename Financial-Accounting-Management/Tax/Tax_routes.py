from fastapi import APIRouter
from Tax.Tax_controller import router as tax_controller

router = APIRouter(
    prefix="/taxes",
    tags=["Taxes"]
)

router.include_router(tax_controller)
