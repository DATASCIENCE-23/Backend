from sqlalchemy.orm import Session
from .issue_models import IssueRequest, IssueDetail

def create_request(db: Session, req: IssueRequest):
    db.add(req)
    db.commit()
    db.refresh(req)
    return req

def get_request_by_id(db: Session, request_id: int):
    return db.query(IssueRequest).filter(IssueRequest.id == request_id).first()

def get_all_requests(db: Session):
    return db.query(IssueRequest).all()

def create_detail(db: Session, detail: IssueDetail):
    db.add(detail)
    db.commit()
    db.refresh(detail)
    return detail
