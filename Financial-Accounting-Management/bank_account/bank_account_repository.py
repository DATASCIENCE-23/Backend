from sqlalchemy.orm import Session
from bank_account.bank_account_models import BankAccount

class BankAccountRepository:

    @staticmethod
    def create(db: Session, bank_account: BankAccount):
        db.add(bank_account)
        db.commit()
        db.refresh(bank_account)
        return bank_account

    @staticmethod
    def get_by_id(db: Session, bank_account_id: int):
        return db.query(BankAccount).filter(
            BankAccount.bank_account_id == bank_account_id
        ).first()

    @staticmethod
    def get_all(db: Session):
        return db.query(BankAccount).all()

    @staticmethod
    def update(db: Session, bank_account: BankAccount, data: dict):
        for key, value in data.items():
            setattr(bank_account, key, value)
        db.commit()
        db.refresh(bank_account)
        return bank_account

    @staticmethod
    def delete(db: Session, bank_account: BankAccount):
        db.delete(bank_account)
        db.commit()
