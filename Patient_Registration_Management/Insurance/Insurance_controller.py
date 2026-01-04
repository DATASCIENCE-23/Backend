from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from Insurance_service import InsuranceService

router = APIRouter()

@router.post("/")
def create_insurance(payload: dict, db: Session = Depends(get_db)):
    try:
        return InsuranceService.create_insurance(db, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{insurance_id}")
def get_insurance(insurance_id: int, db: Session = Depends(get_db)):
    try:
        return InsuranceService.get_insurance(db, insurance_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/")
def list_insurances(db: Session = Depends(get_db)):
    return InsuranceService.list_insurances(db)


@router.put("/{insurance_id}")
def update_insurance(insurance_id: int, payload: dict, db: Session = Depends(get_db)):
    try:
        return InsuranceService.update_insurance(db, insurance_id, payload)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{insurance_id}")
def delete_insurance(insurance_id: int, db: Session = Depends(get_db)):
    try:
        InsuranceService.delete_insurance(db, insurance_id)
        return {"message": "Insurance deleted"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
