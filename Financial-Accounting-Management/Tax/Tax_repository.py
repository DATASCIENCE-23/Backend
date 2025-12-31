from sqlalchemy.orm import Session
from Tax.Tax_model import Tax

class TaxRepository:

    @staticmethod
    def get_by_id(db: Session, tax_id: int):
        return db.query(Tax).filter(Tax.id == tax_id).first()

    @staticmethod
    def get_by_name(db: Session, tax_name: str):
        return db.query(Tax).filter(Tax.tax_name == tax_name).first()

    @staticmethod
    def get_all(db: Session):
        return db.query(Tax).all()

    @staticmethod
    def create(db: Session, tax: Tax):
        db.add(tax)
        db.commit()
        db.refresh(tax)
        return tax

    @staticmethod
    def update(db: Session, tax: Tax):
        db.commit()
        db.refresh(tax)
        return tax

    @staticmethod
    def delete(db: Session, tax: Tax):
        db.delete(tax)
        db.commit()
