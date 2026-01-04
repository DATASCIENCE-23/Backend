from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from .User_model import User
from .User_service import UserService
from database import get_db  # Shared database dependency

router = APIRouter()

@router.post("/", response_model=dict)
def create_user(user: User, service: UserService = Depends(get_user_service)):
    return service.create_user(user)


@router.get("/{user_id}", response_model=dict)
def get_user(user_id: int, service: UserService = Depends(get_user_service)):
    user = service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/", response_model=list)
def get_all_users(service: UserService = Depends(get_user_service)):
    return service.get_all_users()


@router.put("/", response_model=dict)
def update_user(user: User, service: UserService = Depends(get_user_service)):
    return service.update_user(user)


@router.delete("/{user_id}", response_model=dict)
def delete_user(user_id: int, service: UserService = Depends(get_user_service)):
    deleted = service.delete_user(user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}