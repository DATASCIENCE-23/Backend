from sqlalchemy.orm import Session
from .issue_models import IssueRequest, IssueDetail

def create_request(db: Session, req: IssueRequest):
    db.add(req)
    db.commit()
    db.refresh(req)
    return req

def create_detail(db: Session, detail: IssueDetail):
    db.add(detail)
    db.commit()
    db.refresh(detail)
    return detail
