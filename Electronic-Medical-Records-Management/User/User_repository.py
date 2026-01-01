from sqlalchemy.orm import Session
from fastapi import HTTPException
from .User_model import User

class UserRepository:

    @staticmethod
    def create_user(
        db: Session,
        username: str,
        password: str,
        email: str,
        full_name: str = None,
        department_id: int = None
    ):
        # check username
        if db.query(User).filter(User.username == username).first():
            raise HTTPException(status_code=400, detail="Username already exists")

        # check email
        if db.query(User).filter(User.email == email).first():
            raise HTTPException(status_code=400, detail="Email already exists")

        user = User(
            username=username,
            password_hash=password,   # plain (as you requested)
            email=email,
            full_name=full_name,
            department_id=department_id,
            status="ACTIVE"
        )

        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def get_user_by_id(db: Session, user_id: int):
        return db.query(User).filter(User.user_id == user_id).first()

    @staticmethod
    def list_users(db: Session):   # ✅ THIS WAS MISSING
        return db.query(User).all()

    @staticmethod
    def delete_user(db: Session, user_id: int):
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        db.delete(user)
        db.commit()
