from fastapi import Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .Prescription_service import PrescriptionService

def get_prescription_service(db: Session = Depends(get_db)) -> PrescriptionService:
    return PrescriptionService(db)