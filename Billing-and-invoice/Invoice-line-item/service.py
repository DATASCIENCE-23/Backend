from .repository import InvoiceRepository
from .models import Invoice, InvoiceLineItem
from typing import List

class InvoiceService:
    def __init__(self, repo: InvoiceRepository):
        self.repo = repo

    # ── Invoice operations ────────────────────────────────────────────────────
    def create_invoice(self, invoice: Invoice) -> Invoice:
        return self.repo.create_invoice(invoice)

    def get_invoice(self, invoice_id: int) -> Invoice | None:
        return self.repo.get_invoice_by_id(invoice_id)

    def get_all_invoices(self) -> List[Invoice]:
        return self.repo.get_all_invoices()

    def update_invoice(self, invoice: Invoice) -> Invoice:
        return self.repo.update_invoice(invoice)

    def delete_invoice(self, invoice_id: int) -> Invoice | None:
        return self.repo.delete_invoice(invoice_id)

    # ── Line Item operations ──────────────────────────────────────────────────
    def add_line_item(self, line_item: InvoiceLineItem) -> InvoiceLineItem:
        return self.repo.create_line_item(line_item)

    def get_line_item(self, line_item_id: int) -> InvoiceLineItem | None:
        return self.repo.get_line_item_by_id(line_item_id)

    def get_invoice_line_items(self, invoice_id: int) -> List[InvoiceLineItem]:
        return self.repo.get_line_items_by_invoice(invoice_id)

    def update_line_item(self, line_item: InvoiceLineItem) -> InvoiceLineItem:
        return self.repo.update_line_item(line_item)

    def remove_line_item(self, line_item_id: int) -> InvoiceLineItem | None:
        return self.repo.delete_line_item(line_item_id)
