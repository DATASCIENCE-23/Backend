from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..database import get_db
from .Service_service import ServiceService

router = APIRouter()

@router.post("/")
def create_service(payload: dict, db: Session = Depends(get_db)):
    try:
        return ServiceService.create_service(db, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{service_id}")
def get_service(service_id: int, db: Session = Depends(get_db)):
    try:
        return ServiceService.get_service(db, service_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/")
def list_services(
    include_inactive: bool = Query(False),
    db: Session = Depends(get_db)
):
    return ServiceService.list_services(db, include_inactive)

@router.put("/{service_id}")
def update_service(service_id: int, payload: dict, db: Session = Depends(get_db)):
    try:
        return ServiceService.update_service(db, service_id, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{service_id}")
def delete_service(service_id: int, db: Session = Depends(get_db)):
    try:
        ServiceService.delete_service(db, service_id)
        return {"message": "Service deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))