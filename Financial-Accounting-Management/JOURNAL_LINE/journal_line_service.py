from sqlalchemy.orm import Session

from JOURNAL_LINE.journal_line_model import JournalLine
from JOURNAL_LINE.journal_line_repository import JournalLineRepository
from JOURNAL_ENTRY.journal_entry_repository import JournalEntryRepository


class JournalLineService:

    @staticmethod
    def create_journal_line(db: Session, data: dict):
        journal = JournalEntryRepository.get_by_id(db, data["journal_id"])
        if not journal:
            raise ValueError("Journal entry not found")

        if journal.posted_status:
            raise ValueError("Cannot add lines to a posted journal")

        if data.get("debit_amount", 0) > 0 and data.get("credit_amount", 0) > 0:
            raise ValueError("A journal line cannot have both debit and credit")

        if data.get("debit_amount", 0) == 0 and data.get("credit_amount", 0) == 0:
            raise ValueError("Either debit or credit amount must be provided")

        line = JournalLine(**data)
        return JournalLineRepository.create(db, line)

    @staticmethod
    def get_journal_line(db: Session, journal_line_id: int):
        line = JournalLineRepository.get_by_id(db, journal_line_id)
        if not line:
            raise ValueError("Journal line not found")
        return line

    @staticmethod
    def list_journal_lines(db: Session):
        return JournalLineRepository.get_all(db)

    @staticmethod
    def update_journal_line(db: Session, journal_line_id: int, data: dict):
        line = JournalLineRepository.get_by_id(db, journal_line_id)
        if not line:
            raise ValueError("Journal line not found")

        journal = JournalEntryRepository.get_by_id(db, line.journal_id)
        if journal.posted_status:
            raise ValueError("Cannot update lines of a posted journal")

        for key, value in data.items():
            setattr(line, key, value)

        return JournalLineRepository.update(db, line)

    @staticmethod
    def delete_journal_line(db: Session, journal_line_id: int):
        line = JournalLineRepository.get_by_id(db, journal_line_id)
        if not line:
            raise ValueError("Journal line not found")

        journal = JournalEntryRepository.get_by_id(db, line.journal_id)
        if journal.posted_status:
            raise ValueError("Cannot delete lines of a posted journal")

        JournalLineRepository.delete(db, line)
