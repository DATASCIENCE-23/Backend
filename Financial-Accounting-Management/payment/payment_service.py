from datetime import date
from sqlalchemy.orm import Session
from PAYMENT.payment_model import Payment
from PAYMENT.payment_repository import PaymentRepository
from INVOICE.invoice_repository import InvoiceRepository


class PaymentService:

    @staticmethod
    def record_payment(db: Session, payload: dict) -> Payment:
        invoice_id = payload.get("invoice_id")
        amount_paid = payload.get("amount_paid")
        payment_mode = payload.get("payment_mode")
        bank_account_id = payload.get("bank_account_id")

        if not invoice_id or not amount_paid or not payment_mode:
            raise ValueError("invoice_id, amount_paid and payment_mode are required")

        invoice = InvoiceRepository.get_by_id(db, invoice_id)
        if not invoice:
            raise ValueError("Invoice not found")

        total_paid = PaymentRepository.total_paid_for_invoice(db, invoice_id)
        outstanding = invoice.total_amount - total_paid

        if amount_paid > outstanding:
            raise ValueError("Payment exceeds outstanding balance")

        payment = Payment(
            invoice_id=invoice_id,
            payment_date=date.today(),
            amount_paid=amount_paid,
            payment_mode=payment_mode,
            bank_account_id=bank_account_id
        )

        return PaymentRepository.create(db, payment)

    @staticmethod
    def list_payments_for_invoice(db: Session, invoice_id: int):
        return PaymentRepository.list_by_invoice(db, invoice_id)

    @staticmethod
    def calculate_balance(db: Session, invoice_id: int) -> dict:
        invoice = InvoiceRepository.get_by_id(db, invoice_id)
        if not invoice:
            raise ValueError("Invoice not found")

        total_paid = PaymentRepository.total_paid_for_invoice(db, invoice_id)
        balance = invoice.total_amount - total_paid

        return {
            "invoice_id": invoice_id,
            "total_amount": invoice.total_amount,
            "total_paid": total_paid,
            "outstanding_balance": balance
        }

    @staticmethod
    def reconcile_payment(db: Session, invoice_id: int) -> dict:
        balance_info = PaymentService.calculate_balance(db, invoice_id)

        status = (
            "PAID"
            if balance_info["outstanding_balance"] == 0
            else "PARTIALLY_PAID"
        )

        return {
            **balance_info,
            "payment_status": status
        }
