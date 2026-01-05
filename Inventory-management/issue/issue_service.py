from sqlalchemy.orm import Session
from fastapi import HTTPException
from .issue_models import IssueRequest, IssueDetail
from . import issue_repository as repository
from item.item_repository import get_by_id as get_item
from stock.stock_repository import get_by_item_and_location
from stock.stock_repository import update as update_stock

MAIN_STORE_ID = 1  # simplify for college demo

def create_issue_request(db: Session, data):
    req = IssueRequest(department_id=data.department_id)
    req = repository.create_request(db, req)

    for i in data.items:
        item = get_item(db, i.item_id)
        if not item:
            raise HTTPException(400, "Item does not exist")

        stock = get_by_item_and_location(db, i.item_id, MAIN_STORE_ID)
        if not stock or stock.quantity_available < i.quantity:
            raise HTTPException(
                400,
                f"Insufficient stock for item {item.name}"
            )

        # reduce stock
        stock.quantity_available -= i.quantity
        update_stock(db, stock)

        detail = IssueDetail(
            request_id=req.id,
            item_id=i.item_id,
            quantity=i.quantity
        )
        repository.create_detail(db, detail)

    req.status = "approved"
    db.commit()
    return req

def get_issue_request(db: Session, request_id: int):
    req = repository.get_request_by_id(db, request_id)
    if not req:
        raise HTTPException(404, "Issue request not found")
    return req

def list_issue_requests(db: Session):
    return repository.get_all_requests(db)
