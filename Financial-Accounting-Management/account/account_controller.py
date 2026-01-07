from sqlalchemy.orm import Session
from account.account_service import AccountService
from account.account_schema import AccountCreate, AccountUpdate

class AccountController:

    @staticmethod
    def create(db: Session, data: AccountCreate):
        return AccountService.create_account(db, data)

    @staticmethod
    def get(db: Session, account_id: int):
        return AccountService.get_account(db, account_id)

    @staticmethod
    def get_all(db: Session):
        return AccountService.get_all_accounts(db)

    @staticmethod
    def update(db: Session, account_id: int, data: dict):
        return AccountService.update_account(db, account_id, data)

    @staticmethod
    def delete(db: Session, account_id: int):
        return AccountService.delete_account(db, account_id)
