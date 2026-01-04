from sqlalchemy.orm import Session
from .Report_model import Report
from typing import List, Optional


class ReportRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, report: Report) -> Report:
        self.db.add(report)
        self.db.commit()
        self.db.refresh(report)
        return report

    def get_by_id(self, report_id: int) -> Optional[Report]:
        return self.db.query(Report).filter(Report.report_id == report_id).first()

    def get_by_medical_record(self, record_id: int) -> List[Report]:
        return self.db.query(Report).filter(Report.record_id == record_id).order_by(Report.report_date.desc()).all()

    def get_all(self) -> List[Report]:
        return self.db.query(Report).order_by(Report.report_date.desc()).all()

    def update(self, report: Report) -> Report:
        self.db.commit()
        self.db.refresh(report)
        return report

    def delete(self, report_id: int) -> bool:
        report = self.get_by_id(report_id)
        if report:
            self.db.delete(report)
            self.db.commit()
            return True
        return False