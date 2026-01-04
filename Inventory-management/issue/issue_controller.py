from sqlalchemy.orm import Session
from fastapi import Depends
from database import get_db
from .issue_schema import IssueCreate
from .issue_service import create_issue_request

def add_issue_request(payload: IssueCreate, db: Session = Depends(get_db)):
    return create_issue_request(db, payload)
