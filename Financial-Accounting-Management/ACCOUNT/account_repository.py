from sqlalchemy.orm import Session
from typing import List, Optional
from ACCOUNT.account_model import Account  # Adjust import path if needed


class AccountRepository:
    @staticmethod
    def get_by_id(db: Session, account_id: int) -> Optional[Account]:
        return db.query(Account).filter(Account.account_id == account_id).first()

    @staticmethod
    def get_all(db: Session) -> List[Account]:
        return db.query(Account).all()

    @staticmethod
    def get_active_accounts(db: Session) -> List[Account]:
        return db.query(Account).filter(Account.is_active == True).all()

    @staticmethod
    def get_by_type(db: Session, account_type: str) -> List[Account]:
        return db.query(Account).filter(Account.account_type == account_type).all()

    @staticmethod
    def get_children(db: Session, parent_account_id: int) -> List[Account]:
        return db.query(Account).filter(Account.parent_account_id == parent_account_id).all()

    @staticmethod
    def create(db: Session, account: Account) -> Account:
        db.add(account)
        db.commit()
        db.refresh(account)
        return account

    @staticmethod
    def update(db: Session, account: Account) -> Account:
        db.commit()
        db.refresh(account)
        return account

    @staticmethod
    def delete(db: Session, account: Account) -> None:
        db.delete(account)
        db.commit()