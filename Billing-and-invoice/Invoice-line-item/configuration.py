from sqlalchemy.orm import Session
from fastapi import Depends
from ..database import get_db
from .repository import InvoiceRepository
from .service import InvoiceService

def get_invoice_service(db: Session = Depends(get_db)) -> InvoiceService:
    repo = InvoiceRepository(db)
    return InvoiceService(repo)
