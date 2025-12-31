#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 31 14:33:37 2025

@author: cslinux
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from .controller import InvoiceController

router = APIRouter(prefix="/invoices", tags=["Invoices"])
controller = InvoiceController()


@router.post("/")
async def create_invoice(payload: dict, db: AsyncSession = Depends(get_db)):
    return await controller.create_invoice(db, payload)


@router.get("/{invoice_id}")
async def get_invoice(invoice_id: int, db: AsyncSession = Depends(get_db)):
    invoice = await controller.get_invoice(db, invoice_id)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice
