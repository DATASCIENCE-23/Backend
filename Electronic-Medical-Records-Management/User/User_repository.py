from sqlalchemy.orm import Session
from .User_model import User, Role, UserRole, AuditLog
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserRepository:
    @staticmethod
    def create_user(db: Session, username: str, password: str, email: str):
        hashed_password = pwd_context.hash(password)
        new_user = User(username=username, password_hash=hashed_password, email=email)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    @staticmethod
    def get_user_by_id(db: Session, user_id: int):
        return db.query(User).filter(User.user_id == user_id).first()

    @staticmethod
    def get_user_by_username(db: Session, username: str):
        return db.query(User).filter(User.username == username).first()

    @staticmethod
    def list_users(db: Session):
        return db.query(User).all()

    @staticmethod
    def update_user(db: Session, user_id: int, updates: dict):
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user:
            raise ValueError("User not found")
        for key, value in updates.items():
            if key == "password":
                setattr(user, "password_hash", pwd_context.hash(value))
            else:
                setattr(user, key, value)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def delete_user(db: Session, user_id: int):
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user:
            raise ValueError("User not found")
        db.delete(user)
        db.commit()

    @staticmethod
    def log_action(db: Session, user_id: int, action_type: str, ip_address: str):
        log = AuditLog(user_id=user_id, action_type=action_type, ip_address=ip_address)
        db.add(log)
        db.commit()