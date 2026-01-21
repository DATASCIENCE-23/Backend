from fastapi import APIRouter
from .stock_transfer_controller import add_stock_transfer, list_stock_transfers

router = APIRouter(prefix="/stock-transfers", tags=["Stock Transfer"])

router.post("/")(add_stock_transfer)
router.get("/")(list_stock_transfers)