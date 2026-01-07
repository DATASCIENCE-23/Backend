from sqlalchemy.orm import Session
from journal_entry.journal_entry_service import JournalEntryService
from journal_entry.journal_entry_schema import JournalEntryCreate

class JournalEntryController:

    @staticmethod
    def create(db: Session, data: JournalEntryCreate):
        return JournalEntryService.create_journal_entry(db, data)

    @staticmethod
    def get(db: Session, journal_id: int):
        return JournalEntryService.get_journal_entry(db, journal_id)

    @staticmethod
    def get_all(db: Session):
        return JournalEntryService.get_all_journal_entries(db)

    @staticmethod
    def update(db: Session, journal_id: int, data: dict):
        return JournalEntryService.update_journal_entry(db, journal_id, data)

    @staticmethod
    def delete(db: Session, journal_id: int):
        return JournalEntryService.delete_journal_entry(db, journal_id)
