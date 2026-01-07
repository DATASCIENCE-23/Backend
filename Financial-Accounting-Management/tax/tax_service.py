from sqlalchemy.orm import Session
from tax.tax_models import Tax
from tax.tax_repository import TaxRepository
from tax.tax_schema import TaxCreate

class TaxService:

    @staticmethod
    def create_tax(db: Session, data: TaxCreate):
        if data.tax_rate < 0:
            raise ValueError("Tax rate cannot be negative")

        tax = Tax(**data.dict())
        return TaxRepository.create(db, tax)

    @staticmethod
    def get_tax(db: Session, tax_id: int):
        return TaxRepository.get_by_id(db, tax_id)

    @staticmethod
    def get_all_taxes(db: Session):
        return TaxRepository.get_all(db)

    @staticmethod
    def update_tax(db: Session, tax_id: int, data: dict):
        tax = TaxRepository.get_by_id(db, tax_id)
        if not tax:
            raise ValueError("Tax not found")

        return TaxRepository.update(db, tax, data)

    @staticmethod
    def delete_tax(db: Session, tax_id: int):
        tax = TaxRepository.get_by_id(db, tax_id)
        if not tax:
            raise ValueError("Tax not found")

        return TaxRepository.delete(db, tax)
