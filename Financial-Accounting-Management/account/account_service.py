from sqlalchemy.orm import Session
from account.account_models import Account
from account.account_repository import AccountRepository
from account.account_schema import AccountCreate, AccountUpdate

VALID_ACCOUNT_TYPES = ["Asset", "Liability", "Income", "Expense"]

class AccountService:

    @staticmethod
    def create_account(db: Session, data: AccountCreate):
        if data.account_type not in VALID_ACCOUNT_TYPES:
            raise ValueError("Invalid account type")

        account = Account(**data.dict())
        return AccountRepository.create(db, account)

    @staticmethod
    def get_account(db: Session, account_id: int):
        return AccountRepository.get_by_id(db, account_id)

    @staticmethod
    def get_all_accounts(db: Session):
        return AccountRepository.get_all(db)

    @staticmethod
    @staticmethod
    def update_account(db, account_id: int, data: dict):
        account = AccountRepository.get_by_id(db, account_id)
        if not account:
            raise ValueError("Account not found")

        return AccountRepository.update(db, account, data)

    @staticmethod
    def delete_account(db: Session, account_id: int):
        account = AccountRepository.get_by_id(db, account_id)
        if not account:
            raise ValueError("Account not found")

        return AccountRepository.delete(db, account)
