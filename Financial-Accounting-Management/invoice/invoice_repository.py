from sqlalchemy.orm import Session
from invoice.invoice_models import Invoice

class InvoiceRepository:

    @staticmethod
    def create(db: Session, invoice: Invoice):
        db.add(invoice)
        db.commit()
        db.refresh(invoice)
        return invoice

    @staticmethod
    def get_by_id(db: Session, invoice_id: int):
        return db.query(Invoice).filter(
            Invoice.invoice_id == invoice_id
        ).first()

    @staticmethod
    def get_all(db: Session):
        return db.query(Invoice).all()

    @staticmethod
    def get_by_patient(db: Session, patient_id: int):
        return db.query(Invoice).filter(
            Invoice.patient_id == patient_id
        ).all()

    @staticmethod
    def update(db: Session, invoice: Invoice, data: dict):
        for key, value in data.items():
            setattr(invoice, key, value)
        db.commit()
        db.refresh(invoice)
        return invoice

    @staticmethod
    def delete(db: Session, invoice: Invoice):
        db.delete(invoice)
        db.commit()
