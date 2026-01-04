from sqlalchemy.orm import Session
from JOURNAL_ENTRY.journal_entry_model import JournalEntry
from JOURNAL_ENTRY.journal_entry_repository import JournalEntryRepository
from JOURNAL_LINE.journal_line_repository import JournalLineRepository


class JournalEntryService:

    @staticmethod
    def create_journal_entry(db: Session, data: dict):
        journal = JournalEntry(**data)
        journal.posted_status = False
        return JournalEntryRepository.create(db, journal)

    @staticmethod
    def get_journal_entry(db: Session, journal_id: int):
        journal = JournalEntryRepository.get_by_id(db, journal_id)
        if not journal:
            raise ValueError("Journal entry not found")
        return journal

    @staticmethod
    def list_journal_entries(db: Session):
        return JournalEntryRepository.get_all(db)

    @staticmethod
    def update_journal_entry(db: Session, journal_id: int, data: dict):
        journal = JournalEntryRepository.get_by_id(db, journal_id)
        if not journal:
            raise ValueError("Journal entry not found")

        if journal.posted_status:
            raise ValueError("Posted journal entry cannot be updated")

        for key, value in data.items():
            setattr(journal, key, value)

        return JournalEntryRepository.update(db, journal)

    @staticmethod
    def delete_journal_entry(db: Session, journal_id: int):
        journal = JournalEntryRepository.get_by_id(db, journal_id)
        if not journal:
            raise ValueError("Journal entry not found")

        if journal.posted_status:
            raise ValueError("Posted journal entry cannot be deleted")

        JournalEntryRepository.delete(db, journal)

    @staticmethod
    def post_journal_entry(db: Session, journal_id: int):
        journal = JournalEntryRepository.get_by_id(db, journal_id)
        if not journal:
            raise ValueError("Journal entry not found")

        lines = JournalLineRepository.get_by_journal_id(db, journal_id)
        if not lines:
            raise ValueError("Cannot post journal without journal lines")

        total_debit = sum(line.debit_amount for line in lines)
        total_credit = sum(line.credit_amount for line in lines)

        if total_debit != total_credit:
            raise ValueError("Debit and credit totals do not match")

        journal.posted_status = True
        return JournalEntryRepository.update(db, journal)
