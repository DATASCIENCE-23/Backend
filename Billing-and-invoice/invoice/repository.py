#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 31 14:32:16 2025

@author: cslinux
"""

from sqlalchemy.orm import Session
from sqlalchemy import select

from .models import Invoice


class InvoiceRepository:

    def create(self, db: Session, invoice: Invoice) -> Invoice:
        db.add(invoice)
        db.commit()
        db.refresh(invoice)
        return invoice

    def get_by_id(self, db: Session, invoice_id: int) -> Invoice | None:
        result = db.execute(
            select(Invoice).where(Invoice.invoice_id == invoice_id)
        )
        return result.scalar_one_or_none()

    def get_by_patient(self, db: Session, patient_id: int):
        result = db.execute(
            select(Invoice).where(Invoice.patient_id == patient_id)
        )
        return result.scalars().all()

    def update(self, db: Session, invoice: Invoice) -> Invoice:
        db.commit()
        db.refresh(invoice)
        return invoice
