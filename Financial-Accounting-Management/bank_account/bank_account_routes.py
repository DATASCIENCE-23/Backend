from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from bank_account.bank_account_schema import BankAccountCreate, BankAccountResponse
from bank_account.bank_account_service import BankAccountService

router = APIRouter(prefix="/bank-accounts", tags=["Bank Account"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=BankAccountResponse)
def create_bank_account(data: BankAccountCreate, db: Session = Depends(get_db)):
    return BankAccountService.create_bank_account(db, data)

@router.get("/{bank_account_id}", response_model=BankAccountResponse)
def get_bank_account(bank_account_id: int, db: Session = Depends(get_db)):
    return BankAccountService.get_bank_account(db, bank_account_id)

@router.get("/", response_model=list[BankAccountResponse])
def get_all_bank_accounts(db: Session = Depends(get_db)):
    return BankAccountService.get_all_bank_accounts(db)

@router.put("/{bank_account_id}", response_model=BankAccountResponse)
def update_bank_account(bank_account_id: int, data: dict, db: Session = Depends(get_db)):
    return BankAccountService.update_bank_account(db, bank_account_id, data)

@router.delete("/{bank_account_id}")
def delete_bank_account(bank_account_id: int, db: Session = Depends(get_db)):
    BankAccountService.delete_bank_account(db, bank_account_id)
    return {"message": "Bank account deleted successfully"}
