from sqlalchemy.orm import Session
from invoice_line.invoice_line_models import InvoiceLine

class InvoiceLineRepository:

    @staticmethod
    def create(db: Session, invoice_line: InvoiceLine):
        db.add(invoice_line)
        db.commit()
        db.refresh(invoice_line)
        return invoice_line

    @staticmethod
    def get_by_id(db: Session, invoice_line_id: int):
        return db.query(InvoiceLine).filter(
            InvoiceLine.invoice_line_id == invoice_line_id
        ).first()

    @staticmethod
    def get_by_invoice(db: Session, invoice_id: int):
        return db.query(InvoiceLine).filter(
            InvoiceLine.invoice_id == invoice_id
        ).all()

    @staticmethod
    def update(db: Session, invoice_line: InvoiceLine, data: dict):
        for key, value in data.items():
            setattr(invoice_line, key, value)
        db.commit()
        db.refresh(invoice_line)
        return invoice_line

    @staticmethod
    def delete(db: Session, invoice_line: InvoiceLine):
        db.delete(invoice_line)
        db.commit()
