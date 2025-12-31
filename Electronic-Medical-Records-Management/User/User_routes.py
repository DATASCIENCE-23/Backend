from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import Base
from User.User_service import UserService

router = APIRouter()

@router.post("/")
def create_user(payload: dict, db: Session = Depends(get_db)):
    try:
        return UserService.create_user(db, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    try:
        return UserService.get_user(db, user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/")
def list_users(db: Session = Depends(get_db)):
    return UserService.list_users(db)

@router.put("/{user_id}")
def update_user(user_id: int, payload: dict, db: Session = Depends(get_db)):
    try:
        return UserService.update_user(db, user_id, payload)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    try:
        UserService.delete_user(db, user_id)
        return {"message": "User deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))