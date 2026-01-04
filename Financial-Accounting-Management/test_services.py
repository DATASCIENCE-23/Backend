from JOURNAL_ENTRY.database import SessionLocal
from JOURNAL_ENTRY.journal_entry_service import JournalEntryService
from JOURNAL_LINE.journal_line_service import JournalLineService
from BUDGET.budget_service import BudgetService
from BUDGET_LINE.budget_line_service import BudgetLineService

db = SessionLocal()

# ---- Test Budget ----
budget = BudgetService.create_budget(db, {
    "financial_year": "2024-25",
    "department": "Cardiology",
    "total_amount": 100000
})
print("Budget created:", budget.budget_id)

# ---- Test Budget Line ----
budget_line = BudgetLineService.create_budget_line(db, {
    "budget_id": budget.budget_id,
    "account_id": 1,
    "allocated_amount": 50000
})
print("Budget line added")

# ---- Test Journal Entry ----
journal = JournalEntryService.create_journal_entry(db, {
    "journal_date": "2024-12-31",
    "reference_type": "Manual",
    "reference_id": 1,
    "description": "Test Journal"
})
print("Journal created:", journal.journal_id)

# ---- Test Journal Lines ----
JournalLineService.create_journal_line(db, {
    "journal_id": journal.journal_id,
    "account_id": 1,
    "debit_amount": 1000,
    "credit_amount": 0
})

JournalLineService.create_journal_line(db, {
    "journal_id": journal.journal_id,
    "account_id": 2,
    "debit_amount": 0,
    "credit_amount": 1000
})

print("Journal lines added")

# ---- Post Journal ----
JournalEntryService.post_journal_entry(db, journal.journal_id)
print("Journal posted")

db.close()
