from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .User_schema import UserCreate, UserResponse
from .User_service import UserService

router = APIRouter()

@router.post("/", response_model=UserResponse)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    return UserService.create_user(db, payload.dict())


@router.get("/", response_model=list[UserResponse])
def list_users(db: Session = Depends(get_db)):
    return UserService.list_users(db)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = UserService.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    UserService.delete_user(db, user_id)
    return {"message": "User deleted successfully"}
