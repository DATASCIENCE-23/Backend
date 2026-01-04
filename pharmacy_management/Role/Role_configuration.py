# role/configuration.py
from sqlalchemy.orm import Session
from .Role_repository import RoleRepository
from .Role_service import RoleService
from fastapi import Depends
from ..database import get_db

def get_role_service(db: Session = Depends(get_db)):
    repo = RoleRepository(db)
    service = RoleService(repo)
    return service