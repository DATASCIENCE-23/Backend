from sqlalchemy.orm import Session
from issue.issue_model import IssueRequest, IssueDetail
from sqlalchemy import desc

class IssueRepository:
    @staticmethod
    def get_request_by_id(db: Session, request_id: int):
        return db.query(IssueRequest).filter(IssueRequest.request_id == request_id).first()

    @staticmethod
    def get_request_by_number(db: Session, request_number: str):
        return db.query(IssueRequest).filter(IssueRequest.request_number == request_number).first()

    @staticmethod
    def create_request(db: Session, request: IssueRequest):
        db.add(request)
        db.commit()
        db.refresh(request)
        return request

    @staticmethod
    def update_request(db: Session, request: IssueRequest):
        db.commit()
        db.refresh(request)
        return request

    @staticmethod
    def get_all_requests(db: Session, skip: int = 0, limit: int = 100):
        return db.query(IssueRequest).order_by(desc(IssueRequest.request_datetime)).offset(skip).limit(limit).all()

    @staticmethod
    def create_detail(db: Session, detail: IssueDetail):
        db.add(detail)
        db.commit()
        db.refresh(detail)
        return detail