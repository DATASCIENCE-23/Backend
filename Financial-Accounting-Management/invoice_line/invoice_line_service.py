from sqlalchemy.orm import Session
from INVOICE_LINE.invoice_line_model import InvoiceLine
from INVOICE_LINE.invoice_line_repository import InvoiceLineRepository
from INVOICE.invoice_repository import InvoiceRepository
from ACCOUNT.account_repository import AccountRepository


class InvoiceLineService:

    @staticmethod
    def add_invoice_line(db: Session, payload: dict) -> InvoiceLine:
        invoice_id = payload.get("invoice_id")
        service_name = payload.get("service_name")
        account_id = payload.get("account_id")
        quantity = payload.get("quantity")
        unit_price = payload.get("unit_price")

        if not all([invoice_id, service_name, account_id, quantity, unit_price]):
            raise ValueError("All invoice line fields are required")

        if quantity <= 0 or unit_price <= 0:
            raise ValueError("Quantity and unit price must be greater than zero")

        invoice = InvoiceRepository.get_by_id(db, invoice_id)
        if not invoice:
            raise ValueError("Invoice not found")

        account = AccountRepository.get_by_id(db, account_id)
        if not account or account.account_type != "REVENUE":
            raise ValueError("Invalid revenue account")

        # 💰 Price calculation
        line_total = quantity * unit_price

        line = InvoiceLine(
            invoice_id=invoice_id,
            service_name=service_name,
            account_id=account_id,
            quantity=quantity,
            unit_price=unit_price,
            line_total=line_total
        )

        created_line = InvoiceLineRepository.create(db, line)

        # 🔁 Update invoice total
        new_total = InvoiceLineRepository.total_for_invoice(db, invoice_id)
        invoice.total_amount = new_total
        db.commit()

        return created_line

    @staticmethod
    def list_invoice_lines(db: Session, invoice_id: int):
        return InvoiceLineRepository.list_by_invoice(db, invoice_id)
