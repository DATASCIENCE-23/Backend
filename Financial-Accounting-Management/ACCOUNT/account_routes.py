from fastapi import APIRouter
from ACCOUNT.account_controller import router as account_controller

router = APIRouter(
    prefix="/accounts",
    tags=["Accounts"]
)

router.include_router(account_controller)