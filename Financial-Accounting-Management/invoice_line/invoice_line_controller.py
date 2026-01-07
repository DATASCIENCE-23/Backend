from sqlalchemy.orm import Session
from invoice_line.invoice_line_service import InvoiceLineService
from invoice_line.invoice_line_schema import InvoiceLineCreate

class InvoiceLineController:

    @staticmethod
    def create(db: Session, data: InvoiceLineCreate):
        return InvoiceLineService.create_invoice_line(db, data)

    @staticmethod
    def get(db: Session, invoice_line_id: int):
        return InvoiceLineService.get_invoice_line(db, invoice_line_id)

    @staticmethod
    def get_by_invoice(db: Session, invoice_id: int):
        return InvoiceLineService.get_invoice_lines_by_invoice(db, invoice_id)

    @staticmethod
    def update(db: Session, invoice_line_id: int, data: dict):
        return InvoiceLineService.update_invoice_line(db, invoice_line_id, data)

    @staticmethod
    def delete(db: Session, invoice_line_id: int):
        return InvoiceLineService.delete_invoice_line(db, invoice_line_id)
