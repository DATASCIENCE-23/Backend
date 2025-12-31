#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 31 14:32:16 2025

@author: cslinux
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .models import Invoice


class InvoiceRepository:

    async def create(self, db: AsyncSession, invoice: Invoice) -> Invoice:
        db.add(invoice)
        await db.commit()
        await db.refresh(invoice)
        return invoice

    async def get_by_id(self, db: AsyncSession, invoice_id: int) -> Invoice | None:
        result = await db.execute(
            select(Invoice).where(Invoice.invoice_id == invoice_id)
        )
        return result.scalar_one_or_none()

    async def get_by_patient(self, db: AsyncSession, patient_id: int):
        result = await db.execute(
            select(Invoice).where(Invoice.patient_id == patient_id)
        )
        return result.scalars().all()

    async def update(self, db: AsyncSession, invoice: Invoice) -> Invoice:
        await db.commit()
        await db.refresh(invoice)
        return invoice
