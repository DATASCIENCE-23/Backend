
from fastapi import APIRouter
from .stock_controller import add_stock, get_all_stock

router = APIRouter(prefix="/stock", tags=["Stock"])

router.post("/")(add_stock)
router.get("/")(get_all_stock)
