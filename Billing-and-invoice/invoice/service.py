#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 31 14:32:50 2025

@author: cslinux
"""

from sqlalchemy.orm import Session
from decimal import Decimal

from .models import Invoice, InvoiceLineItem
from .repository import InvoiceRepository
from .configuration import InvoiceStatus


class InvoiceService:

    def __init__(self):
        self.repo = InvoiceRepository()

    def create_invoice(
        self,
        db: Session,
        patient_id: int,
        created_by: int,
        invoice_type,
        items: list[dict]
    ) -> Invoice:

        invoice = Invoice(
            patient_id=patient_id,
            created_by=created_by,
            invoice_type=invoice_type,
            status=InvoiceStatus.ISSUED
        )

        subtotal = Decimal("0.00")
        tax_total = Decimal("0.00")

        for item in items:
            line_subtotal = item["quantity"] * item["unit_price"]
            tax_amount = line_subtotal * item.get("tax_rate", Decimal("0.00"))

            invoice.line_items.append(
                InvoiceLineItem(
                    service_id=item["service_id"],
                    description=item.get("description"),
                    quantity=item["quantity"],
                    unit_price=item["unit_price"],
                    line_subtotal=line_subtotal,
                    tax_amount=tax_amount,
                    line_total=line_subtotal + tax_amount
                )
            )

            subtotal += line_subtotal
            tax_total += tax_amount

        invoice.subtotal = subtotal
        invoice.tax_amount = tax_total
        invoice.grand_total = subtotal + tax_total

        return self.repo.create(db, invoice)

    def get_invoice(self, db: Session, invoice_id: int):
        return self.repo.get_by_id(db, invoice_id)
