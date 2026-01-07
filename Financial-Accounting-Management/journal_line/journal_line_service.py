from sqlalchemy.orm import Session
from journal_line.journal_line_models import JournalLine
from journal_line.journal_line_repository import JournalLineRepository
from journal_line.journal_line_schema import JournalLineCreate

class JournalLineService:

    @staticmethod
    def create_journal_line(db: Session, data: JournalLineCreate):
        if data.debit_amount > 0 and data.credit_amount > 0:
            raise ValueError("A journal line cannot have both debit and credit")

        if data.debit_amount == 0 and data.credit_amount == 0:
            raise ValueError("Either debit or credit must be greater than zero")

        line = JournalLine(**data.dict())
        return JournalLineRepository.create(db, line)

    @staticmethod
    def get_journal_line(db: Session, journal_line_id: int):
        return JournalLineRepository.get_by_id(db, journal_line_id)

    @staticmethod
    def get_lines_by_journal(db: Session, journal_id: int):
        return JournalLineRepository.get_by_journal(db, journal_id)

    @staticmethod
    def update_journal_line(db: Session, journal_line_id: int, data: dict):
        line = JournalLineRepository.get_by_id(db, journal_line_id)
        if not line:
            raise ValueError("Journal line not found")

        return JournalLineRepository.update(db, line, data)

    @staticmethod
    def delete_journal_line(db: Session, journal_line_id: int):
        line = JournalLineRepository.get_by_id(db, journal_line_id)
        if not line:
            raise ValueError("Journal line not found")

        return JournalLineRepository.delete(db, line)
