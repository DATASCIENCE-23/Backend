from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_db
from .Medical_Record_service import MedicalRecordService
from .Medical_Record_repository import MedicalRecordRepository

def get_medical_record_service(
    db: Session = Depends(get_db),
) -> MedicalRecordService:
    return MedicalRecordService(MedicalRecordRepository(db))
