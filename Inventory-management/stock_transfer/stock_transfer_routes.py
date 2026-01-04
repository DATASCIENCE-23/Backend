from fastapi import APIRouter
from .stock_transfer_controller import add_stock_transfer

router = APIRouter(prefix="/stock-transfers", tags=["Stock Transfer"])

router.post("/")(add_stock_transfer)
