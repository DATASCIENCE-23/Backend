package visit

import "time"

type Visit struct {
    VisitID        uint      `json:"visit_id" gorm:"primaryKey;autoIncrement"`
    PatientID      uint      `json:"patient_id"`
    DoctorID       uint      `json:"doctor_id"`
    VisitType      string    `json:"visit_type"`
    VisitDate      time.Time `json:"visit_date"`
    ReasonForVisit string    `json:"reason_for_visit"`
    Status         string    `json:"status"`
}
