# user_role/repository.py

from sqlalchemy.orm import Session
from .models import UserRole


class UserRoleRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_user_role(self, user_role: UserRole):
        self.db.add(user_role)
        self.db.commit()
        self.db.refresh(user_role)
        return user_role

    def get_user_role_by_id(self, user_role_id: int):
        return (
            self.db.query(UserRole)
            .filter(UserRole.user_role_id == user_role_id)
            .first()
        )

    def get_all_user_roles(self):
        return self.db.query(UserRole).all()

    def update_user_role(self, user_role: UserRole):
        self.db.merge(user_role)
        self.db.commit()
        return user_role

    def delete_user_role(self, user_role_id: int):
        user_role = self.get_user_role_by_id(user_role_id)
        if user_role:
            self.db.delete(user_role)
            self.db.commit()
        return user_role
