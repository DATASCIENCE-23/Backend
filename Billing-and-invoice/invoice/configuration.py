from enum import Enum


class InvoiceStatus(str, Enum):
    DRAFT = "DRAFT"
    ISSUED = "ISSUED"
    PAID = "PAID"
    CANCELLED = "CANCELLED"


class InvoiceType(str, Enum):
    OPD = "OPD"
    IPD = "IPD"
    PHARMACY = "PHARMACY"
    LAB = "LAB"
