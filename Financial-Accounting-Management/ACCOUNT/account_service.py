from typing import List, Optional, Dict
from sqlalchemy.orm import Session
from ACCOUNT.account_model import Account
from ACCOUNT.account_repository import AccountRepository


class AccountService:
    @staticmethod
    def get_account(db: Session, account_id: int) -> Optional[Account]:
        account = AccountRepository.get_by_id(db, account_id)
        if not account:
            raise ValueError("Account not found")
        return account

    @staticmethod
    def list_accounts(db: Session) -> List[Account]:
        return AccountRepository.get_all(db)

    @staticmethod
    def list_active_accounts(db: Session) -> List[Account]:
        return AccountRepository.get_active_accounts(db)

    @staticmethod
    def list_accounts_by_type(db: Session, account_type: str) -> List[Account]:
        return AccountRepository.get_by_type(db, account_type)

    @staticmethod
    def list_child_accounts(db: Session, parent_account_id: int) -> List[Account]:
        return AccountRepository.get_children(db, parent_account_id)

    @staticmethod
    def create_account(db: Session, data: dict) -> Account:
        account = Account(**data)
        return AccountRepository.create(db, account)

    @staticmethod
    def update_account(db: Session, account_id: int, data: dict) -> Account:
        account = AccountRepository.get_by_id(db, account_id)
        if not account:
            raise ValueError("Account not found")

        for key, value in data.items():
            if hasattr(account, key):
                setattr(account, key, value)

        return AccountRepository.update(db, account)

    @staticmethod
    def delete_account(db: Session, account_id: int) -> None:
        account = AccountRepository.get_by_id(db, account_id)
        if not account:
            raise ValueError("Account not found")

        AccountRepository.delete(db, account)