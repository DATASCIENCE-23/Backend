from fastapi import APIRouter, HTTPException, Depends
from .User_Role_service import UserRoleService
from .User_Role_configuration import get_user_role_service

router = APIRouter()

@router.post("/")
def create_user_role(
    payload: dict,
    service: UserRoleService = Depends(get_user_role_service)
):
    return service.create_user_role(payload)

@router.get("/{user_role_id}")
def get_user_role(
    user_role_id: int,
    service: UserRoleService = Depends(get_user_role_service)
):
    user_role = service.get_user_role_by_id(user_role_id)
    if not user_role:
        raise HTTPException(status_code=404, detail="User role not found")
    return user_role

@router.get("/")
def get_all_user_roles(
    service: UserRoleService = Depends(get_user_role_service)
):
    return service.get_all_user_roles()

@router.put("/{user_role_id}")
def update_user_role(
    user_role_id: int,
    payload: dict,
    service: UserRoleService = Depends(get_user_role_service)
):
    return service.update_user_role(user_role_id, payload)

@router.delete("/{user_role_id}")
def delete_user_role(
    user_role_id: int,
    service: UserRoleService = Depends(get_user_role_service)
):
    service.delete_user_role(user_role_id)
    return {"message": "User role deleted"}
