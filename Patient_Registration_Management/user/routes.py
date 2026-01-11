from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .service import UserService
from .repository import UserRepository
from .schemas import UserCreate, UserUpdate, UserResponse
from Patient_Registration_Management.database import get_db

# ❌ REMOVE prefix="/users" from here
router = APIRouter(tags=["Users"])


def get_service(db: Session = Depends(get_db)):
    return UserService(UserRepository(db))


@router.post("/", response_model=UserResponse)
def create_user(
    data: UserCreate,
    service: UserService = Depends(get_service)
):
    return service.create_user(data)


@router.get("/", response_model=list[UserResponse])
def get_all_users(service: UserService = Depends(get_service)):
    return service.get_all_users()


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, service: UserService = Depends(get_service)):
    user = service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    data: UserUpdate,
    service: UserService = Depends(get_service)
):
    user = service.update_user(user_id, data)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/{user_id}")
def delete_user(user_id: int, service: UserService = Depends(get_service)):
    user = service.delete_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}
