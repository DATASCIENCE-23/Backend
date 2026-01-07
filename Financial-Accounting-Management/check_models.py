from database import Base, engine

# # Import ALL models
from account.account_models import Account
from asset.asset_models import Asset
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




from database import Base, engine

from account.account_models import Account
from bank_account.bank_account_models import BankAccount
from payment.payment_models import Payment

Base.metadata.create_all(bind=engine)
print("All tables created successfully")