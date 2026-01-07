from datetime import date

from database import SessionLocal

from account.account_models import Account
from journal_entry.journal_entry_models import JournalEntry
from journal_line.journal_line_models import JournalLine
from tax.tax_models import Tax
from invoice.invoice_models import Invoice
from invoice_line.invoice_line_models import InvoiceLine
from payment.payment_models import Payment
from expense.expense_models import Expense
from asset.asset_models import Asset
from depreciation.depreciation_models import Depreciation
from vendor.vendor_models import Vendor
from bill.bill_models import Bill
from bill_line.bill_line_models import BillLine
from budget.budget_models import Budget
from budget_line.budget_line_models import BudgetLine

from account.account_repository import AccountRepository
from journal_entry.journal_entry_repository import JournalEntryRepository
from journal_line.journal_line_repository import JournalLineRepository
from tax.tax_repository import TaxRepository
from invoice.invoice_repository import InvoiceRepository
from invoice_line.invoice_line_repository import InvoiceLineRepository
from payment.payment_repository import PaymentRepository
from expense.expense_repository import ExpenseRepository
from depreciation.depreciation_repository import DepreciationRepository
from vendor.vendor_repository import VendorRepository
from bill.bill_repository import BillRepository
from bill_line.bill_line_repository import BillLineRepository
from budget.budget_repository import BudgetRepository
from budget_line.budget_line_repository import BudgetLineRepository

db = SessionLocal()
print("\n===== FINANCE REPOSITORY TEST STARTED =====\n")

print("ACCOUNT TEST")

account = Account(account_name="Cash", account_type="Asset")
account = AccountRepository.create(db, account)

assert account.account_id is not None
print("✔ Account created:", account.account_id)

AccountRepository.update(db, account, {"account_name": "Main Cash"})
assert account.account_name == "Main Cash"
print("✔ Account updated")
print("\nJOURNAL TEST")

journal = JournalEntry(
    journal_date=date.today(),
    description="Test Journal"
)
journal = JournalEntryRepository.create(db, journal)

jl1 = JournalLine(
    journal_id=journal.journal_id,
    account_id=account.account_id,
    debit_amount=500,
    credit_amount=0
)

jl2 = JournalLine(
    journal_id=journal.journal_id,
    account_id=account.account_id,
    debit_amount=0,
    credit_amount=500
)

JournalLineRepository.create(db, jl1)
JournalLineRepository.create(db, jl2)

lines = JournalLineRepository.get_by_journal(db, journal.journal_id)
assert len(lines) == 2
print("✔ Journal balanced with 2 lines")

print("\nTAX TEST")

tax = Tax(
    tax_name="GST",
    tax_rate=18,
    account_id=account.account_id
)

tax = TaxRepository.create(db, tax)
assert tax.tax_id is not None
print("✔ Tax created:", tax.tax_id)

print("\nINVOICE TEST")

invoice = Invoice(
    patient_id=1,  # MUST EXIST
    invoice_date=date.today(),
    total_amount=1000,
    tax_amount=180,
    discount_amount=0,
    status="OPEN"
)

invoice = InvoiceRepository.create(db, invoice)

line = InvoiceLine(
    invoice_id=invoice.invoice_id,
    service_name="Consultation",
    account_id=account.account_id,
    quantity=1,
    unit_price=1000,
    line_total=1000
)

InvoiceLineRepository.create(db, line)

lines = InvoiceLineRepository.get_by_invoice(db, invoice.invoice_id)
assert len(lines) == 1
print("✔ Invoice + line created")

print("\nPAYMENT TEST")

payment = Payment(
    invoice_id=invoice.invoice_id,
    payment_date=date.today(),
    amount_paid=1180,
    payment_mode="CASH"
)

payment = PaymentRepository.create(db, payment)
print("✔ Payment recorded:", payment.payment_id)

payment = PaymentRepository.create(db, payment)
assert payment.payment_id is not None
print("✔ Payment recorded")

print("\nEXPENSE TEST")

expense = Expense(
    expense_date=date.today(),
    account_id=account.account_id,
    amount=500,
    department_id=1,  # MUST EXIST
    description="Office Supplies"
)

expense = ExpenseRepository.create(db, expense)
assert expense.expense_id is not None
print("✔ Expense recorded")

print("\nASSET & DEPRECIATION TEST")

asset = Asset(
    asset_name="X-Ray Machine",
    purchase_date=date.today(),
    purchase_cost=200000,
    useful_life_years=10,
    salvage_value=20000
)

db.add(asset)
db.commit()
db.refresh(asset)

depr = Depreciation(
    asset_id=asset.asset_id,
    depreciation_date=date.today(),
    amount=18000
)

DepreciationRepository.create(db, depr)

records = DepreciationRepository.get_by_asset(db, asset.asset_id)
assert len(records) == 1
print("✔ Asset depreciated")
print("\nVENDOR & BILL TEST")

vendor = Vendor(vendor_name="ABC Medicals")
vendor = VendorRepository.create(db, vendor)

bill = Bill(
    vendor_id=vendor.vendor_id,
    bill_date=date.today(),
    total_amount=5000,
    tax_amount=900,
    status="UNPAID"
)

bill = BillRepository.create(db, bill)

bill_line = BillLine(
    bill_id=bill.bill_id,
    expense_account_id=account.account_id,
    description="Medicines",
    amount=5000
)

BillLineRepository.create(db, bill_line)
print("✔ Vendor bill created")

print("\nBUDGET TEST")

budget = Budget(
    financial_year="2025-2026",
    department_id=1,  # MUST EXIST
    total_amount=100000
)

budget = BudgetRepository.create(db, budget)

budget_line = BudgetLine(
    budget_id=budget.budget_id,
    account_id=account.account_id,
    allocated_amount=50000
)

BudgetLineRepository.create(db, budget_line)
print("✔ Budget allocated")

print("\n===== ALL FINANCE REPOSITORY TESTS PASSED =====")
db.close()
