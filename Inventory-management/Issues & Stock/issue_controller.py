from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from issue.database import get_db
from issue.issue_service import IssueService

router = APIRouter()

@router.post("/raise")
def raise_issue_request(request: Request, payload: dict, db: Session = Depends(get_db)):
    user_id = 1  # Replace with actual auth user ID (e.g., from JWT)
    try:
        return IssueService.raise_request(db, payload, user_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{request_id}/approve")
def approve_issue(request_id: int, request: Request, db: Session = Depends(get_db)):
    user_id = 1  # Store keeper user ID from auth
    try:
        return IssueService.approve_and_issue(db, request_id, user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{request_id}/cancel")
def cancel_issue(request_id: int, db: Session = Depends(get_db)):
    try:
        return IssueService.cancel_request(db, request_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{request_id}")
def get_issue_request(request_id: int, db: Session = Depends(get_db)):
    try:
        return IssueService.get_request(db, request_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/")
def list_issue_requests(db: Session = Depends(get_db)):
    return IssueService.list_requests(db)