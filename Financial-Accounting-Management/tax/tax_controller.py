from sqlalchemy.orm import Session
from tax.tax_service import TaxService
from tax.tax_schema import TaxCreate

class TaxController:

    @staticmethod
    def create(db: Session, data: TaxCreate):
        return TaxService.create_tax(db, data)

    @staticmethod
    def get(db: Session, tax_id: int):
        return TaxService.get_tax(db, tax_id)

    @staticmethod
    def get_all(db: Session):
        return TaxService.get_all_taxes(db)

    @staticmethod
    def update(db: Session, tax_id: int, data: dict):
        return TaxService.update_tax(db, tax_id, data)

    @staticmethod
    def delete(db: Session, tax_id: int):
        return TaxService.delete_tax(db, tax_id)
