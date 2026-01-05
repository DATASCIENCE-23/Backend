
from fastapi import APIRouter
from .stock_controller import add_stock, get_all_stock, get_stock, remove_stock, modify_stock

router = APIRouter(prefix="/stock", tags=["Stock"])

router.post("/")(add_stock)
router.get("/")(get_all_stock)
router.get("/{stock_id}")(get_stock)
router.delete("/{stock_id}")(remove_stock)
router.put("/{stock_id}")(modify_stock)
