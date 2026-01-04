from sqlalchemy.orm import Session
from fastapi import Depends
from database import get_db
from .purchase_schema import PurchaseCreate
from .purchase_service import create_purchase

def add_purchase(payload: PurchaseCreate, db: Session = Depends(get_db)):
    return create_purchase(db, payload)
