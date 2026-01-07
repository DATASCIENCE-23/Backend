from sqlalchemy.orm import Session
from datetime import date

from payment.payment_models import Payment
from payment.payment_repository import PaymentRepository
from payment.payment_schema import PaymentCreate

from journal_entry.journal_entry_models import JournalEntry
from journal_line.journal_line_models import JournalLine
from journal_entry.journal_entry_repository import JournalEntryRepository
from journal_line.journal_line_repository import JournalLineRepository


class PaymentService:

    @staticmethod
    def create_payment(db: Session, data: PaymentCreate):
        """
        Creates a payment and automatically posts accounting journal entries.

        Accounting logic:
        - Dr Cash / Bank
        - Cr Accounts Receivable
        """

        # -----------------------
        # 1️⃣ Validations
        # -----------------------
        if data.amount_paid <= 0:
            raise ValueError("Payment amount must be positive")

        # -----------------------
        # 2️⃣ Create Payment record
        # -----------------------
        payment = Payment(
            invoice_id=data.invoice_id,
            payment_date=data.payment_date,
            amount_paid=data.amount_paid,
            payment_mode=data.payment_mode,
            bank_account_id=data.bank_account_id
        )

        payment = PaymentRepository.create(db, payment)

        # -----------------------
        # 3️⃣ Create Journal Entry
        # -----------------------
        journal = JournalEntry(
            journal_date=date.today(),
            reference_type="PAYMENT",
            reference_id=payment.payment_id,
            description="Payment received from patient"
        )

        journal = JournalEntryRepository.create(db, journal)

        # -----------------------
        # 4️⃣ Determine Debit Account
        # -----------------------
        # If bank_account_id exists → Bank
        # Else → Cash
        #
        # NOTE:
        # - bank_account_id links to BANK_ACCOUNT table
        # - BANK_ACCOUNT.account_id links to ACCOUNT table
        #
        # For simplicity in service layer, we assume:
        #   - Cash account_id = 1
        #
        # (In real systems, this comes from configuration)

        if payment.bank_account_id:
            debit_account_id = payment.bank_account_id
        else:
            debit_account_id = 1  # Cash Account (example)

        # -----------------------
        # 5️⃣ Journal Lines
        # -----------------------

        # Dr Cash / Bank
        debit_line = JournalLine(
            journal_id=journal.journal_id,
            account_id=debit_account_id,
            debit_amount=payment.amount_paid,
            credit_amount=0
        )

        # Cr Accounts Receivable
        credit_line = JournalLine(
            journal_id=journal.journal_id,
            account_id=3,  # Accounts Receivable (example)
            debit_amount=0,
            credit_amount=payment.amount_paid
        )

        JournalLineRepository.create(db, debit_line)
        JournalLineRepository.create(db, credit_line)

        return payment

    # -------------------------------------------------
    # READ OPERATIONS
    # -------------------------------------------------

    @staticmethod
    def get_payment(db: Session, payment_id: int):
        return PaymentRepository.get_by_id(db, payment_id)

    @staticmethod
    def get_payments_by_invoice(db: Session, invoice_id: int):
        return PaymentRepository.get_by_invoice(db, invoice_id)

    # -------------------------------------------------
    # UPDATE / DELETE
    # -------------------------------------------------

    @staticmethod
    def update_payment(db: Session, payment_id: int, data: dict):
        payment = PaymentRepository.get_by_id(db, payment_id)
        if not payment:
            raise ValueError("Payment not found")

        # ⚠️ In real accounting systems, updates are often restricted
        return PaymentRepository.update(db, payment, data)

    @staticmethod
    def delete_payment(db: Session, payment_id: int):
        payment = PaymentRepository.get_by_id(db, payment_id)
        if not payment:
            raise ValueError("Payment not found")

        # ⚠️ Usually blocked after posting
        return PaymentRepository.delete(db, payment)
