from sqlalchemy.orm import Session
from INVOICE.invoice_model import Invoice


class InvoiceRepository:

    @staticmethod
    def create(db: Session, invoice: Invoice) -> Invoice:
        db.add(invoice)
        db.commit()
        db.refresh(invoice)
        return invoice

    @staticmethod
    def get_by_id(db: Session, invoice_id: int):
        return (
            db.query(Invoice)
            .filter(Invoice.invoice_id == invoice_id)
            .first()
        )

    @staticmethod
    def list_by_patient(db: Session, patient_id: int):
        return (
            db.query(Invoice)
            .filter(Invoice.patient_id == patient_id)
            .all()
        )

    @staticmethod
    def list_by_status(db: Session, status: str):
        return (
            db.query(Invoice)
            .filter(Invoice.status == status)
            .all()
        )

    @staticmethod
    def update_status(db: Session, invoice: Invoice, status: str):
        invoice.status = status
        db.commit()
        db.refresh(invoice)
        return invoice
