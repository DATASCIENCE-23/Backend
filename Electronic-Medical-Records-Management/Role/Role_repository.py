# role/repository.py
from sqlalchemy.orm import Session
from .Role_models import Role

class RoleRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_role(self, role: Role):
        self.db.add(role)
        self.db.commit()
        self.db.refresh(role)
        return role

    def get_role_by_id(self, role_id: int):
        return self.db.query(Role).filter(Role.role_id == role_id).first()

    def get_all_roles(self):
        return self.db.query(Role).all()

    def update_role(self, role_id: int, payload: dict):
        role = self.get_role_by_id(role_id)
        if not role:
            return None

        for key, value in payload.items():
            setattr(role, key, value)

        self.db.commit()
        self.db.refresh(role)
        return role

    def delete_role(self, role_id: int):
        role = self.get_role_by_id(role_id)
        if not role:
            return None

        self.db.delete(role)
        self.db.commit()
        return role
