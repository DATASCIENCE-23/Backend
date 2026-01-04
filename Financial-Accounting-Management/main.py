from fastapi import FastAPI

from JOURNAL_ENTRY.journal_entry_route import router as journal_entry_routes
from JOURNAL_LINE.journal_line_routes import router as journal_line_routes
from BUDGET.budget_routes import router as budget_routes
from BUDGET_LINE.budget_line_routes import router as budget_line_routes

app = FastAPI(title="Hospital Finance Module")

app.include_router(journal_entry_routes)
app.include_router(journal_line_routes)
app.include_router(budget_routes)
app.include_router(budget_line_routes)
