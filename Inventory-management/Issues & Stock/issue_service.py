from datetime import datetime
from sqlalchemy.orm import Session
from issue.issue_model import IssueRequest, IssueDetail
from issue.issue_repository import IssueRepository
from sqlalchemy.exc import IntegrityError

# Assume you have a StockService with this function elsewhere
from stock.stock_service import StockService  # StockService.remove(item_id, qty, store_id)

class IssueService:
    @staticmethod
    def generate_request_number(db: Session) -> str:
        from datetime import datetime
        today = datetime.utcnow().strftime("%Y%m%d")
        last = db.query(IssueRequest).filter(IssueRequest.request_number.like(f"ISS{today}%")).order_by(IssueRequest.request_number.desc()).first()
        seq = 1 if not last else int(last.request_number[-4:]) + 1
        return f"ISS{today}{seq:04d}"

    @staticmethod
    def raise_request(db: Session, payload: dict, user_id: int):
        # payload: { "department_id": int, "items": [{"item_id": int, "requested_quantity": int}, ...] }
        request_number = IssueService.generate_request_number(db)

        request = IssueRequest(
            request_number=request_number,
            department_id=payload["department_id"],
            requested_by=user_id,
            status="pending_approval"  # or "draft" if needed
        )
        db.add(request)
        db.flush()  # to get request_id

        for item in payload["items"]:
            detail = IssueDetail(
                request_id=request.request_id,
                item_id=item["item_id"],
                requested_quantity=item["requested_quantity"],
                issued_quantity=0
            )
            db.add(detail)

        db.commit()
        db.refresh(request)
        return request

    @staticmethod
    def approve_and_issue(db: Session, request_id: int, approved_by: int, store_id: int = 1):
        request = IssueRepository.get_request_by_id(db, request_id)
        if not request:
            raise ValueError("Issue request not found")
        if request.status not in ["pending_approval", "approved"]:
            raise ValueError(f"Request cannot be approved in status: {request.status}")

        request.approved_by = approved_by
        request.status = "approved"
        
        all_issued = True
        for detail in request.details:
            if detail.issued_quantity > 0:
                continue
            qty_to_issue = detail.requested_quantity - detail.issued_quantity
            try:
                StockService.remove(item_id=detail.item_id, qty=qty_to_issue, store_id=store_id)
            except ValueError as e:
                raise ValueError(f"Insufficient stock for item {detail.item_id}: {str(e)}")

            detail.issued_quantity = detail.requested_quantity
            detail.issued_datetime = datetime.utcnow()
            detail.issued_by = approved_by

            if detail.issued_quantity < detail.requested_quantity:
                all_issued = False

        request.status = "completed" if all_issued else "partially_issued"
        db.commit()
        return request

    @staticmethod
    def cancel_request(db: Session, request_id: int):
        request = IssueRepository.get_request_by_id(db, request_id)
        if not request:
            raise ValueError("Issue request not found")
        if request.status not in ["draft", "pending_approval"]:
            raise ValueError("Only draft/pending requests can be cancelled")
        request.status = "cancelled"
        db.commit()
        return request

    @staticmethod
    def get_request(db: Session, request_id: int):
        request = IssueRepository.get_request_by_id(db, request_id)
        if not request:
            raise ValueError("Issue request not found")
        return request

    @staticmethod
    def list_requests(db: Session):
        return IssueRepository.get_all_requests(db)