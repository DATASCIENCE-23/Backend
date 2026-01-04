# role/Role_service.py
from fastapi import HTTPException
from .Role_repository import RoleRepository
from .Role_models import Role, RoleName


class RoleService:
    def __init__(self, repo: RoleRepository):
        self.repo = repo

    def create_role(self, payload: dict):
        try:
            payload["role_name"] = RoleName(payload["role_name"].lower())
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail="Invalid role name"
            )

        role = Role(**payload)
        created = self.repo.create_role(role)

        if not created:
            raise HTTPException(
                status_code=400,
                detail=f"Role '{payload['role_name'].value}' already exists"
            )

        return created

    def get_role_by_id(self, role_id: int):
        role = self.repo.get_role_by_id(role_id)
        if not role:
            raise HTTPException(status_code=404, detail="Role not found")
        return role

    def get_all_roles(self):
        return self.repo.get_all_roles()

    def update_role(self, role_id: int, payload: dict):
        if "role_name" in payload:
            try:
                payload["role_name"] = RoleName(payload["role_name"].lower())
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail="Invalid role name"
                )

        updated = self.repo.update_role(role_id, payload)
        if not updated:
            raise HTTPException(
                status_code=404,
                detail="Role not found or duplicate role name"
            )

        return updated

    def delete_role(self, role_id: int):
        deleted = self.repo.delete_role(role_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Role not found")
        return deleted
