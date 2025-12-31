# items/routes.py
from fastapi import APIRouter
from .controller import router as items_router

router = APIRouter(prefix="/masters", tags=["Masters & Items"])

router.include_router(items_router)