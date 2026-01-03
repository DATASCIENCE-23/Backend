from typing import List
from .Report_model import Report
from .Report_repository import ReportRepository
from datetime import date


class ReportService:
    def __init__(self, db):
        self.repository = ReportRepository(db)

    def create_report(self, record_id: int, report_type: str, findings: str) -> Report:
        report = Report(
            record_id=record_id,
            report_type=report_type,
            report_date=date.today(),
            findings=findings
        )
        return self.repository.create(report)

    def get_report(self, report_id: int) -> Report:
        report = self.repository.get_by_id(report_id)
        if not report:
            raise ValueError("Report not found")
        return report

    def get_reports_for_visit(self, record_id: int) -> List[Report]:
        return self.repository.get_by_medical_record(record_id)

    # Example: Doctor creates a discharge summary
    def create_discharge_summary(self, record_id: int, findings: str) -> Report:
        return self.create_report(
            record_id=record_id,
            report_type="discharge_summary",
            findings=findings
        )

    # Example: Lab report attached to visit
    def create_lab_report(self, record_id: int, findings: str) -> Report:
        return self.create_report(
            record_id=record_id,
            report_type="lab",
            findings=findings
        )