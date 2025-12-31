from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Asset.database import get_db
from Asset.Asset_service import AssetService

router = APIRouter()

@router.post("/")
def create_asset(payload: dict, db: Session = Depends(get_db)):
    return AssetService.create_asset(db, payload)

@router.get("/{asset_id}")
def get_asset(asset_id: int, db: Session = Depends(get_db)):
    try:
        return AssetService.get_asset(db, asset_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/")
def list_assets(db: Session = Depends(get_db)):
    return AssetService.list_assets(db)
