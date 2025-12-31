from sqlalchemy.orm import Session
from .User_repository import UserRepository

class UserService:
    @staticmethod
    def create_user(db: Session, payload: dict):
        username = payload.get("username")
        password = payload.get("password")
        email = payload.get("email")
        if not all([username, password, email]):
            raise ValueError("Missing required fields")
        if UserRepository.get_user_by_username(db, username):
            raise ValueError("Username already exists")
        return UserRepository.create_user(db, username, password, email)

    @staticmethod
    def get_user(db: Session, user_id: int):
        user = UserRepository.get_user_by_id(db, user_id)
        if not user:
            raise ValueError("User not found")
        return user

    @staticmethod
    def list_users(db: Session):
        return UserRepository.list_users(db)

    @staticmethod
    def update_user(db: Session, user_id: int, payload: dict):
        return UserRepository.update_user(db, user_id, payload)

    @staticmethod
    def delete_user(db: Session, user_id: int):
        UserRepository.delete_user(db, user_id)

    @staticmethod
    def log_action(db: Session, user_id: int, action_type: str, ip_address: str = "unknown"):
        UserRepository.log_action(db, user_id, action_type, ip_address)