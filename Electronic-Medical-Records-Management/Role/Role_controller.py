# role/controller.py
from fastapi import APIRouter, HTTPException, Depends
from .Role_models import Role
from .Role_service import RoleService
from .Role_configuration import get_role_service

router = APIRouter()

@router.post("/", response_model=dict)
def create_role(role: Role, service: RoleService = Depends(get_role_service)):
    return service.create_role(role)

@router.get("/{role_id}", response_model=dict)
def get_role(role_id: int, service: RoleService = Depends(get_role_service)):
    role = service.get_role_by_id(role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role

@router.get("/", response_model=list)
def get_all_roles(service: RoleService = Depends(get_role_service)):
    return service.get_all_roles()

@router.put("/", response_model=dict)
def update_role(role: Role, service: RoleService = Depends(get_role_service)):
    return service.update_role(role)

@router.delete("/{role_id}", response_model=dict)
def delete_role(role_id: int, service: RoleService = Depends(get_role_service)):
    deleted = service.delete_role(role_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Role not found")
    return {"message": "Role deleted"}