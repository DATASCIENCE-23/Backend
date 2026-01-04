from fastapi import APIRouter
from issue.issue_controller import router as issue_router

router = APIRouter(prefix="/issues", tags=["Issue & Stock Out"])

router.include_router(issue_router)