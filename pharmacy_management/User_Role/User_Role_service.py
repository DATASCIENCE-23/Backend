from .User_Role_repository import UserRoleRepository
from .User_Role_models import UserRole

class UserRoleService:
    def __init__(self, repo: UserRoleRepository):
        self.repo = repo

    def create_user_role(self, payload: dict):
        user_role = UserRole(**payload)
        return self.repo.create_user_role(user_role)

    def get_user_role_by_id(self, user_role_id: int):
        return self.repo.get_user_role_by_id(user_role_id)

    def get_all_user_roles(self):
        return self.repo.get_all_user_roles()

    def update_user_role(self, user_role_id: int, payload: dict):
        return self.repo.update_user_role(user_role_id, payload)

    def delete_user_role(self, user_role_id: int):
        return self.repo.delete_user_role(user_role_id)
