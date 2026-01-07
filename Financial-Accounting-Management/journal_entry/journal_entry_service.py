from sqlalchemy.orm import Session
from journal_entry.journal_entry_models import JournalEntry
from journal_entry.journal_entry_repository import JournalEntryRepository
from journal_entry.journal_entry_schema import JournalEntryCreate

class JournalEntryService:

    @staticmethod
    def create_journal_entry(db: Session, data: JournalEntryCreate):
        journal = JournalEntry(**data.dict())
        return JournalEntryRepository.create(db, journal)

    @staticmethod
    def get_journal_entry(db: Session, journal_id: int):
        return JournalEntryRepository.get_by_id(db, journal_id)

    @staticmethod
    def get_all_journal_entries(db: Session):
        return JournalEntryRepository.get_all(db)

    @staticmethod
    def update_journal_entry(db: Session, journal_id: int, data: dict):
        journal = JournalEntryRepository.get_by_id(db, journal_id)
        if not journal:
            raise ValueError("Journal entry not found")

        return JournalEntryRepository.update(db, journal, data)

    @staticmethod
    def delete_journal_entry(db: Session, journal_id: int):
        journal = JournalEntryRepository.get_by_id(db, journal_id)
        if not journal:
            raise ValueError("Journal entry not found")

        # ⚠️ In real systems, deletion is usually blocked after posting
        return JournalEntryRepository.delete(db, journal)
