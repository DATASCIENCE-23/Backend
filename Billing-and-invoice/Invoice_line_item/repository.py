from sqlalchemy.orm import Session
from .model import Invoice, InvoiceLineItem

class InvoiceRepository:
    def __init__(self, db: Session):
        self.db = db

    # ── Invoice ───────────────────────────────────────────────────────────────
    def create_invoice(self, invoice: Invoice):
        self.db.add(invoice)
        self.db.commit()
        self.db.refresh(invoice)
        return invoice

    def get_invoice_by_id(self, invoice_id: int):
        return self.db.query(Invoice).filter(Invoice.invoice_id == invoice_id).first()

    def get_all_invoices(self):
        return self.db.query(Invoice).all()

    def update_invoice(self, invoice: Invoice):
        self.db.merge(invoice)
        self.db.commit()
        return invoice

    def delete_invoice(self, invoice_id: int):
        invoice = self.get_invoice_by_id(invoice_id)
        if invoice:
            self.db.delete(invoice)
            self.db.commit()
        return invoice

    # ── Invoice Line Item ─────────────────────────────────────────────────────
    def create_line_item(self, line_item: InvoiceLineItem):
        self.db.add(line_item)
        self.db.commit()
        self.db.refresh(line_item)
        return line_item

    def get_line_item_by_id(self, line_item_id: int):
        return self.db.query(InvoiceLineItem).filter(InvoiceLineItem.line_item_id == line_item_id).first()

    def get_line_items_by_invoice(self, invoice_id: int):
        return self.db.query(InvoiceLineItem).filter(InvoiceLineItem.invoice_id == invoice_id).all()

    def update_line_item(self, line_item: InvoiceLineItem):
        self.db.merge(line_item)
        self.db.commit()
        return line_item

    def delete_line_item(self, line_item_id: int):
        item = self.get_line_item_by_id(line_item_id)
        if item:
            self.db.delete(item)
            self.db.commit()
        return item
