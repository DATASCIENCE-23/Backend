# user_role/controller.py

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from .models import UserRole
from .service import UserRoleService
from .configuration import get_user_role_service

router = APIRouter()


@router.post("/", response_model=dict)
def create_user_role(
    user_role: UserRole,
    service: UserRoleService = Depends(get_user_role_service)
):
    return service.create_user_role(user_role)


@router.get("/{user_role_id}", response_model=dict)
def get_user_role(
    user_role_id: int,
    service: UserRoleService = Depends(get_user_role_service)
):
    user_role = service.get_user_role_by_id(user_role_id)
    if not user_role:
        raise HTTPException(status_code=404, detail="User role not found")
    return user_role


@router.get("/", response_model=list)
def get_all_user_roles(
    service: UserRoleService = Depends(get_user_role_service)
):
    return service.get_all_user_roles()


@router.put("/", response_model=dict)
def update_user_role(
    user_role: UserRole,
    service: UserRoleService = Depends(get_user_role_service)
):
    return service.update_user_role(user_role)


@router.delete("/{user_role_id}", response_model=dict)
def delete_user_role(
    user_role_id: int,
    service: UserRoleService = Depends(get_user_role_service)
):
    deleted = service.delete_user_role(user_role_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User role not found")
    return {"message": "User role deleted"}
