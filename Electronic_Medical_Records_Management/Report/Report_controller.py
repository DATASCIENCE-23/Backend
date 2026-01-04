from fastapi import HTTPException
from .Report_service import ReportService


class ReportController:
    def __init__(self, db):
        self.service = ReportService(db)

    def create_report(self, record_id: int, report_type: str, findings: str):
        try:
            report = self.service.create_report(record_id, report_type, findings)
            return {
                "message": "Report created successfully",
                "report_id": report.report_id,
                "report_type": report.report_type,
                "report_date": str(report.report_date)
            }
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    def get_report(self, report_id: int):
        try:
            report = self.service.get_report(report_id)
            return {
                "report_id": report.report_id,
                "record_id": report.record_id,
                "report_type": report.report_type,
                "report_date": str(report.report_date),
                "findings": report.findings
            }
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))

    def get_reports_for_visit(self, record_id: int):
        reports = self.service.get_reports_for_visit(record_id)
        return [
            {
                "report_id": r.report_id,
                "report_type": r.report_type,
                "report_date": str(r.report_date),
                "findings": r.findings
            } for r in reports
        ]