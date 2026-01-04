from sqlalchemy.orm import Session
from sqlalchemy import func
from JOURNAL_LINE.journal_line_model import JournalLine

class JournalLineRepository:

    @staticmethod
    def get_by_id(db: Session, journal_line_id: int):
        return db.query(JournalLine).filter(
            JournalLine.journal_line_id == journal_line_id
        ).first()

    @staticmethod
    def get_by_journal_id(db: Session, journal_id: int):
        return db.query(JournalLine).filter(
            JournalLine.journal_id == journal_id
        ).all()

    @staticmethod
    def get_all(db: Session):
        return db.query(JournalLine).all()

    @staticmethod
    def create(db: Session, line: JournalLine):
        db.add(line)
        db.commit()
        db.refresh(line)
        return line

    @staticmethod
    def update(db: Session, line: JournalLine):
        db.commit()
        db.refresh(line)
        return line

    @staticmethod
    def delete(db: Session, line: JournalLine):
        db.delete(line)
        db.commit()
