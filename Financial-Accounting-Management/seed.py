from datetime import date
from database import SessionLocal

# Controllers
from account.account_controller import AccountController
from bank_account.bank_account_controller import BankAccountController
from tax.tax_controller import TaxController
from vendor.vendor_controller import VendorController
from budget.budget_controller import BudgetController
from budget_line.budget_line_controller import BudgetLineController
from asset.asset_controller import AssetController
from depreciation.depreciation_controller import DepreciationController
from expense.expense_controller import ExpenseController
from invoice.invoice_controller import InvoiceController
from invoice_line.invoice_line_controller import InvoiceLineController
from payment.payment_controller import PaymentController

# Schemas
from account.account_schema import AccountCreate
from bank_account.bank_account_schema import BankAccountCreate
from tax.tax_schema import TaxCreate
from vendor.vendor_schema import VendorCreate
from budget.budget_schema import BudgetCreate
from budget_line.budget_line_schema import BudgetLineCreate
from asset.asset_schema import AssetCreate
from depreciation.depreciation_schema import DepreciationCreate
from expense.expense_schema import ExpenseCreate
from invoice.invoice_schema import InvoiceCreate
from invoice_line.invoice_line_schema import InvoiceLineCreate
from payment.payment_schema import PaymentCreate


def seed():
    db = SessionLocal()

    print(" Seeding Finance Module Data...")

    # 1️Accounts
    cash = AccountController.create(db, AccountCreate(
        account_name="Cash",
        account_type="Asset"
    ))

    revenue = AccountController.create(db, AccountCreate(
        account_name="Consultation Revenue",
        account_type="Income"
    ))

    expense_acc = AccountController.create(db, AccountCreate(
        account_name="Office Expense",
        account_type="Expense"
    ))

    print("✔ Accounts created")

    # 2️Bank Account
    bank = BankAccountController.create(db, BankAccountCreate(
        account_number="0000000000",
        bank_name="State Bank of India",
        branch_name="Chennai",
        account_id=cash.account_id,
        current_balance=100000
    ))

    print("✔ Bank account created")

    # 3️ Tax
    gst = TaxController.create(db, TaxCreate(
        tax_name="GST",
        tax_rate=18,
        account_id=revenue.account_id
    ))

    print("✔ Tax created")

    # 4️ Vendor
    vendor = VendorController.create(db, VendorCreate(
        vendor_name="Medical Supplies Co",
        contact_info="vendor@example.com",
        gst_number="33ABCDE1234F1Z5"
    ))

    print("✔ Vendor created")

    # 5️ Budget
    budget = BudgetController.create(db, BudgetCreate(
        financial_year="2025-2026",
        department_id=1,
        total_amount=500000
    ))

    BudgetLineController.create(db, BudgetLineCreate(
        budget_id=budget.budget_id,
        account_id=expense_acc.account_id,
        allocated_amount=200000
    ))

    print("✔ Budget & budget line created")

    # 6️ Asset
    asset = AssetController.create(db, AssetCreate(
        asset_name="X-Ray Machine",
        purchase_date=date.today(),
        purchase_cost=300000,
        useful_life_years=5,
        salvage_value=20000
    ))

    DepreciationController.create(db, DepreciationCreate(
        asset_id=asset.asset_id,
        depreciation_date=date.today(),
        amount=50000
    ))

    print("✔ Asset & depreciation created")

    # 7️ Expense
    ExpenseController.create(db, ExpenseCreate(
        expense_date=date.today(),
        account_id=expense_acc.account_id,
        amount=15000,
       department_id=1,
        reference_id=1
    ))

    print("✔ Expense created")

    #  ASSUMPTION
    # patient_id = 1 exists in Patient module

    # 8️ Invoice
    invoice = InvoiceController.create(db, InvoiceCreate(
        patient_id=1,
        invoice_date=date.today(),
        total_amount=1000,
        tax_amount=180,
        discount_amount=0,
        status="OPEN"
    ))

    InvoiceLineController.create(db, InvoiceLineCreate(
        invoice_id=invoice.invoice_id,
        service_name="Doctor Consultation",
        account_id=revenue.account_id,
        quantity=1,
        unit_price=1000,
        line_total=1000
    ))

    print("✔ Invoice & invoice line created")

    # 9️ Payment (auto journal posting)
    PaymentController.create(db, PaymentCreate(
        invoice_id=invoice.invoice_id,
        payment_date=date.today(),
        amount_paid=1180,
        payment_mode="CASH",
        bank_account_id=bank.bank_account_id
    ))

    print(" Payment & journal entry created")

    db.close()
    print(" Seeding completed successfully!")


if __name__ == "__main__":
    seed()
