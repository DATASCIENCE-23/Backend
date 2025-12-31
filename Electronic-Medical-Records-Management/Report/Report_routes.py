from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from .Report_controller import ReportController

router = APIRouter(prefix="/reports", tags=["Reports"])

# Create a new report for a medical record (visit)
@router.post("/create")
def create_report(
    record_id: int,
    report_type: str,
    findings: str,
    db: Session = Depends(get_db)
):
    controller = ReportController(db)
    return controller.create_report(record_id, report_type, findings)


# Get one report by ID
@router.get("/{report_id}")
def get_report(report_id: int, db: Session = Depends(get_db)):
    controller = ReportController(db)
    return controller.get_report(report_id)


# Get all reports for a specific visit (medical record)
@router.get("/visit/{record_id}")
def get_reports_for_visit(record_id: int, db: Session = Depends(get_db)):
    controller = ReportController(db)
    return controller.get_reports_for_visit(record_id)