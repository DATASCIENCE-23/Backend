from fastapi import APIRouter
from .purchase_controller import add_purchase, get_all_purchases

router = APIRouter(prefix="/purchases", tags=["Purchase"])

router.post("/")(add_purchase)
router.get("/")(get_all_purchases)
