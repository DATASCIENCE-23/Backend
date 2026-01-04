from fastapi import APIRouter
from .purchase_controller import add_purchase

router = APIRouter(prefix="/purchases", tags=["Purchase"])

router.post("/")(add_purchase)
