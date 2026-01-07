from sqlalchemy.orm import Session
from invoice.invoice_models import Invoice
from invoice.invoice_repository import InvoiceRepository
from invoice.invoice_schema import InvoiceCreate

from journal_entry.journal_entry_models import JournalEntry
from journal_line.journal_line_models import JournalLine
from journal_entry.journal_entry_repository import JournalEntryRepository
from journal_line.journal_line_repository import JournalLineRepository

from datetime import date

class InvoiceService:

    @staticmethod
    def create_invoice(db: Session, data: InvoiceCreate):
        if data.total_amount <= 0:
            raise ValueError("Invoice total must be positive")

        # 1️⃣ Create invoice
        invoice = Invoice(**data.dict())
        invoice = InvoiceRepository.create(db, invoice)

        # 2️⃣ Create journal entry
        journal = JournalEntry(
            journal_date=date.today(),
            reference_type="INVOICE",
            reference_id=invoice.invoice_id,
            description="Invoice generated"
        )
        journal = JournalEntryRepository.create(db, journal)

        # 3️⃣ Journal lines (simplified)
        # Dr Accounts Receivable (example account_id = 1)
        dr = JournalLine(
            journal_id=journal.journal_id,
            account_id=1,
            debit_amount=invoice.total_amount,
            credit_amount=0
        )

        # Cr Revenue (example account_id = 2)
        cr = JournalLine(
            journal_id=journal.journal_id,
            account_id=2,
            debit_amount=0,
            credit_amount=invoice.total_amount
        )

        JournalLineRepository.create(db, dr)
        JournalLineRepository.create(db, cr)

        return invoice

    @staticmethod
    def get_invoice(db: Session, invoice_id: int):
        return InvoiceRepository.get_by_id(db, invoice_id)

    @staticmethod
    def get_all_invoices(db: Session):
        return InvoiceRepository.get_all(db)

    @staticmethod
    def get_invoices_by_patient(db: Session, patient_id: int):
        return InvoiceRepository.get_by_patient(db, patient_id)

    @staticmethod
    def update_invoice(db: Session, invoice_id: int, data: dict):
        invoice = InvoiceRepository.get_by_id(db, invoice_id)
        if not invoice:
            raise ValueError("Invoice not found")

        return InvoiceRepository.update(db, invoice, data)

    @staticmethod
    def delete_invoice(db: Session, invoice_id: int):
        invoice = InvoiceRepository.get_by_id(db, invoice_id)
        if not invoice:
            raise ValueError("Invoice not found")

        # NOTE: In real systems, deletion is usually blocked
        return InvoiceRepository.delete(db, invoice)
