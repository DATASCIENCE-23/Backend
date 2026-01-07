from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from account.account_schema import AccountCreate, AccountUpdate, AccountResponse
from account.account_service import AccountService

router = APIRouter(prefix="/accounts", tags=["Account"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=AccountResponse)
def create_account(data: AccountCreate, db: Session = Depends(get_db)):
    return AccountService.create_account(db, data)

@router.get("/{account_id}", response_model=AccountResponse)
def get_account(account_id: int, db: Session = Depends(get_db)):
    return AccountService.get_account(db, account_id)

@router.get("/", response_model=list[AccountResponse])
def get_all_accounts(db: Session = Depends(get_db)):
    return AccountService.get_all_accounts(db)

@router.put("/{account_id}", response_model=AccountResponse)
def update_account(account_id: int, data: AccountUpdate, db: Session = Depends(get_db)):
    return AccountService.update_account(db, account_id, data)

@router.delete("/{account_id}")
def delete_account(account_id: int, db: Session = Depends(get_db)):
    AccountService.delete_account(db, account_id)
    return {"message": "Account deleted successfully"}
