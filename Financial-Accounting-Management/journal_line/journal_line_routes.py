from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from journal_line.journal_line_schema import JournalLineCreate, JournalLineResponse
from journal_line.journal_line_service import JournalLineService

router = APIRouter(prefix="/journal-lines", tags=["Journal Line"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=JournalLineResponse)
def create_journal_line(data: JournalLineCreate, db: Session = Depends(get_db)):
    return JournalLineService.create_journal_line(db, data)

@router.get("/{journal_line_id}", response_model=JournalLineResponse)
def get_journal_line(journal_line_id: int, db: Session = Depends(get_db)):
    return JournalLineService.get_journal_line(db, journal_line_id)

@router.get("/by-journal/{journal_id}", response_model=list[JournalLineResponse])
def get_lines_by_journal(journal_id: int, db: Session = Depends(get_db)):
    return JournalLineService.get_lines_by_journal(db, journal_id)

@router.put("/{journal_line_id}", response_model=JournalLineResponse)
def update_journal_line(journal_line_id: int, data: dict, db: Session = Depends(get_db)):
    return JournalLineService.update_journal_line(db, journal_line_id, data)

@router.delete("/{journal_line_id}")
def delete_journal_line(journal_line_id: int, db: Session = Depends(get_db)):
    JournalLineService.delete_journal_line(db, journal_line_id)
    return {"message": "Journal line deleted successfully"}
