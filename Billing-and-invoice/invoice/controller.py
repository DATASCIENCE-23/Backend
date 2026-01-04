#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 31 14:33:09 2025

@author: cslinux
"""

from sqlalchemy.orm import Session
from .service import InvoiceService


class InvoiceController:

    def __init__(self):
        self.service = InvoiceService()

    def create_invoice(self, db: Session, payload: dict):
        return self.service.create_invoice(
            db=db,
            patient_id=payload["patient_id"],
            created_by=payload["created_by"],
            invoice_type=payload["invoice_type"],
            items=payload["items"]
        )

    def get_invoice(self, db: Session, invoice_id: int):
        return self.service.get_invoice(db, invoice_id)
