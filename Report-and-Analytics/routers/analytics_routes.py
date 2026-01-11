from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from services.analytics_services import AnalyticsService

router = APIRouter(
    prefix="/analytics",
    tags=["Reports & Analytics"]
)

@router.get("/patient-report/{patient_id}")
def get_patient_medical_report(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = 1
):
    service = AnalyticsService(db)
    report = service.generate_patient_medical_summary(patient_id, current_user_id)

    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient medical records not found"
        )
    return report


@router.post("/refresh-kpis", status_code=status.HTTP_201_CREATED)
def refresh_dashboard_metrics(db: Session = Depends(get_db)):
    service = AnalyticsService(db)
    kpis = service.update_hospital_kpis()
    return {"message": "KPIs refreshed successfully", "data": kpis}
