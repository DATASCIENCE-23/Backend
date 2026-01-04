from fastapi import APIRouter
from .issue_controller import add_issue_request

router = APIRouter(prefix="/issues", tags=["Issue"])

router.post("/")(add_issue_request)
