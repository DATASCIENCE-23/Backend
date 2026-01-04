#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 31 14:30:57 2025

@author: cslinux
"""

from sqlalchemy import (
    Column, Integer, String, DateTime, ForeignKey,
    Numeric, Enum
)
from sqlalchemy.orm import relationship
from datetime import datetime

from ..database import Base
from .configuration import InvoiceStatus, InvoiceType


class Invoice(Base):
    __tablename__ = "invoice"

    invoice_id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patient.patient_id"), nullable=False)

    issue_datetime = Column(DateTime, default=datetime.utcnow)
    invoice_type = Column(Enum(InvoiceType), nullable=False)

    subtotal = Column(Numeric(12, 2), default=0)
    tax_amount = Column(Numeric(12, 2), default=0)
    discount_amount = Column(Numeric(12, 2), default=0)
    grand_total = Column(Numeric(12, 2), default=0)

    status = Column(Enum(InvoiceStatus), default=InvoiceStatus.DRAFT)
    created_by = Column(Integer, ForeignKey("user.user_id"), nullable=False)

    # Relationships
    line_items = relationship(
        "InvoiceLineItem",
        back_populates="invoice",
        cascade="all, delete-orphan"
    )


class InvoiceLineItem(Base):
    __tablename__ = "invoice_line_item"

    line_item_id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey("invoice.invoice_id"), nullable=False)
    service_id = Column(Integer, ForeignKey("service_master.service_id"), nullable=False)

    description = Column(String(255))
    quantity = Column(Integer, default=1)

    unit_price = Column(Numeric(10, 2))
    line_subtotal = Column(Numeric(10, 2))
    tax_amount = Column(Numeric(10, 2))
    line_total = Column(Numeric(10, 2))

    invoice = relationship("Invoice", back_populates="line_items")
