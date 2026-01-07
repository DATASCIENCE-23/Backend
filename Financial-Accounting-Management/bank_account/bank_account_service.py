from sqlalchemy.orm import Session
from bank_account.bank_account_models import BankAccount
from bank_account.bank_account_repository import BankAccountRepository
from bank_account.bank_account_schema import BankAccountCreate

class BankAccountService:

    @staticmethod
    def create_bank_account(db: Session, data: BankAccountCreate):
        bank_account = BankAccount(**data.dict())
        return BankAccountRepository.create(db, bank_account)

    @staticmethod
    def get_bank_account(db: Session, bank_account_id: int):
        return BankAccountRepository.get_by_id(db, bank_account_id)

    @staticmethod
    def get_all_bank_accounts(db: Session):
        return BankAccountRepository.get_all(db)

    @staticmethod
    def update_bank_account(db: Session, bank_account_id: int, data: dict):
        bank_account = BankAccountRepository.get_by_id(db, bank_account_id)
        if not bank_account:
            raise ValueError("Bank account not found")

        return BankAccountRepository.update(db, bank_account, data)

    @staticmethod
    def delete_bank_account(db: Session, bank_account_id: int):
        bank_account = BankAccountRepository.get_by_id(db, bank_account_id)
        if not bank_account:
            raise ValueError("Bank account not found")

        return BankAccountRepository.delete(db, bank_account)
