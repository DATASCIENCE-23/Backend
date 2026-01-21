from fastapi import APIRouter
from .stock_adjustment_controller import add_stock_adjustment, list_stock_adjustments

router = APIRouter(prefix="/stock-adjustments", tags=["Stock Adjustment"])

router.post("/")(add_stock_adjustment)
router.get("/")(list_stock_adjustments)
    