from sqlalchemy.orm import Session
from journal_line.journal_line_models import JournalLine

class JournalLineRepository:

    @staticmethod
    def create(db: Session, line: JournalLine):
        db.add(line)
        db.commit()
        db.refresh(line)
        return line

    @staticmethod
    def get_by_id(db: Session, journal_line_id: int):
        return db.query(JournalLine).filter(
            JournalLine.journal_line_id == journal_line_id
        ).first()

    @staticmethod
    def get_by_journal(db: Session, journal_id: int):
        return db.query(JournalLine).filter(
            JournalLine.journal_id == journal_id
        ).all()

    @staticmethod
    def update(db: Session, line: JournalLine, data: dict):
        for key, value in data.items():
            setattr(line, key, value)
        db.commit()
        db.refresh(line)
        return line

    @staticmethod
    def delete(db: Session, line: JournalLine):
        db.delete(line)
        db.commit()
