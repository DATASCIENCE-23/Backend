from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from JOURNAL_LINE.database import get_db
from JOURNAL_LINE.journal_line_service import JournalLineService

router = APIRouter()

@router.post("/")
def create_journal_line(payload: dict, db: Session = Depends(get_db)):
    try:
        return JournalLineService.create_journal_line(db, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{journal_line_id}")
def get_journal_line(journal_line_id: int, db: Session = Depends(get_db)):
    try:
        return JournalLineService.get_journal_line(db, journal_line_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/")
def list_journal_lines(db: Session = Depends(get_db)):
    return JournalLineService.list_journal_lines(db)


@router.put("/{journal_line_id}")
def update_journal_line(journal_line_id: int, payload: dict, db: Session = Depends(get_db)):
    try:
        return JournalLineService.update_journal_line(db, journal_line_id, payload)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{journal_line_id}")
def delete_journal_line(journal_line_id: int, db: Session = Depends(get_db)):
    try:
        JournalLineService.delete_journal_line(db, journal_line_id)
        return {"message": "Journal line deleted"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
