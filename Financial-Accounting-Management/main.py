from fastapi import FastAPI

from database import engine, Base

# -----------------------------
# IMPORT ALL MODELS (IMPORTANT)
# -----------------------------
# This ensures Base.metadata.create_all() knows about all tables

from account.account_models import Account
from asset.asset_models import Asset
from bank_account.bank_account_models import BankAccount
from bill.bill_models import Bill
from bill_line.bill_line_models import BillLine
from budget.budget_models import Budget
from budget_line.budget_line_models import BudgetLine
from depreciation.depreciation_models import Depreciation
from expense.expense_models import Expense
from invoice.invoice_models import Invoice
from invoice_line.invoice_line_models import InvoiceLine
from journal_entry.journal_entry_models import JournalEntry
from journal_line.journal_line_models import JournalLine
from payment.payment_models import Payment
from tax.tax_models import Tax
from vendor.vendor_models import Vendor

# -----------------------------
# CREATE TABLES (SAFE)
# -----------------------------
Base.metadata.create_all(bind=engine)

# -----------------------------
# FASTAPI APP
# -----------------------------
app = FastAPI(
    title="Hospital Management System – Finance Module",
    description="Accounting, Billing, Assets, Expenses, Budgets & Journals",
    version="1.0.0"
)

# -----------------------------
# IMPORT ROUTERS
# -----------------------------
from account.account_routes import router as account_router
from asset.asset_routes import router as asset_router
from bank_account.bank_account_routes import router as bank_account_router
from bill.bill_routes import router as bill_router
from bill_line.bill_line_routes import router as bill_line_router
from budget.budget_routes import router as budget_router
from budget_line.budget_line_routes import router as budget_line_router
from depreciation.depreciation_routes import router as depreciation_router
from expense.expense_routes import router as expense_router
from invoice.invoice_routes import router as invoice_router
from invoice_line.invoice_line_routes import router as invoice_line_router
from journal_entry.journal_entry_routes import router as journal_entry_router
from journal_line.journal_line_routes import router as journal_line_router
from payment.payment_routes import router as payment_router
from tax.tax_routes import router as tax_router
from vendor.vendor_routes import router as vendor_router

# -----------------------------
# REGISTER ROUTERS
# -----------------------------
app.include_router(account_router)
app.include_router(asset_router)
app.include_router(bank_account_router)
app.include_router(bill_router)
app.include_router(bill_line_router)
app.include_router(budget_router)
app.include_router(budget_line_router)
app.include_router(depreciation_router)
app.include_router(expense_router)
app.include_router(invoice_router)
app.include_router(invoice_line_router)
app.include_router(journal_entry_router)
app.include_router(journal_line_router)
app.include_router(payment_router)
app.include_router(tax_router)
app.include_router(vendor_router)

# -----------------------------
# HEALTH CHECK
# -----------------------------
@app.get("/health")
def health_check():
    return {
        "status": "OK",
        "module": "Finance Accounting",
        "message": "Finance module is up and running"
    }
