"""
SERVICE LAYER TEST SUITE
Run: python test_services.py
Prerequisites:
- DB running
- All tables created
- patient_id = 1, department_id = 1 exist in DB
"""

from datetime import date
from database import SessionLocal

# ========================
# IMPORT SERVICES + SCHEMAS
# ========================

from account.account_service import AccountService
from account.account_schema import AccountCreate

from tax.tax_service import TaxService
from tax.tax_schema import TaxCreate

from vendor.vendor_service import VendorService
from vendor.vendor_schema import VendorCreate

from bill.bill_service import BillService
from bill.bill_schema import BillCreate

from bill_line.bill_line_service import BillLineService
from bill_line.bill_line_schema import BillLineCreate

from budget.budget_service import BudgetService
from budget.budget_schema import BudgetCreate

from budget_line.budget_line_service import BudgetLineService
from budget_line.budget_line_schema import BudgetLineCreate

from asset.asset_service import AssetService
from asset.asset_schema import AssetCreate

from depreciation.depreciation_service import DepreciationService
from depreciation.depreciation_schema import DepreciationCreate

from expense.expense_service import ExpenseService
from expense.expense_schema import ExpenseCreate

from invoice.invoice_service import InvoiceService
from invoice.invoice_schema import InvoiceCreate

from invoice_line.invoice_line_service import InvoiceLineService
from invoice_line.invoice_line_schema import InvoiceLineCreate

from payment.payment_service import PaymentService
from payment.payment_schema import PaymentCreate

from journal_entry.journal_entry_service import JournalEntryService
from journal_entry.journal_entry_schema import JournalEntryCreate

from journal_line.journal_line_service import JournalLineService
from journal_line.journal_line_schema import JournalLineCreate

from bank_account.bank_account_service import BankAccountService
from bank_account.bank_account_schema import BankAccountCreate

def run_tests():
    db = SessionLocal()

    print("\n===== ACCOUNT =====")
    cash = AccountService.create_account(
        db,
        AccountCreate(account_name="Cash", account_type="Asset")
    )
    print("Account ID:", cash.account_id)

    print("\n===== TAX =====")
    gst = TaxService.create_tax(
        db,
        TaxCreate(
            tax_name="GST",
            tax_rate=18,
            account_id=cash.account_id
        )
    )
    print("Tax ID:", gst.tax_id)

    print("\n===== VENDOR =====")
    vendor = VendorService.create_vendor(
        db,
        VendorCreate(vendor_name="ABC Medical Suppliers")
    )
    print("Vendor ID:", vendor.vendor_id)

    bank_account = BankAccountService.create_bank_account(
        db,
        BankAccountCreate(
            account_number="1234567890",
            bank_name="ICICI",
            branch_name="Chennai",
            account_id=cash.account_id,
            current_balance=500000
        )
    )
    print("Bank Account ID:", bank_account.bank_account_id)

    print("\n===== BILL =====")
    bill = BillService.create_bill(
        db,
        BillCreate(
            vendor_id=vendor.vendor_id,
            bill_date=date.today(),
            total_amount=50000,
            tax_amount=9000,
            status="PENDING"
        )
    )
    print("Bill ID:", bill.bill_id)

    print("\n===== BILL LINE =====")
    bill_line = BillLineService.create_bill_line(
        db,
        BillLineCreate(
            bill_id=bill.bill_id,
            expense_account_id=cash.account_id,
            description="Medicine Purchase",
            amount=50000
        )
    )
    print("Bill Line ID:", bill_line.bill_line_id)

    print("\n===== BUDGET =====")
    budget = BudgetService.create_budget(
        db,
        BudgetCreate(
            financial_year="2025-26",
            department_id=1,
            total_amount=300000
        )
    )
    print("Budget ID:", budget.budget_id)

    print("\n===== BUDGET LINE =====")
    budget_line = BudgetLineService.create_budget_line(
        db,
        BudgetLineCreate(
            budget_id=budget.budget_id,
            account_id=cash.account_id,
            allocated_amount=150000
        )
    )
    print("Budget Line ID:", budget_line.budget_line_id)

    print("\n===== ASSET =====")
    asset = AssetService.create_asset(
        db,
        AssetCreate(
            asset_name="Ventilator",
            purchase_date=date.today(),
            purchase_cost=1200000,
            useful_life_years=8,
            salvage_value=100000
        )
    )
    print("Asset ID:", asset.asset_id)

    print("\n===== DEPRECIATION =====")
    depreciation = DepreciationService.create_depreciation(
        db,
        DepreciationCreate(
            asset_id=asset.asset_id,
            depreciation_date=date.today(),
            amount=137500
        )
    )
    print("Depreciation ID:", depreciation.depreciation_id)

    print("\n===== EXPENSE =====")
    expense = ExpenseService.create_expense(
        db,
        ExpenseCreate(
            expense_date=date.today(),
            account_id=cash.account_id,
            amount=12000,
            department_id=1,
            description="Water charges"
        )
    )
    print("Expense ID:", expense.expense_id)

    print("\n===== INVOICE (AUTO JOURNAL) =====")
    invoice = InvoiceService.create_invoice(
        db,
        InvoiceCreate(
            patient_id=1,
            invoice_date=date.today(),
            total_amount=10000,
            tax_amount=1800,
            discount_amount=0,
            status="ISSUED"
        )
    )
    print("Invoice ID:", invoice.invoice_id)

    print("\n===== INVOICE LINE =====")
    invoice_line = InvoiceLineService.create_invoice_line(
        db,
        InvoiceLineCreate(
            invoice_id=invoice.invoice_id,
            service_name="Consultation",
            account_id=cash.account_id,
            quantity=1,
            unit_price=10000,
            line_total=10000
        )
    )
    print("Invoice Line ID:", invoice_line.invoice_line_id)

    print("\n===== PAYMENT (AUTO JOURNAL) =====")
    payment = PaymentService.create_payment(
        db,
        PaymentCreate(
            invoice_id=invoice.invoice_id,
            payment_date=date.today(),
            amount_paid=10000,
            payment_mode="CASH",
            bank_account_id=bank_account.bank_account_id
        )
    )
    print("Payment ID:", payment.payment_id)

    print("\n===== MANUAL JOURNAL ENTRY =====")
    journal = JournalEntryService.create_journal_entry(
        db,
        JournalEntryCreate(
            journal_date=date.today(),
            description="Manual adjustment"
        )
    )
    print("Journal Entry ID:", journal.journal_id)

    print("\n===== MANUAL JOURNAL LINE =====")
    line = JournalLineService.create_journal_line(
        db,
        JournalLineCreate(
            journal_id=journal.journal_id,
            account_id=cash.account_id,
            debit_amount=500,
            credit_amount=0
        )
    )
    print("Journal Line ID:", line.journal_line_id)

    db.close()
    print("\n ALL FINANCE SERVICES TESTED SUCCESSFULLY")


if __name__ == "__main__":
    run_tests()
