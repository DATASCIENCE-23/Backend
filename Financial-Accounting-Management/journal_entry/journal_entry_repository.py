from sqlalchemy.orm import Session
from journal_entry.journal_entry_models import JournalEntry

class JournalEntryRepository:

    @staticmethod
    def create(db: Session, journal: JournalEntry):
        db.add(journal)
        db.commit()
        db.refresh(journal)
        return journal

    @staticmethod
    def get_by_id(db: Session, journal_id: int):
        return db.query(JournalEntry).filter(
            JournalEntry.journal_id == journal_id
        ).first()

    @staticmethod
    def get_all(db: Session):
        return db.query(JournalEntry).all()

    @staticmethod
    def update(db: Session, journal: JournalEntry, data: dict):
        for key, value in data.items():
            setattr(journal, key, value)
        db.commit()
        db.refresh(journal)
        return journal

    @staticmethod
    def delete(db: Session, journal: JournalEntry):
        db.delete(journal)
        db.commit()
