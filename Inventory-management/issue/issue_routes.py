from fastapi import APIRouter
from .issue_controller import add_issue_request, get_issue_request_by_id, get_all_issue_requests

router = APIRouter(prefix="/issues", tags=["Issue"])

router.post("/")(add_issue_request)
router.get("/{request_id}")(get_issue_request_by_id)
router.get("/")(get_all_issue_requests)

