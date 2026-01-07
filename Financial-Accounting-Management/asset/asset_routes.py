from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from asset.asset_schema import AssetCreate, AssetResponse
from asset.asset_service import AssetService

router = APIRouter(prefix="/assets", tags=["Asset"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=AssetResponse)
def create_asset(data: AssetCreate, db: Session = Depends(get_db)):
    return AssetService.create_asset(db, data)

@router.get("/{asset_id}", response_model=AssetResponse)
def get_asset(asset_id: int, db: Session = Depends(get_db)):
    return AssetService.get_asset(db, asset_id)

@router.get("/", response_model=list[AssetResponse])
def get_all_assets(db: Session = Depends(get_db)):
    return AssetService.get_all_assets(db)

@router.put("/{asset_id}", response_model=AssetResponse)
def update_asset(asset_id: int, data: dict, db: Session = Depends(get_db)):
    return AssetService.update_asset(db, asset_id, data)

@router.delete("/{asset_id}")
def delete_asset(asset_id: int, db: Session = Depends(get_db)):
    AssetService.delete_asset(db, asset_id)
    return {"message": "Asset deleted successfully"}
