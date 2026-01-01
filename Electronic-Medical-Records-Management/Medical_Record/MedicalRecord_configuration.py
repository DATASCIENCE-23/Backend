from fastapi import Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .MedicalRecord_service import MedicalRecordService

def get_medical_record_service(db: Session = Depends(get_db)) -> MedicalRecordService:
    return MedicalRecordService(db)