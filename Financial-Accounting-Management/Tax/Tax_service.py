from sqlalchemy.orm import Session
from Tax.Tax_model import Tax
from Tax.Tax_repository import TaxRepository

class TaxService:

    @staticmethod
    def create_tax(db: Session, data: dict):
        if TaxRepository.get_by_name(db, data["tax_name"]):
            raise ValueError("Tax already exists")

        tax = Tax(**data)
        return TaxRepository.create(db, tax)

    @staticmethod
    def get_tax(db: Session, tax_id: int):
        tax = TaxRepository.get_by_id(db, tax_id)
        if not tax:
            raise ValueError("Tax not found")
        return tax

    @staticmethod
    def list_taxes(db: Session):
        return TaxRepository.get_all(db)

    @staticmethod
    def update_tax(db: Session, tax_id: int, data: dict):
        tax = TaxRepository.get_by_id(db, tax_id)
        if not tax:
            raise ValueError("Tax not found")

        for key, value in data.items():
            setattr(tax, key, value)

        return TaxRepository.update(db, tax)

    @staticmethod
    def delete_tax(db: Session, tax_id: int):
        tax = TaxRepository.get_by_id(db, tax_id)
        if not tax:
            raise ValueError("Tax not found")

        TaxRepository.delete(db, tax)
