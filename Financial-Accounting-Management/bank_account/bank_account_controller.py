from sqlalchemy.orm import Session
from bank_account.bank_account_service import BankAccountService
from bank_account.bank_account_schema import BankAccountCreate

class BankAccountController:

    @staticmethod
    def create(db: Session, data: BankAccountCreate):
        return BankAccountService.create_bank_account(db, data)

    @staticmethod
    def get(db: Session, bank_account_id: int):
        return BankAccountService.get_bank_account(db, bank_account_id)

    @staticmethod
    def get_all(db: Session):
        return BankAccountService.get_all_bank_accounts(db)

    @staticmethod
    def update(db: Session, bank_account_id: int, data: dict):
        return BankAccountService.update_bank_account(db, bank_account_id, data)

    @staticmethod
    def delete(db: Session, bank_account_id: int):
        return BankAccountService.delete_bank_account(db, bank_account_id)
