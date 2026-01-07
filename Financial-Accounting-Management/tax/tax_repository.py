from sqlalchemy.orm import Session
from tax.tax_models import Tax

class TaxRepository:

    @staticmethod
    def create(db: Session, tax: Tax):
        db.add(tax)
        db.commit()
        db.refresh(tax)
        return tax

    @staticmethod
    def get_by_id(db: Session, tax_id: int):
        return db.query(Tax).filter(Tax.tax_id == tax_id).first()

    @staticmethod
    def get_all(db: Session):
        return db.query(Tax).all()

    @staticmethod
    def update(db: Session, tax: Tax, data: dict):
        for key, value in data.items():
            setattr(tax, key, value)
        db.commit()
        db.refresh(tax)
        return tax

    @staticmethod
    def delete(db: Session, tax: Tax):
        db.delete(tax)
        db.commit()
