# role/service.py
from .Role_repository import RoleRepository
from .Role_models import Role

class RoleService:
    def __init__(self, repo: RoleRepository):
        self.repo = repo

    def create_role(self, role: Role):
        return self.repo.create_role(role)

    def get_role_by_id(self, role_id: int):
        return self.repo.get_role_by_id(role_id)

    def get_all_roles(self):
        return self.repo.get_all_roles()

    def update_role(self, role: Role):
        return self.repo.update_role(role)

    def delete_role(self, role_id: int):
        return self.repo.delete_role(role_id)