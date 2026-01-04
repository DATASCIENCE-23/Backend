from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_db
from .Prescription_Item_service import PrescriptionItemService

def get_prescription_item_service(
    db: Session = Depends(get_db)
) -> PrescriptionItemService:
    return PrescriptionItemService(db)
