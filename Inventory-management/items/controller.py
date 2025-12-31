# items/controller.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from Patient.database import get_db
from .service import MasterService
from .schemas import *

router = APIRouter()

# Category endpoints
@router.post("/categories/", response_model=CategoryRead)
def create_category(payload: CategoryCreate, db: Session = Depends(get_db)):
    return MasterService.create_category(db, payload)

@router.get("/categories/{id}", response_model=CategoryRead)
def get_category(id: int, db: Session = Depends(get_db)):
    return MasterService.get_category(db, id)

@router.get("/categories/", response_model=list[CategoryRead])
def list_categories(db: Session = Depends(get_db)):
    return MasterService.list_categories(db)

@router.put("/categories/{id}", response_model=CategoryRead)
def update_category(id: int, payload: CategoryUpdate, db: Session = Depends(get_db)):
    return MasterService.update_category(db, id, payload)

@router.delete("/categories/{id}")
def delete_category(id: int, db: Session = Depends(get_db)):
    MasterService.delete_category(db, id)
    return {"message": "Category deleted"}

# Repeat similar endpoints for /suppliers/ and /locations/ (change schemas/service calls)

# Item endpoints
@router.post("/items/", response_model=ItemRead)
def create_item(payload: ItemCreate, db: Session = Depends(get_db)):
    return MasterService.create_item(db, payload)

@router.get("/items/{id}", response_model=ItemRead)
def get_item(id: int, db: Session = Depends(get_db)):
    return MasterService.get_item(db, id)

@router.get("/items/", response_model=list[ItemRead])
def list_items(db: Session = Depends(get_db),
               category_id: Optional[int] = Query(None),
               status: Optional[str] = Query(None)):
    return MasterService.list_items(db, category_id=category_id, status=status)

@router.put("/items/{id}", response_model=ItemRead)
def update_item(id: int, payload: ItemUpdate, db: Session = Depends(get_db)):
    return MasterService.update_item(db, id, payload)

@router.delete("/items/{id}")
def delete_item(id: int, db: Session = Depends(get_db)):
    MasterService.delete_item(db, id)
    return {"message": "Item deleted"}