# user_role/configuration.py

from sqlalchemy.orm import Session
from fastapi import Depends

from .User_Role_repository import UserRoleRepository
from .User_Role_service import UserRoleService
from ..database import get_db


def get_user_role_service(db: Session = Depends(get_db)):
    repo = UserRoleRepository(db)
    service = UserRoleService(repo)
    return service
