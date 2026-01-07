from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from journal_entry.journal_entry_schema import JournalEntryCreate, JournalEntryResponse
from journal_entry.journal_entry_service import JournalEntryService

router = APIRouter(prefix="/journal-entries", tags=["Journal Entry"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=JournalEntryResponse)
def create_journal_entry(data: JournalEntryCreate, db: Session = Depends(get_db)):
    return JournalEntryService.create_journal_entry(db, data)

@router.get("/{journal_id}", response_model=JournalEntryResponse)
def get_journal_entry(journal_id: int, db: Session = Depends(get_db)):
    return JournalEntryService.get_journal_entry(db, journal_id)

@router.get("/", response_model=list[JournalEntryResponse])
def get_all_journal_entries(db: Session = Depends(get_db)):
    return JournalEntryService.get_all_journal_entries(db)

@router.put("/{journal_id}", response_model=JournalEntryResponse)
def update_journal_entry(journal_id: int, data: dict, db: Session = Depends(get_db)):
    return JournalEntryService.update_journal_entry(db, journal_id, data)

@router.delete("/{journal_id}")
def delete_journal_entry(journal_id: int, db: Session = Depends(get_db)):
    JournalEntryService.delete_journal_entry(db, journal_id)
    return {"message": "Journal entry deleted successfully"}
