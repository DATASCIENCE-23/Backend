from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List
from .model import InvoiceLineItem
from .service import InvoiceService
from .configuration import get_invoice_service

router = APIRouter(prefix="/line-items", tags=["Invoice Line Items"])

@router.post("/", response_model=None, status_code=status.HTTP_201_CREATED)
def create_line_item(
    line_item: dict,
    service: InvoiceService = Depends(get_invoice_service)
):
    created = service.add_line_item(line_item)
    return {"line_item_id": created.line_item_id, "message": "Line item created"}

@router.get("/{line_item_id}", response_model=None)
def get_line_item(
    line_item_id: int,
    service: InvoiceService = Depends(get_invoice_service)
):
    item = service.get_line_item(line_item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Line item not found")
    return item.__dict__

@router.get("/invoice/{invoice_id}", response_model=List[dict])
def get_invoice_line_items(
    invoice_id: int,
    service: InvoiceService = Depends(get_invoice_service)
):
    items = service.get_invoice_line_items(invoice_id)
    return [item.__dict__ for item in items]

@router.put("/{line_item_id}", response_model=dict)
def update_line_item(
    line_item_id: int,
    line_item: InvoiceLineItem,
    service: InvoiceService = Depends(get_invoice_service)
):
    if line_item.line_item_id != line_item_id:
        raise HTTPException(400, "Line item ID in body must match URL")
    updated = service.update_line_item(line_item)
    return updated.__dict__

@router.delete("/{line_item_id}", response_model=dict)
def delete_line_item(
    line_item_id: int,
    service: InvoiceService = Depends(get_invoice_service)
):
    deleted = service.remove_line_item(line_item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Line item not found")
    return {"message": "Line item deleted successfully"}
