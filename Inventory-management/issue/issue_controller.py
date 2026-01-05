from sqlalchemy.orm import Session
from fastapi import Depends
from database import get_db
from .issue_schema import IssueCreate
from .issue_service import create_issue_request, get_issue_request, list_issue_requests

def add_issue_request(payload: IssueCreate, db: Session = Depends(get_db)):
    return create_issue_request(db, payload)

def get_issue_request_by_id(request_id: int, db: Session = Depends(get_db)):
    return get_issue_request(db, request_id)

def get_all_issue_requests(db: Session = Depends(get_db)):
    return list_issue_requests(db)