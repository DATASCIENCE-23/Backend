from sqlalchemy.orm import Session
from sqlalchemy import func
from INVOICE_LINE.invoice_line_model import InvoiceLine


class InvoiceLineRepository:

    @staticmethod
    def create(db: Session, line: InvoiceLine) -> InvoiceLine:
        db.add(line)
        db.commit()
        db.refresh(line)
        return line

    @staticmethod
    def list_by_invoice(db: Session, invoice_id: int):
        return (
            db.query(InvoiceLine)
            .filter(InvoiceLine.invoice_id == invoice_id)
            .all()
        )

    @staticmethod
    def total_for_invoice(db: Session, invoice_id: int) -> float:
        return (
            db.query(func.coalesce(func.sum(InvoiceLine.line_total), 0))
            .filter(InvoiceLine.invoice_id == invoice_id)
            .scalar()
        )
