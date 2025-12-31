from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from Depreciation.database import get_db
from Depreciation.Depreciation_service import DepreciationService

router = APIRouter()

@router.post("/")
def create_depreciation(payload: dict, db: Session = Depends(get_db)):
    return DepreciationService.create_depreciation(db, payload)

@router.get("/")
def list_depreciations(db: Session = Depends(get_db)):
    return DepreciationService.list_depreciations(db)
