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
        # 🔎 Check username
        if db.query(User).filter(User.username == username).first():
            raise HTTPException(
                status_code=400,
                detail="Username already exists"
            )

        # 🔎 Check email
        if db.query(User).filter(User.email == email).first():
            raise HTTPException(
                status_code=400,
                detail="Email already exists"
            )

        user = User(
            username=username,
            password_hash=password,   # storing as-is (your request)
            email=email,
            full_name=full_name,
            department_id=department_id,
            status="ACTIVE"
        )

        db.add(user)
        db.commit()
        db.refresh(user)
        return user
