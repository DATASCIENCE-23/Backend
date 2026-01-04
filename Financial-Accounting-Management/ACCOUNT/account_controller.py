from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from ACCOUNT.account_service import AccountService

router = APIRouter(prefix="/accounts", tags=["Accounts"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_account(payload: dict, db: Session = Depends(get_db)):
    try:
        return AccountService.create_account(db, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{account_id}")
def get_account(account_id: int, db: Session = Depends(get_db)):
    try:
        return AccountService.get_account(db, account_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/")
def list_accounts(db: Session = Depends(get_db)):
    return AccountService.list_accounts(db)


@router.get("/active")
def list_active_accounts(db: Session = Depends(get_db)):
    return AccountService.list_active_accounts(db)


@router.get("/type/{account_type}")
def list_accounts_by_type(account_type: str, db: Session = Depends(get_db)):
    return AccountService.list_accounts_by_type(db, account_type)


@router.get("/children/{parent_account_id}")
def list_child_accounts(parent_account_id: int, db: Session = Depends(get_db)):
    return AccountService.list_child_accounts(db, parent_account_id)


@router.put("/{account_id}")
def update_account(account_id: int, payload: dict, db: Session = Depends(get_db)):
    try:
        return AccountService.update_account(db, account_id, payload)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_account(account_id: int, db: Session = Depends(get_db)):
    try:
        AccountService.delete_account(db, account_id)
        return None
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))