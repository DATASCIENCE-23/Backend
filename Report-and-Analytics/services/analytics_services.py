from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from typing import Dict, Any, Optional

from models.core_read_models import (
    Patient, Visit, Invoice, Payment,
    LabTest, LabResult,
    Prescription, PrescriptionItem, Medicine, Dispense
)

from models.analytics_models import (
    AnalyticalSnapshot,
    GeneratedReport
)


class AnalyticsService:
    def __init__(self, db: Session):
        self.db = db

    # ==========================================================
    # 1. INDIVIDUAL PATIENT MEDICAL REPORT (FULL)
    # ==========================================================
    def generate_patient_medical_summary(
        self, patient_id: int, user_id: int
    ) -> Optional[Dict[str, Any]]:

        # A. Demographics
        patient = (
            self.db.query(Patient)
            .filter(Patient.patient_id == patient_id)
            .first()
        )
        if not patient:
            return None

        # B. Clinical History
        visits = (
            self.db.query(Visit)
            .filter(Visit.patient_id == patient_id)
            .all()
        )

        # C. Diagnostics (LAB)
        labs = (
            self.db.query(
                LabTest.test_name,
                LabResult.result_value,
                LabResult.reference_range,
                LabResult.abnormal_flag
            )
            .join(LabTest, LabTest.test_id == LabResult.test_id)
            .all()
        )

        diagnostics = [
            {
                "test": l.test_name,
                "value": l.result_value,
                "reference_range": l.reference_range,
                "flag": l.abnormal_flag
            }
            for l in labs
        ]

        # D. Treatment (PHARMACY)
        treatments = (
            self.db.query(
                Medicine.medicine_name,
                PrescriptionItem.dosage,
                PrescriptionItem.frequency,
                PrescriptionItem.duration_days,
                Dispense.dispensed_at
            )
            .join(PrescriptionItem, Medicine.medicine_id == PrescriptionItem.medicine_id)
            .join(Prescription, Prescription.prescription_id == PrescriptionItem.prescription_id)
            .outerjoin(Dispense, Dispense.prescription_id == Prescription.prescription_id)
            .filter(Prescription.patient_id == patient_id)
            .all()
        )

        treatment_data = [
            {
                "medicine": t.medicine_name,
                "dosage": t.dosage,
                "frequency": t.frequency,
                "duration_days": t.duration_days,
                "dispensed_at": t.dispensed_at
            }
            for t in treatments
        ]

        # E. Financial Summary
        total_billed = (
            self.db.query(func.sum(Invoice.grand_total))
            .filter(Invoice.patient_id == patient_id)
            .scalar()
            or 0
        )

        total_paid = (
            self.db.query(func.sum(Payment.amount_paid))
            .join(Invoice, Payment.invoice_id == Invoice.invoice_id)
            .filter(Invoice.patient_id == patient_id)
            .scalar()
            or 0
        )

        balance = float(total_billed - total_paid)

        # F. Log report generation (analytics-owned)
        report = GeneratedReport(
            template_id=1,
            patient_id=patient_id,
            generated_by_user_id=user_id,
            file_path_url=f"/reports/generated/patient_{patient_id}.pdf",
            generated_at=datetime.utcnow()
        )
        self.db.add(report)
        self.db.commit()

        return {
            "metadata": {
                "generated_at": datetime.utcnow(),
                "patient_id": patient.patient_id
            },
            "demographics": {
                "name": f"{patient.first_name} {patient.last_name}",
                "contact": patient.phone_number
            },
            "clinical_history": [
                {
                    "date": v.visit_datetime,
                    "reason": v.chief_complaint
                }
                for v in visits
            ],
            "diagnostics": diagnostics,
            "treatments": treatment_data,
            "financials": {
                "total_billed": float(total_billed),
                "total_paid": float(total_paid),
                "balance_due": balance,
                "status": "Pending" if balance > 0 else "Paid"
            }
        }

    # ==========================================================
    # 2. DASHBOARD ANALYTICS (SAFE VERSION)
    # ==========================================================
    def update_hospital_kpis(self) -> Dict[str, Any]:

        revenue = self.db.query(func.sum(Invoice.grand_total)).scalar() or 0

        self._save_snapshot("Revenue", float(revenue), "Hospital_Wide")

        return {
            "total_revenue": float(revenue)
        }

    def _save_snapshot(self, metric: str, value: float, dims: str):
        snapshot = AnalyticalSnapshot(
            metric_type=metric,
            value=value,
            dimensions=dims
        )
        self.db.add(snapshot)
        self.db.commit()
