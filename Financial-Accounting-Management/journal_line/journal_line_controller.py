from sqlalchemy.orm import Session
from journal_line.journal_line_service import JournalLineService
from journal_line.journal_line_schema import JournalLineCreate

class JournalLineController:

    @staticmethod
    def create(db: Session, data: JournalLineCreate):
        return JournalLineService.create_journal_line(db, data)

    @staticmethod
    def get(db: Session, journal_line_id: int):
        return JournalLineService.get_journal_line(db, journal_line_id)

    @staticmethod
    def get_by_journal(db: Session, journal_id: int):
        return JournalLineService.get_lines_by_journal(db, journal_id)

    @staticmethod
    def update(db: Session, journal_line_id: int, data: dict):
        return JournalLineService.update_journal_line(db, journal_line_id, data)

    @staticmethod
    def delete(db: Session, journal_line_id: int):
        return JournalLineService.delete_journal_line(db, journal_line_id)
