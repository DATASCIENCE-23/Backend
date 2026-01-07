from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from depreciation.depreciation_schema import DepreciationCreate, DepreciationResponse
from depreciation.depreciation_service import DepreciationService

router = APIRouter(prefix="/depreciations", tags=["Depreciation"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=DepreciationResponse)
def create_depreciation(data: DepreciationCreate, db: Session = Depends(get_db)):
    return DepreciationService.create_depreciation(db, data)

@router.get("/{depreciation_id}", response_model=DepreciationResponse)
def get_depreciation(depreciation_id: int, db: Session = Depends(get_db)):
    return DepreciationService.get_depreciation(db, depreciation_id)

@router.get("/", response_model=list[DepreciationResponse])
def get_all_depreciations(db: Session = Depends(get_db)):
    return DepreciationService.get_all_depreciations(db)

@router.get("/by-asset/{asset_id}", response_model=list[DepreciationResponse])
def get_depreciations_by_asset(asset_id: int, db: Session = Depends(get_db)):
    return DepreciationService.get_depreciation_by_asset(db, asset_id)

@router.put("/{depreciation_id}", response_model=DepreciationResponse)
def update_depreciation(depreciation_id: int, data: dict, db: Session = Depends(get_db)):
    return DepreciationService.update_depreciation(db, depreciation_id, data)

@router.delete("/{depreciation_id}")
def delete_depreciation(depreciation_id: int, db: Session = Depends(get_db)):
    DepreciationService.delete_depreciation(db, depreciation_id)
    return {"message": "Depreciation deleted successfully"}
