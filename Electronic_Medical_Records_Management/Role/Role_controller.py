from fastapi import APIRouter, HTTPException, Depends
from .Role_service import RoleService
from .Role_configuration import get_role_service

router = APIRouter()

@router.post("/")
def create_role(payload: dict, service: RoleService = Depends(get_role_service)):
    return service.create_role(payload)

@router.get("/{role_id}")
def get_role(role_id: int, service: RoleService = Depends(get_role_service)):
    role = service.get_role_by_id(role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role

@router.get("/")
def get_all_roles(service: RoleService = Depends(get_role_service)):
    return service.get_all_roles()

@router.put("/{role_id}")
def update_role(role_id: int, payload: dict, service: RoleService = Depends(get_role_service)):
    return service.update_role(role_id, payload)

@router.delete("/{role_id}")
def delete_role(role_id: int, service: RoleService = Depends(get_role_service)):
    deleted = service.delete_role(role_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Role not found")

    return {"message": "Role deleted"}