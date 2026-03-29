from datetime import date
from sqlalchemy.orm import Session
from INVOICE.invoice_model import Invoice
from INVOICE.invoice_repository import InvoiceRepository
from PATIENT.patient_repository import PatientRepository


class InvoiceService:

    @staticmethod
    def generate_invoice(db: Session, payload: dict) -> Invoice:
        patient_id = payload.get("patient_id")
        total_amount = payload.get("total_amount")
        tax_amount = payload.get("tax_amount", 0)
        discount_amount = payload.get("discount_amount", 0)

        if not patient_id or total_amount is None:
            raise ValueError("patient_id and total_amount are required")

        patient = PatientRepository.get_by_id(db, patient_id)
        if not patient:
            raise ValueError("Patient not found")

        net_amount = total_amount + tax_amount - discount_amount

        invoice = Invoice(
            patient_id=patient_id,
            invoice_date=date.today(),
            total_amount=net_amount,
            tax_amount=tax_amount,
            discount_amount=discount_amount,
            status="UNPAID"
        )

        return InvoiceRepository.create(db, invoice)

    @staticmethod
    def get_invoice(db: Session, invoice_id: int) -> Invoice:
        invoice = InvoiceRepository.get_by_id(db, invoice_id)
        if not invoice:
            raise ValueError("Invoice not found")
        return invoice

    @staticmethod
    def list_invoices_by_patient(db: Session, patient_id: int):
        return InvoiceRepository.list_by_patient(db, patient_id)

    @staticmethod
    def list_invoices_by_status(db: Session, status: str):
        if status not in ["PAID", "UNPAID"]:
            raise ValueError("Status must be PAID or UNPAID")
        return InvoiceRepository.list_by_status(db, status)

    @staticmethod
    def close_invoice(db: Session, invoice_id: int) -> Invoice:
        invoice = InvoiceRepository.get_by_id(db, invoice_id)
        if not invoice:
            raise ValueError("Invoice not found")

        if invoice.status == "PAID":
            raise ValueError("Invoice already closed")

        return InvoiceRepository.update_status(db, invoice, "PAID")
