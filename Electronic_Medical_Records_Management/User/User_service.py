from sqlalchemy.orm import Session
from .User_repository import UserRepository

class UserService:

    @staticmethod
    def create_user(db: Session, payload: dict):
        return UserRepository.create_user(
            db=db,
            username=payload["username"],
            password=payload["password"],
            email=payload["email"],
            full_name=payload.get("full_name"),
            department_id=payload.get("department_id")
        )

    @staticmethod
    def get_user(db: Session, user_id: int):
        return UserRepository.get_user_by_id(db, user_id)

    @staticmethod
    def list_users(db: Session):
        return UserRepository.list_users(db)

    @staticmethod
    def delete_user(db: Session, user_id: int):
        UserRepository.delete_user(db, user_id)
