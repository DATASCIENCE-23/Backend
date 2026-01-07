from sqlalchemy.orm import Session
from invoice.invoice_service import InvoiceService
from invoice.invoice_schema import InvoiceCreate

class InvoiceController:

    @staticmethod
    def create(db: Session, data: InvoiceCreate):
        return InvoiceService.create_invoice(db, data)

    @staticmethod
    def get(db: Session, invoice_id: int):
        return InvoiceService.get_invoice(db, invoice_id)

    @staticmethod
    def get_all(db: Session):
        return InvoiceService.get_all_invoices(db)

    @staticmethod
    def get_by_patient(db: Session, patient_id: int):
        return InvoiceService.get_invoices_by_patient(db, patient_id)

    @staticmethod
    def update(db: Session, invoice_id: int, data: dict):
        return InvoiceService.update_invoice(db, invoice_id, data)

    @staticmethod
    def delete(db: Session, invoice_id: int):
        return InvoiceService.delete_invoice(db, invoice_id)
