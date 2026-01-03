#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 31 14:33:37 2025

@author: cslinux
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from .controller import InvoiceController

router = APIRouter(prefix="/invoices", tags=["Invoices"])
controller = InvoiceController()


@router.post("/", response_model=None)
def create_invoice(payload: dict, db: Session = Depends(get_db)):
    return controller.create_invoice(db, payload)


@router.get("/{invoice_id}", response_model=None)
def get_invoice(invoice_id: int, db: Session = Depends(get_db)):
    invoice = controller.get_invoice(db, invoice_id)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice
