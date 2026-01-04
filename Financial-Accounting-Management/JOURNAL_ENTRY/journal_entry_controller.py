from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from JOURNAL_ENTRY.database import get_db
from JOURNAL_ENTRY.journal_entry_service import JournalEntryService

router = APIRouter()

@router.post("/")
def create_journal_entry(payload: dict, db: Session = Depends(get_db)):
    try:
        return JournalEntryService.create_journal_entry(db, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{journal_id}")
def get_journal_entry(journal_id: int, db: Session = Depends(get_db)):
    try:
        return JournalEntryService.get_journal_entry(db, journal_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/")
def list_journal_entries(db: Session = Depends(get_db)):
    return JournalEntryService.list_journal_entries(db)


@router.put("/{journal_id}")
def update_journal_entry(journal_id: int, payload: dict, db: Session = Depends(get_db)):
    try:
        return JournalEntryService.update_journal_entry(db, journal_id, payload)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{journal_id}")
def delete_journal_entry(journal_id: int, db: Session = Depends(get_db)):
    try:
        JournalEntryService.delete_journal_entry(db, journal_id)
        return {"message": "Journal entry deleted"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
