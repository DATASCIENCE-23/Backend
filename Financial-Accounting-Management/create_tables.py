from JOURNAL_ENTRY.database import engine
from common_base import Base

# Import models so SQLAlchemy registers tables
import JOURNAL_ENTRY.journal_entry_model
import JOURNAL_LINE.journal_line_model
import BUDGET.budget_model
import BUDGET_LINE.budget_line_model

Base.metadata.create_all(bind=engine)

print("All tables created successfully")
