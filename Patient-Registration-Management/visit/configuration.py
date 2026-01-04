# visit/configuration.py
from sqlalchemy.orm import Session
from .repository import VisitRepository
from .service import VisitService
from .models import Base
from fastapi import Depends
from ..database import get_db  

def get_visit_service(db: Session = Depends(get_db)):
    repo = VisitRepository(db)
    service = VisitService(repo)
    return service
