# user_role/configuration.py

from sqlalchemy.orm import Session
from fastapi import Depends

from .repository import UserRoleRepository
from .service import UserRoleService
from .models import Base
from ..database import get_db


def get_user_role_service(db: Session = Depends(get_db)):
    repo = UserRoleRepository(db)
    service = UserRoleService(repo)
    return service
