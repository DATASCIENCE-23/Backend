from sqlalchemy.orm import Session
from account.account_models import Account

class AccountRepository:

    @staticmethod
    def create(db: Session, account: Account):
        db.add(account)
        db.commit()
        db.refresh(account)
        return account

    @staticmethod
    def get_by_id(db: Session, account_id: int):
        return db.query(Account).filter(Account.account_id == account_id).first()

    @staticmethod
    def get_all(db: Session):
        return db.query(Account).all()

    @staticmethod
    def update(db: Session, account: Account, data: dict):
        for key, value in data.items():
            setattr(account, key, value)
        db.commit()
        db.refresh(account)
        return account

    @staticmethod
    def delete(db: Session, account: Account):
        db.delete(account)
        db.commit()
