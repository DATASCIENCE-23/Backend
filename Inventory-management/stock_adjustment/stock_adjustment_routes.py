from fastapi import APIRouter
from .stock_adjustment_controller import add_stock_adjustment

router = APIRouter(prefix="/stock-adjustments", tags=["Stock Adjustment"])

router.post("/")(add_stock_adjustment)
    