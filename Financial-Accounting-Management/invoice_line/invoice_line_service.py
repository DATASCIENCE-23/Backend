from sqlalchemy.orm import Session
from invoice_line.invoice_line_models import InvoiceLine
from invoice_line.invoice_line_repository import InvoiceLineRepository
from invoice_line.invoice_line_schema import InvoiceLineCreate

class InvoiceLineService:

    @staticmethod
    def create_invoice_line(db: Session, data: InvoiceLineCreate):
        if data.quantity <= 0 or data.unit_price <= 0:
            raise ValueError("Quantity and price must be positive")

        invoice_line = InvoiceLine(**data.dict())
        return InvoiceLineRepository.create(db, invoice_line)

    @staticmethod
    def get_invoice_line(db: Session, invoice_line_id: int):
        return InvoiceLineRepository.get_by_id(db, invoice_line_id)

    @staticmethod
    def get_invoice_lines_by_invoice(db: Session, invoice_id: int):
        return InvoiceLineRepository.get_by_invoice(db, invoice_id)

    @staticmethod
    def update_invoice_line(db: Session, invoice_line_id: int, data: dict):
        invoice_line = InvoiceLineRepository.get_by_id(db, invoice_line_id)
        if not invoice_line:
            raise ValueError("Invoice line not found")

        return InvoiceLineRepository.update(db, invoice_line, data)

    @staticmethod
    def delete_invoice_line(db: Session, invoice_line_id: int):
        invoice_line = InvoiceLineRepository.get_by_id(db, invoice_line_id)
        if not invoice_line:
            raise ValueError("Invoice line not found")

        return InvoiceLineRepository.delete(db, invoice_line)
